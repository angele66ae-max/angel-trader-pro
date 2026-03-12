import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

st.set_page_config(layout="wide", page_title="SHARK TERMINAL v6.2")

# Estilo Cyberpunk
st.markdown("""
    <style>
    .stApp { background-color: #05070a; color: #00ff41; font-family: 'Courier New', monospace; }
    .stMetric { background: #0d1117; border: 1px solid #00d4ff; border-radius: 5px; }
    .status-error { border: 2px solid #ff003c; padding: 20px; color: #ff003c; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def get_bitso_balances():
    if not API_KEY or not API_SECRET:
        return None, "ERROR: No hay llaves en Secrets"
    
    nonce = str(int(time.time() * 1000))
    path = "/v3/balances/"
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    
    try:
        r = requests.get(f"https://api.bitso.com{path}", headers=headers, timeout=10)
        # ESTO ES LO IMPORTANTE: Nos dirá el error real si falla
        if r.status_code == 200:
            return r.json()['payload']['balances'], "OK"
        else:
            return None, f"CÓDIGO {r.status_code}: {r.text}"
    except Exception as e:
        return None, f"SISTEMA CAÍDO: {str(e)}"

st.title("🦈 SHARK SYSTEM v6.2")

# --- LÓGICA DE BILLETERA ---
balances, status = get_bitso_balances()

if status == "OK":
    st.success("✅ ACCESO CONCEDIDO: CONEXIÓN ESTABLE")
    # ... (aquí va el resto de tu tabla de criptos)
    df_bal = pd.DataFrame([b for b in balances if float(b['total']) > 0])
    st.table(df_bal[['currency', 'total']])
else:
    st.markdown(f'<div class="status-error">🚨 ERROR CRÍTICO: {status}</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ### 🛠 MANUAL DE REPARACIÓN:
    1. **IP Whitelist:** En Bitso, al crear la API Key, asegúrate de que **NO** tenga ninguna IP anotada. Déjalo en blanco.
    2. **Permisos:** La llave debe tener activado **"Account Balances"** (Consultar saldos).
    3. **Secrets:** En Streamlit, asegúrate de que se vea así exactamente (sin comillas):
       `BITSO_API_KEY = su_llave_aqui`
       `BITSO_API_SECRET = su_secreto_aqui`
    """)

# Gráfica rápida para no perder el estilo
st.subheader("📈 LIVE_MARKET_DATA")
p_usd = requests.get("https://api.bitso.com/v3/ticker/?book=usd_mxn").json()['payload']['last']
st.metric("USD/MXN", f"${p_usd} MXN")
