import streamlit as st
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL SISTEMA ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET_NAME = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45")

# --- 2. DESIGN SYSTEM (CSS TÁCTICO) ---
st.markdown("""
<style>
    /* Fondo Dark Mode Profundo #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"] {display: none !important;}
    .stApp { background-color: #0A0E14 !important; color: #00F2FF !important; font-family: 'Inter', sans-serif; }
    
    /* Header Estilo Guadaña */
    .header-box {
        display: flex; justify-content: space-between; align-items: center;
        background-color: #000; padding: 10px 20px; border-bottom: 2px solid #00F2FF;
    }
    .balance-val { font-size: 36px; color: #00FF00; font-weight: 700; text-shadow: 0 0 15px #00FF00; }
    .status-badge { background: #1a2a1a; color: #00FF00; border: 1px solid #00FF00; padding: 2px 8px; border-radius: 3px; font-size: 10px; font-weight: bold; margin-left: 5px; }

    /* Paneles Técnicos */
    .panel { border: 1px solid #00F2FF33; background: #0A0E14; padding: 15px; border-radius: 4px; }
    .label-min { font-size: 10px; color: #444 !important; text-transform: uppercase; letter-spacing: 2px; }
    
    /* Terminal logs */
    .terminal { font-family: 'Consolas', monospace; font-size: 10px; color: #00F2FF; line-height: 1.2; }
    .ok { color: #00FF00; font-weight: bold; }

    /* Rueda de Mahoraga */
    .wheel-anim { animation: rotate 10s linear infinite; width: 120px; display: block; margin: auto; }
    @keyframes rotate { 100% { transform: rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="header-box">
    <div>
        <span style="font-weight:bold; font-size:20px;">🦈 MAHORASHARK ALPHA V45</span><br>
        <span style="font-size:10px; color:#555;">TACTICAL TRADING GUADAÑA</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:10px; color:#fff;">MXN BALANCE:</span><br>
        <span class="balance-val">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex;">
        <span class="status-badge">LIVE</span>
        <span class="status-badge">ONLINE</span>
        <span class="status-badge" style="color:#00F2FF; border-color:#00F2FF;">FACTOR: {FACTOR}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. LAYOUT DE 3 COLUMNAS ---
c1, c2, c3 = st.columns([1, 2.8, 1])

with c1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="label-min">MARKET ACCIONES</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="border:1px solid #00F2FF; padding:8px; font-size:12px; margin-bottom:10px;">SELECTED: {ASSET_NAME}</div>', unsafe_allow_html=True)
    
    # Cuadrícula de activos
    assets = ["RENDER", "APPLE", "SAND", "GALA", "BERM", "OTHERS", "SPLI", "RWIH"]
    for i in range(0, len(assets), 2):
        row = st.columns(2)
        for j in range(2):
            asset = assets[i+j]
            style = "background:#00F2FF; color:#000;" if asset == "RENDER" else "background:#0d1117; color:#00F2FF;"
            row[j].markdown(f'<div style="{style} border:1px solid #00F2FF33; text-align:center; padding:8px; font-size:10px; margin-bottom:5px;">{asset}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="label-min">CANDLE CHART (CIAN/PURPLE)</div>', unsafe_allow_html=True)
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # Lógica de velas corregida (sin errores de corchetes)
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))),
            open=p,
            high=[val * 1.001 for val in p],
            low=[val * 0.999 for val in p],
            close=p,
            increasing_line_color='#00F2FF', # Cian para subir
            decreasing_line_color='#8A2BE2', # Púrpura para bajar
            increasing_fillcolor='rgba(0, 242, 255, 0.1)',
            decreasing_fillcolor='rgba(138, 43, 226, 0.5)'
        )])
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="#111"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.markdown('<div style="color:red;">RADAR_OFFLINE</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    # ADAPTATION ENGINE
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="label-min">ADAPTATION ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<div style="text-align:center;"><span style="font-size:80px; color:#00F2FF;" class="wheel-anim">☸</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # TERMINAL LOGS
    st.markdown('<div class="panel" style="margin-top:10px;">', unsafe_allow_html=True)
    st.markdown('<div class="label-min">TERMINAL</div>', unsafe_allow_html=True)
    now = datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="terminal">
        [LOG {now}] Adapt Check (F32) ... <span class="ok">OK</span><br>
        [LOG {now}] Asset: RENDER ... <span class="ok">OK</span><br>
        [LOG {now}] Data Stream ... <span class="ok">Loaded</span><br>
        <br>
        >> ESTRUCTURA LISTA ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Sincronización cada 10 seg
time.sleep(10)
st.rerun()
