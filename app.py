import streamlit as st
import edge_tts
import asyncio
import os

st.set_page_config(page_title="Obsidian Narrator", page_icon="🎙️", layout="centered")

# Estética Luxury Dark Academia
st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { 
        background-color: #111111; 
        color: #D4AF37; 
        border: 1px solid #D4AF37; 
        font-family: 'serif';
    }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { 
        background-color: #D4AF37; color: #0A0A0A; font-weight: bold; 
        border: none; width: 100%; padding: 15px;
    }
    .stButton>button:hover { background-color: #FFB347; box-shadow: 0px 0px 15px #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN NARRATOR")
st.markdown("### Cinematic • Authoritative • High-Stakes")

col1, col2 = st.columns(2)
with col1:
    lang = st.selectbox("Language", ["English", "Español", "Français"])
with col2:
    filename = st.text_input("Filename", "CINEMATIC_TAKE")

voices = {
    "English": "en-GB-RyanNeural",
    "Español": "es-MX-GerardoNeural",
    "Français": "fr-FR-HenriNeural"
}

text_input = st.text_area("Input Script:", height=250, placeholder="You need more COURAGE...")

async def generate_audio(text, voice, output_file):
    # Creamos un bloque SSML para controlar la expresión
    # <prosody> controla el tono y la velocidad de fragmentos específicos
    ssml_text = f"""
    <speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>
        <voice name='{voice}'>
            <prosody pitch='-15Hz' rate='+15%' volume='+10%'>
                {text}
            </prosody>
        </voice>
    </speak>
    """
    communicate = edge_tts.Communicate(text, voice, rate="+15%", pitch="-15Hz")
    # Nota: Si el motor soporta SSML directo, usamos communicate.xml_string
    await communicate.save(output_file)

if st.button("INVOKE VOICE"):
    if text_input:
        output_path = f"{filename}.mp3"
        with st.spinner("Channeling Authority..."):
            asyncio.run(generate_audio(text_input, voices[lang], output_path))
        
        with open(output_path, 'rb') as f:
            st.audio(f.read(), format='audio/mp3')
            st.download_button("SAVE MP3", data=open(output_path, 'rb'), file_name=f"{filename}.mp3")







