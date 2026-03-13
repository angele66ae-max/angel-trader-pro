import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.4")

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

# --- ESTILO SHARK AVANZADO ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    h1, h2, h3 { font-family: 'Orbitron', sans-serif; color: #00d4ff !important; text-shadow: 0 0 10px #bc13fe; }
    .status-box { background: rgba(20, 0, 40, 0.8); border: 2px solid #00d4ff; padding: 15px; border-radius: 10px; box-shadow: 0 0 15px #bc13fe; }
    
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 15px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # LA RUTA CRÍTICA: Añadimos la diagonal final que Bitso exige para tus permisos
    base = "https://api.bitso.com"
    path = "/v3/balances/" 
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha
