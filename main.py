import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. ESTÉTICA PRESTIGE RECUPERADA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK IA")

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
META_USD = 115.00

# --- 3. MOTOR DE DATOS ---
try:
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    p_actual = float(ticker['payload']['last'])
    # Simulamos un precio de referencia para la barra de energía (precio promedio de hoy)
    p_referencia = p_actual * 1.02 
    valor_usd = MI_BTC * p_actual
except:
    p_actual, p_referencia, valor_usd = 74000.0, 75500.0, 2.57

# --- 4. PANEL PRINCIPAL ---
st.markdown("<h1 style='color:#00f2ff; text-align:center;'>⛩️ MAHORASHARK IA: ADAPTACIÓN ACTIVA</h1>", unsafe_allow_html=True)

# Barra de Energía (IA)
# Mientras más bajo el precio comparado con la referencia, más energía tiene la IA para comprar
energia = max(0, min(100, ((p_referencia - p_actual) / (p_referencia * 0.05)) * 100))

st.write("### ⚡ ENERGÍA DE ADAPTACIÓN IA")
st.markdown(f"""
    <div class="energy-bar">
        <div class="energy-fill" style="width: {energia}%;"></div>
    </div>
""", unsafe_allow_html=True)
st.write(f"Nivel de oportunidad: **{energia:.1f}%**")

st.write("---")

m1, m2, m3 = st.columns(3)
with m1: st.markdown(f'<div class="metric-card">VALOR ACTUAL<div style="font-size:24px; color:#39FF14;">${valor_usd:.2f} USD</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">PRECIO BTC<div style="font-size:24px; color:#00f2ff;">${p_actual:,.1f}</div></div>', unsafe_allow_html=True)
with m3: 
    progreso = (valor_usd / META_USD) * 100
    st.markdown(f'<div class="metric-card">PROGRESO META<div style="font-size:24px; color:magenta;">{progreso:.3f}%</div></div>', unsafe_allow_html=True)

# --- 5. CONTROL DE IA ---
col_graf, col_ia = st.columns([2, 1])

with col_graf:
    # Gráfica de Velas
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=15, freq='min'),
        open=[p_actual + np.random.uniform(-100, 100) for _ in range(15)],
        high=[p_actual + 200 for _ in range(15)],
        low=[p_actual - 200 for _ in range(15)],
        close=[p_actual + np.random.uniform(-100, 100) for _ in range(15)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta'
    )])
    fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:400px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Mahora Pro")
    
    ia_on = st.toggle("ACTIVAR IA AUTOMÁTICA", value=True)
    
    if ia_on:
        if energia > 70:
            st.success("🎯 IA: ENERGÍA MÁXIMA. LISTO PARA COMPRAR.")
        else:
            st.info("🔄 IA: MONITOREANDO... ESPERANDO CAÍDA.")
    
    st.write("---")
    st.write("💰 **Balance disponible:** $0.00 MXN")
    st.warning("⚠️ Sin fondos para compra real.")
    
    if st.button("🚀 FORZAR ADAPTACIÓN", use_container_width=True):
        st.error("Error: Insufficient Balance. No hay Pesos en la bóveda.")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nModo: IA_SYNC", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(15)
st.rerun()
