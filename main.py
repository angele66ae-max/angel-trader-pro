import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige")

# --- ESTILO CSS CUSTOM (NEÓN/CYBERPUNK) ---
st.markdown("""
    <style>
    /* Fondo general */
    .stApp {
        background-color: #050a0e;
        color: white;
    }
    /* Contenedores de métricas */
    .metric-card {
        background-color: #0b141a;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        text-align: left;
        box-shadow: 0 0 10px #00f2ff55;
    }
    .metric-title {
        color: #ffffff;
        font-size: 12px;
        font-weight: bold;
        margin-bottom: 5px;
    }
    .metric-value {
        color: #00f2ff;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 0 0 5px #00f2ff;
    }
    .gain-value {
        color: #ff00ff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- FUNCIÓN DE DATOS ---
def obtener_datos_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except:
        return 0.0

precio_btc = obtener_bitso()

# --- INTERFAZ TIPO PRESTIGE CENTER ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior de Métricas
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN BITSO</div><div class="metric-value">${precio_btc:,.1f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown('<div class="metric-card"><div class="metric-title">BALANCE REAL</div><div class="metric-value" style="color:#ff00ff">$2.81</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-title">GANANCIA LÍQUIDA</div><div class="metric-value" style="color:#39FF14">+$0.01520</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-card"><div class="metric-title">META 10K</div><div class="metric-value">0.0281%</div></div>', unsafe_allow_html=True)

st.write("") # Espaciador

# Cuerpo Principal (Gráfica y Cuentas)
col_info, col_chart, col_ia = st.columns([1, 2, 1])

with col_info:
    st.subheader("Tu Cuenta")
    st.write(f"**Bitcoin (BTC)** \n ### 0.000039")
    st.write(f"**Pesos (MXN)** \n ### $47.12")
    st.write(f"**Dólares (USD)** \n ### $2.81")

with col_chart:
    st.subheader("Gráfica de Velas Japonesas (Profesional)")
    # Simulamos datos para la gráfica visual
    chart_data = pd.DataFrame(np.random.randn(30, 1), columns=['Precio'])
    st.line_chart(chart_data, color="#ff00ff")

with col_ia:
    st.subheader("Cerebro Mahora")
    st.markdown("""
        <div style="height:300px; border:2px solid #00f2ff; border-radius:10px; padding:10px; background:black;">
            <p style="color:#00f2ff; font-family:monospace;">[SISTEMA]: ACTIVO<br>[IA]: Escaneando Bitso...<br>[META]: $115.00</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("🚀 ACTIVAR COMPRA/VENTA REAL"):
        st.warning("Función en desarrollo...")
