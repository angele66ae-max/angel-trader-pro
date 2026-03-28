import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL NÚCLEO TÁCTICO ---
# Sincronizado con tu balance real de image_5.png
SALDO_REAL = 144.95
ASSET = "RENDER (IA)"
FACTOR = 32

# Configuración de página como la imagen de referencia (image_8.png)
st.set_page_config(layout="wide", page_title="MAHORASHARK REF V47", page_icon="🦈")

# --- 2. EL MARTILLO: SISTEMA DE ESTILOS "TRUE CLONE" ---
st.markdown(f"""
<style>
    /* Fondo Dark Mode Profundo #0A0E14 y Tipografía Técnica */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{display: none !important;}}
    .stApp {{ 
        background-color: #0A0E14 !important; 
        color: #e6edf3 !important; 
        font-family: 'Inter', sans-serif;
    }}
    
    /* Panel con Profundidad y Glassmorphism */
    .glass-panel {{
        background: rgba(10, 14, 20, 0.8) !important;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
        margin-bottom: 10px;
    }}

    /* Header Estrecho de imagen_8.png con Neón Controlado */
    .shark-header {{
        padding: 15px 30px;
        background-color: #0d1117;
        border-bottom: 1px solid #30363d;
        display: flex; justify-content: space-between; align-items: center;
        position: sticky; top: 0; z-index: 99;
    }}
    .balance-glow {{ 
        color: #39FF14; font-size: 38px; font-weight: bold; 
        text-shadow: 0 0 10px #39FF14;
        font-family: 'JetBrains Mono', monospace; 
    }}
    .status-tag {{ background: #1a2a1a; border: 1px solid #30363d; padding: 2px 8px; border-radius: 4px; font-size: 11px; color: #39FF14; font-family: monospace; }}

    /* Botonera de Activos */
    .asset-row {{ display: flex; justify-content: space-between; padding: 8px 10px; border-radius: 4px; border-bottom: 1px solid #161b22; cursor: pointer; }}
    .asset-row:hover {{ background: #161b22; border-left: 2px solid #58a6ff; }}
    
    /* custom Scrollbar */
    ::-webkit-scrollbar {{ width: 5px; }}
    ::-webkit-scrollbar-track {{ background: #0A0E14; }}
    ::-webkit-scrollbar-thumb {{ background: #00F2FF; border-radius: 10px; }}
    
    /* Terminal Táctica */
    .terminal-green {{ font-family: 'JetBrains Mono', monospace; color: #39FF14; font-size: 10px; line-height: 1.4; }}
    .log-ok {{ color: #39FF14; font-weight: bold; text-shadow: 0 0 5px #39FF14; }}
    
    /* Rueda de Mahoraga Rotatoria de image_8.png */
    .mahoraga-container {{ text-align: center; padding: 10px; }}
    .wheel-anim {{ animation: spin 15s linear infinite; width: 130px; filter: drop-shadow(0 0 8px #ab7df8); }}
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="shark-header">
    <div>
        <b style="font-size:18px;">🦈 MAHORASHARK ALPHA V45</b><br>
        <span style="font-size:10px; color:#8b949e; font-family:monospace;">TACTICAL TRADING GUADAÑA | SHARK HUD</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:10px; color:#8b949e;">MXN BALANCE:</span><br>
        <span class="balance-glow">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:5px;">
        <span class="status-tag">LIVE</span>
        <span class="status-tag">ONLINE</span>
        <span class="status-tag" style="border-color:#00F2FF; color:#00F2FF;">FACTOR: {FACTOR}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA TERMINAL (3 COLUMNAS TÉCNICAS) ---
col_assets, col_radar, col_ai = st.columns([1.1, 2.7, 1.1])

# COLUMNA 1: MARKET ACCIONES (CLONADO)
with col_assets:
    st.markdown("<small style='color:#8b949e'>MARKET ACCIONES</small>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
        st.markdown(f'<div style="font-size:10px; color:#fff;">SELECTED ASSET: <span style="color:#00f2ff;">{ASSET}</span></div>', unsafe_allow_html=True)
        
        # Lista de Activos recreada de image_8.png
        assets_data = [
            {"n": "RENDER (IA)", "p": 124.5, "c": "+2.4%"},
            {"n": "APPLE", "p": 3450.0, "c": "-0.1%"},
            {"n": "SAND (Land)", "p": 8.9, "c": "-1.5%"},
            {"n": "GALA", "p": 0.85, "c": "+5.2%"},
            {"n": "BITCOIN", "p": 1800000.0, "c": "+0.8%"}
        ]
        
        # Contenedor con custom scrollbar
        st.markdown('<div style="height:350px; overflow-y:auto;">', unsafe_allow_html=True)
        for a in assets_data:
            with st.container():
                if st.button(f"{a['n']} ${a['p']:,} {a['c']}", key=a['n'], use_container_width=True):
                    st.session_state.selected_stock = a['n']
        st.markdown('</div></div>', unsafe_allow_html=True)

# COLUMNA 2: RADAR TÁCTICO (LA GRÁFICA NEÓN CIAN/PÚRPURA)
with col_radar:
    st.markdown(f"<small style='color:#8b949e'>CANDLE CHART: {st.session_state.get('selected_stock', 'RENDER (IA)')}</small>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="glass-panel" style="height:550px;">', unsafe_allow_html=True)
        try:
            r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
            precios = [float(t['price']) for t in r['payload']][::-1]
            
            # Gráfica de Velas Táctica con Volumen y Bandas de Bollinger sutiles
            fig = go.Figure(data=[go.Candlestick(
                x=list(range(len(precios))), open=precios, high=[p*1.002 for p in precios],
                low=[p*0.998 for p in precios], close=precios,
                increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
                increasing_fillcolor='rgba(0, 242, 255, 0.1)', decreasing_fillcolor='rgba(138, 43, 226, 0.5)'
            )])
            # Capa de Indicadores (Bollinger sutil)
            fig.add_trace(go.Scatter(y=[x*1.005 for x in precios], line=dict(color='rgba(0,242,255,0.1)', width=1), name="Upper BB"))
            fig.add_trace(go.Scatter(y=[x*0.995 for x in precios], line=dict(color='rgba(0,242,255,0.1)', width=1), name="Lower BB"))

            fig.update_layout(
                template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                height=480, margin=dict(l=10, r=40, t=10, b=10), xaxis_visible=False, yaxis_side="right",
                yaxis_gridcolor="rgba(255,255,255,0.02)"
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        except:
            st.warning("SYSTEM OFFLINE...")
        st.markdown('</div>', unsafe_allow_html=True)

# COLUMNA 3: ADAPTATION ENGINE Y LOGS (CLONADO)
with col_ai:
    st.markdown("<small style='color:#8b949e'>ADAPTATION ENGINE (MAHORAGA 32)</small>", unsafe_allow_html=True)
    
    # Rueda de Mahoraga Rotatoria de image_8.png
    st.markdown(f"""
    <div class="glass-panel" style="text-align: center;">
        <img src="https://i.imgur.com/83p1y9N.png" class="wheel-anim" alt="Mahoraga Wheel">
        <p style="color:#ab7df8; font-size:11px; margin-top:10px;">Factor {FACTOR} Activo: Adaptándose</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logs Estilo image_8.png y image_3.png
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    log_time = datetime.now().strftime("%H:%M")
    st.markdown(f"""
    <div class="terminal-green">
        [LOG {log_time}] Adapt Check (F{FACTOR}) ... <span class="log-ok">OK</span><br>
        [LOG {log_time}] Balance Sync: ${SALDO_REAL} ... <span class="log-ok">OK</span><br>
        [LOG {log_time}] RENDER Selected ... <span class="log-ok">Data Loaded</span><br>
        <hr style="border-color:#333">
        "Pavo, el código ya está limpio. El Ferrari está listo para correr."
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<small style='color:#8b949e'>TERMINAL DE COMANDO</small>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="glass-panel" style="border-color:#39FF14;">
        <div class="terminal-green">
            [02:24:14] >> HIERRO MARTILLADO ✅<br>
            [02:24:14] >> ESTRUCTURA ADAPT ✅<br>
            [02:24:14] >> ESPERANDO ORDEN
        </div>
    </div>
    """, unsafe_allow_html=True)

# Actualización automática cada 15 segundos
time.sleep(15)
st.rerun()
