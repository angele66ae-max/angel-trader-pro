import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="MahoraShark Omni-Quantum")
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY else False

# --- CSS PRESTIGE (GOTAS DE AGUA + NEÓN) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); background-size: cover; color: white; }}
    .metric-card {{ background: rgba(11, 20, 26, 0.9); border: 1px solid #00f2ff; border-radius: 8px; padding: 10px; text-align: center; box-shadow: 0 0 10px #00f2ff33; }}
    .metric-val {{ font-size: 22px; font-weight: bold; color: #00f2ff; }}
    .ia-terminal {{ background: rgba(0,0,0,0.8); border-left: 3px solid #ff00ff; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; font-size: 12px; height: 300px; overflow-y: auto; }}
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE DATOS ---
def get_balance():
    if not MODO_REAL: return pd.DataFrame([{"Asset": "MXN", "Total": 68.91}, {"Asset": "BTC", "Total": 0.00003542}])
    nonce = str(int(time.time() * 1000))
    signature = hmac.new(API_SECRET.encode(), (nonce + "GET" + "/v3/balance/").encode(), hashlib.sha256).hexdigest()
    r = requests.get("https://api.bitso.com/v3/balance/", headers={'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}'}).json()
    return pd.DataFrame([{"Asset": b['currency'].upper(), "Total": float(b['total'])} for b in r['payload']['balances'] if float(b['total']) > 0])

def get_market_data():
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
    precio = float(r['last'])
    # Datos simulados para la gráfica pro
    df = pd.DataFrame({'Close': [precio * (1 + np.sin(i/5)*0.002) for i in range(50)]})
    df['Open'] = df['Close'].shift(1).fillna(precio)
    df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
    df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
    df['Vol'] = np.random.randint(100, 1000, 50)
    return precio, df

# --- PROCESO ---
precio, df = get_market_data()
cartera = get_balance()
saldo_mxn = cartera[cartera['Asset'] == 'MXN']['Total'].iloc[0] if 'MXN' in cartera['Asset'].values else 0.0

# --- UI ---
st.markdown("<h2 style='text-align: center; color: #00f2ff;'>ANGEL'S PRESTIGE CENTER</h2>", unsafe_allow_html=True)

# Top Bar
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="metric-card"><small>BTC/MXN</small><div class="metric-val">${precio:,.0f}</div></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="metric-card"><small>MXN BALANCE</small><div class="metric-val" style="color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="metric-card"><small>IA STATUS</small><div class="metric-val" style="color:#39FF14">ACTIVATED 🟢</div></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="metric-card"><small>META 10K PROGRESS</small><div class="metric-val">{(saldo_mxn/10000)*100:.2f}%</div></div>', unsafe_allow_html=True)

st.write("")

col_left, col_right = st.columns([2.5, 1])

with col_left:
    # GRÁFICA COMBINADA (VELAS + VOLUMEN)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.7])
    fig.add_trace(go.Candlestick(open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'], 
                                 increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'), row=1, col=1)
    fig.add_trace(go.Bar(y=df['Vol'], marker_color='#39FF14', opacity=0.3), row=2, col=1)
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, 
                      xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # INDICADOR RSI GAUGE
    st.write("### INDICADORES CUANTITATIVOS")
    rsi_val = 42.5 # Valor ejemplo
    fig_rsi = go.Figure(go.Indicator(
        mode = "gauge+number", value = rsi_val, title = {'text': "RSI (14)"},
        gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00f2ff"},
                 'steps': [{'range': [0, 30], 'color': "#ff00ff"}, {'range': [70, 100], 'color': "#ff00ff"}]}))
    fig_rsi.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=0,b=0))
    st.plotly_chart(fig_rsi, use_container_width=True)

with col_right:
    # TERMINAL CEREBRO MAHORA
    st.markdown(f"""
    <div style="background:#ff00ff22; border:1px solid #ff00ff; border-radius:10px; padding:10px;">
        <h4 style="margin:0; color:#ff00ff;">🧠 CEREBRO MAHORA v4.0</h4>
        <div class="ia-terminal">
            [{datetime.now().strftime("%H:%M:%S")}] >> MERCADO ESTABLE.<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> RSI EN {rsi_val}. NEUTRO.<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> HOLDING MXN...<br>
            <hr>
            >> PENSAMIENTO:<br>
            Angel, el mercado muestra baja volatilidad. Sugiero mantener posición para el viaje a Canadá 🇨🇦.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("### 💰 TUS ACTIVOS")
    st.table(cartera)
    
    if st.button("🚀 EJECUTAR ESCANEO QUANTUM", use_container_width=True):
        st.toast("Escaneando liquidez en Bitso...")

time.sleep(20)
st.rerun()
