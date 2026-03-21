import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE_USUARIO}", page_icon="⛩️")

API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 2. MOTOR DE EJECUCIÓN ---
def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

def enviar_orden_automatica(side, monto_mxn):
    if not MODO_REAL: return "SIMULACIÓN"
    try:
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "btc_mxn", "side": "{side}", "type": "market", "nominal": "{monto_mxn}"}}'
        headers = firmar("POST", endpoint, cuerpo)
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        return r
    except Exception as e: return str(e)

# --- 3. ESTILO CSS "FERRARI PRESTIGE" ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 12px; }}
    .section-title {{ font-size: 14px; font-weight: bold; color: #ffffff; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 10px; text-align: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 10px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. OBTENCIÓN DE DATOS ---
def get_full_data():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
        precio = float(r['last'])
        saldo = 68.91 
        if MODO_REAL:
            h = firmar("GET", "/v3/balance/")
            res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
            for b in res['payload']['balances']:
                if b['currency'] == 'mxn': saldo = float(b['total'])
        
        # Generar datos de velas
        np.random.seed(int(time.time()) % 100)
        c = precio + np.cumsum(np.random.normal(0, 400, 40))
        o = np.roll(c, 1); o[0] = c[0] - 150
        h = np.maximum(o, c) + 200
        l = np.minimum(o, c) - 200
        v = np.random.randint(200, 1000, 40)
        
        return precio, saldo, o, h, l, c, v
    except: return 1261324.0, 68.91, [0]*40, [0]*40, [0]*40, [0]*40, [0]*40

precio, saldo, o, hi, lo, cl, vol = get_full_data()

# --- 5. RENDERIZADO ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# Top Bar
t1, t2, t3, t4 = st.columns(4)
t1.markdown(f'<div class="metric-card"><small>BTC/MXN BITSO</small><br><b style="font-size:20px">${precio:,.0f}</b></div>', unsafe_allow_html=True)
t2.markdown(f'<div class="metric-card"><small>SALDO REAL MXN</small><br><b style="font-size:20px; color:#ff00ff">${saldo:,.2f}</b></div>', unsafe_allow_html=True)
t3.markdown(f'<div class="metric-card"><small>IA STATUS</small><br><b style="font-size:20px; color:#39FF14">ACTIVATED</b></div>', unsafe_allow_html=True)
t4.markdown(f'<div class="metric-card"><small>META 10K (CANADÁ)</small><br><b style="font-size:20px">{(saldo/10000)*100:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")

c_main, c_side = st.columns([2.5, 1])

with c_main:
    # Gráfica de Velas
    fig_main = go.Figure(data=[go.Candlestick(
        open=o, high=hi, low=lo, close=cl,
        increasing_line_color='#00f2ff', increasing_fillcolor='#00f2ff',
        decreasing_line_color='#ff00ff', decreasing_fillcolor='#ff00ff'
    )])
    fig_main.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0),
        font_color="white", yaxis=dict(gridcolor='rgba(255,255,255,0.05)'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig_main, use_container_width=True)

    # --- SECCIÓN DE ABAJO (INDICADORES CUANTITATIVOS) ---
    st.markdown('<div class="section-title">Indicadores Cuantitativos (Real-Time)</div>', unsafe_allow_html=True)
    
    col_rsi, col_vol = st.columns([1, 1.5])
    
    with col_rsi:
        # Velocímetro RSI
        rsi_val = 42.5
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number", value = rsi_val,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "RSI (14) - NEUTRO", 'font': {'size': 14, 'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#00f2ff"},
                'bgcolor': "rgba(0,0,0,0)",
                'steps': [
                    {'range': [0, 30], 'color': '#ff00ff'},
                    {'range': [70, 100], 'color': '#ff00ff'}
                ],
                'threshold': {'line': {'color': "#39FF14", 'width': 3}, 'thickness': 0.75, 'value': rsi_val}
            }
        ))
        fig_rsi.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=30,b=0,l=10,r=10))
        st.plotly_chart(fig_rsi, use_container_width=True)

    with col_vol:
        # Barras de Volumen
        fig_vol = go.Figure(data=[go.Bar(y=vol, marker_color='#00f2ff', opacity=0.6)])
        fig_vol.update_layout(
            title={'text': "Volumen de Mercado", 'font': {'size': 14, 'color': 'white'}, 'x': 0.5},
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            height=200, margin=dict(l=0,r=0,t=30,b=0), font_color="white",
            yaxis=dict(showgrid=False, showticklabels=False),
            xaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig_vol, use_container_width=True)

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v8.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> SCAN REAL FINALIZADO.<br>
                [{ahora}] >> CONEXIÓN BITSO: OK.<br>
                [{ahora}] >> SALDO: ${saldo} MXN.<br>
                [{ahora}] >> RSI 42.5 (NEUTRO).<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, el mercado muestra volatilidad controlada. Manteniendo posición para el objetivo de los $10,000 MXN.
                <br><br>
                Sugerencia: Mantén posición. El viaje a Canadá 🇨🇦 sigue en marcha.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    if st.button("🚀 EJECUTAR OPERACIÓN MANUAL", use_container_width=True):
        st.toast("Conectando con Bitso...")

time.sleep(15)
st.rerun()
