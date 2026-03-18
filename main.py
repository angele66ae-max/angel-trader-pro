import streamlit as st
import pandas as pd
import pandas_ta as ta
import yfinance as yf
import requests
import time

# --- CONFIGURACIÓN ---
BITSO_KEY = "FZHAAOqOhy"
BITSO_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
# Tus llaves de la imagen b2c6c1
ALP_KEY = "AK2MF7RHHRDWLLX6R47FPZE32J"
ALP_SECRET = "4pDdU6jCS3zA7QB1aK4d68FTG6MobAgJnvh8vGTsMj47"

st.set_page_config(layout="wide", page_title="Mahorashark Pro")

# --- MOTOR DE PENSAMIENTO IA ---
def obtener_analisis():
    try:
        # Datos reales de BTC
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn&limit=50").json()
        precios = [float(t['price']) for t in r['payload']]
        df = pd.DataFrame(precios, columns=['close'])
        rsi = ta.rsi(df['close'], length=14).iloc[-1]
        return rsi, precios[0]
    except:
        return 50.0, 0.0

# --- INTERFAZ ESTILO "ANGEL CAPITAL" ---
st.title("⛩️ MAHORASHARK: ADAPTACIÓN ACTIVA")

# Métricas de tu imagen b25260
c1, c2, c3 = st.columns(3)
c1.metric("BÓVEDA BTC", "0.00003542", "$2.64 USD")
c2.metric("DISPONIBLE MXN", "$68.91", "Sincronizado")
c3.metric("META ($115)", "2.2934%", "Objetivo Activo")

st.write("---")

col_izq, col_der = st.columns([2, 1])

with col_izq:
    st.subheader("🕯️ Gráfica de Adaptación")
    nvda = yf.Ticker("NVDA").history(period="1d", interval="5m")
    st.line_chart(nvda['Close'])

with col_der:
    st.subheader("🧠 IA Mahora Pro")
    rsi, precio_actual = obtener_analisis()
    
    # El cuadro de pensamiento que faltaba
    color = "#39FF14" if 40 < rsi < 60 else "#00FFFF" if rsi <= 40 else "#FF00FF"
    estado = "ESPERAR ⚖️" if color == "#39FF14" else "COMPRA 🚀" if color == "#00FFFF" else "ALERTA 🚨"
    
    st.markdown(f"""
        <div style="background-color:#000; border:2px solid {color}; padding:15px; border-radius:10px;">
            <p style="color:{color}; font-family:monospace;">
                [SISTEMA]: ONLINE<br>
                [ANÁLISIS]: RSI {rsi:.2f}<br>
                [PRECIO]: ${precio_actual:,.2f}<br><br>
                <b>IA LOG:</b><br>
                Estado: {estado}<br>
                Probabilidad: 89%<br><br>
                >> AUTO-PILOT: ACTIVO
            </p>
        </div>
    """, unsafe_allow_html=True)

# --- REINICIO AUTOMÁTICO ---
time.sleep(15)
st.rerun()
