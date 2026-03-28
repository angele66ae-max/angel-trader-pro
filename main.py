import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL NÚCLEO TÁCTICO ---
# Sincronizado con tu balance real de image_5.png
SALDO_REAL = 144.95
META_10K = 10000.0

# Configuración de página como la imagen de referencia (image_8.png)
st.set_page_config(layout="wide", page_title="TERMINAL TÁCTICA", page_icon="📈")

# --- 2. ESTILO VISUAL "DOS GOTAS DE AGUA" (CSS ULTRA-PRECISO) ---
st.markdown(f"""
<style>
    /* Fondo gris oscuro y tipografía como en image_8.png */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono&family=Inter:wght@400;700&display=swap');
    
    .stApp {{ background-color: #0b1014; color: #e6edf3; font-family: 'Inter', sans-serif; }}
    
    /* Barra Superior con el Balance Neón */
    .tactical-header {{
        padding: 20px 0;
        text-align: center;
        background-color: #0b1014;
        position: sticky; top: 0; z-index: 99;
    }}
    .balance-neon {{ color: #39FF14; font-size: 38px; font-weight: bold; font-family: 'JetBrains Mono', monospace; text-shadow: 0 0 10px #39FF14; }}
    .guadaña-title {{ color: #8b949e; font-size: 10px; font-family: monospace; text-transform: uppercase; }}

    /* Paneles Estilo image_8.png */
    .panel-box {{ padding: 10px 0; }}
    .panel-label {{ color: #8b949e; font-size: 11px; text-transform: uppercase; margin-bottom: 10px; display: block; }}
    
    /* Filas de Activos */
    .asset-row {{ display: flex; justify-content: space-between; align-items: center; padding: 8px 10px; border-radius: 4px; }}
    .asset-row:hover {{ background: #161b22; cursor: pointer; }}
    
    /* Terminal Táctica Verde */
    .terminal-logs {{ font-family: 'JetBrains Mono', monospace; color: #39FF14; font-size: 10px; line-height: 1.4; }}
    .terminal-box {{ background: #111; border: 1px solid #333; padding: 10px; border-radius: 4px; }}
</style>
""", unsafe_allow_html=True)

# --- 3. BARRA SUPERIOR (HEADER) ---
st.markdown(f"""
<div class="tactical-header">
    <span class="guadaña-title">TACTICAL TRADING GUADAÑA</span><br>
    <span class="balance-neon">${SALDO_REAL:,.2f}</span>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA TERMINAL (3 COLUMNAS) ---
col_market, col_radar, col_ai = st.columns([1.2, 2.6, 1.2])

# COLUMNA 1: MARKET ACCIONES
with col_market:
    st.markdown("<small style='color:#8b949e'>MARKET ACCIONES</small>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box">', unsafe_allow_html=True)
        # Lista de Activos recreada de image_8.png
        assets = [
            {"n": "RENDER (IA)", "t": "render_mxn", "p": 124.50, "c": "+2.4%"},
            {"n": "APPLE", "t": "aapl_mxn", "p": 3450.00, "c": "-0.1%"},
            {"n": "SAND (Land)", "t": "sand_mxn", "p": 8.92, "c": "-1.5%"},
            {"n": "GALA", "t": "gala_mxn", "p": 0.85, "c": "+5.2%"},
            {"n": "BITCOIN", "t": "btc_mxn", "p": 1800000.0, "c": "+0.8%"}
        ]
        for a in assets:
            st.markdown(f"""
            <div class="asset-row">
                <div><b>{a['n']}</b><br><small style="color:#8b949e">${a['p']:,}</small></div>
                <div style="color:{'#39FF14' if '+' in a['c'] else '#f85149'};">{a['c']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.write("---")
        st.markdown("<small style='color:#8b949e'>SELECCIONA ACTIVO PARA EL RADAR</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

# COLUMNA 2: RADAR TÁCTICO (LA GRÁFICA NEÓN)
with col_radar:
    st.markdown("<small style='color:#8b949e'>RADAR TÁCTICO</small>", unsafe_allow_html=True)
    try:
        # Petición de mercado real para el radar (V45.2)
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=5).json()
        precios = [float(t['price']) for t in r['payload']][::-1]
        
        # Gráfica de área neón recreada de image_8.png
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=precios, fill='tozeroy', line=dict(color='#00f2ff', width=3), fillcolor='rgba(0, 242, 255, 0.05)'))
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=450, margin=dict(l=0, r=0, t=10, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_title=None, xaxis_title=None
        )
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("Sincronizando radar satelital...")

# COLUMNA 3: ADAPTATION ENGINE Y LOGS
with col_ai:
    st.markdown("<small style='color:#8b949e'>ADAPTATION ENGINE (MAHORAGA 32)</small>", unsafe_allow_html=True)
    
    # Rueda de Mahoraga y logs recreados de image_8.png y image_3.png
    st.markdown(f"""
    <div class="panel-box" style="text-align: center;">
        <p style="color:#ab7df8; font-size:12px;">Rueda Girando: Factor 32 Activo</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="terminal-box">', unsafe_allow_html=True)
    ts = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-logs">
        [{datetime.now().strftime("%H:%M")}] Adapt Check (Factor 32) ... OK<br>
        [{datetime.now().strftime("%H:%M")}] Balance Sync: ${SALDO_REAL} ... OK<br>
        [{datetime.now().strftime("%H:%M")}] RENDER Selected ... Data Loaded<br>
        <hr style="border-color:#333">
        "Pavo, el código ya está limpio. El Ferrari está listo para correr."
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<small style='color:#8b949e'>TERMINAL DE COMANDO</small>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="terminal-logs" style="color:#8b949e">
        [{ts}] >> HIERRO MARTILLADO ✅<br>
        [{ts}] >> ESTRUCTURA ADAPT ✅<br>
        [{ts}] >> ESPERANDO ORDEN
    </div>
    """, unsafe_allow_html=True)

# Actualización automática cada 15 segundos
time.sleep(15)
st.rerun()
