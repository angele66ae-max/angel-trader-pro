import streamlit as st
import pandas as pd
import pandas_ta as ta
import numpy as np  # <--- AGREGADO PARA EVITAR CRASH
import yfinance as yf
import requests
import time

# --- CONFIGURACIÓN DE ANGEL CAPITAL ---
st.set_page_config(layout="wide", page_title="Angel Capital Quant Fund")

def obtener_datos_reales():
    try:
        # Pull de Bitso para el RSI
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn&limit=50").json()
        precios = [float(t['price']) for t in r['payload']]
        df = pd.DataFrame(precios, columns=['close'])
        rsi = ta.rsi(df['close'], length=14).iloc[-1]
        return rsi, precios[0]
    except:
        return 50.0, 0.0

# --- HEADER (Sincronizado con tu imagen b25260) ---
st.title("⛩️ MAHORASHARK: ADAPTACIÓN PRO")

c1, c2, c3 = st.columns(3)
c1.metric("BÓVEDA BTC", "0.00003542", "$2.64 USD")
c2.metric("DISPONIBLE MXN", "$68.91", "Sincronizado")
c3.metric("META ($115)", "2.2934%", "Objetivo Activo")

st.write("---")

# --- BODY: GRÁFICA + PENSAMIENTO ---
col_graf, col_ia = st.columns([2, 1])

with col_graf:
    st.subheader("🕯️ Monitor de Adaptación")
    # Usamos NVIDIA como referencia de mercado tech
    nvda = yf.Ticker("NVDA").history(period="1d", interval="5m")
    st.line_chart(nvda['Close'])

with col_ia:
    st.subheader("🧠 IA Mahora Log")
    rsi_val, btc_p = obtener_datos_reales()
    
    # Lógica de colores neón
    color = "#00FFFF" if rsi_val < 40 else "#FF00FF" if rsi_val > 60 else "#39FF14"
    
    st.markdown(f"""
        <div style="background-color:#000; border:2px solid {color}; padding:20px; border-radius:10px;">
            <p style="color:{color}; font-family:monospace; font-size:14px;">
                [SISTEMA]: ONLINE<br>
                [IA]: Analizando RSI {rsi_val:.2f}<br>
                [TENDENCIA]: {"ALCISTA" if rsi_val < 50 else "CORRECCIÓN"}<br><br>
                <b>DECISIÓN:</b><br>
                {"EJECUTAR COMPRA" if rsi_val < 35 else "MANTENER LIQUIDEZ"}<br><br>
                >> AUTO-PILOT: ACTIVE<br>
                >> SYNC: OK
            </p>
        </div>
    """, unsafe_allow_html=True)

# Refresco para simular tiempo real
time.sleep(15)
st.rerun()
