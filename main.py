import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. SETTINGS TÁCTICOS ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V57", page_icon="🦈")

# --- 2. CSS ESPECÍFICO: BRILLO NEÓN Y PROFUNDIDAD (GLASSMORPHISM) ---
st.markdown("""
<style>
    /* Reset y Fondo Deep Black #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #0A0E14 !important; color: #FFFFFF !important; font-family: 'JetBrains Mono', monospace; }
    
    /* CAPA DE CRISTAL (Glassmorphism + Borde 1px) */
    .glass-panel {
        background: rgba(13, 17, 23, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 2px;
        padding: 20px;
        box-shadow: 0 0 20px rgba(0, 0, 0, 0.8), inset 0 0 10px rgba(0, 242, 255, 0.05);
        margin-bottom: 15px;
    }

    /* HEADER CON RESPLANDOR VERDE INTENSO */
    .shark-header {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 15px 35px;
        border-bottom: 1px solid #00F2FF;
        box-shadow: 0 10px 30px rgba(0, 242, 255, 0.1);
    }
    .balance-glow {
        font-size: 45px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 20px #39FF14, 0 0 40px rgba(57, 255, 20, 0.3);
    }

    /* TERMINAL CON EFECTO FÓSFORO */
    .terminal-console {
        background: #000; padding: 15px; border-left: 4px solid #00F2FF;
        font-size: 11px; color: #00F2FF; height: 160px; overflow: hidden;
        text-shadow: 0 0 5px rgba(0, 242, 255, 0.7);
    }
    .log-status { color: #39FF14; text-shadow: 0 0 8px #39FF14; font-weight: bold; }

    /* RUEDA DE ADAPTACIÓN SVG (GRAN TAMAÑO + BRILLO) */
    .wheel-container { text-align: center; padding: 30px 0; }
    .mahoraga-gear {
        width: 160px; animation: rotation 20s linear infinite;
        filter: drop-shadow(0 0 15px #8A2BE2) drop-shadow(0 0 5px #00F2FF);
    }
    @keyframes rotation { 100% { transform: rotate(360deg); } }

    /* BOTONERA TÁCTICA */
    .market-btn {
        padding: 12px; border: 1px solid #1A1F26; margin-bottom: 5px;
        display: flex; justify-content: space-between; font-size: 12px;
        transition: 0.3s; cursor: pointer;
    }
    .market-btn:hover { border-color: #00F2FF; background: rgba(0, 242, 255, 0.05); }
    .active-btn { border-color: #00F2FF; background: rgba(0, 242, 255, 0.15); box-shadow: inset 0 0 10px rgba(0, 242, 255, 0.2); }
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER (Balance Central) ---
st.markdown(f"""
<div class="shark-header">
    <div style="line-height: 1.1;">
        <span style="letter-spacing:4px; font-weight:900; font-size:22px; color:#00F2FF;">MAHORASHARK</span><br>
        <span style="font-size:10px; color:#555;">ALPHA V57 | MILITARY_SPEC_ENG</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:10px; color:#8b949e; letter-spacing:2px;">MXN TOTAL BALANCE</span><br>
        <span class="balance-glow">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:15px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:4px 15px; font-size:11px; font-weight:bold; box-shadow: 0 0 10px rgba(57,255,20,0.2);">LIVE_CORE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:4px 15px; font-size:11px; font-weight:bold;">F: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA INTERFAZ (UI PROFUNDA) ---
c1, c2, c3 = st.columns([1.2, 3, 1.2])

with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#444; letter-spacing:2px; margin-bottom:20px;">MARKET_ACCIONES</p>', unsafe_allow_html=True)
    assets = [("RENDER (IA)", "+2.4%", True), ("APPLE", "-0.1%", False), ("SAND", "-1.5%", False), ("GALA", "+5.2%", False), ("BTC", "+0.8%", False)]
    for name, change, active in assets:
        cls = "active-btn" if active else ""
        st.markdown(f'<div class="market-btn {cls}"><span>{name}</span><span style="color:#39FF14;">{change}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel" style="height:600px;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#444; letter-spacing:2px;">RADAR_TACTICO_V57</p>', unsafe_allow_html=True)
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # MOTOR DE VELAS: CIAN (#00F2FF) / PÚRPURA (#8A2BE2)
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.0015 for x in p],
            low=[x*0.9985 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2', # Colores exactos
            increasing_fillcolor='rgba(0, 242, 255, 0.2)', decreasing_fillcolor='rgba(138, 43, 226, 0.6)'
        )])
        
        # INDICADORES: BANDAS DE BOLLINGER (SOMBREADO)
        fig.add_trace(go.Scatter(y=[x*1.008 for x in p], line=dict(color='rgba(0,242,255,0.05)', width=1), fill='tonexty', fillcolor='rgba(0,242,255,0.02)'))
        fig.add_trace(go.Scatter(y=[x*0.992 for x in p], line=dict(color='rgba(0,242,255,0.05)', width=1)))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=540, margin=dict(l=0, r=50, t=10, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)", yaxis_tickfont=dict(family="JetBrains Mono", size=10, color="#555")
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("RADAR_OFFLINE")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    # ENGINE PANEL
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#444; letter-spacing:2px;">ADAPTATION_ENGINE</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wheel-container">
        <img src="https://i.imgur.com/83p1y9N.png" class="mahoraga-gear">
        <p style="font-family:monospace; font-size:11px; color:#8A2BE2; margin-top:25px; letter-spacing:3px;">SYNCING_14s</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL PANEL
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-console">
        [{t}] <span class="log-status">[OK]</span>: System Boot Secure<br>
        [{t}] <span class="log-status">[OK]</span>: {ASSET} Link Established<br>
        [{t}] <span class="log-status">[OK]</span>: Radar Factor {FACTOR} Ingested<br>
        <br>
        "El Ferrari está listo para correr."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Refresh de datos
time.sleep
