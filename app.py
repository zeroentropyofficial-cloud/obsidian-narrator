import streamlit as st
import edge_tts
import asyncio
import os

# Configuración de la página con estética Luxury Dark Academia
st.set_page_config(page_title="The Obsidian Narrator", page_icon="🎙️")

st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #1A1A1A; color: #D4AF37; border: 1px solid #D4AF37; font-family: 'serif'; }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-shadow: 2px 2px #000000; }
    .stButton>button { 
        background-color: #D4AF37; color: #0A0A0A; border-radius: 0px; 
        font-weight: bold; border: none; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #FFD700; color: #000000; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN NARRATOR")
st.subheader("Cinematic High-Stakes Voice Engine")

# Selección de Idioma y Voz (Configuradas para ser las más profundas y rápidas)
col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("Language / Idioma", ["Español", "English", "Français"])
with col2:
    filename = st.text_input("File Name / Nombre del archivo", "narration_01")

voices = {
    "Español": "es-ES-AlvaroNeural", # Voz masculina profunda
    "English": "en-US-ChristopherNeural", # Voz de autoridad
    "Français": "fr-FR-HenriNeural" # Voz grave francesa
}

# Entrada de texto
text_input = st.text_area("Enter your script / Ingrese su guion:", placeholder="El imperio caerá al amanecer...", height=200)

async def generate_audio(text, voice, output_file):
    # 'rate=+35%' aumenta la velocidad para que sea rítmica y rápida
    # 'pitch=-25Hz' baja la frecuencia para que sea ultra-grave y autoritaria
    # 'volume=+0%' asegura claridad total
    communicate = edge_tts.Communicate(
        text, 
        voice, 
        rate="+35%", 
        pitch="-25Hz",
        volume="+0%"
    )
    await communicate.save(output_file)

if st.button("INVOKE VOICE"):
    if text_input:
        output_path = f"{filename}.mp3"
        with st.spinner("Channeling Authority..."):
            asyncio.run(generate_audio(text_input, voices[lang], output_path))
        
        # Reproductor y Descarga
        audio_file = open(output_path, 'rb')
        audio_bytes = audio_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        st.download_button(label="DOWNLOAD MP3", data=audio_bytes, file_name=f"{filename}.mp3", mime="audio/mp3")
        st.success(f"Archived as {filename}.mp3")
    else:
        st.error("The silence is empty. Write something.")

st.markdown("---")
st.caption("Zero Fluff. Maximum Impact. Powered by Obsidian Logic.")

