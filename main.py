import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
SALDO_REAL = 144.95
STOCKS = [
    {"n": "RENDER", "p": 124.50, "c": "+2.4%"},
    {"n": "APPLE", "p": 3450.00, "c": "-0.1%"},
    {"n": "SAND", "p": 8.92, "c": "-1.5%"},
    {"n": "GALA", "p": 0.85, "c": "+5.2%"},
    {"n": "BTC", "p": 1800000.0, "c": "+0.8%"}
]

st.set_page_config(layout="wide", page_title="MAHORASHARK")

# --- 2. EL MARTILLO DEFINITIVO (CSS TOTAL) ---
st.markdown("""
<style>
    /* MATAR TODO EL DISEÑO DE STREAMLIT */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {display: none !important;}
    .main { background-color: #000000 !important; }
    .block-container { padding: 10px !important; max-width: 100% !important; }
    
    /* Fuente y Colores */
    * { color: #39FF14 !important; font-family: 'Consolas', 'Monaco', monospace !important; }
    
    /* Header del Balance */
    .header-center { text-align: center; border-bottom: 1px solid #111; padding-bottom: 15px; margin-bottom: 15px; }
    .balance-val { font-size: 55px; font-weight: 900; text-shadow: 0 0 20px #39FF14; }
    .sub-label { font-size: 9px; color: #444 !important; letter-spacing: 4px; }

    /* Paneles Estilo Militar */
    .panel-title { font-size: 10px; color: #222 !important; border-bottom: 1px solid #111; margin-bottom: 8px; }
    .asset-box { font-size: 12px; margin-bottom: 4px; display: flex; justify-content: space-between; }
    .white-txt { color: #fff !important; }
    
    /* Logs de Mahoraga */
    .log-line { font-size: 10px; line-height: 1.1; margin-bottom: 2px; }
    .cyan-txt { color: #00f2ff !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. INTERFAZ TÁCTICA ---

# BALANCE CENTRAL
st.markdown(f"""
<div class="header-center">
    <div class="sub-label">MAHORASHARK // V45.5 // ALPHA COMMAND</div>
    <div class="balance-val">${SALDO_REAL:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# COLUMNAS (Estrechas para que no haya huecos)
c1, c2, c3 = st.columns([1, 3, 1])

with c1:
    st.markdown('<div class="panel-title">MARKET_MONITOR</div>', unsafe_allow_html=True)
    for s in STOCKS:
        c_color = "#39FF14" if "+" in s['c'] else "#f00"
        st.markdown(f"""
        <div class="asset-box">
            <span>{s['n']}</span>
            <span class="white-txt">${s['p']:,}</span>
            <span style="color:{c_color} !important;">{s['c']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<br><div style="font-size:9px; color:#111 !important;">>> REFRESHING_DATA...</div>', unsafe_allow_html=True)

with c2:
    # Gráfica de Radar pura sin basura
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        px = [float(t['price']) for t in r['payload']][::-1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=px, fill='tozeroy', line=dict(color='#00f2ff', width=1.5), fillcolor='rgba(0, 242, 255, 0.03)'))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=480, margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(visible=False),
            yaxis=dict(side="right", gridcolor="#050505", tickfont=dict(size=9, color="#111"))
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.markdown('<div style="color:red !important;">SYSTEM_OFFLINE</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="panel-title">MAHORAGA_ENGINE</div>', unsafe_allow_html=True)
    now = datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="log-line"><span class="cyan-txt">[{now}]</span> ADAPT_ACTIVE: 32</div>
    <div class="log-line"><span class="cyan-txt">[{now}]</span> SYNC_MXN: OK</div>
    <div class="log-line"><span class="cyan-txt">[{now}]</span> RADAR: SCANNING</div>
    <br>
    <div class="log-line" style="color:#666 !important;">"El Ferrari está listo para correr."</div>
    <br>
    <div class="log-line">>> ESTRUCTURA ADAPTADA ✅</div>
    <div class="log-line">>> HIERRO MARTILLADO ✅</div>
    <div style="font-size:9px; color:#111 !important; margin-top:20px;">>> WAIT_FOR_ORDER...</div>
    """, unsafe_allow_html=True)

# REFRESH AUTOMÁTICO
time.sleep(10)
st.rerun()
