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

# Fondo personalizado y Estilos Neón
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
    }}
    .label {{ color: #00f2ff; letter-spacing: 2px; font-size: 12px; }}
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
    st.markdown(f'<div class="
