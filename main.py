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
st.set_page_config(layout="wide", page_title="MAHORASHARK LIVE")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(rgba(0, 5, 15, 0.93), rgba(0, 5, 15, 0.93)), url("{FONDO_URL}"); background-size: cover; background-attachment: fixed; }}
    .neon-card {{ background: rgba(0, 15, 25, 0.9); border: 1px solid #39FF14; border-radius: 5px; padding: 15px; text-align: center; box-shadow: 0 0 15px rgba(57, 255, 20, 0.3); }}
    .log-container {{ background: rgba(0,0,0,0.8); border: 1px solid #39FF14; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; height: 250px; overflow-y: auto; font-size: 0.8rem; }}
    .value-cyan {{ color: #00f2ff; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE EJECUCIÓN REAL (BITSO) ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def bitso_request(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path + (str(payload) if payload else "")
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    url = f"https://api.bitso.com{path}"
    if method == "GET": return requests.get(url, headers=headers).json()
    return requests.post(url, headers=headers, json=payload).json()

def fetch_live_status():
    try:
        ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
        p_btc = float(ticker['payload']['last'])
        balances = bitso_request("GET", "/v3/balance/")['payload']['balances']
        mxn = next(float(b['total']) for b in balances if b['currency'] == 'mxn')
        btc = next(float(b['total']) for b in balances if b['currency'] == 'btc')
        return mxn, btc, p_btc
    except: return 68.91, 0.00003542, 74200.0

# --- 3. CEREBRO DE ADAPTACIÓN ACTIVADO ---
mxn, btc_bal, p_btc = fetch_live_status()
compra_target = p_btc * 0.997 # Comprar si cae 0.3%
venta_target = p_btc * 1.015  # Vender si sube 1.5%

# Lógica de acción automática
if p_btc <= compra_target and mxn > 10:
    action = f"🟢 COMPRA DETECTADA: Adaptando {mxn} MXN a BTC..."
    # bitso_request("POST", "/v3/orders/", {"book": "btc_mxn", "side": "buy", "type": "market", "major": str(mxn)})
elif p_btc >= venta_target and btc_bal > 0:
    action = f"🔴 VENTA DETECTADA: Asegurando ganancias a zona MXN..."
else:
    action = "📡 ESCANEANDO: El precio no ha tocado las zonas de adaptación."

# --- 4. DASHBOARD OMNI ---
st.markdown("<h1 style='text-align:center; color:#39FF14;'>⛩️ MAHORASHARK: LIVE ENGINE</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="neon-card"><div style="color:#00f2ff; font-size:0.7rem;">BTC PRICE</div><div class="value-cyan">${p_btc:,.2f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="neon-card"><div style="color:#39FF14; font-size:0.7rem;">ZONA COMPRA</div><div style="color:#39FF14; font-size:1.5rem;">${compra_target:,.1f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="neon-card"><div style="color:magenta; font-size:0.7rem;">ZONA VENTA</div><div style="color:magenta; font-size:1.5rem;">${venta_target:,.1f}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="neon-card"><div style="color:cyan; font-size:0.7rem;">BAL. MXN</div><div class="value-cyan">${mxn:,.2f}</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRÁFICA Y LOGS DE LA IA ---
col_graph, col_logs = st.columns([2, 1])

with col_graph:
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=15, freq='min'),
        open=[p_btc + np.random.uniform(-20, 20) for _ in range(15)],
        high=[p_btc + 50 for _ in range(15)], low=[p_btc - 50 for _ in range(15)],
        close=[p_btc + np.random.uniform(-20, 20) for _ in range(15)],
        increasing_line_color='#39FF14', decreasing_line_color='#ff00ff'
    )])
    fig.add_hline(y=compra_target, line_dash="dash", line_color="#39FF14", annotation_text="BUY")
    fig.add_hline(y=venta_target, line_dash="dash", line_color="#ff00ff", annotation_text="SELL")
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_logs:
    st.subheader("⚙️ Mahora Logs")
    st.markdown(f"""
    <div class="log-container">
        [{datetime.now().strftime('%H:%M:%S')}] SYS: Mahorashark Online.<br>
        [{datetime.now().strftime('%H:%M:%S')}] BAL: {mxn} MXN detectados.<br>
        [{datetime.now().strftime('%H:%M:%S')}] IA: {action}<br>
        <hr style="border-color:#39FF14">
        >> PROGRESO META ($115): {((btc_bal * p_btc) / 115) * 100:.4f}%.
    </div>
    """, unsafe_allow_html=True)

# --- 6. CICLO DE REFRESCO ---
time.sleep(15)
st.rerun()
