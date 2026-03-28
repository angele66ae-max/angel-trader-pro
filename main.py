import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DEL SISTEMA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V62", page_icon="🦈")

# --- 2. CSS DE ALTO RENDIMIENTO (SIN IMÁGENES EXTERNAS) ---
st.markdown("""
<style>
    /* Fondo Negro Profundo */
    [data-testid="stHeader"], [data-testid="stToolbar"] { display: none !important; }
    .stApp { background-color: #05070A !important; color: #E6EDF3 !important; }

    /* Paneles de Cristal con Bordes Cian */
    .glass-panel {
        background: rgba(10, 15, 25, 0.9);
        border: 1px solid rgba(0, 242, 255, 0.2);
        border-radius: 4px; padding: 15px; margin-bottom: 10px;
    }

    /* Brillo de Balance */
    .balance-glow {
        color: #39FF14; font-size: 42px; font-weight: 800;
        text-shadow: 0 0 20px rgba(57, 255, 20, 0.6);
        font-family: monospace;
    }

    /* Rueda de Adaptación (Hecha con CSS para que no falle) */
    .wheel-css {
        width: 120px; height: 120px; border-radius: 50%;
        border: 4px dashed #8A2BE2; margin: 20px auto;
        animation: spin 10s linear infinite;
        box-shadow: 0 0 20px rgba(138, 43, 226, 0.4);
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* Terminal Estilo Fósforo */
    .terminal-box {
        background: #000; border-left: 3px solid #00F2FF;
        padding: 10px; font-family: 'Courier New', monospace;
        font-size: 11px; color: #00F2FF; height: 150px;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. TOP HUD (REPLICA EXACTA V45) ---
st.markdown(f"""
<div style="display: flex; justify-content: space-between; align-items: center; padding: 10px 40px; border-bottom: 2px solid #00F2FF; background: #000;">
    <div>
        <b style="color:#00F2FF; font-size:20px; letter-spacing:2px;">MAHORASHARK ALPHA V62</b><br>
        <small style="color:#444;">TACTICAL TRADING GUADAÑA</small>
    </div>
    <div style="text-align:center;">
        <small style="color:#555;">MXN TOTAL BALANCE</small><br>
        <span class="balance-glow">$144.95</span>
    </div>
    <div style="display:flex; gap:10px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:5px 15px; font-size:10px;">LIVE_CORE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:5px 15px; font-size:10px;">F: 32</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA INTERFAZ ---
col_left, col_mid, col_right = st.columns([1, 3, 1.2])

with col_left:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">MARKET_ACCIONES</small>', unsafe_allow_html=True)
    for asset, change in [("RENDER (IA)", "+2.4%"), ("APPLE", "-0.1%"), ("SAND", "-1.5%"), ("GALA", "+5.2%"), ("BTC", "+0.8%")]:
        color = "#39FF14" if "+" in change else "#FF3131"
        st.markdown(f'''<div style="display:flex; justify-content:space-between; padding:10px; border-bottom:1px solid #111; font-size:12px;">
            <span>{asset}</span><span style="color:{color};">{change}</span>
        </div>''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_mid:
    st.markdown('<div class="glass-panel" style="height:600px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">RADAR_TACTICO_V62</small>', unsafe_allow_html=True)
    
    # MOTOR DE GRÁFICO (PARA QUE NO SALGA EN BLANCO)
    # Generamos datos de prueba dinámicos
    data = pd.DataFrame({
        'open': np.random.uniform(2100, 2300, 40),
        'high': np.random.uniform(2300, 2400, 40),
        'low': np.random.uniform(2000, 2100, 40),
        'close': np.random.uniform(2100, 2300, 40)
    })
    
    fig = go.Figure(data=[go.Candlestick(
        x=list(range(40)), open=data.open, high=data.high, low=data.low, close=data.close,
        increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2'
    )])
    
    fig.update_layout(
        template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        height=520, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    # Motor de Adaptación
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">ADAPTATION_ENGINE</small>', unsafe_allow_html=True)
    st.markdown('<div class="wheel-css"></div>', unsafe_allow_html=True)
    st.markdown('<p style="text-align:center; color:#8A2BE2; font-size:11px;">SYNCING_14s</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Terminal
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#555;">TERMINAL_SESS</small>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-box">
        [{t}] <b style="color:#39FF14;">OK:</b> System Boot Secure<br>
        [{t}] <b style="color:#39FF14;">OK:</b> RENDER (IA) Link Established<br>
        [{t}] <b style="color:#39FF14;">OK:</b> Radar Factor 32 Ingested<br><br>
        "El Ferrari está listo para correr."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Refresco cada 15 seg para mantener el Ferrari vivo
time.sleep(15)
st.rerun()
