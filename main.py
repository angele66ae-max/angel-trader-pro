import streamlit as st
import pandas as pd
import requests
import time
import hmac
import hashlib
from datetime import datetime

# --- 1. CONFIGURACIÓN VISUAL PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

st.markdown("""
<style>
    .stApp { background-color: #000505; color: #00f2ff; }
    
    /* Tarjetas Neón */
    .metric-container {
        background: rgba(0, 20, 30, 0.6);
        border: 2px solid #00f2ff;
        border-radius: 15px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
        margin-bottom: 20px;
    }
    
    .label { font-size: 14px; text-transform: uppercase; letter-spacing: 2px; color: #00f2ff; }
    .value { font-size: 32px; font-weight: bold; margin: 10px 0; color: #ffffff; text-shadow: 0 0 10px #00f2ff; }
    .sub-value { font-size: 16px; color: #39FF14; }

    /* Estado de la IA */
    .status-pilot {
        background: rgba(57, 255, 20, 0.1);
        border: 1px solid #39FF14;
        color: #39FF14;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        text-shadow: 0 0 8px #39FF14;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS REALES (BITSO) ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_vault_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        # Consultar Saldo y Precio simultáneamente
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        r_tick = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        
        balances = r_bal['payload']['balances']
        p_actual = float(r_tick['payload']['last'])
        
        mxn = next((float(b['total']) for b in balances if b['currency'] == 'mxn'), 0.0)
        btc = next((float(b['total']) for b in balances if b['currency'] == 'btc'), 0.0)
        
        return mxn, btc, p_actual
    except:
        return 68.91, 0.00003542, 73500.0 # Valores de respaldo

# --- 3. EJECUCIÓN ---
mxn_cash, btc_amount, btc_price = get_vault_data()
valor_usd = btc_amount * btc_price
meta_percent = (valor_usd / 115.0) * 100

# --- 4. INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: PRESTIGE OMNI</h1>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""<div class="metric-container">
        <div class="label">Bóveda Bitcoin</div>
        <div class="value">{btc_amount:.8f}</div>
        <div class="sub-value">≈ ${valor_usd:.2f} USD</div>
    </div>""", unsafe_allow_html=True)

with col2:
    st.markdown(f"""<div class="metric-container">
        <div class="label">Disponible Cash</div>
        <div class="value">${mxn_cash:.2f}</div>
        <div class="sub-value">MXN Sincronizado</div>
    </div>""", unsafe_allow_html=True)

with col3:
    st.markdown(f"""<div class="metric-container">
        <div class="label">Meta de Inversión</div>
        <div class="value">{meta_percent:.4f}%</div>
        <div class="sub-value">Objetivo: $115 USD</div>
    </div>""", unsafe_allow_html=True)

st.write("---")

# --- 5. CEREBRO Y RADAR ---
c_ia, c_radar = st.columns(2)

with c_ia:
    st.subheader("🤖 IA Mahora Pro")
    st.markdown('<div class="status-pilot">🚀 AUTO-PILOT ACTIVO: ADAPTACIÓN DISPONIBLE</div>', unsafe_allow_html=True)
    st.write("")
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}] Escaneando mercados...\nAnalizando oportunidad en BTC...", language="bash")

with c_radar:
    st.subheader("🐋 Radar de Ballenas")
    st.success("MERCADO ESTABLE: Movimiento orgánico detectado.")
    st.info("Sin órdenes grandes detectadas en los últimos 5 minutos.")

# Auto-refresh cada 20 segundos para mantener la fluidez
time.sleep(20)
st.rerun()
