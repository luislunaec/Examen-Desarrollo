import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
import re

class BioAnalyzer:
    def __init__(self):
        self.ignorar = ["de", "la", "el", "en", "y", "a", "que", "con", "del", "mi", "se", "los", "las", "por", "un", "una", "para", "es", "soy"]

    def procesar_y_graficar(self, lista_bios):
        # Convertir a string y minúsculas
        texto_completo = " ".join([str(b) for b in lista_bios]).lower()
        
        # Regex para solo letras
        palabras = re.findall(r'\b[a-záéíóúñ]{4,}\b', texto_completo)
        
        # Filtrar
        palabras_filtradas = [p for p in palabras if p not in self.ignorar]
        
        # Top 10
        top_10 = Counter(palabras_filtradas).most_common(10)
        
        if not top_10:
            print("⚠️ No hay datos suficientes para graficar.")
            return

        # Graficar
        df = pd.DataFrame(top_10, columns=['Palabra', 'Frecuencia'])
        
        plt.figure(figsize=(10, 6))
        plt.bar(df['Palabra'], df['Frecuencia'], color='#C13584')
        plt.title('Conceptos más mencionados en Biografías')
        plt.xlabel('Conceptos')
        plt.ylabel('Frecuencia')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        return top_10