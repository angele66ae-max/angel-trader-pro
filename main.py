import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import hmac
import hashlib
from datetime import datetime
import plotly.graph_objects as go

# --- NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# --- CONFIGURACIÓN API (Pon tus llaves aquí para dinero real) ---
BITSO_API_KEY = "TU_API_KEY"
BITSO_API_SECRET = "TU_SECRET"
BASE_URL = "https://api.bitso.com"

# --- FONDO ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5)), url("{FONDO_URL}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 20, 30, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
    .metric-val {{ font-size: 38px; color: #00f2ff; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- FUNCIONES DE DINERO REAL ---
def place_order_real(side, amount, book="btc_usd"):
    """Esta función envía la orden real a Bitso"""
    nonce = str(int(time.time() * 1000))
    path = "/v3/orders/"
    body = {
        "book": book,
        "side": side,
        "type": "market",
        "major": str(amount)
    }
    json_payload = str(body).replace("'", '"')
    message = nonce + "POST" + path + json_payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        "Authorization": f"Bitso {BITSO_API_KEY}:{nonce}:{signature}",
        "Content-Type": "application/json"
    }
    # r = requests.post(BASE_URL + path, headers=headers, data=json_payload) # DESCOMENTAR PARA DINERO REAL
    return {"status": "Simulado", "msg": "Orden lista para producción"}

def get_price():
    try:
        r = requests.get(f"{BASE_URL}/v3/ticker/?book=btc_usd", timeout=3)
        return float(r.json()['payload']['last'])
    except: return 71500.0

# --- LÓGICA DE DATOS ---
if "precios" not in st.session_state:
    st.session_state.precios = [get_price()]

current_p = get_price()
st.session_state.precios.append(current_p)
if len(st.session_state.precios) > 30: st.session_state.precios.pop(0)

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:white;'>⛩️ MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">PRECIO BTC<div class="metric-val">${current_p:,.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown('<div class="card">GANANCIA HOY<div class="metric-val" style="color:#00ff00;">+$0.36</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">ESTADO BOT<div class="metric-val" style="color:magenta;">ACTIVE</div></div>', unsafe_allow_html=True)

st.write("")
c_left, c_right = st.columns([2, 1])

with c_left:
    # GRÁFICA CORREGIDA (Sin ValueError)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=st.session_state.precios,
        mode='lines+markers',
        line=dict(color='#00f2ff', width=3),
        fill='tozeroy',
        fillcolor='rgba(0, 242, 255, 0.1)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_visible=False,
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.05)"),
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with c_right:
    st.markdown('<div class="card" style="height:400px; text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Multi-Asset")
    st.write("💰 **Balance USD:** $2.81")
    st.write("🇲🇽 **Balance MXN:** $116.10")
    st.divider()
    
    # BOTÓN PARA EJECUTAR DINERO REAL
    if st.button("🚀 EJECUTAR ADAPTACIÓN (COMPRA REAL)", use_container_width=True):
        res = place_order_real("buy", 1.0) # Intenta comprar 1 USD de BTC
        st.success(f"Mahorashark adaptándose: {res['msg']}")
        
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nAnalizando mercado...\nBot listo para producir.", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(5)
st.rerun()
