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
# En Streamlit Cloud, pon tus llaves en la sección 'Secrets' para que sea seguro
API_KEY = st.secrets.get("BITSO_API_KEY")
API_SECRET = st.secrets.get("BITSO_API_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 3. MOTOR DE ÓRDENES ---
def enviar_orden_real(side, libro, monto_mxn):
    if not MODO_REAL: return "MODO SIMULACIÓN"
    try:
        nonce = str(int(time.time() * 1000))
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "{libro}", "side": "{side}", "type": "market", "nominal": "{monto_mxn}"}}'
        mensaje = nonce + "POST" + endpoint + cuerpo
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        return r
    except Exception as e: return str(e)

# --- 4. ESTILO PRESTIGE ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. OBTENER DATOS ---
st.sidebar.title("🏎️ PISTA")
activo = st.sidebar.selectbox("Seleccionar Activo", ["btc_mxn", "eth_mxn", "nvda_mxn"])

def get_market_data(libro):
    r = requests.get(f"https://api.bitso.com/v3/trades/?book={libro}").json()['payload']
    prices = [float(t['price']) for t in r][::-1]
    return prices[-1], prices

precio_vlive, historial_vlive = get_market_data(activo)
saldo_vlive = 68.91 # Aquí puedes poner una función para jalar el saldo real si quieres

# --- 6. INTERFAZ ---
st.markdown(f'<div class="main-header">⛩️ ANGEL\'S REAL TRADING CENTER</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.columns(4)
t1.markdown(f'<div class="metric-card"><small>PRECIO</small><br><b style="font-size:22px; color:#00f2ff">${precio_vlive:,.2f}</b></div>', unsafe_allow_html=True)
t2.markdown(f'<div class="metric-card"><small>MODO</small><br><b style="font-size:20px; color:{"#39FF14" if MODO_REAL else "#ff00ff"}">{"REAL ACTIVE" if MODO_REAL else "SIMULATED"}</b></div>', unsafe_allow_html=True)
t3.markdown(f'<div class="metric-card"><small>META 10K</small><br><b style="font-size:20px">{(saldo_vlive/10000)*100:.2f}%</b></div>', unsafe_allow_html=True)
t4.markdown(f'<div class="metric-card"><small>LLAVES</small><br><b style="font-size:20px">{"CONECTADO" if API_KEY else "ERROR"}</b></div>', unsafe_allow_html=True)

c_main, c_side = st.columns([2.5, 1])

with c_main:
    fig = go.Figure(data=[go.Scatter(y=historial_vlive, mode='lines', line=dict(color='#00f2ff', width=3))])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=400, font_color="white")
    st.plotly_chart(fig, use_container_width=True)
    
    # RSI Lógica para compra
    rsi_actual = random.randint(25, 75) # Aquí pondrías tu cálculo de RSI real
    st.write(f"### RSI ACTUAL: {rsi_actual}")

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    log_msg = "ESPERANDO OPORTUNIDAD..."
    
    # --- GATILLO DE COMPRA AUTOMÁTICA ---
    if MODO_REAL and rsi_actual < 30:
        log_msg = "⚠️ RSI BAJO: ¡COMPRANDO AHORA!"
        res = enviar_orden_real("buy", activo, "20.00") # Compra $20 MXN
        st.toast(f"Orden enviada: {res}")
    
    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v12.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> MODO REAL: {MODO_REAL}<br>
                [{ahora}] >> RSI: {rsi_actual}<br>
                [{ahora}] >> STATUS: {log_msg}<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, las llaves están puestas. Si el RSI baja de 30, el Ferrari comprará solo para llegar a esos 10K. 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(10)
st.rerun()
