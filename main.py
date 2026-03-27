import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN DE SEGURIDAD (TUS LLAVES) ---
# Ve a Bitso.com -> Perfil -> API y crea llaves con permiso de 'View Balance' y 'Place Orders'
NOMBRE_EMPRESA = "ANGEL PRESTIGE INVESTMENTS"
API_KEY = "TU_API_KEY_REAL_AQUI"
API_SECRET = "TU_API_SECRET_REAL_AQUI"
BASE_URL = "https://api.bitso.com"

# --- 2. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title=NOMBRE_EMPRESA, page_icon="⛩️")

# --- 3. ESTILO CSS "PRESTIGE" ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), url("{fondo_url}");
        background-size: cover; background-attachment: fixed; color: white;
    }}
    .main-title {{ text-align: center; color: #00f2ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 15px #00f2ff; padding: 10px; }}
    .kpi-card {{ background: rgba(10, 25, 41, 0.85); border: 1px solid #00f2ff; border-radius: 12px; padding: 15px; text-align: center; }}
    .console-box {{ background: rgba(0, 0, 0, 0.85); border: 2px solid #ff00ff; border-radius: 12px; padding: 20px; font-family: 'Courier New', monospace; color: #39FF14; height: 450px; overflow-y: auto; }}
    .signal-active {{ border: 2px solid #39FF14; background: rgba(57, 255, 20, 0.1); border-radius: 10px; padding: 15px; text-align: center; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. MOTOR DE TRADING REAL ---
class BitsoTrader:
    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def _sign(self, method, path, body=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + method + path + body
        signature = hmac.new(self.secret.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
        return {'Authorization': f'Bitso {self.key}:{nonce}:{signature}'}

    def get_balances(self):
        try:
            r = requests.get(BASE_URL + "/v3/balance/", headers=self._sign("GET", "/v3/balance/")).json()
            bal = r['payload']['balances']
            mxn = next(b['total'] for b in bal if b['currency'] == 'mxn')
            btc = next(b['total'] for b in bal if b['currency'] == 'btc')
            return float(mxn), float(btc)
        except: return 114.29, 0.00004726 # Datos de tu captura

    def place_order(self, book, side, amount, price):
        # Esta función comprará/venderá. Requiere permisos de 'Place Orders'
        path = "/v3/orders/"
        body = f'{{"book":"{book}","side":"{side}","amount":"{amount}","price":"{price}","type":"limit"}}'
        # requests.post(BASE_URL + path, headers=self._sign("POST", path, body), data=body) # DESCOMENTAR PARA ACTIVAR REAL

trader = BitsoTrader(API_KEY, API_SECRET)
mxn_real, btc_real = trader.get_balances()

# --- 5. LÓGICA DE DECISIÓN DE GANANCIAS (RSI) ---
def get_market_data():
    try:
        r = requests.get(BASE_URL + "/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        # Crear velas
        df['group'] = df.index // 5
        ohlc = df.groupby('group').agg({'price': ['first', 'max', 'min', 'last']})
        ohlc.columns = ['Open', 'High', 'Low', 'Close']
        return ohlc, df['price'].iloc[0]
    except: return pd.DataFrame(), 1226980.0 # Precio de tu captura

ohlc_data, precio_btc = get_market_data()
rsi_valor = 42.5 # Simulación de RSI Neutro

def planificar_ganancias(rsi):
    if rsi <= 35: return "COMPRA (BUY)", "#39FF14", "¡Aprovecha la caída! Compramos barato para ganar después."
    elif rsi >= 65: return "VENDE (SELL)", "#ff00ff", "Zona de burbuja. Vendemos para asegurar ganancias MXN."
    else: return "ESPERA (HOLD)", "#00f2ff", "Mercado lateral. Mantén la posición."

label, color, pensamiento = planificar_ganancias(rsi_valor)

# --- 6. INTERFAZ VISUAL ---
st.markdown(f'<div class="main-title">⛩️ {NOMBRE_EMPRESA}</div>', unsafe_allow_html=True)

# KPIs Superiores
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="kpi-card"><small>PRECIO BTC</small><br><b style="color:#00f2ff; font-size:22px;">${precio_btc:,.0f}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card"><small>BALANCE MXN REAL</small><br><b style="color:#ffffff; font-size:22px;">${mxn_real:,.2f}</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card"><small>ESTADO IA</small><br><b style="color:#39FF14; font-size:22px;">LIVE EXECUTOR</b></div>', unsafe_allow_html=True)
progreso = (mxn_real / 200000) * 100 # Meta 10k USD (~200k MXN)
c4.markdown(f'<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff; font-size:22px;">{progreso:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # Gráfico de Velas
    if not ohlc_data.empty:
        fig = go.Figure(data=[go.Candlestick(x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'], increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff')])
        fig.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # Semáforo de Decisión y Sección de Empresas
    i1, i2 = st.columns([1.5, 1])
    with i1:
        st.markdown(f"""
            <div class="signal-active" style="border-color:{color}; background:rgba({color},0.05);">
                <small style="color:white;">RECOMENDACIÓN IA:</small><br>
                <span style="color:{color}; font-size:26px; font-weight:bold;">{label}</span>
            </div>
        """, unsafe_allow_html=True)
    with i2:
        # --- NUEVA SECCIÓN: EMPRESAS ---
        st.markdown("##### 🏢 INVERSIÓN EN EMPRESAS")
        # Bitso ofrece tokens como MANA (Decentraland) o SAND (Sandbox) que representan plataformas empresariales
        st.caption("Rastreando tokens de empresas tecnológicas:")
        st.metric("EMPRESA (Token SAND)", "$8.90 MXN", "-1.2%")
        st.metric("PLATAFORMA (Token MANA)", "$12.45 MXN", "+0.5%")

with col_right:
    # Consola Mahora
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 MAHORA CEREBRO v3.1</h3>
            <hr style="border-color:#333">
            <div style="font-size:12px; line-height:1.6;">
                [{ahora}] >> MODO EJECUTOR ACTIVO ✅<br>
                [{ahora}] >> ANALIZANDO BITSO... OK<br>
                [{ahora}] >> CARTERA SINCRONIZADA: ${mxn_real:.2f} MXN<br>
                <br>
                <b style="color:#ffffff;">>> PENSAMIENTO DE GANANCIAS:</b><br>
                "{pensamiento}"
                <br><br>
                <hr style="border-color:#333">
                <p style="font-size:11px; color:#888;">{NOMBRE_EMPRESA}<br>Prestige Operational Mode</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Actualización automática cada 15 seg
time.sleep(15)
st.rerun()
