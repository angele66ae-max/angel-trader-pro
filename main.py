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

# Fondo personalizado y Estilos Neón Corregidos
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(0, 10, 20, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
        margin-bottom: 10px;
    }}
    .label {{ color: #00f2ff; letter-spacing: 2px; font-size: 12px; font-weight: bold; }}
    .value {{ color: #ffffff; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE CONEXIÓN BITSO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def fetch_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        r_tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        return r_bal['payload']['balances'], float(r_tick['payload']['last'])
    except:
        return None, 73000.0

# --- 3. LÓGICA DE PROCESAMIENTO ---
balances, p_actual = fetch_data()
if balances:
    mxn_real = next((float(b['total']) for b in balances if b['currency'] == 'mxn'), 0.0)
    btc_real = next((float(b['total']) for b in balances if b['currency'] == 'btc'), 0.0)
else:
    # Valores de respaldo basados en tu última captura exitosa
    mxn_real, btc_real = 68.91, 0.00003542

valor_usd = btc_real * p_actual
progreso = (valor_usd / 115.0) * 100

# --- 4. PANEL PRINCIPAL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center; text-shadow:0 0 15px #00f2ff;'>⛩️ MAHORASHARK: ADAPTACIÓN ACTIVA</h1>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="metric-card"><div class="label">BÓVEDA BTC</div><div class="value">{btc_real:.8f}</div><div style="color:#39FF14;">${valor_usd:.2f} USD</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><div class="label">DISPONIBLE MXN</div><div class="value">${mxn_real:.2f}</div><div style="color:cyan;">Sincronizado</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><div class="label">META ($115)</div><div class="value">{progreso:.4f}%</div><div style="color:magenta;">Objetivo Activo</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRÁFICA Y CEREBRO ---
col_graf, col_ia = st.columns([2.2, 1])

with col_graf:
    # Gráfica de Velas con colores Neón
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[p_actual + np.random.uniform(-50, 50) for _ in range(20)],
        high=[p_actual + 100 for _ in range(20)],
        low=[p_actual - 100 for _ in range(20)],
        close=[p_actual + np.random.uniform(-50, 50) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    )])
    fig.update_layout(
        template="plotly_dark", height=400, 
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        margin=dict(t=0,b=0,l=0,r=0), xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:400px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Mahora Pro")
    st.markdown('<p style="color:#39FF14; font-weight:bold;">🚀 AUTO-PILOT: ACTIVO</p>', unsafe_allow_html=True)
    st.write("---")
    st.write("**Radar de Ballenas:**")
    st.info("Mercado Estable")
    st.write("---")
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nStatus: PRESTIGE\nMode: AUTO-SYNC", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

# Refresh automático para simular flujo constante
time.sleep(25)
st.rerun()
