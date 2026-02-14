import requests
import json
import time
import random

class InstagramScraper:
    def __init__(self, raw_cookie, csrf_token):
        self.raw_cookie = raw_cookie.strip()
        self.csrf_token = csrf_token.strip()
        
        self.headers = {
            "authority": "www.instagram.com",
            "accept": "*/*",
            "accept-language": "es-ES,es;q=0.9,en;q=0.8",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://www.instagram.com",
            "referer": "https://www.instagram.com/",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "x-ig-app-id": "936619743392459",
            "x-requested-with": "XMLHttpRequest",
            "x-csrftoken": self.csrf_token,
            "cookie": self.raw_cookie
        }

    def obtener_perfil(self, username):
        """Devuelve datos del perfil y también el ID numérico necesario para buscar seguidores."""
        print(f"📡 Buscando perfil de: {username}...")
        url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
        
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                user_data = data.get('data', {}).get('user', {})
                if user_data:
                    return {
                        "id": user_data.get('id'), # IMPORTANTE: Necesitamos esto
                        "username": user_data.get('username'),
                        "name": user_data.get('full_name'),
                        "biografia": user_data.get('biography'),
                        "seguidores": user_data.get('edge_followed_by', {}).get('count')
                    }
            elif response.status_code == 404:
                print(f"❌ Usuario {username} no encontrado.")
            else:
                print(f"⚠️ Error {response.status_code} al obtener perfil.")
            return None
        except Exception as e:
            print(f"❌ Error de conexión: {e}")
            return None

    def obtener_lista_seguidores(self, user_id, cantidad_minima=150):
        """Obtiene una lista de usernames de los seguidores del ID dado."""
        print(f"🕵️ Recuperando lista de seguidores para ID: {user_id}...")
        seguidores_usernames = []
        max_id = "" # Cursor para paginación
        
        # Bucle para pedir páginas hasta completar la cantidad
        while len(seguidores_usernames) < cantidad_minima:
            url = f"https://www.instagram.com/api/v1/friendships/{user_id}/followers/?count=50&search_surface=follow_list_page"
            if max_id:
                url += f"&max_id={max_id}"

            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    users = data.get('users', [])
                    
                    for u in users:
                        seguidores_usernames.append(u.get('username'))
                    
                    print(f"   ↳ Llevamos {len(seguidores_usernames)} seguidores recolectados...")
                    
                    # Paginación (para pedir los siguientes)
                    max_id = data.get('next_max_id')
                    if not max_id:
                        break # No hay más seguidores
                    
                    # Pausa de seguridad entre páginas de la lista
                    time.sleep(random.uniform(2, 4))
                else:
                    print(f"❌ Error al obtener lista: {response.status_code}")
                    break
            except Exception as e:
                print(f"❌ Error en lista de seguidores: {e}")
                break
        
        return seguidores_usernames[:cantidad_minima]