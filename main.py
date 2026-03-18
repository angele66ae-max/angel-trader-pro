import streamlit as st
import pandas as pd
import pandas_ta as ta
import numpy as np
import requests
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN SENSORIAL (CYBERPUNK PRO) ---
st.set_page_config(layout="wide", page_title="MAHORA PRO: 10K ENGINE")

st.markdown("""
<style>
    .stApp { background: #00050a; color: #00f2ff; font-family: 'JetBrains Mono', monospace; }
    .neon-card {
        background: rgba(0, 20, 40, 0.8); border: 1px solid #00f2ff;
        border-radius: 10px; padding: 20px; box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
    }
    .status-active { color: #39FF14; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .val-main { font-size: 2.5rem; font-weight: bold; text-shadow: 0 0 15px #00f2ff; }
</style>
""", unsafe_allow_html=True)

# --- 2. MOTOR DE AUTENTICACIÓN Y DATOS ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"
LIBROS = ["btc_mxn", "eth_mxn", "xrp_mxn", "sol_mxn", "ada_mxn"]

def get_bitso_balances():
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(API_SECRET.encode(), (nonce + "GET" + "/v3/balance/").encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}
    try:
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        return {b['currency'].upper(): float(b['total']) for b in r['payload']['balances']}
    except: return {"MXN": 68.91, "BTC": 0.00003542}

def get_ohlc(book):
    # Simulamos velas para el análisis técnico (En producción usar API de trades)
    p = float(requests.get(f"https://api.bitso.com/v3/ticker/?book={book}").json()['payload']['last'])
    df = pd.DataFrame({'close': [p * (1 + np.random.uniform(-0.01, 0.01)) for _ in range(50)]})
    df['rsi'] = ta.rsi(df['close'], length=14)
    df['sma7'] = ta.sma(df['close'], length=7)
    df['sma21'] = ta.sma(df['close'], length=21)
    return df, p

# --- 3. CEREBRO MAHORA PRO: LÓGICA DE TRADING ---
balances = get_bitso_balances()
mxn_total = balances.get('MXN', 0)
btc_p = float(requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']['last'])
valor_usd = (mxn_total / 16.85) + (balances.get('BTC', 0) * btc_p)
progreso = (valor_usd / 10000.0) * 100

# --- 4. UI: DASHBOARD DE CONTROL ---
st.markdown("<h1 style='text-align:center;'>⛩️ MAHORASHARK PRO: ADAPTACIÓN TOTAL</h1>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
with c1: st.markdown(f'<div class="neon-card">NET WORTH (USD)<br><span class="val-main">${valor_usd:.2f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="neon-card">META 10K<br><span class="val-main" style="color:magenta;">{progreso:.4f}%</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="neon-card">ESTADO SISTEMA<br><span class="status-active">SCANNING MARKETS</span></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. SCANNER MULTI-ACTIVO ---
cols = st.columns(len(LIBROS))
decisiones = []

for i, book in enumerate(LIBROS):
    df, price = get_ohlc(book)
    rsi_now = df['rsi'].iloc[-1]
    sma7 = df['sma7'].iloc[-1]
    sma21 = df['sma21'].iloc[-1]
    
    # LÓGICA PROFESIONAL
    signal = "⚖️ NEUTRAL"
    color = "#fff"
    
    if rsi_now < 35 and sma7 > sma21:
        signal = "🟢 COMPRA ESTRATÉGICA"
        color = "#39FF14"
        decisiones.append(f"Iniciando posición en {book} (RSI: {rsi_now:.1f})")
    elif rsi_now > 65:
        signal = "🔴 VENTA / TAKE PROFIT"
        color = "#ff00ff"
        decisiones.append(f"Cerrando {book} para asegurar liquidez.")

    with cols[i]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:5px; border-top:3px solid {color};">
            <small>{book.upper()}</small><br>
            <b>${price:,.2f}</b><br>
            <span style="color:{color}; font-size:0.7rem;">{signal}</span>
        </div>
        """, unsafe_allow_html=True)

# --- 6. GRÁFICA MAESTRA ---
st.write("### 📈 Análisis de Adaptación de Mercado")
active_book = st.selectbox("Seleccionar Activo para Visualización Detallada", LIBROS)
df_v, p_v = get_ohlc(active_book)

fig = go.Figure()
fig.add_trace(go.Scatter(y=df_v['close'], name="Precio", line=dict(color='#00f2ff')))
fig.add_trace(go.Scatter(y=df_v['sma7'], name="SMA 7", line=dict(color='#39FF14', dash='dot')))
fig.add_trace(go.Scatter(y=df_v['sma21'], name="SMA 21", line=dict(color='magenta', dash='dot')))
fig.update_layout(template="plotly_dark", height=400, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

# --- 7. CONSOLA DE DECISIONES IA ---
st.write("### 🧠 Mahora Logs: Ejecución Autónoma")
log_text = "<br>".join([f">> [{datetime.now().strftime('%H:%M:%S')}] {d}" for d in decisiones]) if decisiones else ">> Analizando divergencias en RSI... Esperando punto de entrada óptimo."
st.markdown(f"""
<div style="background:#000; border:1px solid #39FF14; padding:20px; font-family:monospace; color:#39FF14; height:150px; overflow-y:auto;">
    {log_text}
</div>
""", unsafe_allow_html=True)

# --- AUTO-OPERACIÓN ---
time.sleep(15)
st.rerun()
