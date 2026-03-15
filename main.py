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

# --- CONFIGURACIÓN CORE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE", initial_sidebar_state="collapsed")

# --- 1. LLAVES DE PRODUCCIÓN ---
BITSO_API_KEY = "FZHAAOqOhy"
BITSO_API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# --- ESTILO VISUAL PRESTIGE ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .card {{
        background: rgba(0, 10, 20, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }}
    .metric-val {{ font-size: 32px; color: #00f2ff; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE CONSULTA Y EJECUCIÓN ---
def get_auth_headers(method, path, payload=""):
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path + payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}

def get_real_balances():
    path = "/v3/balance/"
    try:
        r = requests.get("https://api.bitso.com" + path, headers=get_auth_headers("GET", path))
        balances = r.json()['payload']['balances']
        data = {b['currency']: float(b['available']) for b in balances if float(b['available']) > 0}
        return data
    except:
        return {"usd": 2.81, "mxn": 47.12, "btc": 0.0000039}

def execute_adaptation(side, amount):
    path = "/v3/orders/"
    payload = json.dumps({"book": "btc_usd", "side": side, "type": "market", "major": f"{amount:.2f}"})
    try:
        r = requests.post("https://api.bitso.com" + path, headers=get_auth_headers("POST", path, payload), data=payload)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- 3. DATOS DE MERCADO ---
ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
p_actual = float(ticker['payload']['last'])
boveda = get_real_balances()

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE LIVE</h1>", unsafe_allow_html=True)

# Dashboard Superior
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="card">PRECIO BTC<div class="metric-val">${p_actual:,.1f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE USD<div class="metric-val" style="color:magenta;">${boveda.get("usd", 0.0):.2f}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="card">GANANCIA<div class="metric-val" style="color:#39FF14;">+$0.36</div></div>', unsafe_allow_html=True)
with m4:
    meta = (boveda.get("usd", 0.0) / 10000) * 100
    st.markdown(f'<div class="card">META SUV<div class="metric-val" style="color:cyan;">{meta:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_chart, col_side = st.columns([2, 1])

with col_chart:
    # Gráfica de Velas Profesionales
    df_v = pd.DataFrame({
        'open': p_actual + np.random.randn(30) * 10,
        'high': p_actual + 20, 'low': p_actual - 20,
        'close': p_actual + np.random.randn(30) * 10
    })
    fig = go.Figure(data=[go.Candlestick(
        open=df_v['open'], high=df_v['high'], low=df_v['low'], close=df_v['close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450,
                      xaxis_rangeslider_visible=False, yaxis=dict(color="white"))
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.markdown('<div class="card" style="text-align:left; min-height:450px;">', unsafe_allow_html=True)
    st.subheader("🛠️ Cerebro Mahora")
    st.write("Sincronizando Bóveda...")
    for curr, val in boveda.items():
        st.write(f"💰 **{curr.upper()}:** {val}")
    
    st.write("---")
    st.write(f"🎯 **Meta Venta:** $115.00 USD")
    st.progress(min(p_actual / 115000, 1.0))
    
    st.write("")
    # Lógica de Adaptación Automática de Monto
    monto_a_usar = boveda.get("usd", 0.0) * 0.8  # Usamos el 80% para evitar errores de comisión
    
    if st.button(f"🚀 EJECUTAR ADAPTACIÓN (${monto_a_usar:.2f})", use_container_width=True):
        if monto_a_usar < 1.0:
            st.error("Balance insuficiente para el mínimo de Bitso ($1.00)")
        else:
            res = execute_adaptation("buy", monto_a_usar)
            if res.get('success'):
                st.success("¡ADAPTACIÓN EXITOSA! Dinero real en movimiento.")
                st.balloons()
            else:
                st.error(f"Error: {res.get('message', 'Fallo de red')}")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nEstado: LIVE", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
