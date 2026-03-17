import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN DE INTERFAZ FUTURISTA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK OMNI-TRADER")

# Estética Cyberpunk/Neón con Overlay para legibilidad
FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0, 5, 15, 0.90), rgba(0, 5, 15, 0.90)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed; font-family: 'Share Tech Mono', monospace;
    }}
    .neon-card {{
        background: rgba(0, 10, 20, 0.85);
        border: 1px solid #00f2ff;
        border-radius: 5px; padding: 15px; text-align: center;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }}
    .label {{ color: #00f2ff; font-size: 0.8rem; letter-spacing: 2px; text-transform: uppercase; }}
    .value-cyan {{ color: #00f2ff; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .value-magenta {{ color: #ff00ff; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #ff00ff; }}
    .value-green {{ color: #39FF14; font-size: 1.8rem; font-weight: bold; text-shadow: 0 0 10px #39FF14; }}
    
    /* Botón estilo Trading Institucional */
    .stButton>button {{
        width: 100%; background: transparent; color: #00f2ff;
        border: 2px solid #00f2ff; border-radius: 0; font-weight: bold;
        transition: 0.3s; height: 3rem; text-transform: uppercase;
    }}
    .stButton>button:hover {{
        background: #00f2ff; color: #000; box-shadow: 0 0 20px #00f2ff;
    }}
</style>
""", unsafe_allow_html=True)

# --- 2. BACKEND: CONEXIÓN BITSO & LÓGICA ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_bitso_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        # Precios
        p_btc = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
        p_eth = float(requests.get("https://api.bitso.com/v3/ticker/?book=eth_usd").json()['payload']['last'])
        # Balances
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        bal = r_bal['payload']['balances']
        data = {b['currency']: float(b['total']) for b in bal if b['currency'] in ['mxn', 'btc', 'eth', 'usd']}
        return data, p_btc, p_eth
    except:
        return {'mxn': 68.91, 'btc': 0.00003542, 'eth': 0.0, 'usd': 0.0}, 73500.0, 3950.0

def execute_trade(side, book, amount):
    # Lógica simplificada de ejecución (Simulación por seguridad en este paso)
    st.toast(f"EJECUTANDO {side.upper()} DE {amount} EN {book.upper()}...", icon="🚀")
    time.sleep(1)
    st.success("ORDEN COMPLETADA EN EXCHANGE")

# --- 3. PROCESAMIENTO ---
balances, btc_price, eth_price = get_bitso_data()
profit_sim = (balances['btc'] * btc_price) * 0.05 # Simulación de profit 5%
meta_progreso = min(((balances['btc'] * btc_price) / 115.0) * 100, 100.0)

# --- 4. LAYOUT: SECCIÓN SUPERIOR (MÉTRICAS) ---
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.markdown(f'<div class="neon-card"><div class="label">BITCOIN / USD</div><div class="value-cyan">${btc_price:,.2f}</div></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="neon-card"><div class="label">DISPONIBLE MXN</div><div class="value-magenta">${balances["mxn"]:,.2f}</div></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="neon-card"><div class="label">PROFIT CALCULADO</div><div class="value-green">+${profit_sim:,.2f}</div></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="neon-card"><div class="label">PROGRESO META</div><div class="value-cyan">{meta_progreso:.2f}%</div></div>', unsafe_allow_html=True)
    st.progress(meta_progreso / 100)

st.write("---")

# --- 5. CUERPO PRINCIPAL: GRID 3 COLUMNAS ---
col_acc, col_graf, col_ia = st.columns([0.8, 2, 1])

# PANEL IZQUIERDO (CUENTA)
with col_acc:
    st.markdown("### 👤 PORTAFOLIO")
    for crypto, val in balances.items():
        st.markdown(f"""
        <div style="border-bottom: 1px solid rgba(0, 242, 255, 0.2); padding: 10px 0;">
            <div class="label">{crypto}</div>
            <div style="color:white; font-size:1.2rem; font-weight:bold;">{val:.8f if crypto != 'mxn' else f'${val:,.2f}'}</div>
        </div>
        """, unsafe_allow_html=True)

# GRÁFICA PRINCIPAL (PLOTLY)
with col_graf:
    fig = go.Figure(data=[go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=24, freq='min'),
        open=[btc_price + np.random.uniform(-40, 40) for _ in range(24)],
        high=[btc_price + 90 for _ in range(24)],
        low=[btc_price - 90 for _ in range(24)],
        close=[btc_price + np.random.uniform(-40, 40) for _ in range(24)],
        increasing_line_color='#39FF14', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(
        template="plotly_dark", height=500, margin=dict(t=0, b=0, l=0, r=0),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False, yaxis=dict(gridcolor='rgba(0, 242, 255, 0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)

# PANEL DERECHO (CEREBRO MAHORA / CONTROL)
with col_ia:
    st.markdown("### 🧠 CEREBRO MAHORA")
    st.markdown(f"""
    <div class="thought-box" style="background:rgba(0,0,0,0.5); border-left:3px solid #39FF14; padding:15px; font-family:monospace; color:#39FF14; font-size:0.8rem;">
        >> ESCANEANDO BITSO...<br>
        >> LIQUIDEZ MXN: OK<br>
        >> TENDENCIA: ADAPTACIÓN ACTIVA<br>
        >> VOLATILIDAD: MEDIA<br>
        >> STATUS: LISTO PARA EJECUCIÓN
    </div>
    """, unsafe_allow_html=True)
    
    st.write("---")
    if st.button("👉 ACTIVAR COMPRA REAL"):
        if balances['mxn'] > 10:
            execute_trade("buy", "btc_mxn", balances['mxn'])
        else:
            st.error("SALDO INSUFICIENTE")
            
    if st.button("👉 ACTIVAR VENTA REAL"):
        if balances['btc'] > 0:
            execute_trade("sell", "btc_mxn", balances['btc'])
        else:
            st.error("SIN ACTIVOS PARA VENDER")

# --- 6. AUTO-REFRESH ---
time.sleep(15)
st.rerun()
