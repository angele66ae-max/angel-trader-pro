import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import yfinance as yf # Librería para acciones

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MAHORASHARK MULTI-ASSET")

# (Estilos CSS Neón se mantienen igual que el anterior...)

# --- 2. MOTOR DE DATOS (CRIPTO + ACCIONES) ---
MI_BTC = 0.00003542
META_USD = 115.00

try:
    # Datos Cripto
    t_usd = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_btc = float(t_usd['payload']['last'])
    
    # Datos Acciones (Tesla como ejemplo)
    stock = yf.Ticker("TSLA")
    p_stock = stock.history(period="1d")['Close'].iloc[-1]
    nombre_stock = "TESLA (TSLA)"
except:
    p_btc, p_stock, nombre_stock = 74000.0, 175.0, "TESLA (TSLA)"

# --- 3. PANEL PRINCIPAL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK IA: MULTI-ASSET</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="metric-card">PRECIO BTC<br><span style="color:#39FF14; font-size:24px;">${p_btc:,.2f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">ACCIÓN: {nombre_stock}<br><span style="color:cyan; font-size:24px;">${p_stock:,.2f} USD</span></div>', unsafe_allow_html=True)
with c3: 
    progreso = ((MI_BTC * p_btc) / META_USD) * 100
    st.markdown(f'<div class="metric-card">PROGRESO META<br><span style="color:magenta; font-size:24px;">{progreso:.3f}%</span></div>', unsafe_allow_html=True)

# --- 4. IA Y ADAPTACIÓN ---
col_graf, col_ia = st.columns([2, 1])

with col_graf:
    st.write("### 📊 Comparativa de Mercado")
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=[p_btc*0.98, p_btc*1.02, p_btc], name="Bitcoin", line=dict(color='#00f2ff')))
    fig.add_trace(go.Scatter(y=[p_stock*500, p_stock*510, p_stock*505], name="Acción (Escalada)", line=dict(color='magenta')))
    fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:400px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Mahora Multi-Asset")
    
    opcion_ia = st.selectbox("Activo a Adaptar:", ["Bitcoin (BTC)", "Tesla (TSLA)", "Apple (AAPL)", "Nvidia (NVDA)"])
    
    st.write("---")
    st.warning("⚠️ Nota: Las acciones requieren conexión a Broker (GBM/Interactive).")
    
    if st.button("🚀 EJECUTAR COMPRA IA", use_container_width=True):
        if "Bitcoin" in opcion_ia:
            st.error("Error: Insufficient Balance en Bitso.")
        else:
            st.info(f"IA lista para comprar {opcion_ia}. Conecte API de Broker para ejecutar.")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nStatus: MULTI-SYNC", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(30)
st.rerun()
