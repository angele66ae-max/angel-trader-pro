import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark Prestige", page_icon="⛩️")

API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 2. SELECTOR DE PISTA (SIDEBAR) ---
st.sidebar.title("🏎️ SELECCIONAR PISTA")
activo_actual = st.sidebar.selectbox("Activo", ["btc_mxn", "eth_mxn", "usd_mxn"], index=0)

# --- 3. MOTOR DE EJECUCIÓN ---
def enviar_orden(side, libro, monto_mxn):
    if not MODO_REAL: return "SIMULACIÓN ACTIVA"
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

# --- 4. ESTILO FERRARI PRESTIGE (GOTAS NEÓN) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 320px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. DATA FETCH ---
try:
    r = requests.get(f"https://api.bitso.com/v3/ticker/?book={activo_actual}").json()['payload']
    precio = float(r['last'])
    saldo = 68.91 # Saldo base de tu captura
    
    # Velas simuladas Prestige
    np.random.seed(int(time.time()) % 100)
    c = precio + np.cumsum(np.random.normal(0, precio*0.005, 40))
    o = np.roll(c, 1); o[0] = c[0] * 0.998
    hi = np.maximum(o, c) * 1.002
    lo = np.minimum(o, c) * 0.998
    vol = np.random.randint(100, 1000, 40)
except:
    precio, o, hi, lo, c, vol, saldo = 0.0, [0]*40, [0]*40, [0]*40, [0]*40, [0]*40, 0.0

# --- 6. INTERFAZ (AQUÍ SE DEFINEN LAS COLUMNAS) ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# Top Bar
t1, t2, t3, t4 = st.columns(4)
t1.markdown(f'<div class="metric-card"><small>ACTIVO: {activo_actual.upper()}</small><br><b style="font-size:20px">${precio:,.2f}</b></div>', unsafe_allow_html=True)
t2.markdown(f'<div class="metric-card"><small>SALDO MXN</small><br><b style="font-size:20px; color:#ff00ff">${saldo:,.2f}</b></div>', unsafe_allow_html=True)
t3.markdown(f'<div class="metric-card"><small>ESTADO IA</small><br><b style="font-size:20px; color:#39FF14">SCANNIG</b></div>', unsafe_allow_html=True)
t4.markdown(f'<div class="metric-card"><small>META 10K</small><br><b style="font-size:20px">{(saldo/10000)*100:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
# SOLUCIÓN AL ERROR: Definimos c_main y c_side antes de usarlos
c_main, c_side = st.columns([2.5, 1])

with c_main:
    # Gráfica de Velas Neón
    fig = go.Figure(data=[go.Candlestick(
        open=o, high=hi, low=lo, close=c,
        increasing_line_color='#00f2ff', increasing_fillcolor='#00f2ff',
        decreasing_line_color='#ff00ff', decreasing_fillcolor='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("### INDICADORES CUANTITATIVOS")
    col_rsi, col_vol = st.columns([1, 1.5])
    with col_rsi:
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=42, 
            gauge={'axis':{'range':[0,100]}, 'bar':{'color':'#00f2ff'}, 
                   'steps':[{'range':[0,30],'color':'#ff00ff'},{'range':[70,100],'color':'#ff00ff'}]}))
        fig_rsi.update_layout(height=220, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=30,b=0))
        st.plotly_chart(fig_rsi, use_container_width=True)
    with col_vol:
        fig_vol = go.Figure(data=[go.Bar(y=vol, marker_color='#00f2ff', opacity=0.6)])
        fig_vol.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=30,b=0), font_color="white")
        st.plotly_chart(fig_vol, use_container_width=True)

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v8.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> ACTIVADO: {activo_actual.upper()}<br>
                [{ahora}] >> ANALIZANDO TENDENCIA...<br>
                [{ahora}] >> PRECIO ACTUAL: ${precio}<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, el Ferrari está listo. Vigilando caídas para comprar barato. ¡Rumbo a Canadá! 🇨🇦
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    monto_op = st.number_input("Monto MXN", min_value=10.0, value=20.0)
    if st.button(f"🚀 COMPRAR {activo_actual.split('_')[0].upper()}", use_container_width=True):
        res = enviar_orden("buy", activo_actual, str(monto_op))
        st.toast(f"Resultado: {res}")

# --- 7. AUTO-REFRESCO ---
time.sleep(20)
st.rerun()
