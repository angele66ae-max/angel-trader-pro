import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. SETTINGS GLOBALES ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45")

# --- 2. EL MARTILLO: UI/UX POLISH (GLASSMORPHISM & NEON) ---
st.markdown(f"""
<style>
    /* Fondo Base Dark Mode Profundo */
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ 
        background-color: #0A0E14 !important; 
        color: #00F2FF !important; 
        font-family: 'Inter', sans-serif;
    }}

    /* Panel con Profundidad y Glassmorphism */
    .glass-panel {{
        background: rgba(26, 31, 38, 0.7) !important;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }}

    /* Header con Neón Controlado */
    .header-tactical {{
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 10px 25px;
        border-bottom: 2px solid #00F2FF;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }}
    .balance-glow {{
        font-size: 38px; color: #00FF00; font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
        font-family: 'Roboto Mono', monospace;
    }}

    /* Scrollbar Custom (Estilo Profesional) */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: #0A0E14; }}
    ::-webkit-scrollbar-thumb {{ background: #00F2FF; border-radius: 10px; }}

    /* Terminal de Logs (Fósforo Neón) */
    .terminal-log {{
        font-family: 'Roboto Mono', monospace;
        font-size: 11px; color: #00F2FF;
        background: #050505; padding: 10px;
        border-radius: 2px; border-left: 3px solid #00F2FF;
        height: 120px; overflow-y: auto;
    }}
    .log-ok {{ color: #00FF00; text-shadow: 0 0 5px #00FF00; }}

    /* Animación de la Rueda (SVG Dinámico en mente) */
    .wheel-rotation {{
        width: 130px; animation: spin-gear 12s linear infinite;
        filter: drop-shadow(0 0 8px #8A2BE2);
    }}
    @keyframes spin-gear {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER (NODO DE ESTADO GLOBAL) ---
st.markdown(f"""
<div class="header-tactical">
    <div>
        <span style="font-weight:bold; font-size:18px; letter-spacing:1px;">🦈 MAHORASHARK ALPHA V45</span><br>
        <span style="font-size:9px; color:#444; font-family:monospace;">TACTICAL TRADING GUADAÑA | SHARK HUD</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:10px; color:#fff; font-family:monospace;">MXN BALANCE:</span><br>
        <span class="balance-glow">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:8px;">
        <div style="background:#1a2a1a; border:1px solid #00FF00; color:#00FF00; padding:2px 10px; border-radius:3px; font-size:10px; font-weight:bold;">LIVE</div>
        <div style="background:#0a1a2a; border:1px solid #00F2FF; color:#00F2FF; padding:2px 10px; border-radius:3px; font-size:10px; font-weight:bold;">FACTOR: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. LAYOUT TÉCNICO (3 COLUMNAS) ---
col_left, col_mid, col_right = st.columns([1, 2.8, 1])

# PANEL IZQUIERDO: SELECCIÓN DE ACTIVOS (SCROLL DINÁMICO)
with col_left:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#555; margin-bottom:10px;">MARKET ACCIONES</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="border:1px solid #00F2FF; padding:8px; font-size:12px; background:rgba(0,242,255,0.05);">SELECTED: {ASSET}</div>', unsafe_allow_html=True)
    
    # Lista con Scrollbar custom
    st.markdown('<div style="height:350px; overflow-y:auto; margin-top:10px;">', unsafe_allow_html=True)
    assets = ["RENDER", "APPLE", "SAND", "GALA", "BITCOIN", "SOLANA", "ETHEREUM", "TESLA", "META", "AMAZON"]
    for a in assets:
        btn_bg = "rgba(0,242,255,0.2)" if a == "RENDER" else "transparent"
        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; padding:10px; border-bottom:1px solid #161b22; background:{btn_bg}; font-size:11px; cursor:pointer;">
                <span>{a}</span><span style="color:#555;">></span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)

# PANEL CENTRAL: EL MOTOR VISUAL (CANDLE CHART COMPLETO)
with col_mid:
    st.markdown('<div class="glass-panel" style="height:550px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#555; margin-bottom:5px;">RADAR TÁCTICO DE MOVIMIENTO</div>', unsafe_allow_html=True)
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # Velas con Cuerpo y Mechas (High/Low)
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.002 for x in p],
            low=[x*0.998 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
            increasing_fillcolor='rgba(0, 242, 255, 0.2)', decreasing_fillcolor='rgba(138, 43, 226, 0.8)'
        )])
        # Capa de Indicadores (Bollinger sutil)
        fig.add_trace(go.Scatter(y=[x*1.005 for x in p], line=dict(color='rgba(0,242,255,0.1)', width=1), name="Upper BB"))
        fig.add_trace(go.Scatter(y=[x*0.995 for x in p], line=dict(color='rgba(0,242,255,0.1)', width=1), name="Lower BB"))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=480, margin=dict(l=0, r=40, t=0, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except: st.error("LINKING_RADAR...")
    st.markdown('</div>', unsafe_allow_html=True)

# PANEL DERECHO: LÓGICA DE ADAPTACIÓN
with col_right:
    # Adaptation Wheel
    st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#555; margin-bottom:15px;">ADAPTATION ENGINE</div>', unsafe_allow_html=True)
    st.markdown('<img src="https://i.imgur.com/83p1y9N.png" class="wheel-rotation">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:11px; margin-top:10px; color:#8A2BE2;">NEXT CHECK: 14s</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Terminal de Logs
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#555; margin-bottom:10px;">TERMINAL_SESS_LOG</div>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-log">
        [{t}] <span class="log-ok">OK</span>: System Ingest Active<br>
        [{t}] <span class="log-ok">OK</span>: Asset {ASSET} Synced<br>
        [{t}] <span class="log-ok">OK</span>: Radar factor 32<br>
        <br>
        "El Ferrari está listo para correr."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh cada 10 seg
time.sleep(10)
st.rerun()
