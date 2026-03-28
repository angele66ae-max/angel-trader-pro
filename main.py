import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. SETUP DE PODER ---
st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V60", page_icon="🦈")

# --- 2. CSS DE CLONACIÓN VISUAL (ESTILO GEMINI GENERATED) ---
st.markdown("""
<style>
    /* Fondo Azul Profundo / Negro */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { 
        background-color: #0b111a !important; 
        color: #e0e0e0 !important; 
        font-family: 'Inter', sans-serif;
    }
    
    /* PANELES DE CRISTAL (Glassmorphism) */
    .glass-card {
        background: rgba(16, 24, 39, 0.8);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 8px;
        padding: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
    }

    /* HEADER TÁCTICO */
    .header-container {
        display: flex; justify-content: space-between; align-items: center;
        padding: 15px 30px; background: rgba(10, 15, 25, 0.95);
        border-bottom: 2px solid #00F2FF; margin-bottom: 20px;
    }
    .balance-glow {
        color: #39FF14; font-size: 38px; font-weight: 800;
        text-shadow: 0 0 15px rgba(57, 255, 20, 0.6);
        font-family: 'Roboto Mono', monospace;
    }

    /* MARKET SELECTOR PULIDO */
    .market-item {
        padding: 10px; border-bottom: 1px solid rgba(255,255,255,0.05);
        display: flex; justify-content: space-between; font-size: 13px;
    }
    .market-item:hover { background: rgba(0, 242, 255, 0.1); cursor: pointer; }
    .selected-asset { border-left: 3px solid #00F2FF; background: rgba(0, 242, 255, 0.15); }

    /* TERMINAL DE GRADO MILITAR */
    .terminal-text {
        font-family: 'JetBrains Mono', monospace; font-size: 11px;
        color: #00F2FF; line-height: 1.5;
    }
    .status-ok { color: #39FF14; font-weight: bold; }

    /* RUEDA DE ADAPTACIÓN (ANIMACIÓN PURA) */
    .wheel-container { text-align: center; padding: 20px 0; }
    .adaptation-wheel {
        width: 170px; animation: spin 20s linear infinite;
        filter: drop-shadow(0 0 10px #8A2BE2);
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }
</style>
""", unsafe_allow_html=True)

# --- 3. BARRA DE NAVEGACIÓN (HEADER) ---
st.markdown(f"""
<div class="header-container">
    <div>
        <span style="color:#00F2FF; font-weight:900; font-size:22px; letter-spacing:3px;">MAHORASHARK ALPHA V60</span><br>
        <span style="color:#555; font-size:10px;">TACTICAL TRADING GUADAÑA</span>
    </div>
    <div style="text-align:center;">
        <span style="color:#8b949e; font-size:10px; letter-spacing:1px;">MXN BALANCE:</span><br>
        <span class="balance-glow">$144.95</span>
    </div>
    <div style="display:flex; gap:10px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:5px 15px; font-size:11px; font-weight:bold;">LIVE | ONLINE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:5px 15px; font-size:11px; font-weight:bold;">FACTOR: 32</div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- 4. ESTRUCTURA DE 3 COLUMNAS ---
col_side, col_main, col_engine = st.columns([1.1, 3, 1.2])

with col_side:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">MARKET ACCIONES</small>', unsafe_allow_html=True)
    st.markdown('<div style="background:#070b11; padding:10px; border:1px solid #00F2FF; margin:10px 0; font-size:12px;">SELECTED ASSET: <span style="color:#00F2FF;">RENDER (IA)</span></div>', unsafe_allow_html=True)
    
    assets = [
        ("RENDER", "+2.4%", True), ("APPLE", "-0.1%", False), 
        ("SAND", "-1.5%", False), ("GALA", "+5.2%", False),
        ("RENDER", " ", False), ("CHRA", " ", False), ("EMM", " ", False)
    ]
    
    for name, change, active in assets:
        cls = "selected-asset" if active else ""
        st.markdown(f'<div class="market-item {cls}"><span>{name}</span><span style="color:#39FF14;">{change}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    st.markdown('<div class="glass-card" style="height:620px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">CANDLE CHART - RENDER (IA) 1D</small>', unsafe_allow_html=True)
    
    # GENERACIÓN DE DATOS DE VELAS (Simulación para el clon)
    df = pd.DataFrame({
        'open': np.random.uniform(2100, 2300, 50),
        'high': np.random.uniform(2300, 2400, 50),
        'low': np.random.uniform(2000, 2100, 50),
        'close': np.random.uniform(2100, 2300, 50)
    })

    fig = go.Figure(data=[go.Candlestick(
        x=list(range(len(df))),
        open=df['open'], high=df['high'], low=df['low'], close=df['close'],
        increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2', # Colores Gemini
        increasing_fillcolor='rgba(0, 242, 255, 0.4)', decreasing_fillcolor='rgba(138, 43, 226, 0.7)'
    )])

    # Bandas de Bollinger (El "sombreado" que pediste)
    fig.add_trace(go.Scatter(y=df['high']+20, line=dict(color='rgba(0,242,255,0.1)', width=1), name="B-Upper"))
    fig.add_trace(go.Scatter(y=df['low']-20, line=dict(color='rgba(0,242,255,0.1)', width=1), fill='tonexty', fillcolor='rgba(0,242,255,0.02)'))

    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=550, margin=dict(l=10, r=10, t=10, b=10),
        xaxis_visible=False, yaxis_side="right",
        yaxis_gridcolor="rgba(255,255,255,0.05)"
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_engine:
    # ADAPTATION ENGINE
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">ADAPTATION ENGINE (MAHORAGA)</small>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wheel-container">
        <img src="https://i.imgur.com/83p1y9N.png" class="adaptation-wheel">
        <p style="color:#8A2BE2; font-size:12px; margin-top:15px; font-weight:bold;">SYNCING: 14s</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL SESS
    st.markdown('<div class="glass-card" style="margin-top:15px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">TERMINAL_LOGS</small>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-text">
        [{t}] <span class="status-ok">OK</span>: System Link Stable<br>
        [{t}] <span class="status-ok">OK</span>: Asset Synced (RENDER)<br>
        [{t}] <span class="status-ok">OK</span>: Adaptation Factor 32<br>
        <br>
        "El Ferrari está listo."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh para simular el "Ferrari" en marcha
time.sleep(10)
st.rerun()
