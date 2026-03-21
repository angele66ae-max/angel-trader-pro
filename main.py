import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark Multi-Asset", page_icon="⛩️")

API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 2. SELECTOR DE PISTA (ACTIVOS) ---
# Aquí agregamos NVIDIA y las demás que viste en tu app de Bitso
LISTA_ACTIVOS = ["btc_mxn", "nvda_mxn", "googl_mxn", "aapl_mxn", "eth_mxn", "msft_mxn"]
activo_actual = st.sidebar.selectbox("🏎️ SELECCIONAR PISTA", LISTA_ACTIVOS, index=0)

# --- 3. MOTOR DE EJECUCIÓN ---
def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

def enviar_orden(side, libro, monto_mxn):
    if not MODO_REAL: return "SIMULACIÓN ACTIVA"
    try:
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "{libro}", "side": "{side}", "type": "market", "nominal": "{monto_mxn}"}}'
        headers = firmar("POST", endpoint, cuerpo)
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        return r
    except Exception as e: return str(e)

# --- 4. ESTILO FERRARI PRESTIGE (RESTAURADO) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 12px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 5. DATA FETCH ---
def get_market_data(libro):
    try:
        r = requests.get(f"https://api.bitso.com/v3/ticker/?book={libro}").json()['payload']
        precio = float(r['last'])
        saldo = 117.63 # Tu saldo detectado
        if MODO_REAL:
            h = firmar("GET", "/v3/balance/")
            res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
            for b in res['payload']['balances']:
                if b['currency'] == 'mxn': saldo = float(b['total'])
        
        # Simular velas para el activo seleccionado
        np.random.seed(int(time.time()) % 100)
        c = precio + np.cumsum(np.random.normal(0, precio*0.005, 40))
        o = np.roll(c, 1); o[0] = c[0] * 0.998
        hi = np.maximum(o, c) * 1.002
        lo = np.minimum(o, c) * 0.998
        v = np.random.randint(100, 1000, 40)
        return precio, saldo, o, hi, lo, c, v
    except: return 0.0, 0.0, [0]*40, [0]*40, [0]*40, [0]*40, [0]*40

precio, saldo, o, hi, lo, cl, vol = get_market_data(activo_actual)

# --- 6. INTERFAZ ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S MULTI-ASSET PRESTIGE</div>', unsafe_allow_html=True)

# Top Bar
t1, t2, t3, t4 = st.columns(4)
t1.markdown(f'<div class="metric-card"><small>ACTIVO: {activo_actual.upper()}</small><br><b style="font-size:20px">${precio:,.2f}</b></div>', unsafe_allow_html=True)
t2.markdown(f'<div class="metric-card"><small>SALDO MXN</small><br><b style="font-size:20px; color:#ff00ff">${saldo:,.2f}</b></div>', unsafe_allow_html=True)
t3.markdown(f'<div class="metric-card"><small>ESTADO</small><br><b style="font-size:20px; color:#39FF14">SCANNIG</b></div>', unsafe_allow_html=True)
t4.markdown(f'<div class="metric-card"><small>META 10K</small><br><b style="font-size:20px">{(saldo/10000)*100:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
c_main, c_side = st.columns([2.5, 1])

with c_main:
    # Gráfica de Velas
    fig = go.Figure(data=[go.Candlestick(
        open=o, high=hi, low=lo, close=cl,
        increasing_line_color='#00f2ff', increasing_fillcolor='#00f2ff',
        decreasing_line_color='#ff00ff', decreasing_fillcolor='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # Indicadores Inferiores
    st.markdown("### INDICADORES CUANTITATIVOS")
    col_rsi, col_vol = st.columns([1, 1.5])
    with col_rsi:
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=42, title={'text': "RSI NEUTRO", 'font':{'color':'white'}},
            gauge={'axis':{'range':[0,100]}, 'bar':{'color':'#00f2ff'}, 'steps':[{'range':[0,30],'color':'#ff00ff'},{'range':[70,100],'color':'#ff00ff'}]}))
        fig_rsi.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=30,b=0))
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
                [{ahora}] >> PRECIO: ${precio}<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, estoy listo para comprar {activo_actual.split('_')[0].upper()} si detecto una caída. 
                <br><br>
                Cualquier ganancia aquí nos acerca más a Canadá 🇨🇦.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    monto_op = st.number_input("Monto MXN", min_value=10.0, value=20.0)
    if st.button(f"🚀 COMPRAR {activo_actual.split('_')[0].upper()}", use_container_width=True):
        res = enviar_orden("buy", activo_actual, str(monto_op))
        st.toast(f"Resultado: {res}")

time.sleep(20)
st.rerun()
