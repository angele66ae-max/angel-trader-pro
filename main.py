import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark: Prestige Center", page_icon="⛩️")

# --- ESTILO CSS CYBERPUNK ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: white; }
    .metric-card {
        background-color: #0b141a;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00f2ff33;
    }
    .metric-title { color: #ffffff; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .metric-value { color: #00f2ff; font-size: 24px; font-weight: bold; text-shadow: 0 0 8px #00f2ff; }
    .ia-log {
        background-color: #000;
        border: 1px solid #ff00ff;
        border-radius: 5px;
        padding: 10px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
        font-size: 13px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS REALES (BITSO) ---
def obtener_datos():
    try:
        url = "https://api.bitso.com/v3/trades/?book=btc_mxn"
        r = requests.get(url).json()
        df = pd.DataFrame(r['payload'])
        df['price'] = df['price'].astype(float)
        return df
    except: return pd.DataFrame()

def calcular_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / (loss + 1e-9) # Evitar división por cero
    return 100 - (100 / (1 + rs))

# --- LÓGICA DE PROCESAMIENTO ---
data = obtener_datos()
if not data.empty:
    precio_actual = data['price'].iloc[0]
    rsi_actual = calcular_rsi(data['price']).iloc[-1]
    sma_7 = data['price'].rolling(window=7).mean().iloc[-1]
else:
    precio_actual, rsi_actual, sma_7 = 0.0, 50.0, 0.0

# Decisión de IA
decision = "⚖️ ESPERAR"
if rsi_actual < 35: decision = "🟢 COMPRA ESTRATÉGICA"
elif rsi_actual > 65: decision = "🔴 VENTA / STOP LOSS"

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior (Línea 73 Corregida)
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN REAL</div><div class="metric-value">${precio_actual:,.1f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-title">BALANCE USD</div><div class="metric-value" style="color:#ff00ff">$2.81</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">RSI (14)</div><div class="metric-value" style="color:#39FF14">{rsi_actual:.2f}</div></div>', unsafe_allow_html=True)
with c4:
    progreso = (47.12 / 10000) * 100
    st.markdown(f'<div class="metric-card"><div class="metric-title">META 10K</div><div class="metric-value">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo Principal
col_main, col_ia = st.columns([3, 1])

with col_main:
    st.subheader("📈 Análisis de Mercado (Trades en Tiempo Real)")
    if not data.empty:
        chart_prices = data['price'].head(50).iloc[::-1]
        st.line_chart(chart_prices, color="#00f2ff")
    
    st.subheader("💰 Tu Cuenta")
    st.write(f"**Bitcoin:** 0.000039 | **Pesos:** $47.12 | **Ethereum:** 0.000000")
    if st.button("🚀 ACTIVAR COMPRA/VENTA REAL"):
        st.info("Conectando con Bitso API...")

with col_ia:
    st.subheader("🧠 Cerebro Mahora")
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="ia-log">
            [{ahora}]<br>
            Analizando mercado BTC...<br><br>
            RSI: {rsi_actual:.2f}<br>
            SMA 7: {sma_7:,.1f}<br><br>
            <b>DECISIÓN: {decision}</b><br>
            Probabilidad: {82 if decision != "⚖️ ESPERAR" else 50}%<br>
            <hr>
            >> SIGUIENTE ACTUALIZACIÓN EN 20S
        </div>
    """, unsafe_allow_html=True)

# --- REFRESH AUTOMÁTICO ---
time.sleep(20)
st.rerun()
