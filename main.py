import streamlit as st
import plotly.graph_objects as go
import requests
from datetime import datetime
import time

# --- 1. DATOS REALES (DE TU CAPTURA) ---
BALANCE_ACTUAL = 144.95 
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45")

# --- 2. DESIGN SYSTEM (ARQUITECTURA DE COLOR) ---
st.markdown(f"""
<style>
    /* Fondo Primario: #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"] {{display: none !important;}}
    .stApp {{ background-color: #0A0E14 !important; color: #00F2FF !important; font-family: 'Inter', sans-serif; }}
    
    /* Header Estrecho */
    .header-tactical {{
        display: flex; justify-content: space-between; align-items: center;
        background-color: #000; padding: 5px 20px; border-bottom: 1px solid #00F2FF;
    }}
    .balance-main {{ font-size: 32px; color: #00FF00; font-weight: 700; text-shadow: 0 0 15px #00FF00; }}
    .badge {{ background: #1a2a1a; color: #00FF00; border: 1px solid #00FF00; padding: 1px 6px; border-radius: 3px; font-size: 9px; font-weight: bold; margin-left: 5px; }}

    /* Paneles Cyberpunk */
    .panel {{ border: 1px solid #00F2FF33; background: #0A0E14; padding: 10px; margin-bottom: 10px; }}
    .panel-label {{ font-size: 10px; color: #555; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 10px; }}
    
    /* Terminal de Logs Monospace */
    .terminal-box {{ font-family: 'Courier New', monospace; font-size: 10px; color: #00F2FF; background: #000; padding: 8px; border: 1px solid #00F2FF22; }}
    .log-ok {{ color: #00FF00; }}

    /* Rueda de Adaptación (Rotación Z) */
    .wheel-rotate {{ width: 100px; height: 100px; margin: 0 auto; animation: spin 8s linear infinite; }}
    @keyframes spin {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="header-tactical">
    <div style="line-height: 1;">
        <span style="font-weight:bold; font-size:16px; letter-spacing:-1px;">🦈 MAHORASHARK ALPHA V45</span><br>
        <span style="font-size:9px; color:#444;">TACTICAL TRADING GUADAÑA | SHARK HUD</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:9px; color:#fff;">MXN BALANCE:</span><br>
        <span class="balance-main">${BALANCE_ACTUAL:,.2f}</span>
    </div>
    <div style="display:flex;">
        <span class="badge">LIVE</span><span class="badge">ONLINE</span><span class="badge" style="color:#00F2FF; border-color:#00F2FF;">FACTOR: {FACTOR}</span>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. ESTRUCTURA DE 3 COLUMNAS (LAYOUT TÉCNICO) ---
c1, c2, c3 = st.columns([1, 2.8, 1])

with c1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">MARKET ACCIONES</div>', unsafe_allow_html=True)
    st.markdown(f'<div style="border:1px solid #00F2FF; padding:5px; font-size:11px;">SELECTED: {ASSET}</div>', unsafe_allow_html=True)
    
    assets = ["RENDER", "APPLE", "SAND", "GALA", "BERM", "OTHERS", "SPLI", "RWIH"]
    sub_cols = st.columns(2)
    for i, a in enumerate(assets):
        with sub_cols[i % 2]:
            active = "background:#00F2FF; color:#000;" if a == "RENDER" else "background:#0d1117;"
            st.markdown(f'<div style="{active} border:1px solid #00F2FF33; text-align:center; padding:5px; font-size:10px; margin-top:5px;">{a}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="panel" style="height:500px;">', unsafe_allow_html=True)
    st.markdown('<div class="panel-label">CANDLE CHART (REAL-TIME)</div>', unsafe_allow_html=True)
    try:
        # Simulación de velas con colores de tu Design System
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        prices = [float(t['price']) for t in r['payload']][::-1]
        
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(prices))), open=prices, high=[p*
