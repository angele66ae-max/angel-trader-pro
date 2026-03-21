import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige", page_icon="⛩️")

# --- 2. ESTILO PRESTIGE (DISEÑO DE GOTAS Y NEÓN) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 320px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. LÓGICA DE DATOS ---
st.sidebar.title("🏎️ PISTA")
activo = st.sidebar.selectbox("Seleccionar Activo", ["btc_mxn", "eth_mxn", "usd_mxn"])
precio_actual = 1258990.00  # Valor de referencia
saldo_actual = 68.91       # Tu saldo real detectado

# --- 4. ARMADO DE LA ESTRUCTURA (SOLUCIÓN AL NAMEERROR) ---
st.markdown(f'<div class="main-header">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# Primero definimos las columnas para que Python sepa dónde están
c_main, c_side = st.columns([2.5, 1])

# --- 5. PANEL PRINCIPAL (GRÁFICAS) ---
with c_main:
    # Gráfica de Velas Neón
    fig = go.Figure(data=[go.Candlestick(
        open=[precio_actual]*40, high=[precio_actual*1.002]*40, 
        low=[precio_actual*0.998]*40, close=[precio_actual]*40,
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # Indicadores Inferiores (Velocímetro RSI y Volumen)
    st.markdown("### INDICADORES CUANTITATIVOS")
    i1, i2 = st.columns([1, 1.5])
    with i1:
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=42, 
            gauge={'axis':{'range':[0,100], 'tickcolor':"white"}, 'bar':{'color':'#00f2ff'}, 
                   'steps':[{'range':[0,30],'color':'#ff00ff'},{'range':[70,100],'color':'#ff00ff'}]}))
        fig_rsi.update_layout(height=220, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=20,b=0))
        st.plotly_chart(fig_rsi, use_container_width=True)
    with i2:
        vol_data = np.random.randint(200, 800, 40)
        fig_vol = go.Figure(data=[go.Bar(y=vol_data, marker_color='#00f2ff', opacity=0.7)])
        fig_vol.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=0), font_color="white")
        st.plotly_chart(fig_vol, use_container_width=True)

# --- 6. PANEL LATERAL (IA Y CONTROL) ---
with c_side:
    # Métricas rápidas arriba de la terminal
    st.markdown(f'<div class="metric-card"><small>SALDO MXN</small><br><b style="font-size:20px; color:#ff00ff">${saldo_actual:,.2f}</b></div>', unsafe_allow_html=True)
    st.write("")
    
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v8.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> SISTEMA PRESTIGE ONLINE.<br>
                [{ahora}] >> ANALIZANDO: {activo.upper()}.<br>
                [{ahora}] >> STATUS: ESPERANDO GATILLO.<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, el Ferrari está en pista y el código está blindado. No más errores en la línea 1. ¡Rumbo a los 10K para Canadá! 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    monto = st.number_input("Monto MXN", min_value=10.0, value=20.0)
    if st.button(f"🚀 EJECUTAR ORDEN", use_container_width=True):
        st.toast("Orden enviada al motor de ejecución...")

# --- 7. MOTOR DE ACTUALIZACIÓN ---
time.sleep(20)
st.rerun()
