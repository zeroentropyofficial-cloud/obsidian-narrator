import streamlit as st
import edge_tts
import asyncio
import os

# Configuración de interfaz Luxury Dark Academia
st.set_page_config(page_title="Obsidian Narrator", page_icon="🎙️", layout="centered")

st.markdown("""
    <style>
    /* Fondo Obsidian Black */
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    
    /* Estilo para el área de texto - Oro Mate */
    .stTextArea textarea { 
        background-color: #111111; 
        color: #D4AF37; 
        border: 1px solid #D4AF37; 
        font-family: 'serif';
        font-size: 1.1rem;
    }
    
    /* Títulos en Mármol Blanco y Oro */
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    
    /* Botón Invocar - Ambar Bioluminiscente */
    .stButton>button { 
        background-color: #D4AF37; 
        color: #0A0A0A; 
        border-radius: 0px; 
        font-weight: bold; 
        border: none; 
        width: 100%; 
        padding: 15px;
        transition: 0.5s;
    }
    .stButton>button:hover { 
        background-color: #FFB347; /* Amber glow */
        color: #000000;
        box-shadow: 0px 0px 15px #D4AF37;
    }
    
    /* Selector de idiomas */
    .stSelectbox label { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN NARRATOR")
st.markdown("### Cinematic • Authoritative • Zero Fluff")

# Selección de Parámetros
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("Idioma de Poder", ["English", "Español", "Français"])
with col2:
    filename = st.text_input("Nombre del Archivo", "COURAGE_TAKE")

# Diccionario de Voces de Élite
# Se usan voces con registro bajo natural para evitar el sonido robótico
voices = {
    "English": "en-GB-RyanNeural",  # Autoridad británica profunda
    "Español": "es-MX-GerardoNeural", # Registro bajo y firme
    "Français": "fr-FR-HenriNeural"  # Seriedad absoluta
}

# Área de Entrada de Guion
text_input = st.text_area("Ingrese su guion (Use puntos para marcar el ritmo):", 
    height=250,
    placeholder="You need more COURAGE...")

async def generate_audio(text, voice, output_file):
    """
    Calibración Maestra:
    rate=+10% -> Rapidez rítmica sin sonar apurado.
    pitch=-18Hz -> Profundidad de 'Knights' sin distorsión metálica.
    volume=+15% -> Proyección de voz dominante.
    """
    communicate = edge_tts.Communicate(
        text, 
        voice, 
        rate="+10%", 
        pitch="-18Hz",
        volume="+15%"
    )
    await communicate.save(output_file)

if st.button("INVOKE VOICE"):
    if text_input:
        output_path = f"{filename}.mp3"
        with st.spinner("Fabricating Authority..."):
            asyncio.run(generate_audio(text_input, voices[lang], output_path))
        
        # Interfaz de Audio y Descarga
        with open(output_path, 'rb') as f:
            audio_bytes = f.read()
            st.audio(audio_bytes, format='audio/mp3')
            st.download_button(
                label="SAVE LOCUTION (MP3)", 
                data=audio_bytes, 
                file_name=f"{filename}.mp3", 
                mime="audio/mp3"
            )
        st.success(f"Archivo '{filename}.mp3' listo para exportación local.")
    else:
        st.warning("Escriba su guion para proceder.")

st.markdown("---")
st.caption("Luxury Dark Academia Audio Engine | Powered by Zero Entropy Logic")





