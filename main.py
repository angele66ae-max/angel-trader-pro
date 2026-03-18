import streamlit as st
import pandas as pd
import yfinance as yf
from alpaca_trade_api.rest import REST, TimeFrame # Necesitas: pip install alpaca-trade-api
import time

# --- 1. CREDENCIALES DE BOLSA (ALPACA) ---
ALPACA_KEY = "TU_ALPACA_KEY"
ALPACA_SECRET = "TU_ALPACA_SECRET"
BASE_URL = "https://paper-api.alpaca.markets" # URL de prueba (dinero virtual)

# Conexión con el Broker
alpaca = REST(ALPACA_KEY, ALPACA_SECRET, BASE_URL, api_version='v2')

st.set_page_config(layout="wide", page_title="MAHORA WALL STREET")

# --- 2. MOTOR DE EJECUCIÓN DE ACCIONES ---
def comprar_accion_real(symbol, qty):
    try:
        # Orden de mercado: Compra 'qty' acciones de 'symbol'
        order = alpaca.submit_order(
            symbol=symbol,
            qty=qty,
            side='buy',
            type='market',
            time_in_force='gtc'
        )
        return order
    except Exception as e:
        return f"Error: {e}"

# --- 3. DASHBOARD DE LA BOLSA ---
st.title("⛩️ MAHORASHARK: STOCK MARKET ADAPTATION")

# Seleccionamos las acciones "Top" para los 10k
ticker_buscado = st.selectbox("ACTIVO A OPERAR", ["NVDA", "TSLA", "AAPL", "AMZN", "MSFT"])

# Datos en tiempo real de Yahoo Finance
data = yf.Ticker(ticker_buscado).history(period="1d", interval="1m")
precio_actual = data['Close'].iloc[-1]

c1, c2, c3 = st.columns(3)
c1.metric("ACCIÓN", ticker_buscado)
c2.metric("PRECIO ACTUAL", f"${precio_actual:.2f} USD")
c3.metric("ESTADO BOLSA", "OPEN" if 14 <= time.localtime().tm_hour <= 21 else "CLOSED")

st.write("---")

# --- 4. LÓGICA DE TRADING AUTOMÁTICO ---
st.subheader("🧠 Estrategia Mahora Pro: Cruce de Tendencia")

# Calculamos medias móviles simples (SMA)
data['SMA_20'] = data['Close'].rolling(window=20).mean()
sma_now = data['SMA_20'].iloc[-1]

st.line_chart(data[['Close', 'SMA_20']])

# --- DISPARADOR DE COMPRA ---
# Si el precio cruza hacia arriba la media de 20 periodos -> COMPRA
if precio_actual > sma_now:
    st.success(f"📈 TENDENCIA ALCISTA DETECTADA EN {ticker_buscado}")
    
    if st.button(f"🚀 EJECUTAR COMPRA REAL DE {ticker_buscado}"):
        # Con Alpaca puedes comprar fracciones, ej: 0.1 de una acción
        res = comprar_accion_real(ticker_buscado, 1) 
        st.json(res)
else:
    st.warning("⚖️ ESPERANDO SEÑAL DE ENTRADA EN LA BOLSA")

# --- 5. TU PORTAFOLIO REAL ---
st.write("### 💼 Tu Portafolio en Wall Street")
try:
    positions = alpaca.list_positions()
    if positions:
        for pos in positions:
            st.write(f"**{pos.symbol}**: {pos.qty} acciones | Ganancia: ${pos.unrealized_pl} USD")
    else:
        st.write("No tienes posiciones abiertas todavía.")
except:
    st.write("Conecta tus API Keys de Alpaca para ver tu portafolio.")

time.sleep(30)
st.rerun()
