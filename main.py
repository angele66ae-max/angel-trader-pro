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

# Tus Llaves de Poder
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

st.markdown("""
<style>
    .stApp { background-color: #00050a; color: #e0e0e0; }
    [data-testid="stMetricValue"] { color: #00f2ff !important; font-size: 32px !important; }
    .metric-card {
        background: rgba(0, 20, 40, 0.6);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .status-active { color: #39FF14; font-weight: bold; text-shadow: 0 0 10px #39FF14; }
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE CONEXIÓN REAL (BITSO) ---
def get_bitso_balance():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        return r['payload']['balances']
    except: return []

# --- 3. DATOS DE MERCADO Y PROGRESO ---
try:
    # Precio BTC
    r_tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_actual = float(r_tick['payload']['last'])
    
    # Obtener Saldo Real
    balances = get_bitso_balance()
    btc_real = next((float(b['total']) for b in balances if b['currency'] == 'btc'), 0.0)
    usd_real = next((float(b['total']) for b in balances if b['currency'] == 'usd'), 0.0)
    mxn_real = next((float(b['total']) for b in balances if b['currency'] == 'mxn'), 0.0)
    
    valor_btc_usd = btc_real * p_actual
    progreso = (valor_btc_usd / 115.0) * 100
except:
    p_actual, btc_real, usd_real, mxn_real, valor_btc_usd, progreso = 70000.0, 0.00003542, 0.22, 0.0, 2.5, 2.2

# --- 4. PANEL PRINCIPAL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK: OMNI-SYNCHRONIZED</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st
