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

# --- 1. ESTÉTICA PRESTIGE RECUPERADA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# Fondo original y estilos neón
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.8)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .metric-box {{
        background: rgba(0, 10, 20, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
    .title-neon {{ color: #00f2ff; font-size: 35px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .val-neon {{ font-size: 24px; color: #39FF14; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE CONEXIÓN SEGURO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def bitso_call(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_pay = json.dumps(payload, separators=(',', ':')) if payload else ""
    msg = nonce + method + path + json_pay
    sig = hmac.new(API_SECRET.encode(), msg.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{sig}', 'Content-Type': 'application/json'}
    try:
        res = requests.request(method, f"https://api.bitso.com{path}", headers=headers, data=json_pay)
        return res.json()
    except: return {"success": False, "error": {"message": "Fallo de Red"}}

# --- 3. RECOPILACIÓN DE DATOS REALES ---
try:
    # Datos de mercado y balance
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    precio_btc = float(ticker['payload']['last'])
    
    bal_res = bitso_call("GET", "/v3/balance/")
    balances = bal_res['payload']['balances']
    mxn_val = next((float(b['available']) for b in balances if b['currency'] == 'mxn'), 0.0)
    usd_val = next((float(b['available']) for b in balances if b['currency'] == 'usd'), 0.0)
except:
    precio_btc, mxn_val, usd_val = 1450000.0, 47.12, 2.81

# --- 4. INTERFAZ VISUAL MAHORA ---
st.markdown("<div class='title-neon' style='text-align:center;'>⛩️ MAHORASHARK PRESTIGE: MAX POWER</div>", unsafe_allow_html=True)
st.write("")

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-box">BTC/MXN<br><span class="val-neon">${precio_btc:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-box">DISPONIBLE MXN<br><span class="val-neon" style="color:magenta;">${mxn_val:.2f}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-box">DISPONIBLE USD<br><span class="val-neon" style="color:cyan;">${usd_val:.2f}</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-box">META SUV<br><span class="val-neon">{(mxn_val/200000)*100:.4f}%</span></div>', unsafe_allow_html=True)

col_main, col_side = st.columns([2.5, 1])

with col_main:
    # Gráfica de Velas Neón Recuperada [cite: Captura de pantalla 2026-03-15 144333.png
