import streamlit as st
import edge_tts
import asyncio
import os

# Configuración de página con estética Obsidian & Gold
st.set_page_config(page_title="Obsidian Voice Engine", page_icon="🎙️", layout="wide")

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
        background-color: #D4AF37; color: #0A0A0A; border-radius: 0px; 
        font-weight: bold; border: none; width: 100%; height: 3.5em; transition: 0.5s;
    }
    .stButton>button:hover { background-color: #FFB347; box-shadow: 0px 0px 20px #D4AF37; }
    label { color: #D4AF37 !important; font-weight: bold; }
    .stSelectbox div[data-baseweb="select"] { background-color: #111111; color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN VOICE ENGINE")
st.markdown("### Sudamérica • Neutro • Cinematic English")

# Mapeo de Voces Neuronales (Gratis y de Alta Calidad)
accent_map = {
    "🇦🇷 Argentina (Tomás)": "es-AR-TomasNeural",
    "🇨🇴 Colombia (Gonzalo)": "es-CO-GonzaloNeural",
    "🇨🇱 Chile (Lorenzo)": "es-CL-LorenzoNeural",
    "🇵🇪 Perú (Alex)": "es-PE-AlexNeural",
    "🇲🇽 Neutro LATAM (Gerardo)": "es-MX-GerardoNeural",
    "🇺🇸 English US (Christopher)": "en-US-ChristopherNeural",
    "🇬🇧 English UK (Ryan)": "en-GB-RyanNeural"
}

# Panel Lateral de Control
with st.sidebar:
    st.header("🎚️ Ajustes de Locución")
    selected_accent = st.selectbox("Identidad Regional", list(accent_map.keys()))
    
    st.markdown("---")
    st.subheader("Personalización Tonal")
    # Sliders para emular voces como Algieba o Knights
    pitch_val = st.slider("Profundidad (Pitch)", -50, 10, -15, help="Más bajo = más grave/autoritario")
    rate_val = st.slider("Ritmo (Rate)", -10, 40, 12, help="Ajusta la velocidad del discurso")
    
    st.markdown("---")
    filename = st.text_input("Nombre del Proyecto", "OBSIDIAN_TAKE_01")

# Área de entrada de texto
text_input = st.text_area("Escriba su guion (Use mayúsculas para ÉNFASIS):", 
                          height=350, 
                          placeholder="YOU are waiting for a green light... that is NEVER coming.")

async def generate_audio(text, voice, output_file, p, r):
    # Formateo de parámetros para el motor
    pitch_str = f"{p}Hz"
    rate_str = f"+{r}%" if r >= 0 else f"{r}%"
    
    communicate = edge_tts.Communicate(
        text, 
        voice, 
        rate=rate_str, 
        pitch=pitch_str,
        volume="+15%" # Mayor volumen para impacto cinematográfico
    )
    await communicate.save(output_file)

# Botón de ejecución
if st.button("INVOKE AUTHORITY"):
    if text_input:
        output_path = f"{filename}.mp3"
        with st.spinner("Fabricando resonancia vocal..."):
            try:
                asyncio.run(generate_audio(
                    text_input, 
                    accent_map[selected_accent], 
                    output_path,
                    pitch_val,
                    rate_val
                ))
                
                # Reproductor y Descarga
                with open(output_path, 'rb') as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.download_button(
                        label="DESCARGAR LOCUCIÓN (MP3)", 
                        data=audio_bytes, 
                        file_name=f"{filename}.mp3", 
                        mime="audio/mp3"
                    )
                st.success(f"Sesión completada: Acento {selected_accent} aplicado.")
            except Exception as e:
                st.error(f"Error en la invocación: {e}")
    else:
        st.warning("El silencio no tiene poder. Ingrese un texto.")

st.markdown("---")
st.caption("Professional Multilingual TTS Engine | Obsidian Design | Zero Cost Edition")







