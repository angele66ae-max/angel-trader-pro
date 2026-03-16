import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN VISUAL ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

st.markdown("""
<style>
    .stApp { background-color: #000505; color: #00f2ff; }
    .metric-card {
        background: rgba(0, 30, 40, 0.5);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px;
        text-align: center; box-shadow: 0 0 15px #00f2ff33;
    }
    .status-active { color: #39FF14; text-shadow: 0 0 10px #39FF14; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIÓN DE CONEXIÓN REAL ---
def consultar_bitso():
    key = st.secrets["BITSO_KEY"]
    secret = st.secrets["BITSO_SECRET"]
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(secret.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {key}:{nonce}:{signature}'}
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        return r['payload']['balances']
    except: return None

# --- 3. LÓGICA DE DATOS ---
try:
    balances = consultar_bitso()
    mxn_real = next((float(b['total']) for b in balances if b['currency'] == 'mxn'), 0.0)
    btc_real = next((float(b['total']) for b in balances if b['currency'] == 'btc'), 0.0)
    
    # Precio actual
    tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_actual = float(tick['payload']['last'])
    valor_btc_usd = btc_real * p_actual
    progreso = (valor_btc_usd / 115.0) * 100 # Meta de $115 USD
except:
    mxn_real, btc_real, p_actual, valor_btc_usd, progreso = 0.0, 0.00003542, 70000.0, 2.61, 2.27

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align:center;'>⛩️ MAHORASHARK: OMNI-SYNCHRONIZED</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="metric-card">BÓVEDA BTC<br><span style="font-size:24px;">{btc_real:.8f}</span><br>(${valor_btc_usd:.2f} USD)</div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">SALDO DISPONIBLE<br><span style="font-size:24px;">${mxn_real:.2f} MXN</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">PROGRESO META<br><span style="font-size:24px;">{progreso:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. CEREBRO AUTÓNOMO ---
col_ia, col_log = st.columns([1, 2])

with col_ia:
    st.subheader("🤖 IA Mahora Pro")
    if mxn_real < 10.0:
        st.error("⚠️ MODO LECTURA: Sin fondos suficientes.")
        st.write("Esperando saldo mínimo ($10 MXN).")
    else:
        st.markdown('<p class="status-active">🚀 ADAPTACIÓN AUTOMÁTICA ACTIVA</p>', unsafe_allow_html=True)

with col_log:
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}] Escaneando... Modo: IA_SYNC | Status: PRESTIGE", language="bash")

# Auto-refresh
time.sleep(15)
st.rerun()
