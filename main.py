import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. NÚCLEO DE DATOS ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V60", page_icon="🦈")

# --- 2. CSS DE ALTA INGENIERÍA (CLONACIÓN VISUAL) ---
st.markdown("""
<style>
    /* Fondo Ultra Dark y Reset */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #05070A !important; color: #E6EDF3 !important; font-family: 'Inter', sans-serif; }
    
    /* EFECTO CRISTAL Y BORDES NEÓN SUTILES */
    .glass-panel {
        background: rgba(13, 17, 23, 0.7);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 4px;
        padding: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        margin-bottom: 15px;
    }

    /* HEADER HUD (NAVBAR) */
    .nav-hud {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 12px 40px;
        border-bottom: 1px solid rgba(0, 242, 255, 0.5);
        box-shadow: 0 0 30px rgba(0, 242, 255, 0.1);
    }
    .main-balance {
        font-family: 'JetBrains Mono', monospace;
        font-size: 42px; color: #39FF14; font-weight: 800;
        text-shadow: 0 0 20px rgba(57, 255, 20, 0.5), 0 0 40px rgba(57, 255, 20, 0.2);
    }

    /* TERMINAL FÓSFORO (LOGS) */
    .terminal-box {
        background: #000; padding: 15px; border-left: 2px solid #00F2FF;
        font-family: 'JetBrains Mono', monospace; font-size: 10px;
        color: #00F2FF; height: 180px; overflow: hidden;
        line-height: 1.6;
    }
    .log-ok { color: #39FF14; text-shadow: 0 0 8px #39FF14; }

    /* RUEDA DE ADAPTACIÓN (SVG ANIMADO PRO) */
    .wheel-container { text-align: center; padding: 25px 0; }
    .mahoraga-wheel {
        width: 180px; animation: spin-gear 25s linear infinite;
        filter: drop-shadow(0 0 15px rgba(138, 43, 226, 0.6));
    }
    @keyframes spin-gear { 100% { transform: rotate(360deg); } }

    /* MARKET SELECTOR */
    .market-row {
        display: flex; justify-content: space-between; padding: 12px;
        border-bottom: 1px solid rgba(255,255,255,0.03); font-size: 11px;
    }
    .market-active { background: rgba(0, 242, 255, 0.1); border-left: 3px solid #00F2FF; }
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="nav-hud">
    <div style="line-height: 1;">
        <span style="letter-spacing:5px; font-weight:900; font-size:20px; color:#00F2FF;">MAHORASHARK</span><br>
        <small style="color:#444; font-family:monospace; font-size:10px;">TACTICAL HUD V60.0 | LIVE</small>
    </div>
    <div style="text-align:center;">
        <small style="color:#8b949e; letter-spacing:2px; font-size:9px;">TOTAL MXN BALANCE</small><br>
        <span class="main-balance">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:15px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:2px 12px; font-size:10px; font-weight:bold;">ENGINE_ACTIVE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:2px 12px; font-size:10px; font-weight:bold;">F: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA INTERFAZ (DENSIDAD DE INFO) ---
col_mkt, col_chart, col_engine = st.columns([1, 2.8, 1])

with col_mkt:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#444; letter-spacing:2px; margin-bottom:15px;">MARKET_ASSETS</p>', unsafe_allow_html=True)
    assets = [("RENDER (IA)", "+2.4%", True), ("BTC", "+0.8%", False), ("SAND", "-1.5%", False), ("GALA", "+5.2%", False), ("APPLE", "-0.1%", False)]
    for n, ch, active in assets:
        active_cls = "market-active" if active else ""
        st.markdown(f'<div class="market-row {active_cls}"><span>{n}</span><span style="color:#39FF14;">{ch}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_chart:
    st.markdown('<div class="glass-panel" style="height:580px;">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#444; letter-spacing:2px;">RADAR_VELAS_V60</p>', unsafe_allow_html=True)
    try:
        # Petición real para que el radar se mueva
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # MOTOR DE VELAS: CIAN (#00F2FF) / PÚRPURA (#8A2BE2)
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.0012 for x in p],
            low=[x*0.9988 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
            increasing_fillcolor='rgba(0, 242, 255, 0.3)', decreasing_fillcolor='rgba(138, 43, 226, 0.8)'
        )])
        
        # BANDAS DE BOLLINGER (SOMBREADO)
        fig.add_trace(go.Scatter(y=[x*1.007 for x in p], line=dict(color='rgba(0,242,255,0.05)', width=1), fill='tonexty', fillcolor='rgba(0,242,255,0.02)'))
        fig.add_trace(go.Scatter(y=[x*0.993 for x in p], line=dict(color='rgba(0,242,255,0.05)', width=1)))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=500, margin=dict(l=0, r=40, t=10, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("RADAR_SYNC_LOST")
    st.markdown('</div>', unsafe_allow_html=True)

with col_engine:
    # ADAPTATION ENGINE PANEL
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<p style="font-size:10px; color:#444; letter-spacing:2px;">ENGINE_CORE</p>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wheel-container">
        <img src="https://i.imgur.com/83p1y9N.png" class="mahoraga-wheel">
        <p style="font-family:monospace; font-size:10px; color:#8A2BE2; margin-top:20px; letter-spacing:3px;">MAHORAGA_LEVEL: {FACTOR}</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL PANEL
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-box">
        [{t}] <span class="log-ok">[OK]</span>: HUD_SYNC_SUCCESS<br>
        [{t}] <span class="log-ok">[OK]</span>: {ASSET} RADAR ACTIVE<br>
        [{t}] <span class="log-ok">[OK]</span>: ENGINE_V60_STABLE<br>
        <br>
        "El Ferrari está listo."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUTO-REFRESH TÁCTICO
time.sleep(15)
st.rerun()
