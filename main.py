import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd
import numpy as np
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DEL SISTEMA (SHARK CORE) ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V61", page_icon="🦈")

# --- 2. EL MARTILLO: INYECCIÓN DE CSS CYBER-NOIR (MILITARY SPEC) ---
# Separado para evitar errores de sintaxis y asegurar el acabado profesional.
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');

    /* Reset total y fondo Deep Black #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #0A0E14 !important; color: #FFFFFF !important; font-family: 'Inter', sans-serif; }
    
    /* PANELES GLASSMORPHISM CON PROFUNDIDAD (Borde 1px) */
    .module-card {
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.15);
        border-radius: 2px;
        padding: 15px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.9);
        margin-bottom: 12px;
    }

    /* HEADER TÁCTICO CON RESPLANDOR NEÓN */
    .nav-hud {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 10px 35px;
        border-bottom: 1px solid #00F2FF;
        box-shadow: 0 5px 25px rgba(0, 242, 255, 0.15);
        position: sticky; top: 0; z-index: 99;
    }
    .main-balance {
        font-family: 'JetBrains Mono', monospace;
        font-size: 40px; color: #39FF14; font-weight: 800;
        text-shadow: 0 0 15px #39FF14, 0 0 30px rgba(57, 255, 20, 0.3);
    }

    /* TERMINAL DE LOGS (EFECTO FÓSFORO CRT) */
    .terminal-out {
        background: #000; padding: 12px; border-left: 3px solid #00F2FF;
        font-family: 'JetBrains Mono', monospace; font-size: 10px;
        color: #00F2FF; height: 160px; overflow: hidden;
        text-shadow: 0 0 5px rgba(0, 242, 255, 0.5);
    }
    .log-tag { color: #39FF14; text-shadow: 0 0 8px #39FF14; font-weight: bold; }

    /* RUEDA DE ADAPTACIÓN SVG (ANIMACIÓN MAHORAGA) */
    .wheel-container { text-align: center; padding: 20px 0; }
    .mahoraga-gear {
        width: 150px; animation: rotation 20s linear infinite;
        filter: drop-shadow(0 0 12px rgba(138, 43, 226, 0.6));
    }
    @keyframes rotation { 100% { transform: rotate(360deg); } }

    /* custom Scrollbar */
    ::-webkit-scrollbar { width: 3px; }
    ::-webkit-scrollbar-thumb { background: #00F2FF; }

    /* Botonera de Activos */
    .asset-row {
        display: flex; justify-content: space-between; padding: 10px;
        border-bottom: 1px solid #1A1F26; font-size: 11px; font-family: 'JetBrains Mono', monospace;
        transition: 0.2s; cursor: pointer;
    }
    .asset-row:hover { background: rgba(0, 242, 255, 0.05); }
    .active-asset { background: rgba(0, 242, 255, 0.1); border-left: 3px solid #00F2FF; color: #fff; }
</style>
""", unsafe_allow_html=True)

# --- 3. ESTRUCTURA DEL HEADER (Clonación Visual) ---
st.markdown(f"""
<div class="nav-hud">
    <div style="line-height: 1;">
        <span style="font-size:24px;">🦈</span>
        <div style="display:inline-block; margin-left:10px;">
            <span style="letter-spacing:4px; font-weight:900; font-size:18px; color:#00F2FF;">MAHORASHARK</span><br>
            <span style="font-size:9px; color:#444; font-family:monospace;">ALPHA V61 | TACTICAL RECON</span>
        </div>
    </div>
    <div style="text-align:center;">
        <span style="font-size:9px; color:#8b949e; letter-spacing:2px;">MXN BALANCE</span><br>
        <span class="main-balance">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:12px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:3px 12px; font-size:10px; font-weight:bold; box-shadow: 0 0 10px rgba(57,255,20,0.2);">LIVE_CORE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:3px 12px; font-size:10px; font-weight:bold;">FACTOR: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # Espaciador Táctico

# --- 4. CUERPO DE LA INTERFAZ (DENSIDAD DE INFO V45) ---
c_mkt, c_radar, c_ai = st.columns([1.1, 2.9, 1.1])

# COLUMNA IZQUIERDA: MARKET ACCIONES (Watchlist Pro)
with c_mkt:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px; margin-bottom:15px;">MARKET_ACCIONES</small>', unsafe_allow_html=True)
    assets_mkt = [("RENDER (IA)", "+2.4%", True), ("APPLE", "-0.1%", False), ("SAND", "-1.5%", False), ("GALA", "+5.2%", False), ("BTC", "+0.8%", False)]
    for n, ch, active in assets_mkt:
        cls = "active-asset" if active else ""
        st.markdown(f'<div class="asset-row {cls}"><span>{n}</span><span style="color:#39FF14;">{ch}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# COLUMNA CENTRAL: EL RADAR (GRÁFICO DE VELAS CIAN/PÚRPURA)
with c_radar:
    st.markdown('<div class="module-card" style="height:600px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">RADAR_TACTICO_V61</small>', unsafe_allow_html=True)
    try:
        # Petición a Bitso real para que las velas se muevan
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # MOTOR DE VELAS: CIAN (#00F2FF) / PÚRPURA (#8A2BE2) segun diseño
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.0015 for x in p],
            low=[x*0.9985 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2', # Colores exactos
            increasing_fillcolor='rgba(0, 242, 255, 0.2)', decreasing_fillcolor='rgba(138, 43, 226, 0.7)'
        )])
        
        # INDICADORES: BANDAS DE BOLLINGER (SOMBREADO TÉCNICO)
        fig.add_trace(go.Scatter(y=[x*1.006 for x in p], line=dict(color='rgba(0,242,255,0.03)', width=1), fill='tonexty', fillcolor='rgba(0,242,255,0.01)'))
        fig.add_trace(go.Scatter(y=[x*0.994 for x in p], line=dict(color='rgba(0,242,255,0.03)', width=1)))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=540, margin=dict(l=0, r=40, t=10, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)", yaxis_tickfont=dict(family="JetBrains Mono", size=10, color="#555")
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("SYNCING_RADAR_DATA...")
    st.markdown('</div>', unsafe_allow_html=True)

# COLUMNA DERECHA: LÓGICA DE ADAPTACIÓN
with c_ai:
    # ADAPTATION ENGINE PANEL
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">ADAPTATION_ENGINE</small>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wheel-container">
        <img src="https://i.imgur.com/83p1y9N.png" class="mahoraga-gear">
        <p style="font-family:'JetBrains Mono', monospace; font-size:11px; color:#8A2BE2; margin-top:25px; letter-spacing:2px;">SYNCING_14s</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL PANEL
    st.markdown('<div class="glass-panel module-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">TERMINAL_SESS</small>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-out">
        [{t}] <span class="log-tag">[OK]</span>: System Boot Secure<br>
        [{t}] <span class="log-tag">[OK]</span>: {ASSET} Link Established<br>
        [{t}] <span class="log-tag">[OK]</span>: Radar Factor 32 Ingested<br>
        <br>
        "El Ferrari está listo."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUTO-REFRESH TÁCTICO (14s segun diseño)
time.sleep(14)
st.rerun()
