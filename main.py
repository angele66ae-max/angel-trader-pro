import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL SISTEMA (SHARK CORE) ---
st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V46", page_icon="🦈")

# --- 2. EL MARTILLO: CSS "GLOW UI" (ESTÉTICA CYBER-INSTITUTIONAL) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&family=Inter:wght@400;900&display=swap');

    /* Reset y Fondo Deep Navy #05070A */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #05070A !important; color: #E6EDF3 !important; font-family: 'Inter', sans-serif; }

    /* PANELES DE CRISTAL TÁCTICO */
    .glass-card {
        background: rgba(10, 15, 25, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.15);
        border-radius: 4px;
        padding: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8);
        backdrop-filter: blur(12px);
        margin-bottom: 12px;
    }

    /* BARRA SUPERIOR (TOP HUD) */
    .top-hud {
        display: flex; justify-content: space-between; align-items: center;
        padding: 10px 40px; background: #000; border-bottom: 2px solid #00F2FF;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.2);
    }
    .balance-neon {
        font-family: 'JetBrains Mono', monospace; font-size: 36px; color: #39FF14; font-weight: 800;
        text-shadow: 0 0 15px rgba(57, 255, 20, 0.5);
    }

    /* BOTONES DE ACTIVOS (CONTROL DE GUERRA) */
    .asset-btn {
        background: rgba(0, 242, 255, 0.05); padding: 8px; border: 1px solid rgba(0,242,255,0.1);
        margin-bottom: 6px; display: flex; justify-content: space-between; font-size: 11px;
    }
    .asset-active { border-left: 4px solid #00F2FF; background: rgba(0, 242, 255, 0.15); }

    /* RUEDA DE ADAPTACIÓN (ANIMACIÓN MAHORAGA) */
    .wheel-box { text-align: center; padding: 15px 0; }
    .wheel-svg {
        width: 160px; animation: spin-gear 18s linear infinite;
        filter: drop-shadow(0 0 12px rgba(138, 43, 226, 0.7));
    }
    @keyframes spin-gear { 100% { transform: rotate(360deg); } }

    /* TERMINAL DE LOGS */
    .terminal-output {
        font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #00F2FF;
        height: 140px; overflow-y: hidden; line-height: 1.5; padding: 10px;
        background: rgba(0,0,0,0.5); border-left: 2px solid #00F2FF;
    }
    .log-tag { color: #39FF14; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

# --- 3. BARRA SUPERIOR: MAHORASHARK ALPHA V46 ---
st.markdown(f"""
<div class="top-hud">
    <div style="display:flex; align-items:center; gap:15px;">
        <span style="font-size:30px;">🦈</span>
        <div style="line-height:1;">
            <span style="font-weight:900; letter-spacing:4px; font-size:18px; color:#00F2FF;">MAHORASHARK ALPHA V46</span><br>
            <span style="font-size:9px; color:#555; letter-spacing:2px;">TACTICAL TRADING GUADAÑA</span>
        </div>
    </div>
    <div style="text-align:center;">
        <small style="color:#8b949e; letter-spacing:1px; font-size:9px;">MXN BALANCE</small><br>
        <span class="balance-neon">$142.00</span>
    </div>
    <div style="display:flex; gap:12px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:3px 12px; font-size:10px; font-weight:bold;">LIVE | ONLINE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:3px 12px; font-size:10px; font-weight:bold;">FACTOR: 32</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. ESTRUCTURA DE 3 COLUMNAS ---
c1, c2, c3 = st.columns([1, 2.8, 1.1])

# COLUMNA 1: CONTROL DE ACTIVOS
with c1:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555; letter-spacing:1px;">MARKET ACCIONES</small>', unsafe_allow_html=True)
    st.markdown(f'''
    <div style="background:#000; padding:10px; border:1px solid #00F2FF; margin:10px 0;">
        <small style="color:#555;">SELECTED ASSET:</small><br>
        <b style="color:#00F2FF; font-size:14px;">RENDER (IA) - $2,138.27</b>
    </div>
    ''', unsafe_allow_html=True)
    
    assets = [("RENDER", "+2.4%", True), ("APPLE", "-0.1%", False), ("SAND", "-1.5%", False), ("GALA", "+5.2%", False), ("CHRA", " ", False), ("EMM", " ", False), ("GETI", " ", False)]
    for n, ch, active in assets:
        cls = "asset-active" if active else ""
        st.markdown(f'<div class="asset-btn {cls}"><span>{n}</span><span style="color:#39FF14;">{ch}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# COLUMNA 2: EL CORAZÓN (CHART ENGINE)
with c2:
    st.markdown('<div class="glass-card" style="height:580px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">CANDLE CHART - RENDER (IA) · 1D · PBRINGE</small>', unsafe_allow_html=True)
    
    # Simulación de velas neón
    df = pd.DataFrame({'o':[10,12,11,14,13], 'h':[13,15,12,16,15], 'l':[9,11,10,13,12], 'c':[12,11,14,13,16]})
    fig = go.Figure(data=[go.Candlestick(
        x=[1,2,3,4,5], open=df.o, high=df.h, low=df.l, close=df.c,
        increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
        increasing_fillcolor='rgba(0, 242, 255, 0.4)', decreasing_fillcolor='rgba(138, 43, 226, 0.7)'
    )])
    
    # Sombreado Bollinger
    fig.add_trace(go.Scatter(y=[15,16,15,17,16], line=dict(color='rgba(0,242,255,0.05)', width=1), fill='tonexty', fillcolor='rgba(0,242,255,0.01)'))

    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=500, margin=dict(l=0, r=40, t=10, b=0), xaxis_visible=False, yaxis_side="right",
        yaxis_gridcolor="rgba(255,255,255,0.02)"
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

# COLUMNA 3: ADAPTATION ENGINE
with c3:
    # Módulo Rueda
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">ADAPTATION ENGINE (MAHORAGA 32)</small>', unsafe_allow_html=True)
    st.markdown("""
    <div class="wheel-box">
        <img src="https://i.imgur.com/83p1y9N.png" class="wheel-svg">
        <p style="color:#8A2BE2; font-size:11px; margin-top:10px; font-weight:bold; letter-spacing:2px;">NEXT ADAPTATION CHECK: 14s</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Módulo P/L
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown(f"""
    <small style="color:#555;">PROFIT / LOSS TRACKER</small><br>
    <span style="font-size:18px; color:#39FF14; font-weight:bold;">SESSION P/L: +$12.50 (+8.8%)</span><br>
    <small style="color:#444; font-size:9px;">TRADE HISTORY: last 10 steps</small>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Módulo Terminal
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">TERMINAL</small>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-output">
        [{t}] <span class="log-tag">[OK]</span> Adapt Check (Factor 32)<br>
        [{t}] <span class="log-tag">[OK]</span> RENDER selected ... Data Loaded<br>
        [{t}] <span class="log-tag">[OK]</span> SMA/EMA Indicators Sync<br>
        [{t}] <span class="log-tag">[OK]</span> Bollinger Bands 30090 ... OK<br>
        <br>
        >> EL FERRARI ESTÁ LISTO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. CICLO DE VIDA (14s) ---
time.sleep(14)
st.rerun()
