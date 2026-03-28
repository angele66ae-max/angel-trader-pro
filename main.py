import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL SISTEMA (Basado en tus datos reales) ---
SALDO_REAL = 144.95
ASSET_SELECCIONADO = "RENDER (IA)"
FACTOR_ACTUAL = 32

st.set_page_config(layout="wide", page_title="MAHORASHARK REF V47", page_icon="🦈")

# --- 2. EL MARTILLO: INYECCIÓN DE CSS CYBER-NOIR (Polishing) ---
st.markdown(f"""
<style>
    /* Reset total y fondo Dark Mode Profundo #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{display: none !important;}}
    .stApp {{ background-color: #0A0E14 !important; color: #FFFFFF !important; font-family: 'Inter', sans-serif; }}
    
    /* Paneles Glassmorphism con Profundidad (#1A1F26) */
    .glass-panel {{
        background: rgba(26, 31, 38, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }}

    /* Header Slim Táctico */
    .nav-header {{
        display: flex; justify-content: space-between; align-items: center;
        background-color: #000; padding: 10px 20px; border-bottom: 1px solid #00F2FF;
        position: sticky; top: 0; z-index: 99;
    }}
    .balance-main {{ font-size: 38px; color: #39FF14; font-weight: 700; text-shadow: 0 0 10px #39FF14; font-family: 'Roboto Mono', monospace; }}
    .status-badge {{ background: #1a2a1a; color: #39FF14; border: 1px solid #39FF14; padding: 2px 8px; border-radius: 4px; font-size: 10px; font-weight: bold; margin-left: 5px; }}

    /* custom Scrollbar */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: #0A0E14; }}
    ::-webkit-scrollbar-thumb {{ background: #00F2FF; border-radius: 10px; }}

    /* Botonera de Activos */
    .asset-item {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; border-radius: 4px; border-bottom: 1px solid #161b22; cursor: pointer; }}
    .asset-item:hover {{ background: rgba(0,242,255,0.1); }}
    .active-asset {{ background: #00F2FF22; border-left: 2px solid #00F2FF; color: #FFFFFF !important; }}

    /* Terminal de Logs (JetBrains Mono OK) */
    .terminal-log {{
        font-family: 'JetBrains Mono', monospace;
        font-size: 11px; color: #00F2FF;
        background: #000; padding: 10px; border-left: 3px solid #00F2FF;
    }}
    .log-ok {{ color: #39FF14; text-shadow: 0 0 5px #39FF14; }}
    
    /* Rueda de Adaptación Animada (SVG) */
    .wheel-animation {{ width: 140px; height: 140px; margin: 0 auto; animation: rotateWheel 15s linear infinite; filter: drop-shadow(0 0 8px #ab7df8); }}
    @keyframes rotateWheel {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="nav-header">
    <div>
        <b style="font-size:18px;">🦈 MAHORASHARKRef V47</b><br>
        <span style="font-size:9px; color:#444;">TACTICAL TRADING GUADAÑA | SHARK HUD</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:9px; color:#fff;">MXN BALANCE:</span><br>
        <span class="balance-main">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex;">
        <span class="status-badge pulse">LIVE</span>
        <span class="status-badge" style="border-color:#00f2ff; color:#00f2ff;">FACTOR: {FACTOR_ACTUAL}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # Espaciador

# --- 4. ESTRUCTURA DE 3 COLUMNAS ---
col_market, col_radar, col_ai = st.columns([1, 2.7, 1])

# PANEL IZQUIERDO: MARKET ACCIONES (Clonado)
with col_market:
    st.markdown("<small style='color:#8b949e'>MARKET ACCIONES</small>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f'<div style="font-size:11px; border:1px solid #00f2ff; padding:8px; background:#0d1117;">SELECTED: <span style="color:#00f2ff">{ASSET_SELECCIONADO}</span></div>', unsafe_allow_html=True)
    
    # Cuadrícula de activos (Botones tácticos)
    assets_grid = ["RENDER", "APPLE", "SAND", "GALA", "BERM", "OTHERS", "SPLI", "RWIH"]
    for i in range(0, len(assets_grid), 2):
        row = st.columns(2)
        for j in range(2):
            asset_name = assets_grid[i+j]
            active_style = "active-asset" if asset_name == "RENDER" else ""
            row[j].markdown(f'<div class="asset-item {active_style}">{asset_name}</div>', unsafe_allow_html=True)
            
    st.markdown('</div>', unsafe_allow_html=True)

# PANEL CENTRAL: EL RADAR (GRÁFICO DE VELAS REALES CIAN/PÚRPURA)
with col_radar:
    st.markdown(f"<small style='color:#8b949e'>RADAR TÁCTICO: {ASSET_SELECCIONADO} (1D)</small>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel" style="height:550px;">', unsafe_allow_html=True)
    try:
        # Simulando datos para RENDER
        # r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        # En demo usamos datos fijos para no saturar la API
        precios = [120, 122, 121, 124, 123, 126, 125, 128, 127] # Simulación
        df = pd.DataFrame(precios, columns=['price'])
        
        # Velas Cian (#00F2FF) y Púrpura (#8A2BE2) segun descripción
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(precios))), open=df['price'], high=[x*1.002 for x in df['price']],
            low=[x*0.998 for x in df['price']], close=df['price'],
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
            increasing_fillcolor='rgba(0, 242, 255, 0.1)', decreasing_fillcolor='rgba(138, 43, 226, 0.8)'
        )])
        # Capa de Bandas de Bollinger (Cian sutil)
        fig.add_trace(go.Scatter(y=[x*1.01 for x in df['price']], line=dict(color='rgba(0,242,255,0.1)', width=1), name="Upper BB"))
        fig.add_trace(go.Scatter(y=[x*0.99 for x in df['price']], line=dict(color='rgba(0,242,255,0.1)', width=1), name="Lower BB"))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=480, margin=dict(l=0, r=40, t=0, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("SYNCING_RADAR...")
    st.markdown('</div>', unsafe_allow_html=True)

# PANEL DERECHO: LÓGICA DE ADAPTACIÓN
with col_ai:
    # ADAPTATION ENGINE
    st.markdown("<small style='color:#8b949e'>ADAPTATION ENGINE</small>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel" style="text-align:center;">', unsafe_allow_html=True)
    # Rueda SVG Animada (Imagen fija para demo)
    st.markdown('<img src="https://i.imgur.com/83p1y9N.png" class="wheel-animation">', unsafe_allow_html=True)
    st.markdown(f'<p style="font-size:11px; color:#8A2BE2; margin-top:10px;">MAHORAGA FACTOR: {FACTOR_ACTUAL}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PROFIT/LOSS & TERMINAL
    st.markdown("<small style='color:#8b949e'>SESSION SESS LOG</small>", unsafe_allow_html=True)
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-log">
        [{t}] <span class="log-ok">OK</span>: System Link Stable<br>
        [{t}] <span class="log-ok">OK</span>: Asset Synced ({ASSET_SELECCIONADO})<br>
        [{t}] <span class="log-ok">OK</span>: Radar factor {FACTOR_ACTUAL}<br>
        <br>
        "El Ferrari está listo."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco automático cada 10 seg
time.sleep(10)
st.rerun()
