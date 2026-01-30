import streamlit as st
import edge_tts
import asyncio
import os

# Interfaz High-End Dark Academia
st.set_page_config(page_title="Obsidian Engine Research", page_icon="🏛️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0A0A0A; color: #FFFFFF; }
    .stTextArea textarea { background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37; font-family: 'serif'; font-size: 1.1rem; }
    h1, h3 { color: #D4AF37; font-family: 'serif'; text-align: center; }
    .stButton>button { 
        background-color: #111111; color: #D4AF37; border: 1px solid #D4AF37;
        font-weight: bold; width: 100%; transition: 0.3s;
    }
    .stButton>button:hover { background-color: #D4AF37; color: #0A0A0A; box-shadow: 0px 0px 15px #D4AF37; }
    .action-btn>div>button { background-color: #D4AF37 !important; color: #0A0A0A !important; font-size: 1.2rem !important; height: 4em !important; }
    label { color: #D4AF37 !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏛️ THE OBSIDIAN ENGINE: RESEARCH V1.5")
st.markdown("### Arquitectura Unificada • Control Paralingüístico • SLM Logic")

# Voces del Ecosistema 2026
accent_map = {
    "✨ ALGIEBA (Legacy SLM)": "es-MX-GerardoNeural",
    "🎙️ QWEN3-US (High Latency)": "en-US-ChristopherNeural",
    "🎙️ CHATTERBOX-UK (Narrator)": "en-GB-RyanNeural",
    "🇦🇷 ARG-V1.5 (DualAR)": "es-AR-TomasNeural",
    "🇨🇴 COL-V1.5 (Prosody)": "es-CO-GonzaloNeural"
}

# Configuración de Estados Emocionales (SLM)
mood_settings = {
    "Neutral/Inference": {"pitch": -5, "rate": 5, "volume": "+10%"},
    "Deep Authority (Knights)": {"pitch": -25, "rate": 12, "volume": "+20%"},
    "Ancient Wisdom (Algieba)": {"pitch": -20, "rate": -8, "volume": "+15%"},
    "Aggressive Staccato": {"pitch": -10, "rate": 30, "volume": "+25%"}
}

with st.sidebar:
    st.header("⚙️ Arquitectura")
    selected_voice = st.selectbox("Speech Language Model", list(accent_map.keys()))
    selected_mood = st.selectbox("Inferencia Emocional", list(mood_settings.keys()))
    
    st.markdown("---")
    st.subheader("Control de Latencia")
    latency_mode = st.toggle("Optimizar Latencia (Stream)", value=True)
    
    st.markdown("---")
    st.subheader("Ajuste de Codebook")
    p_adj = st.slider("Pitch (Hz)", -30, 10, 0)
    r_adj = st.slider("Rate (%)", -20, 20, 0)
    
    final_p = mood_settings[selected_mood]["pitch"] + p_adj
    final_r = mood_settings[selected_mood]["rate"] + r_adj
    final_vol = mood_settings[selected_mood]["volume"]

# --- Consola de Comandos Paralingüísticos ---
st.subheader("🎙️ Consola de Comandos (Inserción de Etiquetas)")
c1, c2, c3, c4, c5 = st.columns(5)

# Función para insertar etiquetas en el texto (Simulada por interfaz)
tags = {
    "c1": "[WHISPERING]", 
    "c2": "[SHOUTING]", 
    "c3": "[SIGH]", 
    "c4": "[LAUGH]", 
    "c5": "[PAUSE_2S]"
}

with c1: st.button("🤫 Susurro", on_click=lambda: st.session_state.update(text=st.session_state.get('text', '') + " (whispering) "))
with c2: st.button("📢 Grito", on_click=lambda: st.session_state.update(text=st.session_state.get('text', '') + " (shouting) "))
with c3: st.button("😮‍💨 Suspiro", on_click=lambda: st.session_state.update(text=st.session_state.get('text', '') + " ... (sigh) ... "))
with c4: st.button("🎭 Énfasis", on_click=lambda: st.session_state.update(text=st.session_state.get('text', '') + " --EMPHASIS-- "))
with c5: st.button("⏳ Pausa Larga", on_click=lambda: st.session_state.update(text=st.session_state.get('text', '') + " ...... "))

# Entrada de Texto con persistencia
if 'text' not in st.session_state: st.session_state.text = ""
text_input = st.text_area("Script de Inferencia:", value=st.session_state.text, height=250, key="text_area_input")
st.session_state.text = text_input

async def generate_speech(text, voice, output, p, r, vol):
    # LIMPIEZA DE ETIQUETAS: El motor gratuito no entiende (whispering) 
    # y lo interpreta como ruido, causando el error NoAudioReceived.
    # Esta función las convierte en puntuación que la IA sí entiende.
    processed = text.replace("(whispering)", "...").replace("(shouting)", "!!!")
    processed = processed.replace("(sigh)", "...").replace("(laugh)", " ha ha ha ")
    
    # NORMALIZACIÓN DE PARÁMETROS:
    # Limitamos los valores para no romper el motor de audio
    safe_p = max(min(p, 20), -40) # No bajar de -40Hz
    safe_r = max(min(r, 50), -25) # No bajar de -25%
    
    p_str = f"{safe_p}Hz"
    r_str = f"+{safe_r}%" if safe_r >= 0 else f"{safe_r}%"
    
    try:
        communicate = edge_tts.Communicate(processed, voice, rate=r_str, pitch=p_str, volume=vol)
        await communicate.save(output)
    except Exception as e:
        # Si falla con los parámetros Pro, intenta una versión "Safe" automática
        st.warning("Parámetros demasiado agresivos. Re-intentando en modo seguro...")
        communicate = edge_tts.Communicate(processed, voice, rate="+5%", pitch="-10Hz", volume="+10%")
        await communicate.save(output)

st.markdown("---")
if st.button("INVOKE SLM SYNTHESIS", icon="🔥", use_container_width=True):
    if st.session_state.text:
        out_file = "research_output.mp3"
        with st.spinner("Realizando inferencia semántica..."):
            asyncio.run(generate_speech(st.session_state.text, accent_map[selected_voice], out_file, final_p, final_r, final_vol))
            
            with open(out_file, 'rb') as f:
                st.audio(f.read())
                st.download_button("Exportar Master MP3", f, file_name="obsidian_research.mp3")
    else:
        st.error("No hay datos para la síntesis.")

st.caption("Ecosistema de Síntesis Unificada 2026 | Fish Speech & Qwen3 Optimized Architecture")










