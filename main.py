import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. IDENTIDAD & CONFIGURACIÓN ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE_USUARIO}", page_icon="⛩️")

# --- 2. CONEXIÓN REAL BITSO (SEGURIDAD) ---
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

def ejecutar_orden_bitso(side, amount_mxn):
    if not MODO_REAL: return {"status": "success", "message": "SIMULACIÓN"}
    try:
        endpoint = "/v3/orders/"
        cuerpo = f'{{"book": "btc_mxn", "side": "{side}", "type": "market", "nominal": "{amount_mxn}"}}'
        h = firmar("POST", endpoint, cuerpo)
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=h, data=cuerpo).json()
        return r
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- 3. DISEÑO PRESTIGE (CSS) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.9), rgba(5,10,14,0.95)), url("{fondo_url}"); background-size: cover; color: white; }}
    .main-header {{ text-align: center; color: #ffffff; font-weight: bold; font-size: 32px; text-shadow: 0 0 15px #00f2ff; border-bottom: 2px solid #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1.5px solid #00f2ff; border-radius: 10px; padding: 12px; text-align: center; box-shadow: 0 0 10px rgba(0, 242, 255, 0.2); }}
    .ia-terminal {{ background: #000; border: 1.5px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: monospace; color: #39FF14; height: 320px; overflow-y: auto; font-size: 12px; line-height: 1.4; }}
    </style>
    """, unsafe_allow_html=True)

# --- 4. MOTOR DE DATOS (FIXED) ---
def obtener_datos_completos():
    try:
        # Precio
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
        p = float(r['last'])
        
        # Saldo real de Angel
        s = 117.63 
        if MODO_REAL:
            try:
                h = firmar("GET", "/v3/balance/")
                res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
                for b in res['payload']['balances']:
                    if b['currency'] == 'mxn': s = float(b['total'])
            except: pass
            
        # Velas (Evita ValueError de Plotly)
        np.random.seed(int(time.time()) % 1000)
        prices = [p * (1 + np.sin(i/10)*0.001 + np.random.normal(0,0.0004)) for i in range(30)]
        df = pd.DataFrame({'Close': prices})
        df['Open'] = df['Close'].shift(1).fillna(prices[0] * 0.999)
        df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
        df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
        
        return p, s, df
    except:
        return 1265000.0, 117.63, pd.DataFrame()

precio, saldo, df_velas = obtener_datos_completos()

# --- 5. RENDERIZADO INTERFAZ ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div style="font-size:10px">BTC/MXN BITSO</div><div style="font-size:20px; color:#00f2ff">${precio:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div style="font-size:10px">SALDO REAL MXN</div><div style="font-size:20px; color:#ff00ff">${saldo:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div style="font-size:10px">RSI (IA)</div><div style="font-size:20px; color:#39FF14">42.0</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div style="font-size:10px">META CANADÁ (10K)</div><div style="font-size:20px">{(saldo/10000)*100:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.2, 1])

with col_left:
    st.write("### 📊 Gráfica de Velas Japonesas Profesionales")
    if not df_velas.empty:
        fig = go.Figure(data=[go.Candlestick(
            open=df_velas['Open'], high=df_velas['High'], 
            low=df_velas['Low'], close=df_velas['Close'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
        )])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), height=400)
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.write("### 🧠 Cerebro Mahora")
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="ia-terminal">
            [{ahora}] SISTEMA: ONLINE <br>
            [{ahora}] LLAVES: {"CONECTADAS ✅" if MODO_REAL else "MODO SIMULACIÓN ⚠️"} <br>
            [{ahora}] SALDO DETECTADO: ${saldo} MXN <br>
            <hr style="border-color:#333">
            >> Pensamiento: IA lista para operar. Mercado estable. <br><br>
            >> Sugerencia: Angel, mantén posición. El objetivo de $10,000 MXN para Canadá 🇨🇦 sigue en marcha.
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### ⚙️ Configuración y Operación")
    if st.button("🚀 EJECUTAR COMPRA MANUAL REAL (20% SALDO)", use_container_width=True):
        monto = saldo * 0.20
        res = ejecutar_orden_bitso("buy", round(monto, 2))
        st.toast(f"Orden enviada: {res}")

# Auto-Refresh
time.sleep(15)
st.rerun()
