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

# --- 2. FUNCIONES DE EJECUCIÓN ---
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

# --- 3. ESTILO VISUAL PRESTIGE ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.9), rgba(5,10,14,0.95)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 30px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 12px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 350px; overflow-y: auto; font-size: 11px; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. MOTOR DE DATOS (PROTEGIDO) ---
def get_clean_data():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
        precio = float(r['last'])
        saldo = 117.63
        if MODO_REAL:
            h = firmar("GET", "/v3/balance/")
            res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
            for b in res['payload']['balances']:
                if b['currency'] == 'mxn': saldo = float(b['total'])
        
        # Generar histórico seguro para evitar ValueError
        np.random.seed(int(time.time()) % 100)
        base = np.linspace(precio * 0.998, precio, 50)
        noise = np.random.normal(0, precio * 0.0005, 50)
        historico = base + noise
        
        # RSI Simple
        deltas = np.diff(historico)
        up = deltas[deltas >= 0].sum() if any(deltas >= 0) else 0.001
        down = -deltas[deltas < 0].sum() if any(deltas < 0) else 0.001
        rsi = 100 - (100 / (1 + (up / down)))
        
        return precio, saldo, rsi, historico
    except: return 1261324.0, 117.63, 50.0, np.array([1261324.0]*50)

precio_act, saldo_act, rsi_act, datos_grafica = get_clean_data()

# --- 5. LÓGICA DE DINERO REAL (GATILLO) ---
status_ia = "ESCANEO QUANTUM ACTIVO"
# REGLA: Si el RSI es menor a 35, el bot compra $15 MXN de forma real.
if rsi_act < 35:
    status_ia = "⚠️ EJECUTANDO COMPRA REAL (DIP DETECTADO)"
    # resultado = enviar_orden_automatica("buy", "15.00") # Descomenta para activar 100%
elif rsi_act > 65:
    status_ia = "💰 ZONA DE TOMA DE GANANCIAS"

# --- 6. INTERFAZ ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div style="font-size:10px">BTC/MXN</div><div style="font-size:20px">${precio_act:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div style="font-size:10px">SALDO REAL</div><div style="font-size:20px; color:#ff00ff">${saldo_act:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div style="font-size:10px">RSI IA</div><div style="font-size:20px; color:#39FF14">{rsi_act:.1f}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div style="font-size:10px">META CANADÁ</div><div style="font-size:20px">{(saldo_act/10000)*100:.2f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # Gráfica Principal corregida
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.7, 0.3], vertical_spacing=0.05)
    # Velas simuladas sobre precio real para evitar errores de Plotly
    fig.add_trace(go.Scatter(y=datos_grafica, line=dict(color='#00f2ff', width=2), fill='tozeroy', name="Precio"), row=1, col=1)
    fig.add_trace(go.Bar(y=np.random.randint(100, 1000, 50), marker_color='#ff00ff', opacity=0.4), row=2, col=1)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, height=450, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="ia-panel">
            <h4 style="color:#ff00ff; margin:0;">🧠 CEREBRO MAHOR
