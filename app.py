import streamlit as st
import edge_tts
import asyncio

st.set_page_config(page_title="Obsidian Narrator", page_icon="🎙️")

# Estética Luxury Dark Academia
st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; }
    h1 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { background-color: #D4AF37; color: #0A0A0A; font-weight: bold; border-radius: 0px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN NARRATOR")

col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("Language", ["Español", "English", "Français"])
with col2:
    filename = st.text_input("Filename", "cinematic_take")

# Diccionario de voces de alto impacto
voices = {
    "Español": "es-MX-GerardoNeural",
    "English": "en-GB-RyanNeural",
    "Français": "fr-FR-HenriNeural"
}

text_input = st.text_area("Script", placeholder="Maximum impact starts here...")

async def generate_audio(text, voice, output_file):
    # Ajustes críticos: rate=+35% (rápido) y pitch=-25Hz (ultra grave)
    communicate = edge_tts.Communicate(text, voice, rate="+35%", pitch="-25Hz")
    await communicate.save(output_file)

if st.button("INVOKE VOICE"):
    if text_input:
        output_path = f"{filename}.mp3"
        asyncio.run(generate_audio(text_input, voices[lang], output_path))
        
        audio_file = open(output_path, 'rb')
        st.audio(audio_file.read(), format='audio/mp3')
        st.download_button("DOWNLOAD MP3", data=open(output_path, 'rb'), file_name=output_path)


