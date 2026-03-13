import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd # FIX: Importación correcta para evitar ModuleNotFoundError
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
# FIX: Paréntesis cerrados correctamente para evitar SyntaxError
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK NEON v8")

# --- ESTILO NEÓN ---
st.markdown("""
    <style>
    .stApp { background-color: #020205; color: #bc13fe; }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #bc13fe, #00d4ff);
        box-shadow: 0 0 10px #00d4ff;
    }
    </style>
    """, unsafe_allow_html=True)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    # FIX DEFINITIVO 404: Sin diagonal al final y sin puntos extra
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

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- INTERFAZ ---
st.title("🦈 SHARK SYSTEM: NEON CORE v8.0")

p_usd = get_ticker("usd_mxn") or 17.80
balances, status = get_data()

if status == "OK":
    total_mxn = 0.0
    wallet_list = []
    for b in balances:
        cant = float(b['total'])
        if cant > 0:
            coin = b['currency'].upper()
            price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
            v_mxn = cant * price
            total_mxn += v_mxn
            if v_mxn > 1.0:
                wallet_list.append({"TOKEN": coin, "CANTIDAD": cant, "VALOR": f"${v_mxn:,.2f}"})
    
    # --- BARRA DE PROGRESO ---
    total_usd = total_mxn / p_usd
    progreso = min(total_usd / 10000.0, 1.0)
    
    st.subheader("💰 BILLETERA STARSHIP")
    st.table(pd.DataFrame(wallet_list))
    
    st.metric("NET WORTH (MXN)", f"${total_mxn:,.2f}")
    st.write(f"**Progreso a los $10k USD:** {progreso*100:.2f}%")
    st.progress(progreso)
else:
    # FIX: Mensaje de error con instrucciones claras de tus capturas
    st.error(f"⚠️ FALLO DE ENLACE: {status}")
    st.info("Revisa: 1. Permiso 'Consultar Saldos' en Bitso. 2. URL sin puntos extra.")
