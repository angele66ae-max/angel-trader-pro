import streamlit as st
import time, requests, random
import pandas as pd
import plotly.graph_objects as go

# --- 1. CONFIGURACIÓN DE PANTALLA ANCHA ---
st.set_page_config(layout="wide", page_title="SHARK AI PRESTIGE", page_icon="🦈")

# --- 2. EL "LOOK" PROFESIONAL (CSS NEÓN) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    /* Fondo Oscuro Total */
    .stApp {
        background-color: #050a0f;
        color: #e0e0e0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    /* Tarjetas de Cristal */
    .glass-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 234, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 20px rgba(0,0,0,0.6);
    }
    
    /* Título Neón Animado */
    .neon-text {
        font-family: 'Orbitron', sans-serif;
        color: #00eaff;
        text-shadow: 0 0 10px #00eaff, 0 0 20px #bc13fe;
        text-align: center;
        font-size: 38px;
        margin-bottom: 30px;
    }
    
    /* Caja de Logs de la IA */
    .ai-brain {
        background-color: #000;
        border: 1px solid #00ff00;
        color: #00ff00;
        padding: 15px;
        border-radius: 8px;
        height: 250px;
        overflow-y: auto;
        font-size: 13px;
        box-shadow: inset 0 0 10px #00ff00;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. LÓGICA DE DATOS ---
if "logs" not in st.session_state:
    st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] SISTEMA INICIADO. OPERADOR: PAVO FREE FIRE"]

# Datos simulados de tu última captura
precio_btc = 1278010
rsi_val = 40.22
meta_objetivo = 1700000
progreso = (precio_btc / meta_objetivo) * 100

def add_log(msg):
    st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] {msg}")
    st.session_state.logs = st.session_state.logs[:15]

# --- 4. DISEÑO DE LA TERMINAL ---
st.markdown('<div class="neon-text">🦈 SHARK AI: PRESTIGE CENTER</div>', unsafe_allow_html=True)

# Fila 1: Métricas de Alto Impacto
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="glass-card"><p style="color:#00eaff">MARKET PRICE</p><h3>${precio_btc:,.0f}</h3><small>MXN</small></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="glass-card"><p style="color:#bc13fe">STRENGTH RSI</p><h3>{rsi_val}</h3><small>NEUTRAL</small></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="glass-card"><p style="color:#00ff00">AI ENGINE</p><h3>ACTIVE</h3><small>v10.5 CORE</small></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="glass-card"><p style="color:#00eaff">SUV GOAL</p><h3>{progreso:.1f}%</h3><progress value="{progreso}" max="100" style="width:100%"></progress></div>', unsafe_allow_html=True)

st.write("")

# Fila 2: Gráfico y Pensamientos de la IA
col_graph, col_logs = st.columns([2, 1])

with col_graph:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("📈 LIVE ANALYSIS")
    # Gráfico profesional con Plotly
    fig = go.Figure(go.Scatter(y=[1275000, 1279000, 1278010], fill='tozeroy', line_color='#00eaff', line_width=4))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, 
                      margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(visible=False), yaxis=dict(gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_logs:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🕵️ PENSAMIENTOS DE LA IA")
    log_content = "".join([f"<div>{l}</div>" for l in st.session_state.logs])
    st.markdown(f'<div class="ai-brain">{log_content}</div>', unsafe_allow_html=True)
    
    if st.button("🚀 FORZAR ANÁLISIS", use_container_width=True):
        add_log(f"Analizando BTC/MXN... RSI estable en {rsi_val}. No hay riesgo.")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# --- REFRESH ---
time.sleep(10)
st.rerun()
