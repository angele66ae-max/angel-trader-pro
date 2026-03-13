import streamlit as st
import time, requests, hashlib, hmac
import pandas as pd
import mplfinance as mpf
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="SHARK NEON v8.9")

# --- CREDENCIALES ---
API_KEY = str(st.secrets.get("BITSO_API_KEY", "")).strip()
API_SECRET = str(st.secrets.get("BITSO_API_SECRET", "")).strip()

# --- ESTILO SHARK ---
st.markdown("""
    <style>
    .stApp { background-color: #020205; color: #bc13fe; }
    .status-box { border: 2px solid #00d4ff; padding: 15px; border-radius: 10px; background: rgba(0,0,0,0.8); }
    </style>
    """, unsafe_allow_html=True)

def bitso_request(path):
    """Protocolo de Conexión Directa v8.9"""
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + path
    signature = hmac.new(API_SECRET.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json',
        'User-Agent': 'SharkSystem/8.9'
    }
    # Forzamos la URL limpia sin parámetros extra
    return requests.get(f"https://api.bitso.com{path}", headers=headers, timeout=10)

def get_data():
    if not API_KEY or not API_SECRET: return None, "Faltan Credenciales"
    
    # SISTEMA DE DOBLE RUTA: Si una da 404, probamos la otra automáticamente
    rutas = ["/v3/balances", "/api/v3/balances"]
    ultimo_error = ""
    
    for r_path in rutas:
        try:
            r = bitso_request(r_path)
            if r.status_code == 200: 
                return r.json()['payload']['balances'], "OK"
            ultimo_error = f"Error {r.status_code}"
        except Exception as e:
            ultimo_error = str(e)
            
    return None, ultimo_error

def get_ticker(book):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()
        return float(r['payload']['last'])
    except: return 0.0

# --- INTERFAZ ---
st.title("🦈 SHARK SYSTEM: NEON CORE v8.9")

col1, col2 = st.columns([2, 1])

with col2:
    st.subheader("📡 ESTADO DEL NODO")
    balances, status = get_data()
    st.markdown(f"""
    <div class="status-box">
        <b>SISTEMA:</b> {"🟢 ONLINE" if status == "OK" else "🔴 FALLO DE RUTA"}<br>
        <b>ERROR:</b> {status}<br>
        <b>API:</b> {API_KEY[:6]}...
    </div>
    """, unsafe_allow_html=True)
    
    if status != "OK":
        st.warning("⚠️ SIGUE EL PLAN B: Borra la API 'casa tiburones' y crea una nueva con nombre 'SharkFinal'. Asegúrate de marcar 'Ver saldos'.")

with col1:
    # TICKERS RÁPIDOS
    m1, m2, m3 = st.columns(3)
    m1.metric("₿ BTC", f"${get_ticker('btc_mxn'):,.0f} MXN")
    m2.metric("Ξ ETH", f"${get_ticker('eth_mxn'):,.0f} MXN")
    m3.metric("🌐 USD", f"${get_ticker('usd_mxn'):,.2f}")

    if status == "OK":
        st.success("¡CONEXIÓN ESTABLECIDA!")
        # TABLA DE SALDOS
        df_list = []
        total_mxn = 0.0
        for b in balances:
            qty = float(b['total'])
            if qty > 0.00001:
                coin = b['currency'].upper()
                price = 1.0 if coin == "MXN" else get_ticker(f"{coin.lower()}_mxn")
                val = qty * price
                total_mxn += val
                df_list.append({"TOKEN": coin, "CANTIDAD": qty, "VALOR MXN": f"${val:,.2f}"})
        
        st.table(pd.DataFrame(df_list))
        st.metric("BALANCE TOTAL", f"${total_mxn:,.2f} MXN")
        
        # PROGRESO SUV 1.7M
