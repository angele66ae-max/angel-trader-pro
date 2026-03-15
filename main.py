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
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# --- 1. LAS LLAVES DEL REINO (GENERAR EN BITSO) ---
# Ve a Bitso -> Perfil -> API -> Crear nuevo API Key (con permiso de 'Orders' y 'Balance')
BITSO_API_KEY = "TU_API_KEY_AQUI"
BITSO_API_SECRET = "TU_SECRET_AQUI"

# --- ESTILO PRESTIGE ---
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{FONDO_URL}"); background-size: cover; }}
    .card {{ background: rgba(0, 15, 30, 0.9); border: 2px solid #00f2ff; border-radius: 12px; padding: 15px; text-align: center; }}
    .metric-val {{ font-size: 32px; color: #00f2ff; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 2. FUNCIÓN DE EJECUCIÓN REAL (CONEXIÓN BITSO) ---
def execute_real_order(side, amount, book="btc_usd"):
    """Envía una orden real al servidor de Bitso usando firma HMAC-SHA256"""
    if BITSO_API_KEY == "TU_API_KEY_AQUI":
        return {"status": "error", "msg": "Llaves API no configuradas"}
    
    nonce = str(int(time.time() * 1000))
    http_method = "POST"
    request_path = "/v3/orders/"
    
    payload = {
        "book": book,
        "side": side,
        "type": "market",
        "major": str(amount) # Cantidad en la moneda principal (ej: 1 USD)
    }
    
    json_payload = json.dumps(payload)
    message = nonce + http_method + request_path + json_payload
    signature = hmac.new(BITSO_API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {BITSO_API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post("https://api.bitso.com" + request_path, headers=headers, data=json_payload)
        return response.json()
    except Exception as e:
        return {"status": "error", "msg": str(e)}

# --- LÓGICA DE INTERFAZ ---
res_ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
current_price = float(res_ticker['payload']['last'])

st.markdown("<h1 style='text-align:center; color:white;'>⛩️ MAHORASHARK: MODO PRODUCCIÓN</h1>", unsafe_allow_html=True)

# Dashboard
m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="card">PRECIO REAL BTC<div class="metric-val">${current_price:,.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="card">BALANCE USD<div class="metric-val" style="color:magenta;">$2.81</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="card">MODO ACTUAL<div class="metric-val" style="color:#39FF14;">LIVE READY</div></div>', unsafe_allow_html=True)

# Control de Operación
st.write("---")
col_info, col_action = st.columns([2, 1])

with col_info:
    st.info("⚠️ ADVERTENCIA: Al presionar el botón inferior, MahoraShark enviará una orden de COMPRA REAL a Bitso usando tus fondos.")
    st.write(f"**Objetivo de Adaptación:** Venta automática a los $115.00 USD.")

with col_action:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.button("🚀 EJECUTAR COMPRA REAL (1 USD)", use_container_width=True):
        # EJECUCIÓN: Comprar 1 USD de Bitcoin
        resultado = execute_real_order("buy", 1.0)
        
        if 'success' in str(resultado):
            st.success("¡ADAPTACIÓN EXITOSA! Orden ejecutada en Bitso.")
            st.balloons()
        else:
            st.error(f"Fallo de conexión: {resultado.get('msg
