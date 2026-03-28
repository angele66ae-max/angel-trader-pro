import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DE PODER ---
SALDO_REAL = 144.95
STOCKS = [
    {"n": "RENDER (IA)", "p": 124.50, "c": "+2.4%"},
    {"n": "APPLE", "p": 3450.00, "c": "-0.1%"},
    {"n": "SAND (Land)", "p": 8.92, "c": "-1.5%"},
    {"n": "GALA", "p": 0.85, "c": "+5.2%"},
    {"n": "BITCOIN", "p": 1800000.0, "c": "+0.8%"}
]

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA", page_icon="🦈")

# --- 2. EL MARTILLO: CSS PARA CLONAR LA IMAGEN ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&display=swap');
    
    /* Fondo total de la terminal */
    .stApp {{ background-color: #05080a; color: #8b949e; font-family: 'JetBrains Mono', monospace; }}
    
    /* Header compacto */
    .header-box {{ text-align: center; padding: 10px; border-bottom: 1px solid #1b1f23; margin-bottom: 20px; }}
    .title-small {{ font-size: 10px; letter-spacing: 2px; color: #58a6ff; }}
    .balance-main {{ font-size: 42px; color: #39FF14; font-weight: bold; text-shadow: 0 0 15px rgba(57, 255, 20, 0.4); }}

    /* Paneles de datos */
    .panel-label {{ font-size: 10px; color: #484f58; margin-bottom: 8px; text-transform: uppercase; }}
    .data-card {{ background: #0d1117; border: 1px solid #21262d; border-radius: 2px; padding: 10px; }}
    
    /* Filas de mercado */
    .stock-row {{ display: flex; justify-content: space-between; padding: 5px 0; border-bottom: 1px solid #1b1f23; font-size: 12px; }}
    .stock-price {{ color: #e6edf3; }}
    .stock-up {{ color: #39FF14; }}
    .stock-down {{ color: #f85149; }}

    /* Terminal de Logs */
    .log-line {{ font-size: 10px; color: #39FF14; margin-bottom: 2px; }}
    .hr-mini {{ border-top: 1px solid #21262d; margin: 10px 0; }}

    /* Quitar espacios de Streamlit */
    .block-container {{ padding-top: 1rem; padding-bottom: 0rem; }}
</style>
""", unsafe_allow_html=True)

# --- 3. ESTRUCTURA VISUAL (COPIA FIEL) ---

# HEADER
st.markdown(f"""
<div class="header-box">
    <div class="title-small">MAHORASHARK ALPHA V45.3 // TACTICAL GUADAÑA</div>
    <div class="balance-main">${SALDO_REAL:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# COLUMNAS
c1, c2, c3 = st.columns([1, 2.5, 1])

with c1:
    st.markdown('<div class="panel-label">MARKET ACCIONES</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        for s in STOCKS:
            color_class = "stock-up" if "+" in s['c'] else "stock-down"
            st.markdown(f"""
            <div class="stock-row">
                <div><b>{s['n']}</b><br><span class="stock-price">${s['p']:,}</span></div>
                <div class="{color_class}">{s['c']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('<div style="font-size:9px; margin-top:10px; color:#484f58;">STATUS: SCANNING...</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel-label">RADAR TÁCTICO (LIVE)</div>', unsafe_allow_html=True)
    try:
        # Datos reales de Bitso para que la gráfica se mueva de verdad
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=5).json()
        prices = [float(t['price']) for t in r['payload']][::-1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=prices, fill='tozeroy', line=dict(color='#00f2ff', width=2), fillcolor='rgba(0, 242, 255, 0.05)'))
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=400, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor='#1b1f23'
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("ERROR: RE-SYNCING RADAR...")

with c3:
    st.markdown('<div class="panel-label">ADAPTATION ENGINE</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="data-card">', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="log-line">[{datetime.now().strftime("%H:%M")}] ADAPT_FACTOR: 32</div>
        <div class="log-line">[{datetime.now().strftime("%H:%M")}] SYNC_OK: ${SALDO_REAL}</div>
        <div class="log-line">[{datetime.now().strftime("%H:%M")}] ENGINE: RUNNING</div>
        <div class="hr-mini"></div>
        <div style="font-size:10px; color:#8b949e; font-style:italic;">"Pavo, el código ya está limpio. El Ferrari está listo para correr."</div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('<br><div class="panel-label">TERMINAL DE COMANDO</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="data-card" style="border-color:#39FF14;">
        <div class="log-line">>> ESTRUCTURA ADAPTADA ✅</div>
        <div class="log-line">>> HIERRO MARTILLADO ✅</div>
        <div class="log-line" style="color:#58a6ff;">>> ESPERANDO CAZA...</div>
    </div>
    """, unsafe_allow_html=True)

# Recarga automática rápida
time.sleep(10)
st.rerun()
