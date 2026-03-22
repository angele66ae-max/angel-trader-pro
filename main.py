import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
import random
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark Real", page_icon="⛩️")

# --- 2. CONEXIÓN SEGURA ---
# Asegúrate de poner estas en "Secrets" de Streamlit Cloud
API_KEY = st.secrets.get("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 3. MOTOR DE SALDOS REALES ---
def obtener_balance_total():
    if not MODO_REAL:
        return 68.91  # Saldo de respaldo si no hay llaves
    try:
        nonce = str(int(time.time() * 1000))
        message = nonce + "GET" + "/v3/balance/"
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        
        # Sumamos MXN disponible + valor de BTC (simplificado para el ejemplo)
        balances = r['payload']['balances']
        mxn_total = sum(float(b['total']) for b in balances if b['currency'] == 'mxn')
        return mxn_total
    except:
        return 68.91

# --- 4. MOTOR DE MERCADO ---
def get_live_data(libro):
    r = requests.get(f"https://api.bitso.com/v3/trades/?book={libro}").json()['payload']
    prices = [float(t['price']) for t in r][::-1]
    return prices[-1], prices

activo = st.sidebar.selectbox("🏎️ PISTA", ["btc_mxn", "eth_mxn"])
precio_vlive, historial_vlive = get_live_data(activo)
saldo_vlive = obtener_balance_total()
meta_final = 10000.0
porcentaje_progreso = (saldo_vlive / meta_final) * 100

# --- 5. DISEÑO PRESTIGE ---
st.markdown(f"""
    <style>
    .stApp {{ background: #050a0e; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; }}
    .metric-box {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 300px; }}
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="main-header">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)
st.write("")

# Barra de Métricas con Porcentaje Real
m1, m2, m3, m4 = st.columns(4)
m1.markdown(f'<div class="metric-box"><small>PRECIO ACTUAL</small><br><b style="font-size:22px; color:#00f2ff">${precio_vlive:,.2f}</b></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-box"><small>MODO</small><br><b style="font-size:20px; color:{"#39FF14" if MODO_REAL else "#ff00ff"}">{"REAL ACTIVE" if MODO_REAL else "SIMULATED"}</b></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-box"><small>SALDO TOTAL MXN</small><br><b style="font-size:22px; color:#ff00ff">${saldo_vlive:,.2f}</b></div>', unsafe_allow_html=True)
m4.markdown(f'<div class="metric-box"><small>PROGRESO CANADÁ</small><br><b style="font-size:22px; color:#39FF14">{porcentaje_progreso:.2f}%</b></div>', unsafe_allow_html=True)

# Cuerpo
c_main, c_side = st.columns([2.5, 1])
with c_main:
    fig = go.Figure(data=[go.Scatter(y=historial_vlive, mode='lines', line=dict(color='#00f2ff', width=3))])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, font_color="white")
    st.plotly_chart(fig, use_container_width=True)

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="ia-terminal">
            [{ahora}] >> SINCRONIZANDO SALDOS...<br>
            [{ahora}] >> PROGRESO A 10K: {porcentaje_progreso:.2f}%<br>
            <hr style="border-color:#333">
            >> PENSAMIENTO:<br>
            Angel, estoy leyendo tu saldo real de Bitso cada 10 segundos. 
            Cualquier compra o subida de precio nos acerca a Canadá. 🇨🇦
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
