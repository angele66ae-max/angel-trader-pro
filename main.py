import streamlit as st
import yfinance as yf
import pandas as pd
import pandas_ta as ta
import requests
import hmac
import hashlib
import time
import json

# --- 1. CONEXIÓN Y SETTINGS ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
ACCIONES_REFERENCIA = ["NVDA", "AAPL", "TSLA"] # Las que "mandan" en el mercado
MONEDAS_BITSO = ["btc_mxn", "sol_mxn", "eth_mxn"]

st.set_page_config(layout="wide", page_title="MAHORA STOCK-SYNC")

# --- 2. MOTOR DE ACCIONES REALES (NYSE/NASDAQ) ---
def analizar_acciones():
    try:
        # Usamos NVIDIA como el motor principal de decisión
        stock = yf.Ticker("NVDA")
        hist = stock.history(period="1d", interval="1m")
        if hist.empty: return 0, "CERRADO"
        
        precio_actual = hist['Close'].iloc[-1]
        precio_apertura = hist['Open'].iloc[0]
        cambio = ((precio_actual - precio_apertura) / precio_apertura) * 100
        return cambio, precio_actual
    except:
        return 0, 0

# --- 3. EJECUCIÓN DE ORDEN EN BITSO ---
def enviar_orden_bitso(book, side, monto_mxn):
    path = "/v3/orders/"
    nonce = str(int(time.time() * 1000))
    payload = {
        "book": book, 
        "side": side, 
        "type": "market", 
        "minor": f"{monto_mxn:.2f}"
    }
    json_payload = json.dumps(payload)
    message = nonce + "POST" + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    
    headers = {
        'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}',
        'Content-Type': 'application/json'
    }
    res = requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload)
    return res.json()

# --- 4. INTERFAZ Y ESTRATEGIA ---
st.title("⛩️ MAHORASHARK: STOCK-SYNC ADAPTATION")

cambio_stock, precio_nvda = analizar_acciones()

c1, c2, c3 = st.columns(3)
c1.metric("NVIDIA (NVDA)", f"${precio_nvda:.2f}", f"{cambio_stock:.2f}%")
c2.metric("CAPITAL", "$68.91 MXN")
c3.info("ESTADO: Sincronizando Wall Street con Bitso")

st.write("---")

# --- 5. EL DISPARADOR (ESTRATEGIA OMNI) ---
# Si las acciones tecnológicas suben más de 0.2%, compramos Cripto
if cambio_stock > 0.20:
    st.success(f"🚀 SEÑAL ALCISTA EN ACCIONES ({cambio_stock:.2f}%)")
    
    # Decisión de la IA: Comprar SOL porque es la que más sigue a las acciones tech
    if st.session_state.get('ultimo_trade_omni', 0) < time.time() - 300: # 5 min de respiro
        monto = 25.00 # Vamos a usar $25 de tus $68 para probar
        resultado = enviar_orden_bitso("sol_mxn", "buy", monto)
        st.write("### 📜 RESULTADO DE LA ORDEN:")
        st.json(resultado)
        st.session_state['ultimo_trade_omni'] = time.time()
    else:
        st.write(">> Esperando ventana de tiempo para no sobreoperar...")
else:
    st.warning("⚖️ MERCADO DE ACCIONES LATERAL O BAJISTA - Esperando oportunidad.")

# Gráfico de la acción para que veas qué está viendo el bot
st.write("### 📈 Monitor Real: NVDA (Referencia para Cripto)")
df_grafica = yf.download("NVDA", period="1d", interval="5m")
st.line_chart(df_grafica['Close'])

time.sleep(20)
st.rerun()
