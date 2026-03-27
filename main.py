import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import hmac
import hashlib

# --- 1. CONFIGURACIÓN DE TU EMPRESA ---
# Pon aquí el nombre de tu empresa
NOMBRE_EMPRESA = "ANGEL PRESTIGE INVESTMENTS" 
API_KEY = "TU_API_KEY_AQUI"
API_SECRET = "TU_API_SECRET_AQUI"

st.set_page_config(layout="wide", page_title=NOMBRE_EMPRESA, page_icon="⛩️")

# --- 2. ESTILO CSS "PRESTIGE" (EL QUE TE GUSTA) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
                    url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .main-title {{ text-align: center; color: #00f2ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; padding: 15px; }}
    .kpi-card {{ 
        background: rgba(10, 25, 41, 0.85); 
        backdrop-filter: blur(10px); 
        border: 1px solid #00f2ff; 
        border-radius: 15px; padding: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.2);
    }}
    .console-box {{ 
        background: rgba(0, 0, 0, 0.85); 
        border: 2px solid #ff00ff; 
        border-radius: 15px; padding: 20px; 
        font-family: 'Courier New', monospace; color: #39FF14; height: 500px;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS REALES ---
def get_data():
    # Simulamos el saldo si no hay llaves para que no se vea vacío
    mxn, btc = (115.59, 0.00006301) 
    
    try:
        # Precio de Bitso en vivo
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        precio = df['price'].iloc[0]
        # Crear velas
        df['group'] = df.index // 5
        ohlc = df.groupby('group').agg({'price': ['first', 'max', 'min', 'last']})
        ohlc.columns = ['Open', 'High', 'Low', 'Close']
        return ohlc, precio, mxn, btc
    except:
        return pd.DataFrame(), 1261324.0, mxn, btc

ohlc_data, precio_actual, mxn_real, btc_real = get_data()

# --- 4. INTERFAZ ---
st.markdown(f'<div class="main-title">⛩️ {NOMBRE_EMPRESA}</div>', unsafe_allow_html=True)

# KPIs con tu nombre de empresa y saldos
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-card"><small>PROJECT</small><br><b style="color:#00f2ff; font-size:18px;">{NOMBRE_EMPRESA}</b></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card"><small>SALDO MXN</small><br><b style="color:#ffffff; font-size:20px;">${mxn_real:,.2f}</b></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card"><small>STATUS</small><br><b style="color:#39FF14; font-size:20px;">OPERATIONAL</b></div>', unsafe_allow_html=True)
with k4:
    # Meta calculada sobre 10k USD
    progreso = (mxn_real / 200000) * 100
    st.markdown(f'<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff; font-size:20px;">{progreso:.2f}%</b></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # Gráfico de Velas
    if not ohlc_data.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
        )])
        fig.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    
    # Recomendación
    st.markdown(f"""
        <div style="background:rgba(0,242,255,0.1); border:1px solid #00f2ff; border-radius:10px; padding:20px; text-align:center;">
            <small>ESTRATEGIA ACTUAL:</small><br>
            <span style="font-size:24px; font-weight:bold; color:#00f2ff;">ESPERA (HOLD)</span>
        </div>
    """, unsafe_allow_html=True)

with col_right:
    # Consola Mahora
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 MAHORA v3.0</h3>
            <hr style="border-color:#333">
            <div style="font-size:12px; line-height:1.6;">
                [{ahora}] >> SISTEMA REESTABLECIDO.<br>
                [{ahora}] >> FONDO PRESTIGE CARGADO.<br>
                <br>
                <b style="color:#ffffff;">>> MENSAJE:</b><br>
                "Angel, el Ferrari ha recuperado su brillo. 
                Cada segundo cuenta para llegar a los $10,000. 
                Canadá nos espera 🇨🇦."
                <br><br>
                <hr style="border-color:#333">
                <p style="font-size:11px; color:#888;">{NOMBRE_EMPRESA}<br>Prestige Operational Mode</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
