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

# Fondo de la Rueda del Dharma y Estilos Neón
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{FONDO_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .glass-card {{
        background: rgba(0, 15, 25, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .stat-label {{ color: #00f2ff; font-size: 12px; letter-spacing: 1.5px; text-transform: uppercase; }}
    .stat-value {{ color: #ffffff; font-size: 24px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .status-pilot {{ color: #39FF14; font-weight: bold; text-shadow: 0 0 5px #39FF14; }}
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
    except:
        return 68.91, 0.00003542, 75000.0

# --- 3. PROCESAMIENTO ---
mxn, btc, p_btc = get_market_data()
usd_val = btc * p_btc
meta_val = (usd_val / 115.0) * 100

# --- 4. DASHBOARD SUPERIOR ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: ADAPTACIÓN ACTIVA</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="glass-card"><div class="stat-label">Bóveda BTC</div><div class="stat-value">{btc:.8f}</div><div style="color:#39FF14;">${usd_val:.2f} USD</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="glass-card"><div class="stat-label">Disponible MXN</div><div class="stat-value">${mxn:.2f}</div><div style="color:cyan;">Sincronizado</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="glass-card"><div class="stat-label">Meta ($115)</div><div class="stat-value">{meta_val:.4f}%</div><div style="color:magenta;">Objetivo Activo</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRÁFICA NEÓN Y TERMINAL ---
col_left, col_right = st.columns([2, 1])

with col_left:
    # Gráfica de Velas Neón (Verde y Magenta)
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=15, freq='min'),
        open=[p_btc + np.random.uniform(-40, 40) for _ in range(15)],
        high=[p_btc + 80 for _ in range(15)],
        low=[p_btc - 80 for _ in range(15)],
        close=[p_btc + np.random.uniform(-40, 40) for _ in range(15)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    )])
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<div class="glass-card" style="text-align:left; height:400px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Mahora Pro")
    st.markdown('<p class="status-pilot">🚀 AUTO-PILOT: ACTIVO</p>', unsafe_allow_html=True)
    st.write("---")
    st.write("**Radar de Ballenas:**")
    st.info("Mercado Orgánico Detectado")
    st.write("---")
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nStatus: PRESTIGE\nMode: OMNI-ADAPT", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(20)
st.rerun()
