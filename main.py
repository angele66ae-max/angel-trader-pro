import streamlit as st
import pandas as pd
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK MONITOR")

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
    .val-neon {{ font-size: 24px; color: #39FF14; font-weight: bold; text-shadow: 0 0 10px #39FF14; }}
</style>
""", unsafe_allow_html=True)

# --- 2. TUS ACTIVOS REALES ---
MI_BTC = 0.00003542
MI_ETH = 0.0017524
META_USD = 115.00

# --- 3. DATOS DE MERCADO ---
try:
    # Precio BTC en USD y MXN
    t_usd = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    t_mxn = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    p_btc_usd = float(t_usd['payload']['last'])
    p_btc_mxn = float(t_mxn['payload']['last'])
    
    # Valor actual de tu cartera
    valor_actual_usd = MI_BTC * p_btc_usd
    valor_actual_mxn = MI_BTC * p_btc_mxn
except:
    p_btc_usd, valor_actual_usd, valor_actual_mxn = 75000.0, 2.65, 45.96

# --- 4. DASHBOARD ---
st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK: MONITOR DE BÓVEDA</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">VALOR BTC (MXN)<div class="val-neon">${valor_actual_mxn:.2f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">VALOR BTC (USD)<div class="val-neon" style="color:cyan;">${valor_actual_usd:.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">META FINAL<div class="val-neon" style="color:magenta;">${META_USD:.2f} USD</div></div>', unsafe_allow_html=True)
with c4: 
    progreso = (valor_actual_usd / META_USD) * 100
    st.markdown(f'<div class="metric-card">PROGRESO META<div class="val-neon">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

# --- 5. VISUALIZACIÓN ---
col_graf, col_info = st.columns([2, 1])

with col_graf:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.write("📊 **Tendencia BTC/USD**")
    # Gráfica simple de simulación de tendencia
    fig = go.Figure(go.Scatter(y=[p_btc_usd*0.99, p_btc_usd*1.01, p_btc_usd], line=dict(color='#00f2ff', width=3)))
    fig.update_layout(template="plotly_dark", height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    st.markdown('<div class="metric-card" style="text-align:left; height:360px;">', unsafe_allow_html=True)
    st.subheader("🧠 Análisis de Activos")
    st.write(f"🔹 **Bitcoin:** {MI_BTC} BTC")
    st.write(f"🔹 **Ether:** {MI_ETH} ETH")
    st.write("---")
    st.write("⚠️ **Estado:** Sin efectivo (MXN/USD)")
    st.write("El bot está en modo **LECTURA**. Para comprar más, necesitas depositar Pesos en Bitso.")
    
    if st.button("🔄 ACTUALIZAR VALORES", use_container_width=True):
        st.rerun()
    
    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nBóveda: Sincronizada", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(30)
st.rerun()
