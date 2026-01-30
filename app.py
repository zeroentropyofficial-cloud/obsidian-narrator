import streamlit as st
import edge_tts
import asyncio
import os

# Interfaz High-End
st.set_page_config(page_title="Obsidian Engine US", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; font-family: 'serif'; }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #D4AF37; color: #0A0A0A; }
    label { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN ENGINE: US EDITION")

# --- Mapa de Voces Americanas y Regionales ---
accent_map = {
    "🇺🇸 ALGIEBA-US (Deep & Ancient)": "en-US-ChristopherNeural",
    "🇺🇸 US Authority (Knights Style)": "en-US-EricNeural",
    "🇺🇸 US Narrative (Smooth)": "en-US-GuyNeural",
    "🇺🇸 US Professional (Neutral)": "en-US-AndrewNeural",
    "🇲🇽 Neutro LATAM": "es-MX-GerardoNeural",
    "🇨🇴 Colombia": "es-CO-GonzaloNeural",
    "🇦🇷 Argentina": "es-AR-TomasNeural"
}

# --- Configuración de Ánimos ---
mood_settings = {
    "Neutral": {"pitch": -5, "rate": 5},
    "🔥 Autoridad Máxima": {"pitch": -20, "rate": 15},
    "📜 Sabiduría (Algieba)": {"pitch": -18, "rate": -5},
    "🌑 Sombrío": {"pitch": -30, "rate": -10}
}

with st.sidebar:
    st.header("⚙️ Configuración")
    selected_voice = st.selectbox("Voz Americana / Regional", list(accent_map.keys()))
    selected_mood = st.selectbox("Inferencia de Ánimo", list(mood_settings.keys()))
    
    st.markdown("---")
    p_adj = st.slider("Ajuste de Graves (Pitch)", -20, 10, 0)
    r_adj = st.slider("Ajuste de Ritmo (Rate)", -20, 20, 0)
    
    # Parámetros finales con protección de límites
    final_p = max(min(mood_settings[selected_mood]["pitch"] + p_adj, 10), -40)
    final_r = max(min(mood_settings[selected_mood]["rate"] + r_adj, 50), -25)

# --- Consola de Etiquetas ---
st.subheader("🎙️ Comandos de Actuación")
if 'text' not in st.session_state: st.session_state.text = ""

c1, c2, c3, c4 = st.columns(4)
with c1: 
    if st.button("🤫 Susurro"): st.session_state.text += " ... (whispering) ... "
with c2: 
    if st.button("📢 Grito"): st.session_state.text += " !! (shouting) !! "
with c3: 
    if st.button("😮‍💨 Suspiro"): st.session_state.text += " ... (sigh) ... "
with c4: 
    if st.button("⏳ Pausa"): st.session_state.text += " ...... "

text_input = st.text_area("Script:", value=st.session_state.text, height=250)
st.session_state.text = text_input

# --- Función de Síntesis con Manejo de Errores ---
async def generate_speech(text, voice, output, p, r):
    # Limpiamos etiquetas para evitar el error NoAudioReceived
    clean_text = text.replace("(whispering)", "").replace("(shouting)", "").replace("(sigh)", "")
    
    p_str = f"{p}Hz"
    r_str = f"+{r}%" if r >= 0 else f"{r}%"
    
    try:
        communicate = edge_tts.Communicate(clean_text, voice, rate=r_str, pitch=p_str, volume="+15%")
        await communicate.save(output)
    except Exception as e:
        # Modo de rescate si los parámetros fallan
        st.error(f"Error detectado. Re-intentando con parámetros seguros...")
        communicate = edge_tts.Communicate(clean_text, voice, rate="+5%", pitch="-5Hz")
        await communicate.save(output)

if st.button("INVOKE US VOICE", use_container_width=True):
    if st.session_state.text:
        out_file = "output_us.mp3"
        with st.spinner("Procesando Voz Americana..."):
            asyncio.run(generate_speech(st.session_state.text, accent_map[selected_voice], out_file, final_p, final_r))
            
            with open(out_file, 'rb') as f:
                st.audio(f.read())
                st.download_button("Descargar Master MP3", f, file_name="obsidian_us.mp3")
    else:
        st.warning("Escriba un guion para proceder.")










