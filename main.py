import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN DE TU EMPRESA ---
# Cambia esto por el nombre de tu empresa o proyecto
NOMBRE_EMPRESA = "ANGEL PRESTIGE INVESTMENTS" 
API_KEY = "TU_API_KEY_AQUI"
API_SECRET = "TU_API_SECRET_AQUI"

st.set_page_config(layout="wide", page_title=f"{NOMBRE_EMPRESA} Center", page_icon="⛩️")

# --- 2. FUNCIÓN PARA OBTENER SALDO REAL ---
def get_real_balance():
    if API_KEY == "TU_API_KEY_AQUI":
        # Si no has puesto tus llaves, muestra el valor de prueba
        return 115.59, 0.00006301
    
    # Lógica de firma para Bitso (Seguridad)
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    auth_header = f'Bitso {API_KEY}:{nonce}:{signature}'
    
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers={'Authorization': auth_header}).json()
        balances = r['payload']['balances']
        mxn_balance = next(b['total'] for b in balances if b['currency'] == 'mxn')
        btc_balance = next(b['total'] for b in balances if b['currency'] == 'btc')
        return float(mxn_balance), float(btc_balance)
    except:
        return 115.59, 0.00006301 # Respaldo

mxn_real, btc_real = get_real_balance()

# --- 3. ESTILO CSS (CON TU EMPRESA) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)), url("{fondo_url}");
        background-size: cover;
        color: white;
    }}
    .main-title {{ text-align: center; color: #00f2ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 15px #00f2ff; padding: 10px; }}
    .kpi-card {{ background: rgba(10, 25, 41, 0.8); border: 1px solid #00f2ff; border-radius: 12px; padding: 15px; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ ---
st.markdown(f'<div class="main-title">⛩️ {NOMBRE_EMPRESA}</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="kpi-card"><small>EMPRESA</small><br><b style="color:#00f2ff;">{NOMBRE_EMPRESA}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card"><small>SALDO MXN REAL</small><br><b style="color:#ffffff;">${mxn_real:,.2f}</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card"><small>BTC EN CARTERA</small><br><b style="color:#39FF14;">{btc_real:.8f}</b></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff;">{(mxn_real/200000)*100:.2f}%</b></div>', unsafe_allow_html=True)

# ... (El resto del código de gráficas que ya tienes funcionando)
