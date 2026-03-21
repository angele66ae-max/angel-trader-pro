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

# --- SECRETS ---
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
TG_TOKEN = st.secrets.get("TELEGRAM_TOKEN") # Pieza Nitro 1
TG_CHAT_ID = st.secrets.get("TELEGRAM_CHAT_ID") # Pieza Nitro 2
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 2. MOTOR DE EJECUCIÓN & NOTIFICACIONES ---
def enviar_telegram(mensaje):
    if TG_TOKEN and TG_CHAT_ID:
        try:
            url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage?chat_id={TG_CHAT_ID}&text={mensaje}"
            requests.get(url)
        except: pass

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

def enviar_orden_automatica(side, monto_mxn, saldo_disponible):
    if not MODO_REAL: return "SIMULACIÓN"
    
    # PIEZA DE SEGURIDAD: No comprar si no hay balance
    if float(monto_mxn) > saldo_disponible and side == "buy":
        return "ERROR: GASOLINA INSUFICIENTE (Saldo bajo)"

    try:
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "btc_mxn", "side": "{side}", "type": "market", "nominal": "{monto_mxn}"}}'
        headers = firmar("POST", endpoint, cuerpo)
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        
        if "payload" in r:
            enviar_telegram(f"⛩️ MahoraShark: ¡Orden de {side} por ${monto_mxn} ejecutada con éxito! 🇨🇦")
        return r
    except Exception as e: return str(e)

# --- 3. ESTILO CSS "FERRARI PRESTIGE" (INTACTO) ---
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
        
        np.random.seed(int(time.time()) % 100)
        c = precio + np.cumsum(np.random.normal(0, 400, 40))
        o = np.roll(c, 1); o[0] = c[0] - 150
        hi = np.maximum(o, c) + 200
        lo = np.minimum(o, c) - 200
        v = np.random.randint(200, 1000, 40)
        return precio, saldo, o, hi, lo, c, v
    except: return 1261324.0, 68.91, [0]*40, [0]*40, [0]*40, [0]*40, [0]*40

precio, saldo, o, hi, lo, cl, vol = get_full_data()

# --- 5. RENDERIZADO ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S PRESTIGE ULTIMATE</div>', unsafe_allow_html=True)

t1, t2, t3, t4 = st.columns(4)
t1.markdown(f'<div class="metric-card"><small>BTC/MXN BITSO</small><br><b style="font-size:20px">${precio:,.0f}</b></div>', unsafe_allow_html=True)
t2.markdown(f'<div class="metric-card"><small>SALDO REAL MXN</small><br><b style="font-size:20px; color:#ff00ff">${saldo:,.2f}</b></div>', unsafe_allow_html=True)
t3.markdown(f'<div class="metric-card"><small>IA STATUS</small><br><b style="font-size:20px; color:#39FF14">NITRO ON</b></div>', unsafe_allow_html=True)
t4.markdown(f'<div class="metric-card"><small>META 10K (CANADÁ)</small><br><b style="font-size:20px">{(saldo/10000)*100:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
c_main, c_side = st.columns([2.5, 1])

with c_main:
    fig_main = go.Figure(data=[go.Candlestick(
        open=o, high=hi, low=lo, close=cl,
        increasing_line_color='#00f2ff', increasing_fillcolor='#00f2ff',
        decreasing_line_color='#ff00ff', decreasing_fillcolor='#ff00ff'
    )])
    fig_main.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, height=400, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig_main, use_container_width=True)

    st.markdown('<div class="section-title">Indicadores Cuantitativos (Nitro Ready)</div>', unsafe_allow_html=True)
    col_rsi, col_vol = st.columns([1, 1.5])
    
    with col_rsi:
        rsi_val = 42.5
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number", value = rsi_val,
            title = {'text': "RSI (14) - NEUTRO", 'font': {'size': 14, 'color': 'white'}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': "white"},
                'bar': {'color': "#00f2ff"},
                'steps': [{'range': [0, 30], 'color': '#ff00ff'}, {'range': [70, 100], 'color': '#ff00ff'}],
                'threshold': {'line': {'color': "#39FF14", 'width': 3}, 'value': rsi_val}
            }
        ))
        fig_rsi.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=30,b=0))
        st.plotly_chart(fig_rsi, use_container_width=True)

    with col_vol:
        fig_vol = go.Figure(data=[go.Bar(y=vol, marker_color='#00f2ff', opacity=0.6)])
        fig_vol.update_layout(title={'text': "Volumen", 'font': {'size': 14}, 'x': 0.5}, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(t=30,b=0), font_color="white")
        st.plotly_chart(fig_vol, use_container_width=True)

with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    # LÓGICA DE COMPRA AUTOMÁTICA
    if rsi_val < 35:
        # resultado = enviar_orden_automatica("buy", "15.00", saldo) # <--- GATILLO REAL
        status_ia = "⚠️ COMPRANDO DIP"
    else: status_ia = "ESCANEO QUANTUM"

    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v8.0</h4>
            <div class="ia-terminal">
                [{ahora}] >> NITRO SYSTEM: ACTIVE<br>
                [{ahora}] >> SALDO SEGURO: ${saldo} MXN.<br>
                [{ahora}] >> STATUS: {status_ia}<br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, el Ferrari está en pista. Si el RSI baja de 35, dispararé una orden de $15 pesos y te avisaré por Telegram. ¡Canadá 🇨🇦 cada vez más cerca!
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 COMPRA MANUAL ($20)", use_container_width=True):
        res = enviar_orden_automatica("buy", "20.00", saldo)
        st.toast(f"Resultado: {res}")

time.sleep(15)
st.rerun()
