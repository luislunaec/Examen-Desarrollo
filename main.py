from scraper_instagram import InstagramScraper
from graficos import BioAnalyzer 
import pandas as pd
import time
import random

if __name__ == "__main__":
    # ------------------------------------------------------------------
    # 1. TUS CREDENCIALES (Esto déjalo como ya lo tienes, que funciona)
    # ------------------------------------------------------------------
    MIS_COOKIES = 'sessionid=1171342961%3ATCOhy2EPBa122D%3A3%3AAYiARox3-WIqm6qITzQx4Y0I-4TToD4wy75xvMGFRQ; ds_user_id=1171342961; csrftoken=v4ry4Hu472Qo1NCdx2rRv78Kv6jvVB0H' 
    
    # Copia el valor de "x-csrftoken" (o búscalo dentro de la cookie como csrftoken)
    MI_CSRF = 'v4ry4Hu472Qo1NCdx2rRv78Kv6jvVB0H' 
    
    # ------------------------------------------------------------------
    # 2. ¿A QUIÉN QUIERES INVESTIGAR?
    # ------------------------------------------------------------------
    # Si pones "luisandreluna01", sacará TUS seguidores.
    # Si pones "dilan.sanmartin_", sacará los seguidores de Dilan.
    OBJETIVO = "luisandreluna01" 

    # Instancias
    scraper = InstagramScraper(raw_cookie=MIS_COOKIES, csrf_token=MI_CSRF)
    analizador = BioAnalyzer()
    
    datos_recolectados = []
    bios_texto = []

    print(f"--- 🚀 INICIANDO INVESTIGACIÓN DE: {OBJETIVO} ---")

    # PASO A: Obtener el ID numérico del objetivo
    perfil_objetivo = scraper.obtener_perfil(OBJETIVO)
    
    if perfil_objetivo and perfil_objetivo['id']:
        id_objetivo = perfil_objetivo['id']
        print(f"✅ Objetivo localizado. ID: {id_objetivo}")
        
        # PASO B: ¡Aquí está la magia! Sacar la lista de SU gente
        print("\n--- 📥 Extrayendo lista de seguidores... ---")
        # Aquí le pedimos 150 seguidores de ese ID
        lista_amigos = scraper.obtener_lista_seguidores(id_objetivo, cantidad_minima=150)
        
        print(f"✅ Se encontraron {len(lista_amigos)} seguidores. Analizándolos uno por uno...\n")
        
        # PASO C: Recorrer esa lista (Esto es lo que te faltaba)
        contador = 1
        for amigo_user in lista_amigos:
            print(f"[{contador}/{len(lista_amigos)}] Analizando a: {amigo_user} ... ", end="")
            
            dato = scraper.obtener_perfil(amigo_user)
            
            if dato:
                datos_recolectados.append(dato)
                if dato['biografia']:
                    bios_texto.append(dato['biografia'])
            
            contador += 1
            # Pausa para que Instagram no se enoje
            time.sleep(random.uniform(2, 4))

    else:
        print("❌ No se pudo encontrar al usuario objetivo. Revisa el nombre.")

    # 3. GUARDAR RESULTADOS
    if datos_recolectados:
        df = pd.DataFrame(datos_recolectados)
        df.to_csv("datos_investigacion_uce.csv", index=False)
        print(f"\n✅ ¡Listo! {len(datos_recolectados)} perfiles guardados en 'datos_investigacion_uce.csv'.")
    
    # 4. GRAFICAR
    if bios_texto:
        print("📊 Generando gráfico...")
        analizador.procesar_y_graficar(bios_texto)
    else:
        print("\n⚠️ No se encontraron suficientes biografías.")