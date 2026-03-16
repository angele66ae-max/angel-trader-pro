import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import hmac
import hashlib
import json
import plotly.graph_objects as go
from datetime import datetime

# --- 1. ESTÉTICA PRESTIGE TOTAL ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(0, 10, 20, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.5);
    }}
    .val-neon {{ font-size: 28px; color: #39FF14; font-weight: bold; text-shadow: 0 0 10px #39FF14; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR BITSO SEGURO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_pay = json.dumps(payload, separators=(',', ':')) if payload else ""
    msg = nonce + method + path + json_pay
    sig = hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{sig}', 'Content-Type': 'application/json'}
    try:
        r = requests.request(method, f"https://api.bitso.com{path}", headers=headers, data=json_pay)
        return r.json()
    except: return {"success": False, "error": {"message": "Error de Red"}}

# --- 3. RECOPILACIÓN DE DATOS ---
try:
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_btc = float(ticker['payload']['last'])
    
    bal_res = bitso_api("GET", "/v3/balance/")
    balances = bal_res['payload']['balances']
    usd_bal = next((float(b['available']) for b in balances if b['currency'] == 'usd'), 0.0)
except:
    p_btc, usd_bal = 75000.0, 2.81 # Datos de respaldo

# --- 4. INTERFAZ VISUAL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center; text-shadow:0 0 15px #00f2ff;'>⛩️ MAHORASHARK: USD MODE</h1>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="metric-card">BTC/USD<div class="val-neon">${p_btc:,.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">DISPONIBLE USD<div class="val-neon" style="color:cyan;">${usd_bal:.2f}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">ORDEN OBJETIVO<div class="val-neon" style="color:magenta;">$2.00</div></div>', unsafe_allow_html=True)

col_viz, col_ctrl = st.columns([2.5, 1])

with col_viz:
    # Gráfica de Velas Neón
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[p_btc + np.random.uniform(-50, 50) for _ in range(20)],
        high=[p_btc + 100 for _ in range(20)],
        low=[p_btc - 100 for _ in range(20)],
        close=[p_btc + np.random.uniform(-50, 50) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    )])
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0, b=0, l=0, r=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_ctrl:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:450px;">', unsafe_allow_html=True)
    st.subheader("🧠 Cerebro Mahora")
    
    # Lógica de los 2 Dólares
    # Intentamos usar $2.00, pero si el balance es menor, usamos el 99% del balance
    monto_ejecucion = 2.00 if usd_bal >= 2.05 else (usd_bal * 0.99)
    
    st.write(f"Estado: **CONECTADO**")
    st.write(f"Par: **BTC/USD**")
    st.info(f"Monto Programado: **${monto_ejecucion:.2f} USD**")
    
    if st.button("🚀 EJECUTAR ADAPTACIÓN (2 USD)", use_container_width=True):
        if usd_bal < 1.0:
            st.error("Error: Saldo menor al mínimo de $1 USD")
        else:
            order = {
                "book": "btc_usd",
                "side": "buy",
                "type": "market",
                "minor": f"{monto_ejecucion:.2f}"
            }
            res = bitso_api("POST", "/v3/orders/", order)
            if res.get('success'):
                st.success(f"¡ADAPTACIÓN DE ${monto_ejecucion:.2f} EXITOSA!")
                st.balloons()
            else:
                msg = res.get('error', {}).get('message', 'Fallo de firma')
                st.error(f"Bitso: {msg}")

    st.write("---")
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nModo: PRESTIGE\nAsset: USD", language="bash")
    st.markdown('</div>', unsafe
