import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PODER ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45")

# --- 2. EL MARTILLO: CSS DE GRADO MILITAR (CERO STREAMLIT STYLE) ---
st.markdown(f"""
<style>
    /* Reset total y fondo profundo */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{display: none !important;}}
    .stApp {{ background-color: #0A0E14 !important; color: #00F2FF !important; }}
    
    /* Contenedores con profundidad (Glassmorphism Real) */
    .inner-panel {{
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid #00F2FF33;
        border-radius: 2px;
        padding: 15px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.8), inset 0 0 10px rgba(0, 242, 255, 0.05);
        margin-bottom: 15px;
    }}

    /* Header Táctico Slim */
    .shark-header {{
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 12px 25px;
        border-bottom: 2px solid #00F2FF;
        box-shadow: 0 5px 20px rgba(0, 242, 255, 0.15);
    }}
    .balance-neon {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 38px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 15px rgba(57, 255, 20, 0.6);
    }}

    /* Botones Estilo Terminal */
    .asset-item {{
        padding: 10px; border-bottom: 1px solid #161b22;
        font-family: 'JetBrains Mono', monospace; font-size: 11px;
        display: flex; justify-content: space-between; cursor: pointer;
    }}
    .asset-item:hover {{ background: rgba(0, 242, 255, 0.1); border-left: 3px solid #00F2FF; }}
    .active-asset {{ background: rgba(0, 242, 255, 0.15); border-left: 3px solid #00F2FF; color: #fff; }}

    /* Terminal de Logs Real */
    .terminal-output {{
        background: #000; padding: 12px; border: 1px solid #333;
        font-family: 'JetBrains Mono', monospace; font-size: 11px;
        color: #00F2FF; height: 150px; overflow-y: hidden;
    }}
    .log-green {{ color: #39FF14; text-shadow: 0 0 5px #39FF14; }}

    /* Rueda de Mahoraga Dinámica */
    .wheel-container {{
        text-align: center; padding: 20px 0;
    }}
    .wheel-svg {{
        width: 130px; animation: rotation 20s linear infinite;
        filter: drop-shadow(0 0 10px #8A2BE2);
    }}
    @keyframes rotation {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. HEADER DE ALTA FIDELIDAD ---
st.markdown(f"""
<div class="shark-header">
    <div>
        <span style="font-weight:bold; font-size:18px; letter-spacing:2px;">🦈 MAHORASHARK ALPHA V45</span><br>
        <span style="font-size:9px; color:#555; font-family:monospace;">TACTICAL TRADING GUADAÑA | SHARK HUD</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:9px; color:#8b949e; font-family:monospace;">MXN BALANCE:</span><br>
        <span class="balance-neon">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:10px;">
        <div style="background:#1a2a1a; border:1px solid #39FF14; color:#39FF14; padding:2px 10px; border-radius:2px; font-size:10px; font-weight:bold;">LIVE</div>
        <div style="background:#0a1a2a; border:1px solid #00F2FF; color:#00F2FF; padding:2px 10px; border-radius:2px; font-size:10px; font-weight:bold;">FACTOR: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. LAYOUT DE TRES NÚCLEOS ---
c1, c2, c3 = st.columns([1, 2.8, 1])

with c1:
    st.markdown('<div class="inner-panel">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#444; margin-bottom:15px; letter-spacing:1px;">MARKET ACCIONES</div>', unsafe_allow_html=True)
    
    # Lista de activos sin botones feos de Streamlit
    assets = [
        ("RENDER (IA)", "$124.50", "+2.4%"),
        ("APPLE", "$3,450.00", "-0.1%"),
        ("SAND (Land)", "$8.92", "-1.5%"),
        ("GALA", "$0.85", "+5.2%"),
        ("BITCOIN", "$1.8M", "+0.8%")
    ]
    for name, price, change in assets:
        active_class = "active-asset" if "RENDER" in name else ""
        st.markdown(f"""
            <div class="asset-item {active_class}">
                <span>{name}</span>
                <span style="color:#39FF14;">{change}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="inner-panel" style="height:550px;">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#444; margin-bottom:10px; letter-spacing:1px;">RADAR TÁCTICO DE MOVIMIENTO</div>', unsafe_allow_html=True)
    
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # Gráfica de Velas con el Design System #00F2FF / #8A2BE2
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.001 for x in p],
            low=[x*0.999 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
            increasing_fillcolor='rgba(0, 242, 255, 0.1)', decreasing_fillcolor='rgba(138, 43, 226, 0.4)'
        )])
        
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=480, margin=dict(l=0, r=45, t=0, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)", yaxis_tickfont=dict(family="JetBrains Mono", size=10, color="#555")
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except: st.error("RADAR_SYNC_LOST")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    # ADAPTATION ENGINE
    st.markdown('<div class="inner-panel">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#444; margin-bottom:15px; letter-spacing:1px;">ADAPTATION ENGINE</div>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="wheel-container">
            <img src="https://i.imgur.com/83p1y9N.png" class="wheel-svg">
            <p style="font-family:monospace; font-size:11px; color:#8A2BE2; margin-top:15px;">NEXT_CHECK: 14s</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL LOGS
    st.markdown('<div class="inner-panel">', unsafe_allow_html=True)
    st.markdown('<div style="font-size:10px; color:#444; margin-bottom:10px; letter-spacing:1px;">TERMINAL_LOG</div>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-output">
        [{t}] <span class="log-green">OK</span>: System Ingest Active<br>
        [{t}] <span class="log-green">OK</span>: Asset {ASSET} Synced<br>
        [{t}] <span class="log-green">OK</span>: Radar factor 32<br>
        <br>
        "El Ferrari está listo para correr."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Actualización cada 15 seg
time.sleep(15)
st.rerun()
