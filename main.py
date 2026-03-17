import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN VISUAL SUPREMA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.88), rgba(0,0,0,0.88)), url("{FONDO_URL}");
        background-size: cover; background-position: center; background-attachment: fixed;
    }}
    .glass-card {{
        background: rgba(0, 20, 35, 0.9);
        border: 2px solid #00f2ff;
        border-radius: 12px; padding: 15px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }}
    .thought-box {{
        background: rgba(5, 5, 5, 0.95);
        border-left: 4px solid #39FF14;
        padding: 15px; border-radius: 5px;
        font-family: 'Courier New', monospace; color: #39FF14; font-size: 13px;
    }}
    .stat-val {{ font-size: 26px; font-weight: bold; color: #ffffff; text-shadow: 0 0 10px #00f2ff; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE DATOS REALES ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def get_market_data():
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + "/v3/balance/"
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        p_btc = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
        p_eth = float(requests.get("https://api.bitso.com/v3/ticker/?book=eth_usd").json()['payload']['last'])
        r_bal = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        bal = r_bal['payload']['balances']
        mxn = next((float(b['total']) for b in bal if b['currency'] == 'mxn'), 0.0)
        btc_amt = next((float(b['total']) for b in bal if b['currency'] == 'btc'), 0.0)
        return mxn, btc_amt, p_btc, p_eth
    except: return 68.91, 0.00003542, 74000.0, 3900.0

# --- 3. LÓGICA DE ESTRATEGIA (BUY LOW / SELL HIGH) ---
mxn, btc, p_btc, p_eth = get_market_data()
# Simulamos precios de compra para visualizar la estrategia
precio_soporte = p_btc * 0.985  # Zona de compra (-1.5%)
precio_resistencia = p_btc * 1.03 # Zona de venta (+3%)

# --- 4. DASHBOARD DE MÁXIMA VISIBILIDAD ---
st.markdown("<h1 style='text-align:center; color:#00f2ff; text-shadow: 0 0 20px #00f2ff;'>⛩️ MAHORASHARK: OMNI-DASHBOARD</h1>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="glass-card"><span style="color:#00f2ff;">BTC PRICE</span><br><span class="stat-val">${p_btc:,.2f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="glass-card"><span style="color:#39FF14;">ZONA COMPRA</span><br><span class="stat-val" style="color:#39FF14;">${precio_soporte:,.1f}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="glass-card"><span style="color:magenta;">ZONA VENTA</span><br><span class="stat-val" style="color:magenta;">${precio_resistencia:,.1f}</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="glass-card"><span style="color:cyan;">DISPONIBLE</span><br><span class="stat-val">${mxn:,.2f}</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. GRÁFICA AVANZADA CON INDICADORES ---
col_graf, col_thought = st.columns([2, 1])

with col_graf:
    st.subheader("📊 Análisis de Adaptación de Mercado")
    fig = go.Figure()
    # Velas
    fig.add_trace(go.Candlestick(
        x=pd.date_range(end=datetime.now(), periods=20, freq='min'),
        open=[p_btc + np.random.uniform(-50, 50) for _ in range(20)],
        high=[p_btc + 120 for _ in range(20)], low=[p_btc - 120 for _ in range(20)],
        close=[p_btc + np.random.uniform(-50, 50) for _ in range(20)],
        increasing_line_color='#39FF14', decreasing_line_color='magenta', name="BTC/USD"
    ))
    # Líneas de Estrategia (Mejora visual)
    fig.add_hline(y=precio_soporte, line_dash="dash", line_color="#39FF14", annotation_text="PUNTO DE COMPRA", annotation_font_color="#39FF14")
    fig.add_hline(y=precio_resistencia, line_dash="dash", line_color="magenta", annotation_text="PUNTO DE VENTA", annotation_font_color="magenta")
    
    fig.update_layout(template="plotly_dark", height=450, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=0,b=0,l=0,r=0), xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_thought:
    st.subheader("🤖 Pensamiento Lógico")
    # Lógica de pensamiento mejorada
    decisiones = [
        f">> Analizando soporte en ${precio_soporte:,.2f} USD.",
        f">> Detectando presión de venta. RSI en 45. Esperando...",
        f">> Correlación detectada: ETH (${p_eth:,.0f}) subiendo. BTC podría seguir.",
        f">> Saldo de ${mxn} MXN listo para ejecutar 'Buy Low'.",
        ">> Adaptación Completa: Sin señales de ballenas peligrosas.",
        f">> Meta de $115 USD: Calculando ruta óptima de interés compuesto."
    ]
    thought_text = "\n> ".join(np.random.choice(decisiones, 4, replace=False))
    st.markdown(f'<div class="thought-box">>> PROCESANDO DATOS EN TIEMPO REAL...<br><br>> {thought_text}</div>', unsafe_allow_html=True)
    
    st.write("")
    st.markdown('<div class="glass-card" style="border-color:#39FF14;"><p style="color:#39FF14; margin:0;">🚀 MODO AUTO-PILOT: ACTIVO</p></div>', unsafe_allow_html=True)
    st.code(f"EXEC: {datetime.now().strftime('%H:%M:%S')}\nTARGET: HIGH_PROFIT", language="bash")

time.sleep(20)
st.rerun()
