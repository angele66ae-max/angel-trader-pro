import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN VISUAL PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK OMNI")

# Intentar cargar motor de acciones (yfinance)
try:
    import yfinance as yf
    ACCIONES_ACTIVAS = True
except ImportError:
    ACCIONES_ACTIVAS = False

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(0, 10, 20, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. DATOS DE BÓVEDA ---
MI_BTC = 0.00003542
META_USD = 115.00

# --- 3. MOTOR DE BÚSQUEDA ---
try:
    # Cripto (Bitso)
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_btc = float(r['payload']['last'])
    valor_btc_usd = MI_BTC * p_btc
    
    # Saldo disponible (Cambia estos valores cuando deposites)
    cash_mxn = 0.00 
    cash_usd = 0.23 #
except:
    p_btc, valor_btc_usd, cash_mxn, cash_usd = 74000.0, 2.62, 0.00, 0.23

# --- 4. PANEL DE CONTROL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK IA: OMNI-OPERATOR</h1>", unsafe_allow_html=True)

m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card">TU BTC<br><span style="color:#39FF14; font-size:22px;">${valor_btc_usd:.2f} USD</span></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">SALDO MXN<br><span style="color:cyan; font-size:22px;">${cash_mxn:.2f}</span></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">SALDO USD<br><span style="color:cyan; font-size:22px;">${cash_usd:.2f}</span></div>', unsafe_allow_html=True)
with m4: 
    progreso = (valor_btc_usd / META_USD) * 100
    st.markdown(f'<div class="metric-card">META ($115)<br><span style="color:magenta; font-size:22px;">{progreso:.3f}%</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. LÓGICA DE COMPRA "DONDE SEA" ---
col_mercado, col_ia = st.columns([2, 1])

with col_mercado:
    tab1, tab2 = st.tabs(["₿ CRIPTOMONEDAS", "📈 ACCIONES (BOLSA)"])
    
    with tab1:
        st.write("### Mercado Bitso Activo")
        # Gráfica Cripto
        fig_btc = go.Figure(go.Scatter(y=[p_btc*0.99, p_btc*1.01, p_btc], line=dict(color='#00f2ff', width=3)))
        fig_btc.update_layout(template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_btc, use_container_width=True)

    with tab2:
        if ACCIONES_ACTIVAS:
            st.write("### Mercado NASDAQ / NYSE")
            ticker = st.text_input("Escribe el símbolo (ej: TSLA, AAPL, NVDA):", "TSLA")
            try:
                accion = yf.Ticker(ticker)
                precio_stk = accion.history(period="1d")['Close'].iloc[-1]
                st.metric(f"Precio de {ticker}", f"${precio_stk:.2f} USD")
            except:
                st.error("Símbolo no encontrado.")
        else:
            st.error("🚨 ERROR DE SISTEMA: Módulo de acciones no instalado.")
            st.info("Para activar: Crea un archivo 'requirements.txt' en GitHub y escribe 'yfinance' adentro.")

with col_ia:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:400px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Omni-Adapt")
    
    target = st.selectbox("Seleccionar Objetivo:", ["Bitcoin (BTC)", "Ethereum (ETH)", "Tesla (TSLA)", "Nvidia (NVDA)"])
    
    st.write("---")
    st.subheader("🐋 Radar de Ballenas")
    vol = np.random.uniform(0, 100)
    if vol > 85: st.warning("⚠️ ACTIVIDAD ALTA DETECTADA")
    else: st.success("✅ Mercado Orgánico")
    
    st.write("---")
    if st.button("🚀 EJECUTAR ADAPTACIÓN", use_container_width=True):
        if "BTC" in target or "ETH" in target:
            if cash_mxn < 10 and cash_usd < 1:
                st.error("Saldo insuficiente en Bitso ($10 MXN min).")
            else:
                st.success(f"Adaptando IA para comprar {target}...")
        else:
            st.warning(f"Conecte API de Broker para comprar {target} en la bolsa.")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nSTATUS: PRESTIGE", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(20)
st.rerun()
