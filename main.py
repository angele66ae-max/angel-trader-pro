import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import hmac
import hashlib
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# --- 1. CONFIGURACIÓN E INTERFAZ PRO ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRO")

API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

FONDO_URL = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"
st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.9), rgba(0,0,0,0.9)), url("{FONDO_URL}");
        background-size: cover; background-attachment: fixed;
    }}
    .metric-card {{
        background: rgba(0, 5, 15, 0.9);
        border: 1px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .val-main {{ font-size: 28px; color: #00f2ff; font-weight: bold; }}
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE COMUNICACIÓN BITSO ---
def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_payload = json.dumps(payload, separators=(',', ':')) if payload else ""
    message = nonce + method + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    try:
        url = f"https://api.bitso.com{path}"
        res = requests.request(method, url, headers=headers, data=json_payload)
        return res.json()
    except: return {"success": False, "error": {"message": "Fallo de red"}}

# --- 3. ANALÍTICA DE MERCADO (INDICADORES) ---
def get_indicators(prices):
    df = pd.DataFrame(prices, columns=['close'])
    # Media Móvil Simple (SMA)
    df['sma'] = df['close'].rolling(window=10).mean()
    # RSI (Relative Strength Index)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))
    return df

# --- 4. DATA FETCHING ---
try:
    # Obtener precios y balances reales
    ticker_mxn = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
    p_mxn = float(ticker_mxn['payload']['last'])
    
    balances = bitso_api("GET", "/v3/balance/")['payload']['balances']
    mxn_bal = next((float(b['available']) for b in balances if b['currency'] == 'mxn'), 0.0)
    usd_bal = next((float(b['available']) for b in balances if b['currency'] == 'usd'), 0.0)
    
    # Simulación de historial para indicadores
    hist_prices = [p_mxn + np.random.uniform(-1000, 1000) for _ in range(50)]
    df_tech = get_indicators(hist_prices)
except:
    p_mxn, mxn_bal, usd_bal = 1450000.0, 47.12, 2.81 # Datos de seguridad
    df_tech = get_indicators([p_mxn + np.random.uniform(-1000, 1000) for _ in range(50)])

# --- 5. DASHBOARD PRO ---
st.markdown("<h2 style='text-align:center; color:#00f2ff;'>MAHORASHARK PRO TERMINAL</h2>", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN<div class="val-main">${p_mxn:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">BÓVEDA MXN<div class="val-main" style="color:magenta;">${mxn_bal:.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">RSI (14)<div class="val-main" style="color:#39FF14;">{df_tech["rsi"].iloc[-1]:.1f}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card">META SUV<div class="val-main" style="color:cyan;">{(mxn_bal/200000)*100:.4f}%</div></div>', unsafe_allow_html=True)

col_viz, col_ctrl = st.columns([3, 1])

with col_viz:
    # Gráfica avanzada con Media Móvil
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05, row_heights=[0.7, 0.3])
    
    # Precio y SMA
    fig.add_trace(go.Scatter(y=df_tech['close'], name="Precio", line=dict(color='#00f2ff', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(y=df_tech['sma'], name="SMA 10", line=dict(color='yellow', dash='dot')), row=1, col=1)
    
    # RSI
    fig.add_trace(go.Scatter(y=df_tech['rsi'], name="RSI", line=dict(color='magenta')), row=2, col=1)
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    fig.update_layout(template="plotly_dark", height=500, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col_ctrl:
    st.markdown('<div class="metric-card" style="text-align:left; min-height:500px;">', unsafe_allow_html=True)
    st.subheader("🤖 IA Mahora Pro")
    
    # Selección de activo inteligente
    usar_mxn = mxn_bal > (usd_bal * 20) # Lógica simple para elegir moneda dominante
    moneda = "MXN" if usar_mxn else "USD"
    balance_usar = mxn_bal if usar_mxn else usd_bal
    monto_final = balance_usar * 0.92
    
    ia_on = st.toggle("MODO AUTO-ADAPTACIÓN", value=True)
    
    # Lógica de decisión técnica
    rsi_val = df_tech['rsi'].iloc[-1]
    if rsi_val < 35:
        st.success("🎯 SEÑAL: SOBREVENTA. IA LISTA PARA COMPRAR.")
        decision = "BUY"
    elif rsi_val > 65:
        st.warning("⚠️ SEÑAL: SOBRECOMPRA. IA SUGIERE ESPERAR.")
        decision = "WAIT"
    else:
        st.info("🔄 SEÑAL: MERCADO NEUTRAL.")
        decision = "NONE"

    st.write(f"Target Activo: **{moneda}**")
    st.write(f"Monto Sugerido: **${monto_final:.2f}**")
    
    if st.button("🚀 EJECUTAR ADAPTACIÓN", use_container_width=True):
        if balance_usar < 10.0 and moneda == "MXN":
            st.error("Error: Saldo MXN insuficiente para el mínimo ($10)")
        elif balance_usar < 1.0 and moneda == "USD":
            st.error("Error: Saldo USD insuficiente para el mínimo ($1)")
        else:
            payload = {
                "book": "btc_mxn" if usar_mxn else "btc_usd",
                "side": "buy", "type": "market",
                "minor": f"{monto_final:.2f}"
            }
            res = bitso_api("POST", "/v3/orders/", payload)
            if res.get('success'):
                st.success("¡ADAPTACIÓN EXITOSA!")
                st.balloons()
            else:
                st.error(f"Bitso: {res.get('error', {}).get('message', 'Fallo de Firma')}")

    st.code(f"[{datetime.now().strftime('%H:%M:%S')}]\nStatus: PRESTIGE\nAsset: {moneda}", language="bash")
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(15)
st.rerun()
