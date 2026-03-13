import streamlit as st
import time, requests, hashlib, hmac, json
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(layout="wide", page_title="SHARK AI TERMINAL", page_icon="🦈")

# --- API SECRETS ---
API_KEY = st.secrets.get("BITSO_API_KEY", "")
API_SECRET = st.secrets.get("BITSO_API_SECRET", "")
BASE_URL = "https://api.bitso.com"

# --- DISEÑO CINEMATOGRÁFICO ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background: radial-gradient(circle at center, #050a0f 0%, #000000 100%); color: #e0e0e0; font-family: 'JetBrains Mono', monospace; }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 234, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        backdrop-filter: blur(15px);
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
    }
    
    .neon-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 40px;
        text-align: center;
        color: #00eaff;
        text-shadow: 0 0 15px #00eaff, 0 0 30px #bc13fe;
        margin-bottom: 25px;
    }
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS ---
def get_market_data():
    try:
        t = requests.get(f"{BASE_URL}/v3/ticker/?book=btc_mxn").json()["payload"]
        tr = requests.get(f"{BASE_URL}/v3/trades/?book=btc_mxn&limit=50").json()["payload"]
        df = pd.DataFrame(tr)
        df["price"] = df["price"].astype(float)
        return float(t["last"]), df
    except: return 0.0, pd.DataFrame()

# --- CÁLCULOS PREVIOS (Evita errores de variable no definida) ---
if "ai_on" not in st.session_state: st.session_state.ai_on = False
precio, df_trades = get_market_data()

# Simulación de balance para la meta de la SUV (esto se conectará a tu wallet real)
# Meta: $1,700,000 MXN
total_mxn_simulado = precio * 1.2 # Ejemplo: 1.2 BTC
meta_suv = 1700000
progreso_porcentaje = min((total_mxn_simulado / meta_suv) * 100, 100)

# --- INTERFAZ ---
st.markdown('<div class="neon-title">🦈 SHARK AI: PRESTIGE TERMINAL</div>', unsafe_allow_html=True)

# Dashboard de 4 Columnas
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="glass-card"><p style="color:#00eaff;margin:0">BTC MARKET</p><h2 style="margin:0">${precio:,.0f}</h2><small>MXN</small></div>', unsafe_allow_html=True)
with c2:
    # Cálculo rápido de RSI para el dashboard
    rsi_val = 54.20 # Valor estático para prueba de diseño
    st.markdown(f'<div class="glass-card"><p style="color:#bc13fe;margin:0">RSI INDEX</p><h2 style="margin:0">{rsi_val}</h2><small>STRENGTH</small></div>', unsafe_allow_html=True)
with c3:
    status = "ACTIVE" if st.session_state.ai_on else "OFFLINE"
    color = "#00ff00" if st.session_state.ai_on else "#ff4b4b"
    st.markdown(f'<div class="glass-card"><p style="color:{color};margin:0">AI ENGINE</p><h2 style="margin:0">{status}</h2><small>v10.1 CORE</small></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="glass-card"><p style="color:#00eaff;margin:0">GOAL SUV</p><h2 style="margin:0">{progreso_porcentaje:.1f}%</h2><progress value="{progreso_porcentaje}" max="100" style="width:100%"></progress></div>', unsafe_allow_html=True)

st.write("")

# Panel Principal
col_control, col_graph = st.columns([1, 2.5])

with col_control:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("🕹️ CONTROL")
    if st.button("🚀 DEPLOY AI", use_container_width=True): st.session_state.ai_on = True
    if st.button("🔒 STOP ENGINE", use_container_width=True): st.session_state.ai_on = False
    st.divider()
    st.write("MANUAL TRADE")
    if st.button("💸 BUY $100", use_container_width=True): st.toast("Order Sent", icon="⚡")
    st.markdown('</div>', unsafe_allow_html=True)

with col_graph:
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=df_trades["price"], mode='lines', line=dict(color='#00eaff', width=3), fill='tozeroy', fillcolor='rgba(0, 234, 255, 0.1)'))
    fig.update_layout(
        margin=dict(l=0, r=0, t=0, b=0), height=350,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False, visible=False), yaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig, use_container_width=True)

# --- REFRESH AUTOMÁTICO ---
time.sleep(15)
st.rerun()
