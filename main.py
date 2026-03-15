import streamlit as st
import pandas as pd
import numpy as np
import time
import ccxt # Conector real
from datetime import datetime

# --- CONFIGURACIÓN DE NÚCLEO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: REAL")

# --- CREDENCIALES BITSO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# Conexión profesional
bitso = ccxt.bitso({
    'apiKey': API_KEY,
    'secret': API_SECRET,
})

# --- FONDO DE LA RUEDA DE MAHAGA ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("{fondo_url}");
        background-size: cover;
        background-attachment: fixed;
    }}
    .card {{
        background: rgba(10, 10, 15, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- MOTOR DE DATOS EN VIVO ---
def get_bitso_data():
    try:
        # Balance Real
        bal = bitso.fetch_balance()
        usd = bal['total'].get('USD', 2.81)
        
        # Precio Real
        tick = bitso.fetch_ticker('BTC/USD')
        precio = tick['last']
        
        return usd, precio, "CONEXIÓN EXITOSA"
    except Exception as e:
        return 2.81, 70965.0, f"ERROR: {str(e)}"

# --- LÓGICA DE SESIÓN ---
if "hist" not in st.session_state:
    st.session_state.hist = []

saldo, btc_p, status = get_bitso_data()
st.session_state.hist.append(btc_p)
st.session_state.hist = st.session_state.hist[-50:]

# --- INTERFAZ ---
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK: MODO EJECUCIÓN</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="card">BITSO<br><h2 style="color:#00ff00;">LIVE</h2></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="card">SALDO REAL<br><h2 style="color:magenta;">${saldo:.2f}</h2></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="card">PRECIO BTC<br><h2>${btc_p:,.2f}</h2></div>', unsafe_allow_html=True)
with m4: 
    progreso = (saldo / 10000.0)
    st.markdown(f'<div class="card">META 10K<br><h2>{(progreso*100):.4f}%</h2></div>', unsafe_allow_html=True)
    st.progress(progreso if progreso <= 1.0 else 1.0)

# Gráfica Real (Sin cuadrados azules)
st.markdown('<div class="card">', unsafe_allow_html=True)
st.subheader("Flujo de Mercado Bitso")
st.line_chart(pd.DataFrame(st.session_state.hist, columns=["BTC/USD"]), color="#00f2ff")
st.markdown('</div>', unsafe_allow_html=True)

# Logs de la IA
st.markdown("### 🤖 Pensamientos de Mahorashark")
current_time = datetime.now().strftime('%H:%M:%S')
st.code(f"[{current_time}] STATUS: {status}\n[ALERTA]: Objetivo fijado en 115.\n[ADAPTACIÓN]: Protegiendo capital de ${saldo}.")

# Auto-actualización cada 5 segundos
time.sleep(5)
st.rerun()
