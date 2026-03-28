import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. SETTINGS DE LA GUADAÑA ---
SALDO_REAL = 142.00  # Según tu descripción del Header
SESSION_PL = 12.50
PL_PERCENT = 8.8
FACTOR = 32

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45")

# --- 2. EL MOTOR VISUAL (CSS CYBERPUNK) ---
st.markdown(f"""
<style>
    /* Fondo Azul Muy Oscuro (Cyberpunk Mode) */
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #030a12 !important; color: #e6edf3 !important; font-family: 'Inter', sans-serif; }}
    
    /* Barra Superior (Header) */
    .header-bar {{
        display: flex; justify-content: space-between; align-items: center;
        background-color: #000; padding: 10px 20px; border-bottom: 2px solid #00f2ff;
    }}
    .header-brand {{ color: #fff; font-weight: bold; font-size: 18px; }}
    .header-balance {{ color: #39FF14; font-size: 26px; font-weight: bold; text-shadow: 0 0 10px #39FF14; }}
    .status-tag {{ background: #1a2a1a; color: #39FF14; border: 1px solid #39FF14; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; }}

    /* Paneles con borde Cian */
    .panel-box {{ border: 1px solid #00f2ff; background: rgba(0, 242, 255, 0.02); padding: 10px; border-radius: 2px; margin-bottom: 10px; }}
    .panel-title {{ font-size: 11px; color: #00f2ff; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px; }}
    
    /* Botonera de Activos */
    .asset-btn {{ 
        background: #0d1117; border: 1px solid #00f2ff; color: #00f2ff; 
        padding: 5px; text-align: center; margin: 2px; font-size: 11px; cursor: pointer;
    }}
    .asset-active {{ background: #00f2ff; color: #000; font-weight: bold; }}

    /* Terminal y Logs */
    .terminal-log {{ font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #00f2ff; line-height: 1.2; }}
    .log-ok {{ color: #39FF14; font-weight: bold; }}
    
    /* Rueda de Adaptación (Animación) */
    .adapt-wheel {{ 
        width: 120px; height: 120px; border-radius: 50%; border: 4px double #ab7df8;
        display: flex; align-items: center; justify-content: center;
        margin: 0 auto; animation: spin 10s linear infinite;
        box-shadow: 0 0 20px rgba(171, 125, 248, 0.3);
    }}
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="header-bar">
    <div>
        <span class="header-brand">🦈 MAHORASHARK ALPHA V45</span><br>
        <span style="font-size:10px; color:#8b949e;">TACTICAL TRADING GUADAÑA | SHARK HUD</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:10px; color:#fff;">MXN BALANCE:</span><br>
        <span class="header-balance">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:5px;">
        <span class="status-tag">LIVE</span>
        <span class="status-tag">ONLINE</span>
        <span class="status-tag" style="border-color:#00f2ff; color:#00f2ff;">FACTOR: {FACTOR}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. ESTRUCTURA DE 3 PANELES ---
col_left, col_mid, col_right = st.columns([1, 2.5, 1])

# PANEL IZQUIERDO: SELECCIÓN DE ACTIVOS
with col_left:
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">MARKET ACCIONES</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:10px; color:#fff;">SELECTED ASSET: <span style="color:#00f2ff;">RENDER (IA)</span></div>', unsafe_allow_html=True)
    
    # Cuadrícula de botones (clonada de tu descripción)
    btns = ["RENDER", "APPLE", "SAND", "GALA", "BERM", "OTHERS", "SPLI", "RWIH"]
    cols_btns = st.columns(2)
    for i, b in enumerate(btns):
        with cols_btns[i % 2]:
            st.markdown(f'<div class="asset-btn {"asset-active" if b=="RENDER" else ""}">{b}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# PANEL CENTRAL: GRÁFICO DE VELAS CIAN/PÚRPURA
with col_mid:
    st.markdown('<div class="panel-box" style="height:550px;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">CANDLE CHART: RENDER (IA) - 1D</div>', unsafe_allow_html=True)
    
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        df = pd.DataFrame(r['payload'])
        df['price'] = df['price'].astype(float)
        
        # Velas Cian (Subida) y Púrpura (Bajada) según tu descripción
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['price'], high=df['price']*1.001,
            low=df['price']*0.999, close=df['price'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ab7df8',
            increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ab7df8'
        )])
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=450, margin=dict(l=0, r=40, t=0, b=0), xaxis_visible=False, yaxis_side="right"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("RADAR SYNC ERROR")
    st.markdown('</div>', unsafe_allow_html=True)

# PANEL DERECHO: MOTOR Y TERMINAL
with col_right:
    # ADAPTATION ENGINE
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">ADAPTATION ENGINE (MAHORAGA 32)</div>', unsafe_allow_html=True)
    st.markdown('<div class="adapt-wheel"><span style="font-size:24px; color:#00f2ff;">☸</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # P/L TRACKER
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">PROFIT/LOSS TRACKER</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:20px; color:#39FF14; font-weight:bold;">SESSION P/L: +${SESSION_PL:,.2f} (+{PL_PERCENT}%)</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TERMINAL LOGS (CLON EXACTO DE TUS TEXTOS)
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">TERMINAL</div>', unsafe_allow_html=True)
    log_time = datetime.now().strftime("%H:%M")
    logs = [
        f"[LOG {log_time}] Adapt Check (Factor 32) ... <span class='log-ok'>OK</span>",
        f"[LOG {log_time}] Render selected ... <span class='log-ok'>OK</span>",
        f"[LOG {log_time}] RENDER selected ... <span class='log-ok'>Data Loaded</span>"
    ]
    for l in logs:
        st.markdown(f'<div class="terminal-log">{l}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# FOOTER WATERMARK
st.markdown('<div style="text-align:right; font-size:8px; color:#444;">MADE IN USA - 2024</div>', unsafe_allow_html=True)

# REFRESH DINÁMICO
time.sleep(10)
st.rerun()
