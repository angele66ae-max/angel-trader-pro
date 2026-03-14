import streamlit as st
import pandas as pd
import numpy as np
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="SHARK AI: PRESTIGE CENTER")

# --- SISTEMA DE FONDO Y ESTILO ---
# He usado una técnica de CSS para asegurar que el fondo cósmico cubra toda la pantalla
fondo_url = "https://i.postimg.cc/g0K6y469/image-25526f.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), 
                    url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Contenedores estilo "Prestige" */
    .prestige-card {{
        background-color: rgba(17, 20, 24, 0.85);
        border: 1px solid rgba(0, 255, 255, 0.2);
        border-radius: 10px;
        padding: 20px;
        backdrop-filter: blur(10px);
    }}
    
    .stMetric {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 5px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.markdown("<h1 style='text-align: center; color: #e0e0e0; font-family: monospace;'>SHARK AI: PRESTIGE CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #00ffcc;'>MAHORA ADAPTATION PROTOCOL v19.3</p>", unsafe_allow_html=True)

# --- PANEL SUPERIOR: MÉTRICAS ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.metric("MERCADO DE BTC (REAL)", "$70,705", "USD")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.metric("SALDO DISPONIBLE (REAL)", "$2.81", "USD")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.metric("ESTADO DEL PROTOCOLO", "ADAPTANDO", "v22.0 CORE")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # Barra de meta SUV al 90.2%
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.write("OBJETIVO SUV")
    st.subheader("90.2%")
    st.progress(0.902)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # Espaciador

# --- CUERPO PRINCIPAL: GRÁFICAS Y LOGS ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    # Selector para incluir acciones
    tipo_activo = st.radio("SELECCIONAR MERCADO:", ["BTC (Cripto)", "AAPL (Acciones)"], horizontal=True)
    
    if tipo_activo == "BTC (Cripto)":
        st.subheader("Live Analysis - BTC")
        chart_data = pd.DataFrame(np.random.randn(20, 1) + 70705, columns=['Price'])
        st.area_chart(chart_data, color="#008080")
    else:
        st.subheader("Live Analysis - AAPL")
        # Simulación de acciones
        chart_data = pd.DataFrame(np.random.randn(20, 1) + 175, columns=['Price'])
        st.area_chart(chart_data, color="#ff00ff")
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="prestige-card" style="height: 450px;">', unsafe_allow_html=True)
    st.write("🕵️ PENSAMIENTOS DE LA IA")
    
    if st.button("🚀 DEPLOY AI"):
        st.success("Adaptación iniciada...")
    
    # Consola de Logs corregida
    st.code(f"""
[07:19:00] SISTEMA INICIADO.
OPERADOR: MAHORASHARK
[ADAPTACIÓN]: Escaneando {tipo_activo}...
[OBJETIVO]: Venta en 115 detectada.
    """, language="bash")
    st.markdown('</div>', unsafe_allow_html=True)
