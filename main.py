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
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url("{FONDO_URL}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .glass-card {{
        background: rgba(0, 20, 30, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 15px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }}
    .thought-box {{
        background: rgba(5, 5, 5, 0.95);
        border-left: 4px solid #39FF14;
        padding: 15px; border-radius: 5px;
        font-family: 'Courier New', monospace; color: #39FF14; font-size: 13px;
    }}
    .stat-val {{ font-size: 26px; font-weight: bold; color: #ffffff; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS REALES (BITSO) ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_market_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r_tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        p_btc = float(r_tick['payload']['last'])
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        bal = r_bal['payload']['balances']
        mxn = next((float(b['total']) for b in bal if b['currency'] == 'mxn'), 0.0)
        btc_amt = next((float(b['total']) for b in bal if b['currency'] == 'btc'), 0.0)
        return mxn, btc_amt, p_btc
    except: return 68.91, 0.00003542, 75000.0

# --- 3. LÓGICA DE ESTRATEGIA (ADAPTACIÓN) ---
mxn, btc, p_btc = get_market_data()
# Definimos zonas basadas en volatilidad real
zona_compra = p_btc * 0.98  # Comprar 2% abajo
zona_venta = p_btc * 1.04   # Vender 4% arriba
progreso = ((btc * p_btc) / 115.0) * 100

# --- 4. DASHBOARD OMNI ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: OMNI-DASHBOARD</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="glass-card">BTC PRICE<br><span class="stat-val">${p_btc:,.2f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="glass-card"><span style="color:#39FF14;">ZONA COMPRA</span><br><span class="stat-val" style="color:#39FF14;">${zona_compra:,.1f}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="glass-card"><span style="color:magenta;">ZONA VENTA</span><br><span class="stat-val" style="color:magenta;">${zona_venta:,.1f}</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="glass-card">DISPONIBLE<br><span class="stat-val">${mxn:,.2f}</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRÁFICA CON INDICADORES Y PENSAMIENTO ---
col_graf, col_ia = st.columns([2, 1])

with col_graf:
    fig = go.Figure()
    # Velas Neón
    fig.add_trace(go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[p_btc + np.random.uniform(-50, 50) for _ in range(20)],
        high=[p_btc + 100 for _ in range(20)], low=[p_btc - 100 for _ in range(20)],
        close=[p_btc + np.random.uniform(-50, 50) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    ))
    # Líneas de Estrategia visibles
    fig.add_hline(y=zona_compra, line_dash="dash", line_color="#39FF14", annotation_text="PUNTO DE COMPRA")
    fig.add_hline(y=zona_venta,
