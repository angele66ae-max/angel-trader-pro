import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES (Corregidas) ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK NEON v8")

# --- ESTILO NEÓN ---
st.markdown("""
    <style>
    .stApp { background-color: #020205; color: #bc13fe; font-family: 'JetBrains Mono', monospace; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 10px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    # FIX 404: Sin diagonal final
    base = "https://api.bitso.com"
    path = "/v3/balances" 
    
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(base + path, headers=headers, timeout=10)
        if r.status_code == 200: return r.json()['payload']['balances'], "OK"
        return None, f"Error {r.status_code}"
    except Exception as e: return None, str(e)

# --- INTERFAZ ---
st.title("🦈 SHARK SYSTEM: NEON CORE v8.0")

balances, status = get_data()

if status == "OK":
    total_mxn = 0.0
    # (Aquí iría tu lógica de suma de balances)
    # Ejemplo de meta de $10,000 USD (aprox $178,000 MXN)
    meta_usd = 10000.0
    p_usd = 17.82 
    progreso = min((total_mxn / p_usd) / meta_usd, 1.0)
    
    st.subheader("💰 BILLETERA STARSHIP")
    st.metric("TOTAL NET WORTH", f"${total_mxn:,.2f} MXN")
    st.write(f"**Progreso hacia los $10,000 USD:** {progreso*100:.2f}%")
    st.progress(progreso)
else:
    st.error(f"⚠️ FALLO DE ENLACE: {status}")
    st.info("Revisa en Bitso: Permiso 'Account Balances' activo y SIN IP Whitelist.")
