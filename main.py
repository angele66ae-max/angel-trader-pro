import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. NÚCLEO DE PODER (SEGURIDAD) ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"
PROYECTO = "ANGEL PRESTIGE COMMAND"

st.set_page_config(layout="wide", page_title=PROYECTO, page_icon="⚔️")

# --- 2. MOTOR DE EJECUCIÓN ---
def bitso_api(method, path, payload=""):
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(API_SECRET.encode(), (nonce + method + path + payload).encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    url = f"https://api.bitso.com{path}"
    if method == "GET": return requests.get(url, headers=headers).json()
    return requests.post(url, headers=headers, data=payload).json()

def cargar_balance():
    try:
        r = bitso_api("GET", "/v3/balance/")
        balances = {b['currency']: float(b['total']) for b in r['payload']['balances']}
        return balances.get('mxn', 0.0), balances.get('btc', 0.0), balances.get('eth', 0.0), True
    except: return 114.29, 0.00004726, 0.0012, False

mxn, btc, eth, online = cargar_balance()

# --- 3. DISEÑO "TACTICAL BLACK" ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #020608; color: #e1e1e1; font-family: 'Inter', sans-serif; }}
    .header-bar {{ background: #0a0f12; border-bottom: 2px solid #00f2ff; padding: 15px; display: flex; justify-content: space-around; }}
    .card {{ background: #0d1216; border: 1px solid #1e252b; border-radius: 6px; padding: 15px; box-shadow: 2px 2px 10px rgba(0,0,0,0.5); }}
    .glow-text {{ color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }}
    .stButton>button {{ background: #131722; border: 1px solid #363c4e; color: white; width: 100%; }}
    .stButton>button:hover {{ border-color: #ff00ff; color: #ff00ff; }}
    .terminal {{ font-family: 'JetBrains Mono', monospace; color: #39FF14; font-size: 11px; line-height: 1.2; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. TOP HUD (SALA DE GUERRA) ---
st.markdown(f"""
    <div class="header-bar">
        <div style="text-align:center"><small style="color:#666">ESTADO</small><br><b style="color:{'#39FF14' if online else '#ff4b4b'}">● {'TACTICAL LIVE' if online else 'OFFLINE'}</b></div>
        <div style="text-align:center"><small style="color:#666">FONDOS MXN</small><br><b class="glow-text
