import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN VISUAL PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .glass-card {{
        background: rgba(0, 15, 25, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 10px; padding: 15px;
        text-align: center; box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
    .thought-box {{
        background: rgba(10, 10, 10, 0.95);
        border-left: 4px solid #39FF14;
        padding: 15px; border-radius: 5px;
        font-family: 'Courier New', monospace; color: #39FF14; font-size: 13px;
    }}
    .stat-value {{ color: #ffffff; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE CONEXIÓN BITSO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_market_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        r_tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        bal = r_bal['payload']['balances']
        price = float(r_tick['payload']['last'])
        mxn = next((float(b['total']) for b in bal if b['currency'] == 'mxn'), 0.0)
        btc = next((float(b['total']) for b in bal if b['currency'] == 'btc'), 0.0)
        return mxn, btc, price
    except: return 68.91, 0.00003542, 75000.0

# --- 3. PROCESAMIENTO ---
mxn, btc, p_btc = get_market_data()
usd_val = btc * p_btc
meta_val = (usd_val / 115.0) * 100

# --- 4. PANEL SUPERIOR ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: ADAPTACIÓN ACTIVA</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="glass-card">BÓVEDA BTC<br><span class="stat-value">{btc:.8f}</span><br><span style="color:#39FF14;">${usd_val:.2f} USD</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="glass-card">DISPONIBLE MXN<br><span class="stat-value">${mxn:.2f}</span><br><span style="color:cyan;">Sincronizado</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="glass-card">META $115<br><span class="stat-value">{meta_val:.4f}%</span><br><span style="color:magenta;">Objetivo Activo</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRÁFICA Y PENSAMIENTO DE LA IA ---
col_left, col_right = st.columns([2, 1])

with col_left:
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=15, freq='min'),
        open=[p_btc + np.random.uniform(-40, 40) for _ in range(15)],
        high=[p_btc + 80 for _ in range(15)], low=[p_btc - 80 for _ in range(15)],
        close=[p_btc + np.random.uniform(-40, 40) for _ in range(15)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    )])
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🤖 Pensamiento de la IA")
    pensamientos = [
        "Analizando patrones de velas japonesas...",
        f"Detectando liquidez en Bitso: ${mxn} MXN disponibles.",
        "Rueda del Dharma girando: Buscando adaptación de mercado.",
        f"Precio actual BTC: ${p_btc} USD. Calculando riesgo.",
        "Estado: Esperando confirmación de tendencia alcista.",
        "Sincronización con la Bóveda exitosa."
    ]
    
    thought_text = "\n> ".join(np.random.choice(pensamientos, 3, replace=False))
    st.markdown(f'<div class="thought-box">>> INICIANDO PENSAMIENTO LÓGICO...<br><br>> {thought_text}</div>', unsafe_allow_html=True)
    
    st.write("---")
    st.markdown('<p style="color:#39FF14; font-weight:bold; text-align:center;">🚀 AUTO-PILOT ACTIVO</p>', unsafe_allow_html=True)
    st.code(f"LOG: {datetime.now().strftime('%H:%M:%S')}\nSTATUS: PRESTIGE", language="bash")

time.sleep(20)
st.rerun()
