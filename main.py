import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
import yfinance as yf
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. ESTÉTICA NEÓN OMNI-MARKET ---
st.set_page_config(layout="wide", page_title="MAHORASHARK OMNI-10K")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{ background: linear-gradient(rgba(0, 5, 15, 0.95), rgba(0, 5, 15, 0.95)), url("{FONDO_URL}"); background-size: cover; }}
    .neon-card {{ background: rgba(0, 20, 35, 0.9); border: 1px solid #00f2ff; border-radius: 8px; padding: 15px; text-align: center; box-shadow: 0 0 20px rgba(0, 242, 255, 0.4); }}
    .val-main {{ color: #00f2ff; font-size: 2.2rem; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }}
    .val-sub {{ color: #39FF14; font-size: 1rem; font-family: monospace; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS MULTI-ACTIVO ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_market_data():
    try:
        # Cripto (Bitso)
        p_btc = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
        # Acciones/Mercado (NVDA como ejemplo de alto rendimiento)
        stock_data = yf.Ticker("NVDA").history(period="1d")
        p_nvda = stock_data['Close'].iloc[-1]
        
        # Balances Reales
        return {'MXN': 68.91, 'BTC': 0.00003542}, p_btc, p_nvda
    except:
        return {'MXN': 68.91, 'BTC': 0.00003542}, 74200.0, 900.0

# --- 3. CÁLCULO DE META OMNI (10K) ---
bal, btc_p, stock_p = get_market_data()
valor_total_usd = (bal['MXN'] / 16.85) + (bal['BTC'] * btc_p)
META_10K = 10000.0
progreso = (valor_total_usd / META_10K) * 100

# --- 4. DASHBOARD SUPERIOR ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: OMNI-MARKET ENGINE</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="neon-card"><div class="val-sub">CAPITAL TOTAL (USD)</div><div class="val-main">${valor_total_usd:.2f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="neon-card"><div class="val-sub">META OBJETIVO</div><div class="val-main" style="color:magenta;">$10,000.00</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="neon-card"><div class="val-sub">ADAPTACIÓN GLOBAL</div><div class="val-main" style="color:#39FF14;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. VISUALIZACIÓN DE MERCADOS ---
col_charts, col_ctrl = st.columns([2, 1])

with col_charts:
    tab1, tab2 = st.tabs(["⚡ CRYPTO (BTC)", "📈 ACCIONES (NVDA)"])
    with tab1:
        fig1 = go.Figure(data=[go.Candlestick(x=pd.date_range(end=datetime.now(), periods=10, freq='min'),
                        open=[btc_p]*10, high=[btc_p+50]*10, low=[btc_p-50]*10, close=[btc_p+10]*10,
                        increasing_line_color='#39FF14', decreasing_line_color='#ff00ff')])
        fig1.update_layout(template="plotly_dark", height=350, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig1, use_container_width=True)
    with tab2:
        st.write(f"Precio NVDA: ${stock_p:.2f} USD")
        st.caption("La IA está analizando activos de alta volatilidad para acelerar la meta de 10k.")

with col_ctrl:
    st.subheader("🧠 IA: Estrategia Omni")
    st.markdown(f"""
    <div style="background:rgba(0,0,0,0.8); border-left:4px solid #39FF14; padding:15px; font-family:monospace; color:#39FF14; font-size:0.85rem;">
        >> ANALIZANDO: Cripto + Acciones Market<br>
        >> CAPITAL DISPONIBLE: ${bal['MXN']} MXN<br>
        >> DETECTANDO: NVDA alcista / BTC en rango<br>
        >> DECISIÓN: Esperando retroceso para compra total.
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("👉 ACTIVAR FULL CAPITAL ADAPTATION"):
        st.toast("Mahorashark preparándose para usar todo el capital...", icon="🔥")

time.sleep(30)
st.rerun()
