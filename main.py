import streamlit as st
import pandas as pd
import numpy as np
import time
import hmac
import hashlib
import requests
from datetime import datetime

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="MAHORASHARK AI")

# Usa Secretos de Streamlit o variables seguras
BITSO_API_KEY = st.secrets.get("API_KEY", "TU_KEY")
BITSO_API_SECRET = st.secrets.get("API_SECRET", "TU_SECRET")
BASE_URL = "https://api.bitso.com"

# ---------- FONDO ----------
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>
.stApp {{
    background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url("{fondo_url}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.card {{
    background: rgba(15,20,25,0.85);
    border: 1px solid #00f2ff;
    border-radius: 10px;
    padding: 15px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0,242,255,0.2);
}}
.metric {{
    font-size: 32px;
    color: #00f2ff;
    font-weight: bold;
    text-shadow: 0 0 10px #00f2ff;
}}
</style>
""", unsafe_allow_html=True)

# ---------- SESIÓN ----------
if "log" not in st.session_state: st.session_state.log = []
if "price_history" not in st.session_state: st.session_state.price_history = []
if "ai_on" not in st.session_state: st.session_state.ai_on = False

# ---------- FUNCIONES ----------
def get_price():
    try:
        r = requests.get(f"{BASE_URL}/v3/ticker/?book=btc_mxn", timeout=5)
        return float(r.json()["payload"]["last"])
    except:
        return st.session_state.price_history[-1] if st.session_state.price_history else 0.0

# ---------- LÓGICA ----------
price = get_price()
st.session_state.price_history.append(price)
if len(st.session_state.price_history) > 60: st.session_state.price_history.pop(0)

# ---------- UI ----------
st.markdown("<h1 style='text-align:center; color:#00f2ff;'>⛩️ MAHORASHARK AI</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="card">BTC MXN<div class="metric">${price:,.0f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="card">ESTADO IA<div class="metric">{"ACTIVA" if st.session_state.ai_on else "OFF"}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="card">META SUV<div class="metric">0.01%</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="card">BALANCE<div class="metric">$2.81</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("Gráfica de Adaptación")
    st.line_chart(pd.DataFrame(st.session_state.price_history), height=300)

with col_right:
    st.subheader("Comandos")
    if st.button("🚀 ACTIVAR", use_container_width=True):
        st.session_state.ai_on = True
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M')}] IA Online")
    if st.button("⛔ DETENER", use_container_width=True):
        st.session_state.ai_on = False
        st.session_state.log.append(f"[{datetime.now().strftime('%H:%M')}] IA Offline")
    
    st.code("\n".join(st.session_state.log[-5:]))

time.sleep(5)
st.rerun()
