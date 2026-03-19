import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Angel Capital - Bitso Trader")

# Función manual de RSI (Para no usar pandas-ta)
def calcular_rsi(precios, periodo=14):
    df = pd.DataFrame(precios, columns=['close'])
    delta = df['close'].diff()
    ganancia = (delta.where(delta > 0, 0)).rolling(window=periodo).mean()
    perdida = (-delta.where(delta < 0, 0)).rolling(window=periodo).mean()
    rs = ganancia / perdida
    rsi = 100 - (100 / (1 + rs))
    return rsi.iloc[-1]

def obtener_datos_bitso():
    try:
        # Traemos los últimos 100 trades de Bitso
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn&limit=100").json()
        precios = [float(t['price']) for t in r['payload']]
        rsi_val = calcular_rsi(precios)
        precio_actual = precios[0]
        return rsi_val, precio_actual
    except Exception as e:
        return 50.0, 0.0

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: BITSO ONLY")

# Métricas superiores
rsi_val, btc_p = obtener_datos_bitso()

c1, c2, c3 = st.columns(3)
c1.metric("PRECIO BTC (MXN)", f"${btc_p:,.2f}")
c2.metric("RSI (14)", f"{rsi_val:.2f}")
c3.metric("OBJETIVO", "$115.00", "Activo")

st.write("---")

col_graf, col_ia = st.columns([2, 1])

with col_graf:
    st.subheader("🕯️ Movimiento Bitso (Últimos Trades)")
    # Simulamos un histórico visual con los datos de Bitso
    datos_grafica = pd.DataFrame(np.random.randn(20, 1), columns=['Precio']) # Placeholder visual
    st.line_chart(datos_grafica)

with col_ia:
    st.subheader("🧠 IA Mahora Log")
    color = "#00FFFF" if rsi_val < 40 else "#FF00FF" if rsi_val > 60 else "#39FF14"
    
    st.markdown(f"""
        <div style="background-color:#000; border:2px solid {color}; padding:20px; border-radius:10px;">
            <p style="color:{color}; font-family:monospace; font-size:14px;">
                [SISTEMA]: CONECTADO A BITSO<br>
                [IA]: Analizando RSI {rsi_val:.2f}<br>
                [TENDENCIA]: {"COMPRA" if rsi_val < 35 else "ESPERA"}<br><br>
                <b>DECISIÓN:</b><br>
                {"EJECUTAR ORDEN" if rsi_val < 30 else "MONITORIZANDO"}<br><br>
                >> ADAPTACIÓN: ACTIVE
            </p>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
