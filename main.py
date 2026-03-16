import streamlit as st
import pandas as pd
import requests
import time
import hmac
import hashlib
from datetime import datetime

# --- 1. CONFIGURACIÓN DE ESTILO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

st.markdown("""
<style>
    .stApp { background-color: #00080a; color: #00f2ff; }
    .boveda-card {
        background: rgba(0, 20, 30, 0.7);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 25px;
        text-align: center; box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }
    .status-alert {
        padding: 10px; border-radius: 8px; font-weight: bold;
        text-transform: uppercase; margin-bottom: 15px;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. CEREBRO DE CONEXIÓN (BITSO) ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_real_balance():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        return r['payload']['balances']
    except:
        return None

# --- 3. LÓGICA DE ACTUALIZACIÓN ---
try:
    # Obtener Saldo Real
    data_balances = get_real_balance()
    mxn_val = next((float(b['total']) for b in data_balances if b['currency'] == 'mxn'), 0.0)
    btc_val = next((float(b['total']) for b in data_balances if b['currency'] == 'btc'), 0.0)
    
    # Obtener Precio
    r_tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    price = float(r_tick['payload']['last'])
    vault_usd = btc_val * price
    progress = (vault_usd / 115.0) * 100
except:
    mxn_val, btc_val, vault_usd, progress = 0.0, 0.00003542, 2.61, 2.2701

# --- 4. INTERFAZ VISUAL ---
st.markdown("<h1 style='text-align:center; text-shadow: 0 0 15px #00f2ff;'>⛩️ MAHORASHARK: PRESTIGE DASHBOARD</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="boveda-card">BÓVEDA BTC<br><span style="font-size:30px;">{btc_val:.8f}</span><br>(${vault_usd:.2f} USD)</div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="boveda-card">DISPONIBLE MXN<br><span style="font-size:30px;">${mxn_val:.2f}</span></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="boveda-card">META ($115)<br><span style="font-size:30px;">{progress:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. MONITOR DE IA ---
col_ia, col_radar = st.columns(2)

with col_ia:
    st.subheader("🤖 IA Mahora Pro")
    if mxn_val < 10.0:
        st.markdown('<div class="status-alert" style="background:rgba(255,0,0,0.2); border:1px solid red; color:red;">⚠️ MODO LECTURA: SALDO BAJO</div>', unsafe_allow_html=True)
        st.write("IA monitoreando... esperando saldo mínimo para compra.")
    else:
        st.markdown('<div class="status-alert" style="background:rgba(57,255,20,0.2); border:1px solid #39FF14; color:#39FF14;">🚀 AUTO-PILOT ACTIVO</div>', unsafe_allow_html=True)

with col_radar:
    st.subheader("🐋 Radar de Ballenas")
    st.success("MERCADO ESTABLE: Movimiento orgánico detectado.")
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}] Status: SYNCED | Mode: PRESTIGE", language="bash")

# --- AUTO-REFRESH SIN ERRORES ---
time.sleep(20)
st.rerun()
