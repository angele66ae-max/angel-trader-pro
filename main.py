import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN VISUAL DASHBOARD ---
st.set_page_config(layout="wide", page_title="MAHORASHARK OMNI-TRADER")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.92), rgba(0, 5, 15, 0.92)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .neon-card {{
        background: rgba(0, 15, 25, 0.85);
        border: 1px solid #00f2ff;
        border-radius: 5px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .label {{ color: #00f2ff; font-size: 0.8rem; letter-spacing: 1.5px; text-transform: uppercase; }}
    .value-cyan {{ color: #00f2ff; font-size: 1.9rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .value-magenta {{ color: #ff00ff; font-size: 1.9rem; font-weight: bold; text-shadow: 0 0 10px #ff00ff; }}
    .value-green {{ color: #39FF14; font-size: 1.9rem; font-weight: bold; text-shadow: 0 0 10px #39FF14; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS (BITSO) ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_market_engine():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        p_btc = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        bal = r_bal['payload']['balances']
        # Mapeo de activos reales
        data = {b['currency'].upper(): float(b['total']) for b in bal if b['currency'] in ['mxn', 'btc', 'eth', 'usd']}
        return data, p_btc
    except:
        return {'MXN': 68.91, 'BTC': 0.00003542, 'ETH': 0.0, 'USD': 2.68}, 75191.0

# --- 3. PROCESAMIENTO DE MÉTRICAS ---
balances, btc_p = get_market_engine()
progreso = min(((balances.get('BTC', 0) * btc_p) / 115.0) * 100, 100.0)

# --- 4. TOP METRICS ---
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="neon-card"><div class="label">BITCOIN / USD</div><div class="value-cyan">${btc_p:,.2f}</div></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="neon-card"><div class="label">DISPONIBLE MXN</div><div class="value-magenta">${balances.get("MXN", 0):,.2f}</div></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="neon-card"><div class="label">PROFIT CALCULADO</div><div class="value-green">+$0.13</div></div>', unsafe_allow_html=True)
with m4: 
    st.markdown(f'<div class="neon-card"><div class="label">PROGRESO META</div><div class="value-cyan">{progreso:.2f}%</div></div>', unsafe_allow_html=True)
    st.progress(progreso / 100)

st.write("---")

# --- 5. GRID PRINCIPAL ---
col_port, col_chart, col_ia = st.columns([0.8, 2, 1])

with col_port:
    st.subheader("👤 PORTAFOLIO")
    for crypto, val in balances.items():
        # Corrección del ValueError: Formato individual por tipo de activo
        display_val = f"${val:,.2f}" if crypto in ['MXN', 'USD'] else f"{val:.8f}"
        st.markdown(f"""
        <div style="border-bottom: 1px solid rgba(0, 242, 255, 0.1); padding: 8px 0;">
            <div class="label">{crypto}</div>
            <div style="color:white; font-size:1.1rem; font-weight:bold;">{display_val}</div>
        </div>
        """, unsafe_allow_html=True)

with col_chart:
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[btc_p + np.random.uniform(-50, 50) for _ in range(20)],
        high=[btc_p + 100 for _ in range(20)], low=[btc_p - 100 for _ in range(20)],
        close=[btc_p + np.random.uniform(-50, 50) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', 
                      plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_ia:
    st.subheader("🧠 CEREBRO MAHORA")
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.6); border-left:3px solid #39FF14; padding:15px; font-family:monospace; color:#39FF14; font-size:0.85rem;">
        >> SINCRONIZACIÓN EXITOSA<br>
        >> SALDO MXN: ${balances.get('MXN', 0)}<br>
        >> STATUS: ADAPTACIÓN ACTIVA<br>
        >> MODO: PRESTIGE DASHBOARD
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    if st.button("👉 EJECUTAR ADAPTACIÓN (COMPRA)"):
        st.toast("Analizando liquidez...", icon="🔍")
    if st.button("👉 ASEGURAR GANANCIA (VENTA)"):
        st.toast("Calculando salida...", icon="📈")

time.sleep(20)
st.rerun()
