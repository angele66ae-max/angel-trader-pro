import streamlit as st
import pandas as pd
import pandas_ta as ta
import numpy as np # <-- IMPORTADO
import requests
import hmac
import hashlib
import time
import json
import yfinance as yf
from alpaca_trade_api.rest import REST

# --- 1. LLAVES DE PODER (CONFIGURACIÓN) ---
BITSO_KEY = "FZHAAOqOhy"
BITSO_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

# NOTA: Para operar en la bolsa necesitas tus llaves de Alpaca.markets
ALP_KEY = "TU_ALPACA_KEY"
ALP_SECRET = "TU_ALPACA_SECRET"
alpaca = REST(ALP_KEY, ALP_SECRET, "https://paper-api.alpaca.markets")

st.set_page_config(layout="wide", page_title="MAHORA OMNI-BOT")

# --- 2. GESTIÓN DE MEMORIA Y PROTECCIÓN ---
if "ultimo_movimiento" not in st.session_state:
    st.session_state.ultimo_movimiento = 0

# --- 3. FUNCIONES DE DISPARO (ACCIONES Y CRIPTO) ---
def trade_bitso(book, side, monto):
    path = "/v3/orders/"
    nonce = str(int(time.time() * 1000))
    payload = {"book": book, "side": side, "type": "market", "minor": f"{monto:.2f}"}
    json_payload = json.dumps(payload)
    sig = hmac.new(BITSO_SECRET.encode(), (nonce + "POST" + path + json_payload).encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {BITSO_KEY}:{nonce}:{sig}', 'Content-Type': 'application/json'}
    return requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload).json()

def trade_alpaca(symbol, monto_usd):
    try:
        return alpaca.submit_order(symbol=symbol, notional=monto_usd, side='buy', type='market', time_in_force='day')
    except Exception as e: return {"error": str(e)}

# --- 4. CEREBRO DE INTERCAMBIO (REBALANCEO) ---
st.title("⛩️ MAHORASHARK: OMNI-EXCHANGE ENGINE")

# Monitor Cripto Real
r_btc = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
btc_p = float(r_btc['last'])

# Monitor Bolsa Real (NVDA)
nvda_data = yf.Ticker("NVDA").history(period="1d", interval="1m")
nvda_p = nvda_data['Close'].iloc[-1]

c1, c2, c3 = st.columns(3)
c1.metric("BITCOIN (MXN)", f"${btc_p:,.2f}")
c2.metric("NVIDIA (USD)", f"${nvda_p:.2f}")
c3.metric("CAPITAL TOTAL", "$68.91 MXN")

st.write("---")

# --- 5. LÓGICA DE ROTACIÓN ---
# Si BTC está caro y la bolsa está barata -> ROTAR
st.subheader("🧠 Estrategia: Rotación de Capital para los 10K")

col_l, col_r = st.columns(2)

with col_l:
    st.write("### ₿ Lado Cripto")
    # RSI Real de Bitcoin
    trades = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn&limit=50").json()['payload']
    df_btc = pd.DataFrame([float(t['price']) for t in trades], columns=['close'])
    rsi_btc = ta.rsi(df_btc['close'], length=14).iloc[-1]
    st.write(f"RSI BTC: {rsi_btc:.2f}")
    
    if rsi_btc > 70: # Sobrecompra en BTC
        st.success("🎯 Sugerencia: Vender BTC y comprar NVIDIA")
        if st.button("🔄 EJECUTAR ROTACIÓN: CRIPTO -> BOLSA"):
            # 1. Vende en Bitso
            res_b = trade_bitso("btc_mxn", "sell", 30) # Ejemplo $30 MXN
            # 2. Compra en Alpaca (Simulado el paso de dinero)
            res_a = trade_alpaca("NVDA", 1.75) # Aprox $30 MXN en USD
            st.json({"Bitso": res_b, "Alpaca": res_a})

with col_r:
    st.write("### 📈 Lado Bolsa")
    # Tendencia de NVIDIA
    nvda_data['sma'] = nvda_data['Close'].rolling(20).mean()
    if nvda_p > nvda_data['sma'].iloc[-1]:
        st.write("Estado: **TENDENCIA ALCISTA EN NVDA** 🚀")
    else:
        st.write("Estado: **MERCADO LENTO** ⚖️")

# --- 6. LOGS DE OPERACIÓN ---
st.write("---")
st.info(">> Mahora está monitoreando ambos mercados. El rebalanceo protege tus ganancias.")

time.sleep(15)
st.rerun()
