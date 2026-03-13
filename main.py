import streamlit as st
import time, requests, hashlib, hmac, json
import pandas as pd
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(layout="wide", page_title="SHARK SYSTEM v10", page_icon="🦈")

# --- CREDENCIALES (Asegúrate de configurar esto en .streamlit/secrets.toml) ---
API_KEY = st.secrets.get("BITSO_API_KEY", "")
API_SECRET = st.secrets.get("BITSO_API_SECRET", "")
BASE_URL = "https://api.bitso.com"

# --- MOTOR DE ESTILO CYBER-GLASS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp {
        background: radial-gradient(circle at center, #050a0f 0%, #000000 100%);
        color: #e0e0e0;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .title-container {
        font-family: 'Orbitron', sans-serif;
        font-size: 42px;
        text-align: center;
        background: linear-gradient(90deg, #00eaff, #bc13fe, #00eaff);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: shine 5s linear infinite;
        padding: 20px;
    }
    
    @keyframes shine { to { background-position: 200% center; } }

    /* Tarjetas con Efecto Cristal */
    .glass-card {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid rgba(0, 234, 255, 0.15);
        border-radius: 12px;
        padding: 18px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        height: 100%;
    }
</style>
<div class="title-container">🦈 SHARK SYSTEM: NEON CORE v10.0</div>
""", unsafe_allow_html=True)

# --- SISTEMA DE DATOS Y DIAGNÓSTICO ---
def fetch_market_data():
    try:
        # Ticker y Trades
        t_resp = requests.get(f"{BASE_URL}/v3/ticker/?book=btc_mxn", timeout=10).json()
        tr_resp = requests.get(f"{BASE_URL}/v3/trades/?book=btc_mxn&limit=50", timeout=10).json()
        
        if "payload" not in t_resp:
            return None, None, f"Error Bitso: {t_resp.get('error', {}).get('message', 'Desconocido')}"
            
        price = float(t_resp["payload"]["last"])
        df = pd.DataFrame(tr_resp["payload"])
        df["price"] = df["price"].astype(float)
        return price, df, None
    except Exception as e:
        return None, None, str(e)

# --- LÓGICA DE PROCESAMIENTO ---
precio, df_trades, error_msg = fetch_market_data()

# --- INTERFAZ DE USUARIO ---
if error_msg:
    st.error(f"🚨 FALLO DE ENLACE: {error_msg}")
    st.info("💡 TIP: Revisa tus API Secrets y que la IP Whitelist esté vacía en Bitso.")
else:
    # 1. MÉTRICAS PRINCIPALES
    c1, c2, c3, c4 = st.columns(4)
    
    with c1:
        st.markdown(f'<div class="glass-card"><p style="color:#00eaff;margin:0">BTC PRICE</p><h2 style="margin:0">${precio:,.0f}</h2><small>MXN/UNIT</small></div>', unsafe_allow_html=True)
    
    with c2:
        # Cálculo simple de RSI para la interfaz
        delta = df_trades["price"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain/loss))).iloc[-1]
        color = "#00ff00" if rsi < 35 else ("#ff4b4b" if rsi > 65 else "#bc13fe")
        st.markdown(f'<div class="glass-card"><p style="color:{color};margin:0">RSI SIGNAL</p><h2 style="margin:0">{rsi:.2f}</h2><small>STRENGTH INDEX</small></div>', unsafe_allow_html=True)

    with c3:
        status = "ACTIVO" if st.session_state.get("ai_on", False) else "STANDBY"
        s_col = "#00ff00" if status == "ACTIVO" else "#666"
        st.markdown(f'<div class="glass-card"><p style="color:{s_col};margin:0">AI ENGINE</p><h2 style="margin:0">{status}</h2><small>OPERADOR: Pavo Free Fire</small></div>', unsafe_allow_html=True)

    with c4:
        # Meta de la SUV de 1.7M
        meta = 1700000
        progreso = (precio / 1300000) * 100 # Simulación de porcentaje de ahorro
        st.markdown(f'<div class="glass-card"><p style="color:#00eaff;margin:0">GOAL: SUV $1.7M</p><h2 style="margin:0">{progreso:.1f}%</h2><progress value="{progreso}" max="100" style="width:100%"></progress></div>', unsafe_allow_html=True)

    st.write("")

    # 2. PANEL DE CONTROL Y GRÁFICO
    col_ctrl, col_graph = st.columns([1, 2.5])

    with col_ctrl:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("🕹️ COMMANDS")
        if st.button("🚀 DEPLOY AI AGENT", use_container_width=True):
            st.session_state.ai_on = True
        if st.button("🔒 TERMINATE SESSION", use_container_width=True):
            st.session_state.ai_on = False
        
        st.divider()
        st.write("MANUAL OVERRIDE")
        if st.button("💸 QUICK BUY $100", use_container_width=True):
            st.toast("Procesando orden...", icon="⚡")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_graph:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=df_trades["price"], mode='lines', line=dict(color='#00eaff', width=3), fill='tozeroy', fillcolor='rgba(0, 234, 255, 0.1)'))
        fig.update_layout(
            margin=dict(l=0, r=0, t=10, b=0), height=350,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis=dict(showgrid=False, visible=False), 
            yaxis=dict(gridcolor='rgba(255,255,255,0.05)', font=dict(family='JetBrains Mono'))
        )
        st.plotly_chart(fig, use_container_width=True)

# --- AUTO REFRESH ---
time.sleep(15)
st.rerun()
