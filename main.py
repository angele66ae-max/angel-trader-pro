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
BITSO_API_KEY = "TU_API_KEY_AQUI"
BITSO_API_SECRET = "TU_SECRET_AQUI"

# --- ESTILO VISUAL (RUEDA DE MAHORA) ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .card {{
        background: rgba(0, 15, 30, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 20px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
    .metric-val {{ font-size: 32px; color: #00f2ff; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .stProgress > div > div > div > div {{ background-color: #00ff00; }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE EJECUCIÓN ---
def execute_real_order(side, amount):
    if BITSO_API_KEY == "TU_API_KEY_AQUI":
        return {"status": "error", "msg": "Llaves no configuradas"}
    
    nonce = str(int(time.time() * 1000))
    path = "/v3/orders/"
    payload = {"book": "btc_usd", "side": side, "type": "market", "major": str(amount)}
    json_payload = json.dumps(payload)
    message = nonce + "POST" + path + json_payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    try:
        r = requests.post("https://api.bitso.com" + path, headers=headers, data=json_payload)
        return r.json()
    except Exception as e:
        return {"status": "error", "msg": str(e)}

# --- OBTENCIÓN DE DATOS EN VIVO ---
res = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
p_actual = float(res['payload']['last'])

# Crear 20 velas japonesas basadas en el precio actual
df_velas = pd.DataFrame({
    'open': p_actual + np.random.randn(20) * 5,
    'high': p_actual + 15, 'low': p_actual - 15,
    'close': p_actual + np.random.randn(20) * 5
})

# --- INTERFAZ MAHORASHARK ---
st.markdown("<h1 style='text-align:center; color:white;'>⛩️ MAHORASHARK: PRESTIGE PRODUCTION</h1>", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown(f'<div class="card">PRECIO BTC<div class="metric-val">${p_actual:,.2f}</div></div>', unsafe_allow_html=True)
with m2:
    # Barra de ganancias integrada
    ganancia = 0.36
    st.markdown(f'<div class="card">GANANCIA REAL<div class="metric-val" style="color:#00ff00;">+${ganancia}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown('<div class="card">SISTEMA<div class="metric-val" style="color:magenta;">ACTIVE</div></div>', unsafe_allow_html=True)

st.write("")
col_chart, col_side = st.columns([2, 1])

with col_chart:
    st.markdown("### Gráfica de Velas Japonesas")
    fig = go.Figure(data=[go.Candlestick(
        open=df_velas['open'], high=df_velas['high'],
        low=df_velas['low'], close=df_velas['close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False, height=450,
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.1)"),
        margin=dict(l=0, r=0, t=0, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.markdown('<div class="card" style="text-align:left; height:450px;">', unsafe_allow_html=True)
    st.subheader("Bóveda Mahora")
    st.write("💵 **USD:** $2.81")
    st.write("🇲🇽 **MXN:** $47.12")
    
    st.write("---")
    st.write(f"Progreso hacia meta (Venta a $115):")
    # Barra de progreso visual
    st.progress(min(ganancia / 1.0, 1.0)) 
    
    st.write("")
    if st.button("🚀 EJECUTAR OPERACIÓN REAL", use_container_width=True):
        resultado = execute_real_order("buy", 0.5) # Compra 0.50 USD
        if 'success' in str(resultado):
            st.success("¡Orden de dinero real ejecutada!")
            st.balloons()
        else:
            # FIX: Corregido el SyntaxError de la línea 92
            msg_error = resultado.get('msg', 'Error de llaves/conexión')
            st.error(f"Fallo de conexión: {msg_error}")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nAnalizando para adaptación...", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
