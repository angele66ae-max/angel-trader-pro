import streamlit as st
import pandas as pd
import numpy as np
import time
import requests
import hashlib
import hmac

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="SHARK AI: PRESTIGE CENTER")

# URL DIRECTA DEL FONDO CÓSMICO (Rueda Mahora)
# He usado una URL que garantiza que la imagen cargue como fondo
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

# --- SISTEMA DE FONDO Y ESTILO ---
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.4)), 
                    url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    
    /* Contenedores estilo "Prestige" Táctico */
    .prestige-card {{
        background-color: rgba(17, 20, 24, 0.85);
        border: 2px solid rgba(0, 242, 255, 0.2);
        border-radius: 12px;
        padding: 22px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 15px rgba(0,242,255,0.1);
    }}
    
    .stMetric {{
        background-color: rgba(0, 0, 0, 0.5);
        padding: 10px;
        border-radius: 8px;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HEADER TÁCTICO ---
st.markdown("<h1 style='text-align: center; color: #00f2ff; font-family: sans-serif; text-shadow: 0 0 10px #00f2ff;'>MAHORASHARK: PRESTIGE CENTER</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #e0e0e0; font-family: monospace;'>MAHORA ADAPTATION PROTOCOL v23.0</p>", unsafe_allow_html=True)

# --- PANEL SUPERIOR: MÉTRICAS (Tal cual la captura) ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.metric("MERCADO DE BTC (REAL)", "$70,961", delta="USD")
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.metric("SALDO DISPONIBLE (REAL)", "$2.81", delta="USD")
    st.markdown('</div>', unsafe_allow_html=True)

with col3:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.metric("MOTOR IA", "v10.1 CORE", delta="OPTIMIZADO", delta_color="normal")
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    # Barra de meta SUV al 90.2%
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    st.write("META SUV")
    st.subheader("90.2%")
    st.progress(0.902)
    st.markdown('</div>', unsafe_allow_html=True)

st.write("") # Espaciador

# --- CUERPO PRINCIPAL: GRÁFICAS MULTI-ACTIVO ---
c_left, c_right = st.columns([2, 1])

with c_left:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    
    # Selector de activos Multi-Mercado
    tab1, tab2 = st.tabs(["Cripto (BTC)", "Acciones (Simulado)"])
    
    with tab1:
        st.subheader("Live Analysis - BTC")
        # Gráfica corregida de Pandas/Numpy
        df_chart = pd.DataFrame(np.random.randn(20, 1) + 70961, columns=['Price'])
        st.area_chart(df_chart, color="#008080")
        
    with tab2:
        st.subheader("Live Analysis - Acciones Multi-Mercado")
        st.info("PROTOCOL ADAPTATION INITIATED: Conectando con mercado de acciones... RSI: Adaptando.")
    st.markdown('</div>', unsafe_allow_html=True)

with c_right:
    st.markdown('<div class="prestige-card">', unsafe_allow_html=True)
    # Solución al error de sintaxis de st.markdown
    st.markdown('<p style="font-size:18px;">🕵️ LOGS DE OPERACIÓN</p>', unsafe_allow_html=True)
    
    if st.button("🚀 DEPLOY AI"):
        st.success("Adaptación iniciada...")
    
    # Consola de trading blindada
    st.code(f"""
[12:30:15] SISTEMA INICIADO.
OPERADOR: MAHORASHARK
[ADAPTACIÓN]: Escaneando volatilidad...
[MERCADO]: Objetivo de venta fijado en 115.
    """, language="bash")
    st.markdown('</div>', unsafe_allow_html=True)
