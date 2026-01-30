import streamlit as st
import edge_tts
import asyncio
import os
import re

# Configuración Estética Luxury Dark Academia
st.set_page_config(page_title="Obsidian Engine Pro", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; font-family: 'serif'; font-size: 1.2rem; }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { 
        background-color: #D4AF37; color: #0A0A0A; border-radius: 0px; 
        font-weight: bold; border: none; width: 100%; height: 3.5em; transition: 0.5s;
    }
    .stButton>button:hover { background-color: #FFB347; box-shadow: 0px 0px 25px #D4AF37; }
    label { color: #D4AF37 !important; font-weight: bold; }
    .stCheckbox { color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN ENGINE PRO")
st.markdown("### Aggressive Authority • Cathedral Echo • Algieba Legacy")

# Voces Neuronales
accent_map = {
    "✨ ALGIEBA (Cathedral Deep)": "es-MX-GerardoNeural",
    "🎙️ English US (Christopher - Authority)": "en-US-ChristopherNeural",
    "🎙️ English UK (Ryan - Royal)": "en-GB-RyanNeural",
    "🎙️ English US (Eric - Deep)": "en-US-EricNeural",
    "🇲🇽 Neutro LATAM": "es-MX-LibertadNeural",
    "🇨🇴 Colombia": "es-CO-GonzaloNeural"
}

# Modos de Sala
mood_settings = {
    "🔥 Autoridad Máxima (Knights)": {"pitch": -25, "rate": 18, "echo": False},
    "📜 Sabiduría Antigua (Algieba)": {"pitch": -22, "rate": -5, "echo": True},
    "⚡ Staccato Directo": {"pitch": -5, "rate": 35, "echo": False},
    "🏛️ Catedral (Max Reverb)": {"pitch": -15, "rate": 0, "echo": True}
}

with st.sidebar:
    st.header("🎚️ Panel Maestro")
    selected_accent = st.selectbox("Voz", list(accent_map.keys()))
    selected_mood = st.selectbox("Ánimo/Efecto", list(mood_settings.keys()))
    
    st.markdown("---")
    st.subheader("🛠️ Modificadores de Fuerza")
    agressive_mode = st.checkbox("💥 MODO AGRESIVO (Auto-Enphasis)", value=False)
    
    pitch_adj = st.slider("Graves Extra", -20, 15, 0)
    rate_adj = st.slider("Velocidad Extra", -20, 20, 0)
    
    final_pitch = mood_settings[selected_mood]["pitch"] + pitch_adj
    final_rate = mood_settings[selected_mood]["rate"] + rate_adj
    apply_echo = mood_settings[selected_mood]["echo"]
    
    filename = st.text_input("Nombre", "OBSIDIAN_GEN")

# Área de Texto
raw_text = st.text_area("Guion:", height=300, placeholder="Escribe tu mensaje...")

def apply_aggression(text):
    # En lugar de punto en cada palabra, usamos comas para velocidad
    # y exclamaciones para fuerza, manteniendo las frases unidas.
    text = text.upper()
    # Creamos grupos de 3 palabras para mantener el ritmo rápido
    words = text.split()
    phrases = [" ".join(words[i:i+3]) for i in range(0, len(words), 3)]
    return ", ".join(phrases) + "!"

async def generate_audio(text, voice, output_file, p, r, echo_mode, agg_mode):
    # Procesamiento Híbrido
    if agg_mode:
        # Mantiene la estructura pero inyecta micro-pausas de tensión
        processed = apply_aggression(text)
    else:
        processed = text
    
    # Calibración de 'Knights' fluida:
    # Subimos el rate para que la agresividad no sea lenta
    p_str = f"{p}Hz"
    r_str = f"+{r+10}%" if agg_mode else f"{r}%" # Auto-aceleración en modo agresivo
    
    communicate = edge_tts.Communicate(processed, voice, rate=r_str, pitch=p_str, volume="+20%")
    await communicate.save(output_file)

if st.button("INVOKE AUTHORITY"):
    if raw_text:
        output_path = f"{filename}.mp3"
        with st.spinner("Inyectando Coraje..."):
            try:
                asyncio.run(generate_audio(raw_text, accent_map[selected_accent], output_path, final_pitch, final_rate, apply_echo, agressive_mode))
                
                with open(output_path, 'rb') as f:
                    st.audio(f.read(), format='audio/mp3')
                    st.download_button("SAVE MASTER MP3", data=open(output_path, 'rb'), file_name=f"{filename}.mp3")
                
                if agressive_mode:
                    st.warning("MODO AGRESIVO ACTIVO: Se ha forzado la entonación palabra por palabra.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("El silencio es debilidad. Escribe algo.")

st.markdown("---")
st.caption("The Obsidian Engine Pro | Cathedral & Aggression Logic | Zero Cost")










