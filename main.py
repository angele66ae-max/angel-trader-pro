import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title="MahoraShark Prestige", page_icon="⛩️")

# --- 2. ESTILO PRESTIGE (GOTAS + NEÓN) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DATOS ---
activo_actual = st.sidebar.selectbox("🏎️ PISTA", ["btc_mxn", "eth_mxn", "usd_mxn"])
precio = 1258990.00  # Valor de tu captura
saldo = 68.91       # Tu saldo real

# --- 4. ESTRUCTURA (AQUÍ SE DEFINE C_SIDE) ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# Definimos las columnas primero para evitar el NameError
c_main, c_side = st.columns([2.5, 1])

with c_main:
    # Gráfica de Velas Neón
    fig = go.Figure(data=[go.Candlestick(
        open=[precio]*40, high=[precio*1.01]*40, low=[precio*0.99]*40, close=[precio]*40,
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # Velocímetro RSI (Rosa/Cian como en la foto)
    st.markdown("### INDICADORES CUANTITATIVOS")
    fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=42, 
        gauge={'axis':{'range':[0,100]}, 'bar':{'color':'#00f2ff'}, 
               'steps':[{'range':[0,30],'color':'#ff00ff'},{'range':[70,100],'color':'#ff00ff'}]}))
    fig_rsi.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig_rsi, use_container_width=True)

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v8.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> ACTIVADO: {activo_actual.upper()}<br>
                [{ahora}] >> STATUS: SCANNIG...<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, estoy vigilando el mercado. No hay errores, el Ferrari está en la pista. 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.number_input("Monto MXN", value=20.0)
    st.button("🚀 COMPRAR")

time.sleep(10)
st.rerun()
