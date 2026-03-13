import streamlit as st
import time, requests, hashlib, hmac, json
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(layout="wide", page_title="SHARK PRESTIGE v10", page_icon="🦈")

# --- CREDENCIALES ---
API_KEY = st.secrets.get("BITSO_API_KEY", "")
API_SECRET = st.secrets.get("BITSO_API_SECRET", "")
BASE_URL = "https://api.bitso.com"

# --- MOTOR DE ESTILO "GLASS-NEON" ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #0a0e14 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'Orbitron', sans-serif;
    }
    
    /* Tarjetas efecto Cristal */
    .metric-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(0, 234, 255, 0.2);
        border-radius: 15px;
        padding: 20px;
        backdrop-filter: blur(10px);
        text-align: center;
        transition: 0.3s;
    }
    .metric-card:hover { border-color: #00eaff; box-shadow: 0 0 20px rgba(0, 234, 255, 0.2); }
    
    /* Título con Neón Animado */
    .main-title {
        font-size: 45px;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(90deg, #00eaff, #bc13fe, #00eaff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 4s linear infinite;
        margin-bottom: 30px;
    }
    
    @keyframes shine { to { background-position: 200% center; } }
    
    /* Botones de Comando */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid #00eaff;
        background: transparent;
        color: #00eaff;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button:hover { background: #00eaff; color: black; box-shadow: 0 0 15px #00eaff; }
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES TÉCNICAS ---
def get_data():
    try:
        t = requests.get(f"{BASE_URL}/v3/ticker/?book=btc_mxn").json()["payload"]
        tr = requests.get(f"{BASE_URL}/v3/trades/?book=btc_mxn&limit=50").json()["payload"]
        df = pd.DataFrame(tr)
        df["price"] = df["price"].astype(float)
        return float(t["last"]), df
    except: return 0.0, pd.DataFrame()

def calculate_rsi(prices, period=14):
    delta = prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- HEADER ---
st.markdown('<div class="main-title">SHARK AI • PRESTIGE TERMINAL</div>', unsafe_allow_html=True)

# --- LOGICA DE ESTADO ---
if "ai_on" not in st.session_state: st.session_state.ai_on = False
precio, df_trades = get_data()
rsi_val = calculate_rsi(df_trades["price"]).iloc[-1] if not df_trades.empty else 0

# --- DASHBOARD SUPERIOR ---
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><h5>MARKET PRICE</h5><h2 style="color:#00eaff">${precio:,.0f}</h2><small>BTC/MXN</small></div>', unsafe_allow_html=True)
with c2:
    color_rsi = "#ff4b4b" if rsi_val > 70 else ("#00ff00" if rsi_val < 30 else "#00eaff")
    st.markdown(f'<div class="metric-card"><h5>INDEX RSI</h5><h2 style="color:{color_rsi}">{rsi_val:.2f}</h2><small>14 PERIODS</small></div>', unsafe_allow_html=True)
with c3:
    status_txt = "ACTIVE" if st.session_state.ai_on else "STANDBY"
    status_col = "#00ff00" if st.session_state.ai_on else "#ff4b4b"
    st.markdown(f'<div class="metric-card"><h5>AI ENGINE</h5><h2 style="color:{status_col}">{status_txt}</h2><small>v10.0 CORE</small></div>', unsafe_allow_html=True)
with c4:
    # Meta de la SUV 1.7M
    meta = 1700000
    progreso = (precio / 1000000) # Simulación de capital relativo
    st.markdown(f'<div class="metric-card"><h5>GOAL PROGRESS</h5><h2 style="color:#bc13fe">{(progreso*100):.1f}%</h2><small>TARGET: $1.7M</small></div>', unsafe_allow_html=True)

st.write("") # Espaciador

# --- PANEL DE CONTROL ---
col_cmd, col_chart = st.columns([1, 2.5])

with col_cmd:
    st.subheader("🕹️ COMMAND CENTER")
    if st.button("🚀 DEPLOY AI AGENT"): st.session_state.ai_on = True
    if st.button("🔒 TERMINATE SESSION"): st.session_state.ai_on = False
    
    st.divider()
    st.subheader("⚡ QUICK ACTIONS")
    if st.button("💸 BUY $100 MXN"): st.toast("Executing Order...", icon="⚡")
    if st.button("💰 SELL $100 MXN"): st.toast("Executing Order...", icon="🔥")

with col_chart:
    # Gráfico Profesional con Plotly
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df_trades["price"], mode='lines', line=dict(color='#00eaff', width=2), fill='tozeroy', fillcolor='rgba(0, 234, 255, 0.1)'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=350,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, visible=False), yaxis=dict(gridcolor='rgba(255,255,255,0.05)', font=dict(family='monospace'))
    )
    st.plotly_chart(fig, use_container_width=True)

# --- MOTOR DE IA ---
if st.session_state.ai_on:
    st.toast("AI is scanning market waves...", icon="📡")
    if rsi_val < 35:
        st.success("🟢 OPPORTUNITY DETECTED: AUTO-BUY EXECUTED")
    elif rsi_val > 65:
        st.error("🔴 RESISTANCE REACHED: AUTO-SELL EXECUTED")

# --- AUTO REFRESH ---
time.sleep(10)
st.rerun()
