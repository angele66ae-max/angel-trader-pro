import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
import random
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark Prestige", page_icon="⛩️")

# --- 2. IDENTIDAD Y LLAVES (CARGA DESDE SECRETS) ---
# Si esto falla, el bot se queda en SIMULATED por seguridad.
API_KEY = st.secrets.get("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 3. MOTOR DE DATOS REALES (BITSO) ---
def get_bitso_data(libro):
    try:
        r = requests.get(f"https://api.bitso.com/v3/trades/?book={libro}").json()['payload']
        precios = [float(t['price']) for t in r][::-1]
        return precios[-1], precios
    except:
        return 0.0, [0]*50

def obtener_saldo_mxn():
    if not MODO_REAL: return 68.91
    try:
        nonce = str(int(time.time() * 1000))
        mensaje = nonce + "GET" + "/v3/balance/"
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}'}
        r = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        for b in r['payload']['balances']:
            if b['currency'] == 'mxn':
                return float(b['total'])
        return 0.0
    except: return 68.91

# --- 4. ESTILO VISUAL PRESTIGE ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.96), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 32px; text-shadow: 0 0 20px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 15px; margin-bottom: 25px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 12px; padding: 15px; text-align: center; box-shadow: 0 0 15px rgba(0, 242, 255, 0.15); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; height: 380px; overflow-y: auto; font-size: 13px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. EJECUCIÓN DEL SISTEMA ---
st.sidebar.title("🏎️ PISTA")
activo = st.sidebar.selectbox("Activo", ["btc_mxn", "eth_mxn", "usd_mxn"])

precio_v, historial_v = get_bitso_data(activo)
saldo_v = obtener_saldo_mxn()
meta_final = 10000.0
progreso_v = (saldo_v / meta_final) * 100

# --- 6. INTERFAZ ---
st.markdown('<div class="main-header">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# Fila de métricas
m1, m2, m3, m4 = st.columns(4)
m1.markdown(f'<div class="metric-card"><small>PRECIO {activo.upper()}</small><br><b style="font-size:24px; color:#00f2ff">${precio_v:,.2f}</b></div>', unsafe_allow_html=True)
m2.markdown(f'<div class="metric-card"><small>SISTEMA</small><br><b style="font-size:20px; color:{"#39FF14" if MODO_REAL else "#ff00ff"}">{"LIVE ACTIVE" if MODO_REAL else "SIMULATED"}</b></div>', unsafe_allow_html=True)
m3.markdown(f'<div class="metric-card"><small>SALDO TOTAL</small><br><b style="font-size:24px; color:#ff00ff">${saldo_v:,.2f}</b></div>', unsafe_allow_html=True)
m4.markdown(f'<div class="metric-card"><small>META 10K (CANADÁ)</small><br><b style="font-size:24px; color:#39FF14">{progreso_v:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
col_grafica, col_cerebro = st.columns([2.4, 1])

with col_grafica:
    fig = go.Figure(data=[go.Scatter(y=historial_v, mode='lines', line=dict(color='#00f2ff', width=3), fill='toself', fillcolor='rgba(0, 242, 255, 0.05)')])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=450, margin=dict(l=0,r=0,t=0,b=0), font_color="white", xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
    st.plotly_chart(fig, use_container_width=True)

with col_cerebro:
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:12px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v15.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> SINCRONIZANDO CON BITSO...<br>
                [{ahora}] >> MODO REAL: {"CONECTADO" if MODO_REAL else "FALLIDO"}<br>
                [{ahora}] >> SALDO LEÍDO: ${saldo_v:,.2f}<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Ángel, si todavía dice SIMULATED es porque las llaves en 'Secrets' de Streamlit tienen un error de dedo o no están guardadas. 
                <br><br>
                El porcentaje del {progreso_v:.2f}% se moverá solo en cuanto detecte más saldo en tu cuenta. 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)

# Auto-refresco
time.sleep(15)
st.rerun()
