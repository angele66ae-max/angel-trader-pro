import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: white; }
    .metric-card {
        background-color: #0b141a;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 10px #00f2ff55;
    }
    .metric-title { color: #ffffff; font-size: 11px; font-weight: bold; text-transform: uppercase; }
    .metric-value { color: #00f2ff; font-size: 24px; font-weight: bold; text-shadow: 0 0 5px #00f2ff; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
def obtener_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 0.0

precio_btc = obtener_bitso()

# Valores de tu cuenta (Ajustables)
saldo_mxn = 47.12 
meta_objetivo = 10000.0
progreso = (saldo_mxn / meta_objetivo) * 100

# --- INTERFAZ PRESTIGE ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila de Métricas
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN BITSO</div><div class="metric-value">${precio_btc:,.0f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">SALDO ACTUAL</div><div class="metric-value" style="color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-title">ESTADO DE IA</div><div class="metric-value" style="color:#39FF14">HOLDING</div></div>', unsafe_allow_html=True)
with c4:
    # Aquí calculamos el progreso real hacia los 10k
    st.markdown(f'<div class="metric-card"><div class="metric-title">PROGRESO META 10K</div><div class="metric-value">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo
col_chart, col_ia = st.columns([2, 1])

with col_chart:
    st.subheader("Análisis de Tendencia (Meta $10,000)")
    chart_data = pd.DataFrame(np.random.randn(50, 1), columns=['Precio'])
    st.line_chart(chart_data, color="#00f2ff")

with col_ia:
    st.subheader("Cerebro Mahora")
    falta = meta_objetivo - saldo_mxn
    st.markdown(f"""
        <div style="height:250px; border:2px solid #ff00ff; border-radius:10px; padding:15px; background:black; font-family:monospace;">
            <p style="color:#ff00ff;">
            [ALGORITMO]: ACTIVE<br>
            [META]: $10,000.00 MXN<br>
            [RESTANTE]: ${falta:,.2f}<br><br>
            <span style="color:#39FF14;">>> IA analizando oportunidad de compra...</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
