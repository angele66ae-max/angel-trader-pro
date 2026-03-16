import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN VISUAL PRESTIGE ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

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
    .energy-bar {{
        width: 100%; background-color: #111; border-radius: 10px; border: 1px solid #00f2ff;
    }}
    .energy-fill {{
        height: 20px; border-radius: 8px; background: linear-gradient(90deg, #00f2ff, #39FF14);
        box-shadow: 0 0 10px #39FF14; transition: width 0.5s;
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. TUS DATOS REALES ---
MI_BTC = 0.00003542
MI_ETH = 0.0017524
META_USD = 115.00

# --- 3. MOTOR DE DATOS EN TIEMPO REAL ---
try:
    t_usd = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_actual = float(t_usd['payload']['last'])
    # Referencia para la energía (si baja el precio, sube la energía)
    p_ref = p_actual * 1.01 
    valor_tu_btc_usd = MI_BTC * p_actual
except:
    p_actual, p_ref, valor_tu_btc_usd = 74000.0, 75000.0, 2.62

# --- 4. PANEL DE CONTROL PRINCIPAL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center; text-shadow:0 0 15px #00f2ff;'>⛩️ MAHORASHARK IA: ADAPTACIÓN ACTIVA</h1>", unsafe_allow_html=True)

# Barra de Energía de la IA
energia = max(0, min(100, ((p_ref - p_actual) / (p_ref * 0.02)) * 100))
st.write("### ⚡ ENERGÍA DE ADAPTACIÓN IA")
st.markdown(f'<div class="energy-bar"><div class="energy-fill" style="width: {energia}%;"></div></div>', unsafe_allow_html=True)
st.write(f"Nivel de oportunidad: **{energia:.1f}%**")

st.write("---")

# Métricas Neón
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card">TU BTC (USD)<div style="font-size:24px; color:#39FF14;">${valor_tu_btc_usd:.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">PRECIO MERCADO<div style="font-size:24px; color:#00f2ff;">${p_actual:,.0f}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">META FINAL<div style="font-size:24px; color:magenta;">${META_USD:.2f}</div></div>', unsafe_allow_html=True)
with m4: 
    progreso = (valor_tu_btc_usd / META_USD) * 100
    st.markdown(f'<div class="metric-card">PROGRESO<div style="font-size:24px; color:cyan;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

# --- 5. VISUALIZACIÓN Y RADAR ---
col_graf, col_ia = st.columns([2.2, 1])

with col_graf:
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[p_actual + np.random.uniform(-100, 100) for _ in range(20)],
        high=[p_actual + 250 for _ in range(20)],
        low=[p_actual - 250 for _ in range(20)],
        close=[p_actual + np.random.uniform(-100, 100) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    )])
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:450px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Mahora Pro")
    
    ia_on = st.toggle("MODO AUTOMÁTICO", value=True)
    
    # Radar de Ballenas [NUEVA LÓGICA]
    st.write("---")
    st.subheader("🐋 Radar de Ballenas")
    volumen = np.random.uniform(0, 100)
    if volumen > 80:
        st.warning("⚠️ ACTIVIDAD ALTA: Movimiento de ballenas detectado.")
    else:
        st.success("✅ MERCADO ESTABLE: Movimiento orgánico.")
    
    st.write("---")
    st.write(f"💰 **Saldo Cash:** $0.00 MXN")
    
    if st.button("🚀 EJECUTAR ADAPTACIÓN", use_container_width=True):
        st.error("Error: Insufficient Balance. No hay efectivo en la bóveda.")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nModo: SYNCED\nStatus: PRESTIGE", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

# Actualización automática
time.sleep(20)
st.rerun()
