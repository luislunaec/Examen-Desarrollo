import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import matplotlib.pyplot as plt
from dotenv import load_dotenv
import io

st.set_page_config(page_title="Examen Sistemas - Instagram AI", layout="wide", page_icon="🎓")

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    st.error("❌ ERROR: No se encontró la GOOGLE_API_KEY en .env")
    st.stop()

genai.configure(api_key=API_KEY)

def analizar_biografias_con_gemini(lista_bios):
    # Unir bios (filtrando vacíos)
    texto_bios = "\n".join([str(b) for b in lista_bios if str(b) != "nan" and str(b) != "Sin biografia"])
    
    try:
        # Modelo solicitado
        model = genai.GenerativeModel("models/gemini-2.5-flash") 
        
        prompt = f"""
        Actúa como analista de datos. Analiza estas biografías de Instagram:
        '''
        {texto_bios[:15000]} 
        '''
        TAREA:
        Identifica los 10 conceptos más frecuentes.
        
        FORMATO OBLIGATORIO:
        Responde ÚNICAMENTE con formato CSV (Concepto,Frecuencia).
        NO uses bloques de código markdown (```csv).
        Ejemplo:
        Futbol,15
        Musica,10
        """
        
        with st.spinner('Gemini procesando... 🤖'):
            response = model.generate_content(prompt)
        
        # Limpieza de seguridad: quitar ```csv y ``` si Gemini los pone
        texto_limpio = response.text.replace("```csv", "").replace("```", "").strip()
        return texto_limpio
        
    except Exception as e:
        st.error(f"Error Gemini: {e}")
        return None

# --- FRONTEND ---
st.title("📊 Examen: Análisis Instagram con Gemini")

uploaded_file = st.file_uploader("Cargar datos_instagram.csv", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    if 'biografia' in df.columns:
        st.success(f"✅ Cargado: {len(df)} registros.")
        
        if st.button("✨ Generar Análisis"):
            res_txt = analizar_biografias_con_gemini(df['biografia'].tolist())
            
            if res_txt:
                try:
                    # Leer CSV desde texto
                    df_g = pd.read_csv(io.StringIO(res_txt), names=["Concepto", "Frecuencia"])
                    
                    c1, c2 = st.columns([1, 2])
                    with c1:
                        st.write("### Tabla")
                        st.dataframe(df_g)
                    with c2:
                        st.write("### Gráfico")
                        fig, ax = plt.subplots()
                        ax.bar(df_g["Concepto"], df_g["Frecuencia"], color="purple")
                        plt.xticks(rotation=45)
                        st.pyplot(fig)
                except:
                    st.error("Error al procesar respuesta de IA. Intenta de nuevo.")
                    st.write(res_txt)
    else:
        st.error("El CSV no tiene columna 'biografia'")