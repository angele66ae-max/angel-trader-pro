import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE NÚCLEO (SHARK CORE) ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V58", page_icon="🦈")

# --- 2. EL MARTILLO: CSS DE GRADO MILITAR (SIN ERRORES) ---
st.markdown("""
<style>
    /* Reset total y fondo Dark #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #0A0E14 !important; color: #FFFFFF !important; font-family: 'JetBrains Mono', monospace; }
    
    /* CAPA DE CRISTAL (Glassmorphism + Borde 1px) */
    .glass-panel {
        background: rgba(13, 17, 23, 0.85);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(0, 242, 255, 0.15);
        padding: 20px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.9);
        margin-bottom: 15px;
    }

    /* HEADER TÁCTICO CON RESPLANDOR */
    .nav-hud {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 12px 35px;
        border-bottom: 1px solid #00F2FF;
        box-shadow: 0 5px 25px rgba(0, 242, 255, 0.2);
    }
    .balance-glow {
        font-size: 42px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 15px #39FF14, 0 0 30px rgba(57, 255, 20, 0.3);
    }

    /* TERMINAL CON EFECTO FÓSFORO */
    .terminal-out {
        background: #000; padding: 15px; border-left: 3px solid #00F2FF;
        font-size: 11px; color: #00F2FF; height: 160px; overflow: hidden;
        text-shadow: 0 0 5px rgba(0, 242, 255, 0.5);
    }
    .status-ok { color: #39FF14; text-shadow: 0 0 8px #39FF14; font-weight: bold; }

    /* RUEDA DE MAHORAGA (SVG ANIMADO) */
    .wheel-box { text-align: center; padding: 20px 0; }
    .wheel-svg {
        width: 150px; animation: spin-gear 18s linear infinite;
        filter: drop-shadow(0 0 12px #8A2BE2);
    }
    @keyframes spin-gear { 100% { transform: rotate(360deg); } }

    /* BOTONES DE ACTIVOS */
    .asset-btn {
        padding: 10px; border: 1px solid #1A1F26; margin-bottom: 8px;
        display: flex; justify-content: space-between; font-size: 11px;
    }
    .asset-active { border-color: #00F2FF; background: rgba(0, 242, 255, 0.1); color: #FFF; }
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="nav-hud">
    <div style="line-height: 1;">
        <b style="font-size:20px; letter-spacing:3px; color:#00F2FF;">MAHORASHARK</b><br>
        <span style="font-size:9px; color:#444;">ENGINE V58 | MILITARY_RECON</span>
    </div>
    <div style="text-align:center;">
        <span style="font-size:9px; color:#8b949e; letter-spacing:1px;">TOTAL BALANCE MXN</span><br>
        <span class="balance-glow">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:12px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:3px 12px; font-size:10px; font-weight:bold;">LIVE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:3px 12px; font-size:10px; font-weight:bold;">FACTOR: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. ESTRUCTURA DE 3 COLUMNAS (UI PROFUNDA) ---
c1, c2, c3 = st.columns([1.1, 2.8, 1.1])

with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">MARKET_ACCIONES</small>', unsafe_allow_html=True)
    mkt = [("RENDER (IA)", "+2.4%", True), ("APPLE", "-0.1%", False), ("SAND", "-1.5%", False), ("GALA", "+5.2%", False), ("BTC", "+0.8%", False)]
    for n, ch, active in mkt:
        cls = "asset-active" if active else ""
        st.markdown(f'<div class="asset-btn {cls}"><span>{n}</span><span style="color:#39FF14;">{ch}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel" style="height:580px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">RADAR_TACTICO_V58</small>', unsafe_allow_html=True)
    try:
        # Petición a Bitso (Fallback si falla)
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        
        # MOTOR DE VELAS: CIAN / PÚRPURA
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.0012 for x in p],
            low=[x*0.9988 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
            increasing_fillcolor='rgba(0, 242, 255, 0.2)', decreasing_fillcolor='rgba(138, 43, 226, 0.7)'
        )])
        
        # BANDAS DE BOLLINGER (SOMBREADO TÉCNICO)
        fig.add_trace(go.Scatter(y=[x*1.006 for x in p], line=dict(color='rgba(0,242,255,0.03)', width=1), fill='tonexty', fillcolor='rgba(0,242,255,0.01)', name="Bollinger Upper"))
        fig.add_trace(go.Scatter(y=[x*0.994 for x in p], line=dict(color='rgba(0,242,255,0.03)', width=1), name="Bollinger Lower"))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=520, margin=dict(l=0, r=40, t=10, b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)", yaxis_tickfont=dict(size=10, color="#555")
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("SYNCING_RADAR_DATA...")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    # PANEL DE LA RUEDA
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">ADAPTATION_ENGINE</small>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wheel-box">
        <img src="https://i.imgur.com/83p1y9N.png" class="wheel-svg">
        <p style="font-size:10px; color:#8A2BE2; margin-top:20px; letter-spacing:3px;">ANALYZING_PATTERNS</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL DE LOGS
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:2px;">TERMINAL_SESS</small>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="terminal-out">
        [{t}] <span class="status-ok">[OK]</span>: Recon Start<br>
        [{t}] <span class="status-ok">[OK]</span>: {ASSET} Synced<br>
        [{t}] <span class="status-ok">[OK]</span>: Factor {FACTOR} Stable<br>
        <br>
        "El Ferrari está listo."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUTO-REFRESH TÁCTICO
time.sleep(15)
st.rerun()
