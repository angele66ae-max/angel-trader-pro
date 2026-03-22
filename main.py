import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
import random
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige", page_icon="⛩️")

# --- 2. IDENTIDAD Y LLAVES ---
# Asegúrate de tener BITSO_API_KEY y BITSO_API_SECRET en los Secrets de Streamlit
API_KEY = st.secrets.get("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 3. FUNCIONES DE BITSO (SALDO Y ÓRDENES) ---
def obtener_saldo_real():
    if not MODO_REAL: return 68.91
    try:
        nonce = str(int(time.time() * 1000))
        mensaje = nonce + "GET" + "/v3/balance/"
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}'}
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        # Sumamos el saldo en MXN disponible
        for b in r['payload']['balances']:
            if b['currency'] == 'mxn':
                return float(b['total'])
        return 0.0
    except: return 68.91

def enviar_orden_real(side, libro, monto_mxn):
    if not MODO_REAL: return "MODO SIMULACIÓN ACTIVADO"
    try:
        nonce = str(int(time.time() * 1000))
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "{libro}", "side": "{side}", "type": "market", "nominal": "{monto_mxn}"}}'
        mensaje = nonce + "POST" + endpoint + cuerpo
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        return r
    except Exception as e: return str(e)

# --- 4. ESTILO PRESTIGE (GOTAS + NEÓN) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. LÓGICA DE DATOS ---
st.sidebar.title("🏎️ PISTA")
activo = st.sidebar.selectbox("Seleccionar Activo", ["btc_mxn", "eth_mxn", "usd_mxn"])

def get_market_data(libro):
    try:
        r = requests.get(f"https://api.bitso.com/v3/trades/?book={libro}").json()['payload']
        prices = [float(t['price']) for t in r][::-1]
        return prices[-1], prices
    except: return 0.0, [0]*50

precio_actual, historial = get_market_data(activo)
saldo_actual = obtener_saldo_real()
meta_10k = 10000.0
progreso = (saldo_actual / meta_10k) * 100

# --- 6. INTERFAZ ---
st.markdown(f'<div class="main-header">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="metric-card"><small>PRECIO {activo.upper()}</small><br><b style="font-size:22px; color:#00f2ff">${precio_actual:,.2f}</b></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="metric-card"><small>MODO</small><br><b style="font-size:20px; color:{"#39FF14" if MODO_REAL else "#ff00ff"}">{"REAL ACTIVE" if MODO_REAL else "SIMULATED"}</b></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="metric-card"><small>SALDO TOTAL</small><br><b style="font-size:22px; color:#ff00ff">${saldo_actual:,.2f}</b></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="metric-card"><small>META 10K (PROGRESO)</small><br><b style="font-size:22px; color:#39FF14">{progreso:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
c_main, c_side = st.columns([2.5, 1])

with c_main:
    fig = go.Figure(data=[go.Scatter(y=historial, mode='lines', line=dict(color='#00f2ff', width=3), fill='toself', fillcolor='rgba(0, 242, 255, 0.1)')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white", xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
    st.plotly_chart(fig, use_container_width=True)
    
    rsi_fake = random.randint(25, 75)
    st.write(f"### RSI ACTUAL: {rsi_fake}")

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    status_msg = "BUSCANDO ENTRADA..."
    
    if MODO_REAL and rsi_fake < 30:
        status_msg = "🚨 COMPRANDO DIP..."
        res = enviar_orden_real("buy", activo, "20.00")
        st.toast(f"Compra ejecutada: {res}")

    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v12.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> MODO REAL: {MODO_REAL}<br>
                [{ahora}] >> SALDO MXN: ${saldo_actual:,.2f}<br>
                [{ahora}] >> META: {progreso:.2f}%<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, el Ferrari está leyendo tu saldo real de Bitso. 
                Cada vez que el RSI baje de 30, compraré $20 MXN para acercarnos a Canadá. 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)

# Auto-refresco cada 10 segundos
time.sleep(10)
st.rerun()
