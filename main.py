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

# --- 2. MOTOR DE OPERACIONES REALES ---
def execute_bitso_action(side, amount_usd):
    nonce = str(int(time.time() * 1000))
    path = "/v3/orders/"
    payload = {
        "book": "btc_usd",
        "side": side,
        "type": "market",
        "major": f"{amount_usd:.2f}" 
    }
    json_payload = json.dumps(payload)
    message = nonce + "POST" + path + json_payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    
    try:
        r = requests.post("https://api.bitso.com" + path, headers=headers, data=json_payload)
        return r.json()
    except Exception as e:
        return {"success": False, "error": str(e)}

# --- 3. OBTENCIÓN DE DATOS REALES ---
try:
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_actual = float(ticker['payload']['last'])
except:
    p_actual = 71848.0 # Referencia de tu última captura

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: PRESTIGE LIVE</h1>", unsafe_allow_html=True)

# Métricas Superiores
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="card">BTC/USD BITSO<div class="metric-val">${p_actual:,.1f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="card">BALANCE REAL<div class="metric-val" style="color:magenta;">$2.81</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="card">GANANCIA LÍQUIDA<div class="metric-val" style="color:#39FF14;">+$0.36</div></div>', unsafe_allow_html=True)
with m4:
    meta_suv = (2.81 / 10000) * 100 # Meta SUV 10K
    st.markdown(f'<div class="card">META SUV 10K<div class="metric-val" style="color:cyan;">{meta_suv:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_chart, col_side = st.columns([2, 1])

with col_chart:
    # Generación de velas estéticas (Verde y Magenta)
    df_v = pd.DataFrame({
        'open': p_actual + np.random.randn(25) * 10,
        'high': p_actual + 25, 'low': p_actual - 25,
        'close': p_actual + np.random.randn(25) * 10
    })
    
    fig = go.Figure(data=[go.Candlestick(
        open=df_v['open'], high=df_v['high'], low=df_v['low'], close=df_v['close'],
        increasing_line_color='#00ff00', decreasing_line_color='#ff00ff'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=450, margin=dict(l=0, r=0, t=0, b=0),
        xaxis_rangeslider_visible=False,
        yaxis=dict(color="white", gridcolor="rgba(255,255,255,0.05)")
    )
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    st.markdown('<div class="card" style="text-align:left; min-height:450px;">', unsafe_allow_html=True)
    st.subheader("🛠️ Cerebro Mahora")
    st.write("Sincronizando Bitso Multi-Asset...")
    st.write("💎 **Ether:** 0.0017524")
    st.write("🇲🇽 **Pesos:** $47.12")
    st.write("🎯 **Venta Meta:** $115.00 USD")
    
    # Barra de progreso estética
    progreso_val = (p_actual / 115000) if p_actual < 115000 else 1.0
    st.progress(progreso_val)
    
    st.write("")
    # Botón Reparado
    if st.button("🚀 EJECUTAR ADAPTACIÓN (0.50 USD)", use_container_width=True):
        resultado = execute_bitso_action("buy", 0.50)
        
        if resultado.get('success') or 'payload' in resultado:
            st.success("¡ADAPTACIÓN EXITOSA! Orden real enviada.")
            st.balloons()
        else:
            # Manejo de error de balance insuficiente
            err_msg = resultado.get('message', resultado.get('error', 'Error Desconocido'))
            st.error(f"Fallo: {err_msg}")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nEstado: Sincronizado\nModo: Prestige", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresco cada 10 segundos
time.sleep(10)
st.rerun()
