import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
from datetime import datetime

# --- CONFIGURACIÓN CORE ---
st.set_page_config(layout="wide", page_title="SHARK NEON v9.0")

# --- CREDENCIALES (Limpia espacios invisibles) ---
API_KEY = st.secrets.get("BITSO_API_KEY", "").strip()
API_SECRET = st.secrets.get("BITSO_API_SECRET", "").strip()

# --- ESTILO VISUAL ---
st.markdown("""
    <style>
    .stApp { background-color: #020205; color: #00d4ff; }
    .card { background: rgba(20, 0, 40, 0.9); border: 1px solid #bc13fe; padding: 20px; border-radius: 15px; box-shadow: 0 0 20px #bc13fe; }
    </style>
    """, unsafe_allow_html=True)

def bitso_api_call(method, path):
    """Motor de conexión de alta fidelidad v9.0"""
    nonce = str(int(time.time() * 1000))
    message = nonce + method + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    
    url = f"https://api.bitso.com{path}"
    return requests.get(url, headers=headers)

def get_wallet():
    if not API_KEY: return None, "Faltan llaves en Secrets"
    try:
        # Usamos el endpoint más básico para forzar la respuesta
        r = bitso_api_call("GET", "/v3/balances")
        if r.status_code == 200:
            return r.json()['payload']['balances'], "OK"
        return None, f"Error {r.status_code}: {r.json().get('error', {}).get('message', 'Recurso no encontrado')}"
    except Exception as e:
        return None, str(e)

def get_price(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- UI ---
st.title("🦈 SHARK SYSTEM v9.0")
st.write(f"Protocolo de Red: **Starship 2026** | Usuario: **Pavo Free Fire**")

col_bal, col_meta = st.columns([2, 1])

with col_bal:
    balances, status = get_wallet()
    if status == "OK":
        st.success("🛰️ CONEXIÓN ESTABLE")
        wallet_data = []
        total_mxn = 0.0
        for b in balances:
            qty = float(b['total'])
            if qty > 0:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_price(f"{coin.lower()}_mxn")
                val = qty * price
                total_mxn += val
                wallet_data.append({"TOKEN": coin, "SALDO": qty, "VALOR MXN": f"${val:,.2f}"})
        
        st.table(pd.DataFrame(wallet_data))
        st.metric("BALANCE TOTAL", f"${total_mxn:,.2f} MXN")
    else:
        st.error(f"Fallo de Nodo: {status}")
        st.info("🆘 **SOLUCIÓN FINAL:** Si ves Error 404, la API Key 'casa tiburones' está muerta. Crea una nueva llamada 'SharkV9' y cámbiala en Streamlit.")

with col_meta:
    st.subheader("🎯 OBJETIVO SUV")
    # Meta de la camioneta de 1.7 millones
    meta = 1700000
    actual = total_mxn if status == "OK" else 0.0
    progreso = min(actual / meta, 1.0)
    
    st.markdown(f"""
    <div class="card">
        <h3>Meta: $1,700,000 MXN</h3>
        <p>Progreso actual: {progreso*100:.2f}%</p>
    </div>
    """, unsafe_allow_html=True)
    st.progress(progreso)
    
    if actual >= meta:
        st.balloons()
        st.success("¡LO LOGRASTE, TIBURÓN!")

# --- TICKERS ---
st.divider()
c1, c2, c3 = st.columns(3)
c1.metric("₿ BTC", f"${get_price('btc_mxn'):,.0f}")
c2.metric("Ξ ETH", f"${get_price('eth_mxn'):,.0f}")
c3.metric("💵 USD", f"${get_price('usd_mxn'):,.2f}")
