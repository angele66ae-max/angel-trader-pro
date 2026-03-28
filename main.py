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

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA")

# --- 2. ESTILO TÁCTICO (CORREGIDO) ---
st.markdown("""
<style>
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .main { background-color: #000000 !important; }
    .block-container { padding: 10px !important; }
    * { color: #39FF14 !important; font-family: 'Consolas', monospace !important; }
    .header-box { text-align: center; border-bottom: 1px solid #111; padding: 15px; }
    .balance-neon { font-size: 50px; font-weight: bold; text-shadow: 0 0 15px #39FF14; }
    .panel-label { font-size: 10px; color: #444 !important; text-transform: uppercase; border-bottom: 1px solid #111; }
    .asset-row { display: flex; justify-content: space-between; font-size: 12px; padding: 4px 0; }
</style>
""", unsafe_allow_html=True)

# --- 3. ESTRUCTURA VISUAL ---

# HEADER
st.markdown(f"""
<div class="header-box">
    <div style="font-size:10px; color:#222 !important; letter-spacing:3px;">MAHORASHARK // V45.7</div>
    <div class="balance-neon">${SALDO_REAL:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# COLUMNAS
c1, c2, c3 = st.columns([1, 2.5, 1])

with c1:
    st.markdown('<div class="panel-label">MARKET_MONITOR</div>', unsafe_allow_html=True)
    for s in STOCKS:
        color = "#39FF14" if "+" in s['c'] else "#f00"
        st.markdown(f"""
        <div class="asset-row">
            <span>{s['n']}</span>
            <span style="color:#fff !important;">${s['p']:,}</span>
            <span style="color:{color} !important;">{s['c']}</span>
        </div>
        """, unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel-label">RADAR_TACTICO</div>', unsafe_allow_html=True)
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        px = [float(t['price']) for t in r['payload']][::-1]
        fig = go.Figure(go.Scatter(y=px, fill='tozeroy', line=dict(color='#00f2ff', width=2), fillcolor='rgba(0, 242, 255, 0.02)'))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450, margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False, yaxis_side="right", yaxis_gridcolor="#050505")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.markdown('<div style="color:red !important;">OFFLINE</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="panel-label">MAHORAGA_LOGS</div>', unsafe_allow_html=True)
    now = datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div style="font-size:11px;">
        <span style="color:#00f2ff !important;">[{now}]</span> ADAPT_STEP: 32<br>
        <span style="color:#00f2ff !important;">[{now}]</span> SYNC: OK<br>
        <br>
        <div style="color:#444 !important;">"El Ferrari está listo para correr."</div>
        <br>
        >> ESTRUCTURA ADAPTADA ✅<br>
        >> HIERRO MARTILLADO ✅<br>
    </div>
    """, unsafe_allow_html=True)

# REFRESH
time.sleep(10)
st.rerun()
