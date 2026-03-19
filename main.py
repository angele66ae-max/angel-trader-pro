import streamlit as st
import requests
import pandas as pd
import numpy as np

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige")

# --- ESTILO CSS NEÓN ---
st.markdown("""
    <style>
    .stApp { background-color: #050a0e; color: white; }
    .metric-card {
        background-color: #0b141a;
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00f2ff33;
    }
    .metric-title { color: #ffffff; font-size: 11px; font-weight: bold; }
    .metric-value { color: #00f2ff; font-size: 26px; font-weight: bold; text-shadow: 0 0 8px #00f2ff; }
    .progress-bar {
        background-color: #1a262f;
        border-radius: 5px;
        margin-top: 10px;
    }
    .progress-fill {
        background: linear-gradient(90deg, #ff00ff, #00f2ff);
        height: 10px;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NEGOCIO ---
def obtener_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 0.0

precio_btc = obtener_bitso()
saldo_mxn = 47.12  # Tu saldo actual
meta_10k = 10000.0
progreso_porcentaje = (saldo_mxn / meta_10k) * 100
falta_dinero = meta_10k - saldo_mxn

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila de Métricas Superiores
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">PRECIO BTC (BITSO)</div><div class="metric-value">${precio_btc:,.0f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">SALDO ACTUAL</div><div class="metric-value" style="color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-card"><div class="metric-title">IA STATUS</div><div class="metric-value" style="color:#39FF14">ADAPTIVE</div></div>', unsafe_allow_html=True)
with c4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">PROGRESO META 10K</div><div class="metric-value">{progreso_porcentaje:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo Principal
col_main, col_ia = st.columns([2, 1])

with col_main:
    st.subheader("📊 Análisis de Mercado")
    # Gráfica estética
    chart_data = pd.DataFrame(np.random.randn(40, 1), columns=['Tendencia'])
    st.line_chart(chart_data, color="#ff00ff")
    
    # Barra de progreso visual hacia los 10k
    st.write(f"**Camino a la Meta: ${saldo_mxn} / $10,000.00**")
    st.markdown(f"""
        <div class="progress-bar">
            <div class="progress-fill" style="width: {min(progreso_porcentaje * 10, 100)}%;"></div>
        </div>
    """, unsafe_allow_html=True)

with col_ia:
    st.subheader("🧠 Cerebro Mahora")
    st.markdown(f"""
        <div style="border:2px solid #00f2ff; border-radius:10px; padding:20px; background:black; font-family:monospace;">
            <p style="color:#00f2ff;">
            [OBJETIVO]: $10,000.00<br>
            [RESTANTE]: ${falta_dinero:,.2f}<br>
            [ESTRATEGIA]: Acumulación Silenciosa<br><br>
            <span style="color:#39FF14;">>> IA esperando punto de entrada óptimo...</span>
            </p>
        </div>
    """, unsafe_allow_html=True)
