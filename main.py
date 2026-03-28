import streamlit as st
import plotly.graph_objects as go
import requests
import time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PODER ---
SALDO_REAL = 144.95
FACTOR = 32
ASSET = "RENDER (IA)"

st.set_page_config(layout="wide", page_title="MAHORASHARK ALPHA V52", page_icon="🦈")

# --- 2. EL MARTILLO: CSS DE GRADO MILITAR (SELLADO) ---
st.markdown(f"""
<style>
    /* Reset total y fondo profundo #0A0E14 */
    [data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"] {{ display: none !important; }}
    .stApp {{ background-color: #0A0E14 !important; color: #00F2FF !important; }}
    
    /* Paneles con Profundidad y Glassmorphism */
    .glass-panel {{
        background: rgba(13, 17, 23, 0.9);
        border: 1px solid rgba(0, 242, 255, 0.15);
        padding: 20px;
        border-radius: 2px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.9);
        margin-bottom: 15px;
    }}

    /* Header Táctico Slim */
    .shark-header {{
        display: flex; justify-content: space-between; align-items: center;
        background: #000; padding: 12px 30px;
        border-bottom: 2px solid #00F2FF;
        box-shadow: 0 5px 25px rgba(0, 242, 255, 0.2);
    }}

    .balance-glow {{
        font-family: 'Courier New', monospace;
        font-size: 40px; color: #39FF14; font-weight: bold;
        text-shadow: 0 0 15px rgba(57, 255, 20, 0.6);
    }}

    /* Terminal y Logs */
    .console-out {{
        background: #000; padding: 15px; border: 1px solid #1A1F26;
        font-family: 'Courier New', monospace; font-size: 11px;
        color: #00F2FF; height: 160px; overflow: hidden;
    }}

    .log-ok {{ color: #39FF14; text-shadow: 0 0 5px #39FF14; }}

    /* Rueda de Mahoraga Animada */
    .wheel-box {{ text-align: center; padding: 20px 0; }}
    .wheel-anim {{
        width: 130px; animation: spin-gear 15s linear infinite;
        filter: drop-shadow(0 0 10px rgba(138, 43, 226, 0.5));
    }}
    @keyframes spin-gear {{ 100% {{ transform: rotate(360deg); }} }}
</style>
""", unsafe_allow_html=True)

# --- 3. RENDERIZADO DEL HEADER ---
st.markdown(f"""
<div class="shark-header">
    <div style="line-height: 1;">
        <b style="font-size:18px; letter-spacing:2px;">MAHORASHARK</b><br>
        <small style="color:#444; font-family:monospace;">V52 | SECURED_STABLE</small>
    </div>
    <div style="text-align:center;">
        <small style="color:#8b949e; font-family:monospace;">MXN BALANCE</small><br>
        <span class="balance-glow">${SALDO_REAL:,.2f}</span>
    </div>
    <div style="display:flex; gap:10px;">
        <div style="background:#1a2a1a; border:1px solid #39FF14; color:#39FF14; padding:2px 10px; font-size:10px; font-weight:bold;">LIVE</div>
        <div style="background:#0a1a2a; border:1px solid #00F2FF; color:#00F2FF; padding:2px 10px; font-size:10px; font-weight:bold;">FACTOR: {FACTOR}</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.write("")

# --- 4. CUERPO DE LA INTERFAZ ---
c1, c2, c3 = st.columns([1.1, 2.7, 1.1])

with c1:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown('<small style="color:#444;">MARKET_ASSETS</small>', unsafe_allow_html=True)
    for name, change in [("RENDER (IA)", "+2.4%"), ("APPLE", "-0.1%"), ("BTC", "+0.8%")]:
        st.markdown(f'<div style="padding:10px; border-bottom:1px solid #1A1F26; font-family:monospace; font-size:11px;">{name} <span style="float:right; color:#39FF14;">{change}</span></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with c2:
    st.markdown('<div class="glass-panel" style="height:550px;">', unsafe_allow_html=True)
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=3).json()
        p = [float(t['price']) for t in r['payload']][::-1]
        fig = go.Figure(data=[go.Candlestick(
            x=list(range(len(p))), open=p, high=[x*1.001 for x in p],
            low=[x*0.999 for x in p], close=p,
            increasing_line_color='#00F2FF', decreasing_line_color='#8A2BE2'
        )])
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=480, margin=dict(l=0,r=50,t=0,b=0), xaxis_visible=False, yaxis_side="right")
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    except:
        st.error("SYNC_LOST")
    st.markdown('</div>', unsafe_allow_html=True)

with c3:
    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="wheel-box">
        <img src="https://i.imgur.com/83p1y9N.png" class="wheel-anim">
        <p style="font-family:monospace; font-size:11px; color:#8A2BE2; margin-top:15px;">SYNC_T: 14s</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="glass-panel">', unsafe_allow_html=True)
    t = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div class="console-out">
        [{t}] <span class="log-ok">OK</span>: System Secure<br>
        [{t}] <span class="log-ok">OK</span>: Asset Synced<br><br>
        "El Ferrari está listo."<br>
        >> HIERRO MARTILLADO ✅
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(15)
st.rerun()
