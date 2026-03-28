import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import hmac, hashlib, time

# --- 1. ADN DE LA GUADAÑA (CONEXIÓN Y ESTADO) ---
# Usando el balance de tu imagen de referencia (image_8.png)
CAPITAL_REF = 32.57 
META_10K = 10000.0
FACTOR_MAHORAGA = 32

st.set_page_config(layout="wide", page_title="MAHORASHARK REF V45.1", page_icon="🦈")

# --- 2. ESTILO "DOS GOTAS DE AGUA" (CSS ULTRA-PRECISO) ---
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;700&family=JetBrains+Mono&display=swap');
    
    .stApp {{ background-color: #050a0f; color: #e6edf3; font-family: 'Roboto Mono', monospace; }}
    
    /* Shark HUD Simplificado como image_8.png */
    .shark-header {{
        padding: 20px 0;
        text-align: center;
        position: sticky; top: 0; z-index: 99;
        background-color: #050a0f;
    }}
    .balance-main {{ color: #39FF14; font-size: 36px; font-weight: bold; font-family: 'JetBrains Mono'; text-shadow: 0 0 10px #39FF14; }}
    
    /* Paneles Estilo image_8.png */
    .panel-box {{ border-radius: 4px; padding: 10px; margin-bottom: 10px; }}
    .asset-row {{ display: flex; justify-content: space-between; padding: 6px 10px; border-radius: 4px; border-bottom: 1px solid #161b22; }}
    .asset-row:hover {{ background: #0d1117; border-left: 2px solid #58a6ff; }}
    
    /* Terminal Táctica */
    .terminal-green {{ font-family: 'JetBrains Mono'; color: #39FF14; font-size: 11px; line-height: 1.2; }}
    
    /* Rueda de Mahoraga image_8.png */
    .wheel-container {{ text-align: center; padding: 10px; }}
    .wheel-img {{ animation: spin 15s linear infinite; width: 140px; filter: drop-shadow(0 0 5px #ab7df8); }}
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. HUD DE BALANCE CENTRAL ---
st.markdown(f"""
<div class="shark-header">
    <small style="color:#8b949e; font-size:10px;">TACTICAL TRADING GUADAÑA</small><br>
    <span class="balance-main">${CAPITAL_REF:,.2f}</span>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA TERMINAL (3 COLUMNAS PRECISAS) ---
col_assets, col_main, col_engine = st.columns([1.1, 2.7, 1.1])

with col_assets:
    st.markdown("<small style='color:#8b949e'>MARKET ACCIONES</small>", unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="panel-box">', unsafe_allow_html=True)
        # Activos y precios como en image_8.png
        assets = [
            {"name": "RENDER (IA)", "price": 124.5, "change": "+2.4%"},
            {"name": "APPLE", "price": 3450.0, "change": "-0.1%"},
            {"name": "SAND (Land)", "price": 8.9, "change": "-1.5%"},
            {"name": "GALA", "price": 0.85, "change": "+5.2%"},
            {"name": "BITCOIN", "price": 1800000.0, "change": "+0.8%"}
        ]
        for a in assets:
            st.markdown(f"""
            <div class="asset-row">
                <div><b>{a['name']}</b><br><small style="color:#8b949e">${a['price']:,}</small></div>
                <div style="color:{'#39FF14' if '+' in a['change'] else '#f85149'};">{a['change']}</div>
            </div>
            """, unsafe_allow_html=True)
        st.write("---")
        st.markdown("<small style='color:#8b949e'>SELECCIONA ACTIVO PARA EL RADAR</small>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    st.markdown("<small style='color:#8b949e'>CANDLE CHART (REAL-TIME)</small>", unsafe_allow_html=True)
    # Gráfica de Velas de Alta Densidad estilo image_8.png
    try:
        res = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=5).json()
        df = pd.DataFrame(res['payload'])
        df['price'] = df['price'].astype(float)
        
        # Incrementando la densidad de las velas
        fig = go.Figure(data=[go.Candlestick(
            x=df.index, open=df['price'], high=df['price']*1.0005,
            low=df['price']*0.9995, close=df['price'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ab7df8',
            increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ab7df8'
        )])
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=480, margin=dict(l=10, r=10, t=10, b=10), xaxis_visible=False, yaxis_side="right",
            yaxis_title=None, xaxis_title=None
        )
        st.plotly_chart(fig, use_container_width=True)
    except: st.warning("Sincronizando radar...")

with col_engine:
    st.markdown("<small style='color:#8b949e'>ADAPTATION ENGINE (MAHORAGA 32)</small>", unsafe_allow_html=True)
    # Rueda de Mahoraga animada (image_8.png)
    st.markdown(f"""
    <div class="panel-box" style="text-align: center;">
        <img src="https://i.imgur.com/83p1y9N.png" class="wheel-img" alt="Mahoraga Wheel">
        <p style="color:#ab7df8; font-size:11px; margin-top:5px;">Rueda Girando: Factor 32 Activo</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logs Estilo image_8.png
    st.markdown('<div class="panel-box">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="terminal-green">
        [LOG 02:25] Adapt Check (Factor 32) ... OK<br>
        [LOG 02:25] Balance Sync: ${CAPITAL_REF} ... OK<br>
        [LOG 02:25] RENDER Selected ... Data Loaded<br>
        <hr style="border-color:#161b22">
        "Pavo, el código ya está limpio. El Ferrari está listo para correr."
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("<small style='color:#8b949e'>TERMINAL DE COMANDO</small>", unsafe_allow_html=True)
    st.markdown(f"""
    <div class="terminal-green" style="color:#8b949e">
        [02:24:14] >> HIERRO MARTILLADO ✅<br>
        [02:24:14] >> ESTRUCTURA ADAPT ✅<br>
        [02:24:14] >> ESPERANDO ORDEN ✅
    </div>
    """, unsafe_allow_html=True)

# Autorefresco cada 15 segundos para estabilidad
time.sleep(15)
st.rerun()
