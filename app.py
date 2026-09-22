import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración de la interfaz
st.set_page_config(
    page_title="Agente IA - Gestión Normativa de Residuos", 
    page_icon="🏗️", 
    layout="wide"
)

st.title("🏗️ Agente IA: Inspección Normativa de Residuos en Obra")
st.markdown("---")

# Barra lateral para credenciales y configuración
with st.sidebar:
    st.header("⚙️ Configuración del Agente")
    api_key = st.text_input("Ingresa tu API Key (Google AI Studio):", type="password")
    st.markdown("""
    **Marcos Normativos Inyectados:**
    * 📐 **Norma E.060:** Concreto Armado (Criterios de traslape, corrosión y reuso estructural de acero).
    * ♻️ **NTP 900.058:** Código de Colores para Almacenamiento de Residuos en Construcción.
    """)

if api_key:
    genai.configure(api_key=api_key)
    modelo = genai.GenerativeModel('gemini-1.5-flash')

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📷 Carga de Material para Inspección")
        foto_subida = st.file_uploader("Sube una foto del sobrante (Acero, Madera, etc.):", type=["jpg", "jpeg", "png"])
        
        if foto_subida:
            imagen = Image.open(foto_subida)
            st.image(imagen, caption="Muestra capturada en obra", use_container_width=True)

    with col2:
        st.subheader("🧠 Dictamen Técnico Automatizado")
        if foto_subida and st.button("🔍 Evaluar bajo Norma E.060 y NTP 900.058", type="primary"):
            with st.spinner("Procesando características del material y consultando normativas..."):
                
                # Prompt estructurado con reglas de ingeniería
                prompt = """
                Eres un Ingeniero Civil Supervisor especialista en Control de Calidad y Gestión Ambiental en Obras (ODS 9 y 12).
                Analiza la imagen adjunta y genera un dictamen técnico estructurado en Markdown con las siguientes secciones exactas:

                ### 1. Identificación y Diagnóstico Visual
                * **Material Detectado:** (Nombre específico del material)
                * **Estado Físico Observado:** (Evalúa estado de corrosión, deformaciones, fisuras o desgaste visual)
                * **Dimensión/Utilidad Estimada:** (Indica si por dimensión parece un retazo aprovechable o escombro)

                ### 2. Evaluación de Reuso Estructural (Norma Técnica E.060)
                * **Aptitud Estructural:** (Aprobado para reuso / Rechazado para elementos portantes)
                * **Criterio Técnico:** (Justifica según la E.060. Si es acero: indicar si la longitud permite doblado para estribos/ganchos o si la corrosión compromete la adherencia).

                ### 3. Segregación y Disposición Ambiental (NTP 900.058)
                * **Destino Sugerido:** (Reuso Directo / Reciclaje / Disposición Final en Escombrera)
                * **Contenedor Normado:** (Indica el color del contenedor según NTP 900.058, ej. Amarillo para Metales, Marrón para Orgánico/Madera, Gris/Pardo para RCD).

                ### 4. Matriz de Decisión
                Crea una tabla en Markdown con 3 columnas:
                | Parámetro Evaluado | Diagnóstico | Acción Requerida |
                """
                
                try:
                    respuesta = modelo.generate_content([prompt, imagen])
                    st.markdown(respuesta.text)
                except Exception as e:
                    st.error(f"Error al conectar con la API: {e}")
        elif not foto_subida:
            st.info("👈 Sube una imagen en el panel izquierdo para habilitar el botón de análisis.")
else:
    st.warning("⚠️ Por favor, ingresa tu API Key en la barra lateral para activar el Agente de IA.")
