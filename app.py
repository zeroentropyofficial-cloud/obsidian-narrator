import streamlit as st
import edge_tts
import asyncio
import os

# Configuración Luxury Dark Academia
st.set_page_config(page_title="Obsidian Voice Engine Pro", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; font-family: 'serif'; }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { 
        background-color: #D4AF37; color: #0A0A0A; border-radius: 0px; 
        font-weight: bold; border: none; width: 100%; height: 3.5em; transition: 0.5s;
    }
    .stButton>button:hover { background-color: #FFB347; box-shadow: 0px 0px 20px #D4AF37; }
    label { color: #D4AF37 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN VOICE ENGINE PRO")

# Diccionario Maestro de Voces (Expandido)
accent_map = {
    "🏛️ ALGEIBA (Legacy Deep)": "es-MX-GerardoNeural", 
    "🇲🇽 Neutro LATAM": "es-MX-LibertadNeural",
    "🇨🇴 Colombia": "es-CO-GonzaloNeural",
    "🇦🇷 Argentina": "es-AR-TomasNeural",
    "🇨🇱 Chile": "es-CL-LorenzoNeural",
    "🇵🇪 Perú": "es-PE-AlexNeural",
    "🇺🇸 English US (Authority)": "en-US-ChristopherNeural",
    "🇬🇧 English UK (Royal)": "en-GB-RyanNeural",
    "🇺🇸 English US (Deep Male)": "en-US-EricNeural",
    "🇺🇸 English US (Narrator)": "en-US-GuyNeural",
    "🇦🇺 English AU (Steady)": "en-AU-WilliamNeural"
}

# Definición de Estilos/Ánimos Predefinidos
mood_settings = {
    "Normal": {"pitch": -10, "rate": 10},
    "🔥 Autoridad Máxima (Knights)": {"pitch": -25, "rate": 15},
    "📜 Sabiduría Antigua (Algieba Style)": {"pitch": -20, "rate": -5},
    "⚡ Rápido e Impactante (Staccato)": {"pitch": -5, "rate": 30},
    "🌑 Sombrío y Susurrado": {"pitch": -35, "rate": -10}
}

with st.sidebar:
    st.header("🎚️ Configuración")
    selected_accent = st.selectbox("Identidad Vocal", list(accent_map.keys()))
    
    st.markdown("---")
    st.subheader("🎭 Estilo de Interpretación")
    selected_mood = st.selectbox("Selecciona el Ánimo", list(mood_settings.keys()))
    
    # Valores base del ánimo seleccionado
    base_pitch = mood_settings[selected_mood]["pitch"]
    base_rate = mood_settings[selected_mood]["rate"]
    
    st.markdown("---")
    st.subheader("Ajuste Fino (Manual)")
    pitch_val = st.slider("Profundidad Extra", -20, 20, 0)
    rate_val = st.slider("Velocidad Extra", -20, 20, 0)
    
    # Cálculo final de parámetros
    final_pitch = base_pitch + pitch_val
    final_rate = base_rate + rate_val
    
    st.markdown("---")
    filename = st.text_input("Nombre del Proyecto", "OBSIDIAN_PRO")

# Área de Texto
text_input = st.text_area("Guion Cinematográfico:", height=300, 
                          placeholder="Introduce el texto aquí...")

async def generate_audio(text, voice, output_file, p, r):
    p_str = f"{p}Hz"
    r_str = f"+{r}%" if r >= 0 else f"{r}%"
    communicate = edge_tts.Communicate(text, voice, rate=r_str, pitch=p_str, volume="+15%")
    await communicate.save(output_file)

if st.button("INVOKE MASTER VOICE"):
    if text_input:
        output_path = f"{filename}.mp3"
        with st.spinner(f"Invocando estilo: {selected_mood}..."):
            try:
                # Ajuste especial para emular a Algieba si se selecciona
                current_voice = accent_map[selected_accent]
                asyncio.run(generate_audio(text_input, current_voice, output_path, final_pitch, final_rate))
                
                with open(output_path, 'rb') as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.download_button("DESCARGAR MP3", data=audio_bytes, file_name=f"{filename}.mp3")
                st.success(f"Locución terminada con perfil {selected_mood}")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("El silencio no tiene eco en la eternidad. Escribe algo.")

st.markdown("---")
st.caption("The Obsidian Engine Pro | Multilingual Authority | Zero Cost")








