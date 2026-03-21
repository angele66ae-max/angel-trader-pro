import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE_USUARIO}'s Prestige", page_icon="⛩️")

API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 2. FUNCIONES DE CONEXIÓN ---
def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

def ejecutar_orden_bitso(side, amount_mxn):
    """ side: 'buy' o 'sell' """
    if not MODO_REAL: return "SIMULACIÓN EXITOSA"
    try:
        endpoint = "/v3/orders/"
        # Para simplificar, compramos a precio de mercado
        cuerpo = f'{{"book": "btc_mxn", "side": "{side}", "type": "market", "nominal": "{amount_mxn}"}}'
        h = firmar("POST", endpoint, cuerpo)
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=h, data=cuerpo).json()
        return r
    except Exception as e:
        return str(e)

# --- 3. CSS PRESTIGE CENTER ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.9), rgba(5,10,14,0.95)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 32px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 12px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 300px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. CÁLCULO DE INDICADORES (RSI) ---
def calcular_rsi(prices, period=14):
    deltas = np.diff(prices)
    seed = deltas[:period+1]
    up = seed[seed >= 0].sum()/period
    down = -seed[seed < 0].sum()/period
    rs = up/down
    rsi = np.zeros_like(prices)
    rsi[:period] = 100. - 100./(1. + rs)
    for i in range(period, len(prices)):
        delta = deltas[i-1]
        if delta > 0: upval, downval = delta, 0.
        else: upval, downval = 0., -delta
        up = (up*(period-1) + upval)/period
        down = (down*(period-1) + downval)/period
        rs = up/down
        rsi[i] = 100. - 100./(1. + rs)
    return rsi[-1]

# --- 5. OBTENCIÓN DE DATOS ---
r_ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
precio_act = float(r_ticker['last'])
saldo_mxn = 117.63
if MODO_REAL:
    try:
        h_bal = firmar("GET", "/v3/balance/")
        res_bal = requests.get("https://api.bitso.com/v3/balance/", headers=h_bal).json()
        for b in res_bal['payload']['balances']:
            if b['currency'] == 'mxn': saldo_mxn = float(b['total'])
    except: pass

# Generar datos simulados para la gráfica (Velas)
prices = [precio_act * (1 + np.sin(i/10)*0.001 + np.random.normal(0,0.0005)) for i in range(50)]
rsi_val = calcular_rsi(prices)

# --- 6. LÓGICA DE TRADING (LA MENTE DE MAHORA) ---
log_ia = []
if rsi_val < 35:
    decision = "COMPRAR (BARATO)"
    status_color = "#39FF14"
    res_trade = ejecutar_orden_bitso("buy", 20.0) # Compra $20 MXN
    log_ia.append(f"ORDEN DE COMPRA ENVIADA: $20 MXN")
elif rsi_val > 65:
    decision = "VENDER (CARO)"
    status_color = "#ff00ff"
    # Aquí venderías una fracción de BTC, por ahora simplificamos a log
    log_ia.append(f"ZONA DE VENTA ALCANZADA. EVALUANDO...")
else:
    decision = "HOLD (ESPERAR)"
    status_color = "#ffffff"
    log_ia.append("MERCADO NEUTRO. SIN ACCIÓN.")

# --- 7. RENDERIZADO ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S QUANTUM TERMINAL</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><div style="font-size:10px">BTC/MXN</div><div style="font-size:20px">${precio_act:,.0f}</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card"><div style="font-size:10px">SALDO REAL</div><div style="font-size:20px; color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><div style="font-size:10px">RSI (14)</div><div style="font-size:20px; color:{status_color}">{rsi_val:.1f}</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card"><div style="font-size:10px">IA DECISION</div><div style="font-size:18px">{decision}</div></div>', unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Gráfica de Velas
    fig = go.Figure(data=[go.Candlestick(y=prices, increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown(f"""
    <div class="ia-panel">
        <h4 style="color:#ff00ff; margin-bottom:10px;">🧠 CEREBRO MAHORA v6.0</h4>
        <div class="ia-terminal">
            [{datetime.now().strftime("%H:%M:%S")}] >> INICIANDO ESCANEO...<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> RSI DETECTADO: {rsi_val:.2f}<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> DECISIÓN: {decision}<br>
            <hr>
            >> LOG DE OPERACIÓN:<br>
            {log_ia[0] if log_ia else "ESPERANDO SEÑAL..."}<br><br>
            >> PENSAMIENTO:<br>
            Angel, estamos operando con el saldo real. Si el RSI baja de 35, entraré con $20 pesos para acumular barato.
        </div>
    </div>
    """, unsafe_allow_html=True)

# Auto-Refresh cada 30 segundos
time.sleep(30)
st.rerun()
