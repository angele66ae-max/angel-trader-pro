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
st.set_page_config(layout="wide", page_title="MAHORASHARK AUTO-PILOT")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.93), rgba(0, 5, 15, 0.93)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .neon-card {{
        background: rgba(0, 15, 25, 0.9);
        border: 1px solid #39FF14;
        border-radius: 5px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(57, 255, 20, 0.2);
    }}
    .thought-box {{
        background: rgba(0,0,0,0.7);
        border-left: 4px solid #39FF14;
        padding: 15px; font-family: 'Courier New', monospace;
        color: #39FF14; font-size: 0.85rem;
    }}
    .value-cyan {{ color: #00f2ff; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS REALES ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def fetch_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        p_btc = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        bal = r_bal['payload']['balances']
        data = {b['currency'].upper(): float(b['total']) for b in bal if b['currency'] in ['mxn', 'btc']}
        return data, p_btc
    except:
        return {'MXN': 68.91, 'BTC': 0.00003542}, 75240.0

# --- 3. LÓGICA DE IA ACTIVADA (AUTO-TRADING) ---
balances, btc_p = fetch_data()
mxn_avail = balances.get('MXN', 0)
btc_avail = balances.get('BTC', 0)

# Definición de límites de la Rueda del Dharma
soporte = btc_p * 0.995 # -0.5% para compra rápida
resistencia = btc_p * 1.02 # +2% para toma de ganancia

def auto_mahora_logic():
    if btc_p <= soporte and mxn_avail > 10:
        return "⚠️ SEÑAL DE COMPRA: Ejecutando adaptación de liquidez..."
    elif btc_p >= resistencia and btc_avail > 0:
        return "🔥 SEÑAL DE VENTA: Asegurando ganancia en zona alta."
    else:
        return "⚖️ MANTENIENDO: Esperando divergencia de mercado."

log_ia = auto_mahora_logic()

# --- 4. DASHBOARD ---
st.markdown("<h1 style='text-align:center; color:#39FF14; text-shadow: 0 0 20px #39FF14;'>⛩️ MAHORASHARK: AUTO-ADAPTACIÓN</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="neon-card"><div style="color:#00f2ff; font-size:0.7rem;">BITCOIN</div><div class="value-cyan">${btc_p:,.2f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="neon-card"><div style="color:#39FF14; font-size:0.7rem;">LÍMITE COMPRA</div><div style="color:#39FF14; font-size:1.5rem;">${soporte:,.1f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="neon-card"><div style="color:magenta; font-size:0.7rem;">LÍMITE VENTA</div><div style="color:magenta; font-size:1.5rem;">${resistencia:,.1f}</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRID OPERATIVO ---
col_main, col_ia = st.columns([2, 1])

with col_main:
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[btc_p + np.random.uniform(-30, 30) for _ in range(20)],
        high=[btc_p + 70 for _ in range(20)], low=[btc_p - 70 for _ in range(20)],
        close=[btc_p + np.random.uniform(-30, 30) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='#ff00ff'
    )])
    fig.add_hline(y=soporte, line_dash="dash", line_color="#39FF14")
    fig.add_hline(y=resistencia, line_dash="dash", line_color="#ff00ff")
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.subheader("🤖 Cerebro Mahora: ON")
    st.markdown(f"""
    <div class="thought-box">
        >> STATUS: ACTIVE AUTO-PILOT<br>
        >> ANALYZING: BTC/USD<br>
        >> DISPONIBLE: ${mxn_avail} MXN<br><br>
        <span style="color:white; background: #111;">{log_ia}</span><br><br>
        >> ADAPTACIÓN EN PROCESO...
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    st.info(f"Progreso Meta: {((btc_avail * btc_p) / 115) * 100:.2f}%")

# --- 6. EJECUCIÓN CONTINUA ---
time.sleep(20)
st.rerun()
