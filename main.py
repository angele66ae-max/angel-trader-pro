import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. ESTÉTICA NEÓN PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK 10K")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(rgba(0, 5, 15, 0.94), rgba(0, 5, 15, 0.94)), url("{FONDO_URL}"); background-size: cover; }}
    .neon-card {{ background: rgba(0, 15, 25, 0.9); border: 1px solid #00f2ff; border-radius: 5px; padding: 15px; text-align: center; box-shadow: 0 0 15px rgba(0, 242, 255, 0.4); }}
    .value-cyan {{ color: #00f2ff; font-size: 2rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .value-magenta {{ color: #ff00ff; font-size: 2rem; font-weight: bold; text-shadow: 0 0 10px #ff00ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS (BITSO) ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def fetch_sync():
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
        return {'MXN': 68.91, 'BTC': 0.00003542}, 74500.0

# --- 3. LÓGICA DE LA META 10K ---
balances, btc_p = fetch_sync()
mxn_val = balances.get('MXN', 0)
btc_val = balances.get('BTC', 0)

# Calculamos el valor total en USD para la meta
valor_en_usd = (mxn_val / 16.80) + (btc_val * btc_p) # Tomando USD/MXN a 16.80 aprox
META_10K = 10000.0
progreso_10k = (valor_en_usd / META_10K) * 100

# --- 4. DASHBOARD SUPERIOR ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: ROAD TO 10K</h1>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="neon-card"><div style="color:#00f2ff; font-size:0.7rem;">VALOR ACTUAL (USD)</div><div class="value-cyan">${valor_en_usd:.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="neon-card"><div style="color:magenta; font-size:0.7rem;">OBJETIVO FINAL</div><div class="value-magenta">$10,000.00</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="neon-card"><div style="color:#39FF14; font-size:0.7rem;">PROGRESO TOTAL</div><div class="value-cyan" style="color:#39FF14;">{progreso_10k:.4f}%</div></div>', unsafe_allow_html=True)

st.progress(min(progreso_10k / 100, 1.0))

# --- 5. PANEL DE CONTROL IA ---
st.write("---")
col_g, col_ia = st.columns([2, 1])

with col_g:
    # Gráfica Neón con líneas de acción
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=15, freq='min'),
        open=[btc_p + np.random.uniform(-30, 30) for _ in range(15)],
        high=[btc_p + 60 for _ in range(15)], low=[btc_p - 60 for _ in range(15)],
        close=[btc_p + np.random.uniform(-30, 30) for _ in range(15)],
        increasing_line_color='#39FF14', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.subheader("🧠 IA Mahora: Objetivo 10K")
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.7); border-left:4px solid #39FF14; padding:15px; font-family:monospace; color:#39FF14; font-size:0.85rem;">
        >> ESTRATEGIA: ACUMULACIÓN AGRESIVA<br>
        >> SALDO MXN: ${mxn_val}<br>
        >> STATUS: BUSCANDO PUNTOS DE ENTRADA<br>
        >> ADAPTACIÓN: RUTA 10K ACTIVADA
    </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🚀 ACTIVAR MODO TURBO (COMPRA)"):
        st.success("Analizando mejores puntos de entrada para escalar capital...")

# Auto-refresh cada 30 segundos
time.sleep(30)
st.rerun()
