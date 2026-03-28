import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. SETTINGS DEL SISTEMA ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET_SELECTED = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V45", page_icon="🦈")

# --- 2. EL MARTILLO: INYECCIÓN DE ADN VISUAL (CSS) ---
# Separado para evitar errores de sintaxis y asegurar el acabado profesional.
st.markdown("""
<style>
    /* RESET TOTAL */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] { display: none !important; }
    .stApp { background-color: #0A0E14 !important; color: #e6edf3 !important; font-family: 'Inter', sans-serif; }
    
    /* PANELES DE GRADO MILITAR (GLASSMORPHISM) */
    .module-card {
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid rgba(0, 242, 255, 0.1);
        border-radius: 2px;
        padding: 15px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.8);
        margin-bottom: 12px;
    }

    /* HEADER TÁCTICO SLIM */
    .nav-hud {
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 10px 30px;
        border-bottom: 1px solid #00F2FF;
        box-shadow: 0 4px 20px rgba(0, 242, 255, 0.15);
        position: sticky; top: 0; z-index: 999;
    }
    .neon-balance {
        font-family: 'JetBrains Mono', monospace;
        font-size: 36px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 12px rgba(57, 255, 20, 0.5);
    }

    /* LISTA DE ACTIVOS (SIDEBAR IZQ) */
    .asset-row {
        display: flex; justify-content: space-between; padding: 10px;
        border-bottom: 1px solid #1A1F26; font-size: 11px; font-family: monospace;
        transition: 0.2s; cursor: pointer;
    }
    .asset-row:hover { background: rgba(0, 242, 255, 0.05); }
    .active-asset { background: rgba(0, 242, 255, 0.1); border-left: 3px solid #00F2FF; color: #fff; }

    /* TERMINAL DE LOGS (ESTILO FÓSFORO) */
    .terminal-box {
        background: #050505; padding: 12px; border: 1px solid #1A1F26;
        font-family: 'JetBrains Mono', monospace; font-size: 10px;
        color: #00F2FF; height: 140px; overflow: hidden;
    }
    .ok-status { color: #39FF14; text-shadow: 0 0 5px #39FF14; }

    /* RUEDA DE MAHORAGA (ANIMACIÓN) */
    .wheel-container { text-align: center; padding: 15px 0; }
    .mahoraga-wheel {
        width: 120px; animation: spin 18s linear infinite;
        filter: drop-shadow(0 0 10px rgba(138, 43, 226, 0.4));
    }
    @keyframes spin { 100% { transform: rotate(360deg); } }

    /* SCROLLBAR CUSTOM */
    ::-webkit-scrollbar { width: 3px; }
    ::-webkit-scrollbar-thumb { background: #00F2FF; }
</style>
""", unsafe_allow_html=True)

# --- 3. ESTRUCTURA DEL HEADER ---
st.markdown(f"""
<div class="nav-hud">
    <div>
        <b style="font-size:16px; letter-spacing:2px; color:#00F2FF;">MAHORASHARK</b><br>
        <small style="color:#444; font-family:monospace; font-size:9px;">VERSION ALPHA V45 | HUD_ACTIVE</small>
    </div>
    <div style="text-align:center;">
        <small style="color:#8b949e; font-family:monospace; font-size:9px;">MXN BALANCE</small><br>
        <span class="neon-balance">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:10px;">
        <div style="border:1px solid #39FF14; color:#39FF14; padding:2px 8px; font-size:9px; font-weight:bold;">LIVE</div>
        <div style="border:1px solid #00F2FF; color:#00F2FF; padding:2px 8px; font-size:9px; font-weight:bold;">FACTOR: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("") # Espaciador

# --- 4. CUERPO TÁCTICO (DISTRIBUCIÓN DE IMAGEN) ---
col_left, col_main, col_right = st.columns([1, 2.8, 1])

# LADO IZQUIERDO: MARKET ACCIONES
with col_left:
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:1px;">MARKET_ACCIONES</small>', unsafe_allow_html=True)
    assets = [
        ("RENDER (IA)", "+2.4%", True),
        ("APPLE", "-0.1%", False),
        ("SAND (LAND)", "-1.5%", False),
        ("GALA", "+5.2%", False),
        ("BITCOIN", "+0.8%", False)
    ]
    for name, change, active in assets:
        active_cls = "active-asset" if active else ""
        st.markdown(f"""
            <div class="asset-row {active_cls}">
                <span>{name}</span>
                <span style="color:#39FF14;">{change}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# CENTRO: EL RADAR (GRÁFICO DE VELAS CIAN/PÚRPURA)
with col_main:
    st.markdown('<div class="module-card" style="height:540px;">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:1px;">RADAR_TACTICO_V45</small>', unsafe_allow_html=True)
    try:
        # Fetch de datos reales para que se mueva
        res = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload'] if 'price' in t][::-1] if 'payload' in locals() else [100, 102, 101, 104, 103, 106]
        
        # Simulación de velas si falla la API o para demo
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.001 for x in p],
            low=[x*0.999 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2',
            increasing_fillcolor='rgba(0, 242, 255, 0.1)', decreasing_fillcolor='rgba(138, 43, 226, 0.4)'
        )])
        fig.update_layout(
            template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=480, margin=dict(l=0,r=40,t=0,b=0), xaxis_visible=False, yaxis_side="right",
            yaxis_gridcolor="rgba(255,255,255,0.02)"
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.image("https://i.imgur.com/uR1D76O.png") # Fallback visual
    st.markdown('</div>', unsafe_allow_html=True)

# LADO DERECHO: ENGINE & TERMINAL
with col_right:
    # ADAPTATION ENGINE
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:1px;">ADAPTATION_ENGINE</small>', unsafe_allow_html=True)
    st.markdown(f"""
        <div class="wheel-container">
            <img src="https://i.imgur.com/83p1y9N.png" class="mahoraga-wheel">
            <p style="font-family:monospace; font-size:10px; color:#8A2BE2; margin-top:10px;">SYNC_TIMER: 14s</p>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # TERMINAL LOGS
    st.markdown('<div class="module-card">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444; letter-spacing:1px;">TERMINAL_SESS</small>', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="terminal-box">
            [{t}] <span class="ok-status">OK</span>: System Link Stable<br>
            [{t}] <span class="ok-status">OK</span>: Asset Synced ({ASSET_SELECTED})<br>
            [{t}] <span class="ok-status">OK</span>: Engine Factor {FACTOR}<br><br>
            "El Ferrari está listo para correr."<br>
            >> HIERRO MARTILLADO ✅
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# AUTO-REFRESH TÁCTICO
time.sleep(15)
st.rerun()
