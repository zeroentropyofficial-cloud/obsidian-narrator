import streamlit as st
import edge_tts
import asyncio
import os

# Configuración Estética Luxury Dark Academia
st.set_page_config(page_title="Obsidian Engine Pro", page_icon="🎙️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; font-family: 'serif'; }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { 
        background-color: #D4AF37; color: #0A0A0A; border-radius: 0px; 
        font-weight: bold; border: none; width: 100%; height: 3.5em; transition: 0.5s;
    }
    .stButton>button:hover { background-color: #FFB347; box-shadow: 0px 0px 25px #D4AF37; }
    label { color: #D4AF37 !important; font-weight: bold; }
    .stSelectbox div[data-baseweb="select"] { background-color: #111111; color: #D4AF37; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN ENGINE PRO")
st.markdown("### Cathedral Echo • Algieba Legacy • Cinematic Authority")

# Catálogo Expandido de Voces
accent_map = {
    "✨ ALGIEBA (Cathedral Deep)": "es-MX-GerardoNeural",
    "🎙️ English US (Christopher - Authority)": "en-US-ChristopherNeural",
    "🎙️ English UK (Ryan - Royal)": "en-GB-RyanNeural",
    "🎙️ English US (Eric - Deep)": "en-US-EricNeural",
    "🎙️ English US (Guy - Narrator)": "en-US-GuyNeural",
    "🇦🇷 Argentina": "es-AR-TomasNeural",
    "🇨🇴 Colombia": "es-CO-GonzaloNeural",
    "🇲🇽 Neutro LATAM": "es-MX-LibertadNeural",
    "🇨🇱 Chile": "es-CL-LorenzoNeural",
    "🇵🇪 Perú": "es-PE-AlexNeural"
}

# Configuración de Ánimos y Efectos de Sala
mood_settings = {
    "📜 Sabiduría Antigua (Algieba Style)": {"pitch": -22, "rate": -8, "echo": True},
    "🔥 Autoridad Máxima (Knights)": {"pitch": -25, "rate": 15, "echo": False},
    "⚡ Rápido e Impactante (Staccato)": {"pitch": -8, "rate": 35, "echo": False},
    "🌑 Sombrío y Susurrado": {"pitch": -38, "rate": -15, "echo": True},
    "🏛️ Gran Salón (Reverb)": {"pitch": -12, "rate": -2, "echo": True}
}

with st.sidebar:
    st.header("🎚️ Configuración Maestra")
    selected_accent = st.selectbox("Voz Base", list(accent_map.keys()))
    
    st.markdown("---")
    st.subheader("🎭 Interpretación y Sala")
    selected_mood = st.selectbox("Efecto de Ambiente", list(mood_settings.keys()))
    
    # Parámetros base del ánimo
    base_pitch = mood_settings[selected_mood]["pitch"]
    base_rate = mood_settings[selected_mood]["rate"]
    apply_echo = mood_settings[selected_mood]["echo"]
    
    st.markdown("---")
    st.subheader("Sintonía Fina")
    pitch_adj = st.slider("Ajuste de Graves", -20, 15, 0)
    rate_adj = st.slider("Ajuste de Velocidad", -20, 20, 0)
    
    # Cálculo final
    final_pitch = base_pitch + pitch_adj
    final_rate = base_rate + rate_adj
    
    filename = st.text_input("Nombre del Proyecto", "ALGEIBA_RESONANCE")

# Input de texto
text_input = st.text_area("Guion Cinematográfico:", height=300, 
                          placeholder="Escribe aquí... El eco se genera automáticamente en modos de sabiduría.")

async def generate_audio(text, voice, output_file, p, r, echo_mode):
    # Simulamos el efecto de 'Catedral' añadiendo pausas SSML si el echo_mode está activo
    # Nota: edge-tts aplica el rate y pitch al stream completo.
    p_str = f"{p}Hz"
    r_str = f"+{r}%" if r >= 0 else f"{r}%"
    
    # Si es modo eco, procesamos el texto para espaciarlo más y que retumbe
    processed_text = text.replace(".", "... ").replace(",", ", ... ") if echo_mode else text
    
    communicate = edge_tts.Communicate(processed_text, voice, rate=r_str, pitch=p_str, volume="+18%")
    await communicate.save(output_file)

if st.button("INVOKE AUTHORITY"):
    if text_input:
        output_path = f"{filename}.mp3"
        with st.spinner(f"Aplicando resonancia de {selected_mood}..."):
            try:
                current_voice = accent_map[selected_accent]
                asyncio.run(generate_audio(text_input, current_voice, output_path, final_pitch, final_rate, apply_echo))
                
                with open(output_path, 'rb') as f:
                    audio_bytes = f.read()
                    st.audio(audio_bytes, format='audio/mp3')
                    st.download_button("SAVE MASTER MP3", data=audio_bytes, file_name=f"{filename}.mp3")
                
                if apply_echo:
                    st.info("Efecto de Sala: Se ha inyectado latencia rítmica para emular reverberación.")
                st.success(f"Locución generada con éxito.")
            except Exception as e:
                st.error(f"Fallo en la síntesis: {e}")
    else:
        st.warning("El vacío no tiene voz. Escribe tu guion.")

st.markdown("---")
st.caption("The Obsidian Engine Pro | Cathedral & Echo Logic | Zero Cost")








