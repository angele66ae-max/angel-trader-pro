import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. ADN DE LA GUADAÑA ---
SALDO_REAL = 144.95 # Sincronizado con tu imagen real
STOCKS = [
    {"n": "RENDER", "p": 124.50, "c": "+2.4%"},
    {"n": "APPLE", "p": 3450.00, "c": "-0.1%"},
    {"n": "SAND", "p": 8.92, "c": "-1.5%"},
    {"n": "GALA", "p": 0.85, "c": "+5.2%"},
    {"n": "BTC", "p": 1800000.0, "c": "+0.8%"}
]

st.set_page_config(layout="wide", page_title="MAHORASHARK", page_icon="🦈")

# --- 2. EL HACK VISUAL (PARA QUE SEA IDÉNTICA) ---
st.markdown("""
<style>
    /* Forzar fondo negro total y ocultar basura de Streamlit */
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #000000 !important; color: #39FF14 !important; font-family: 'Courier New', Courier, monospace !important; }
    
    /* Contenedor principal */
    .main-terminal { padding: 10px; border: 1px solid #111; }
    
    /* Balance central gigante neón */
    .balance-box { text-align: center; margin-bottom: 20px; border-bottom: 1px solid #111; padding-bottom: 10px; }
    .balance-text { font-size: 50px; font-weight: bold; color: #39FF14; text-shadow: 0 0 20px #39FF14; }
    .tagline { font-size: 10px; color: #444; letter-spacing: 3px; }

    /* Estilo de los paneles laterales */
    .panel-header { font-size: 11px; color: #555; margin-bottom: 5px; border-bottom: 1px solid #222; }
    .asset-item { display: flex; justify-content: space-between; font-size: 13px; padding: 4px 0; border-bottom: 1px solid #111; }
    .price-text { color: #fff; }
    
    /* Terminal de Logs */
    .log-text { font-size: 10px; color: #39FF14; line-height: 1.1; }
    .log-blue { color: #00f2ff; }
    
    /* Quitar padding de columnas */
    [data-testid="column"] { padding: 0 5px !important; }
</style>
""", unsafe_allow_html=True)

# --- 3. ESTRUCTURA DE LA TERMINAL ---

# Header: Balance Central
st.markdown(f"""
<div class="balance-box">
    <div class="tagline">MAHORASHARK ALPHA V45.4 // TACTICAL INTERFACE</div>
    <div class="balance-text">${SALDO_REAL:,.2f}</div>
</div>
""", unsafe_allow_html=True)

# Cuerpo: 3 Columnas
c1, c2, c3 = st.columns([1, 2.8, 1])

with c1:
    st.markdown('<div class="panel-header">MARKET ACCIONES</div>', unsafe_allow_html=True)
    for s in STOCKS:
        change_color = "#39FF14" if "+" in s['c'] else "#f00"
        st.markdown(f"""
        <div class="asset-item">
            <span>{s['n']}</span>
            <span class="price-text">${s['p']:,}</span>
            <span style="color:{change_color}">{s['c']}</span>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('<div style="font-size:9px; color:#222; margin-top:20px;">>> SCANNING_SECTORS...</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel-header">RADAR TÁCTICO DE MOVIMIENTO</div>', unsafe_allow_html=True)
    try:
        # Petición real para que se mueva
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        prices = [float(t['price']) for t in r['payload']][::-1]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=prices, fill='tozeroy', line=dict(color='#00f2ff', width=2), fillcolor='rgba(0, 242, 255, 0.05)'))
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor='#111', yaxis_tickfont=dict(color='#333', size=10)
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.markdown('<div style="color:red;">!! RADAR_SYNC_ERROR !!</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="panel-header">ADAPTATION ENGINE</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="log-text">
        <span class="log-blue">[{datetime.now().strftime("%H:%M")}]</span> ADAPT_STEP: 32/32<br>
        <span class="log-blue">[{datetime.now().strftime("%H:%M")}]</span> STATUS: OPTIMIZED<br>
        <span class="log-blue">[{datetime.now().strftime("%H:%M")}]</span> TARGET: 10K MXN<br>
        <br>
        "El Ferrari está listo para correr."<br>
        <br>
        >> ESTRUCTURA ADAPTADA ✅<br>
        >> HIERRO MARTILLADO ✅<br>
        <br>
        <span style="color:#222">>> ESPERANDO_ORDEN...</span>
    </div>
    """, unsafe_allow_html=True)

# Autorefresco para que sea dinámica
time.sleep(10)
st.rerun()
