import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS CON EL FONDO DE CIRCUITOS ---
# Usamos el enlace directo a tu imagen de fondo
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.8)), 
                    url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .main-title {{ text-align: center; color: #00f2ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 15px #00f2ff; padding: 10px; }}
    .kpi-card {{ 
        background: rgba(10, 25, 41, 0.7); 
        backdrop-filter: blur(8px); 
        border: 1px solid #00f2ff; 
        border-radius: 12px; padding: 12px; text-align: center;
    }}
    .console-box {{ 
        background: rgba(0, 0, 0, 0.85); 
        border: 2px solid #ff00ff; 
        border-radius: 15px; padding: 20px; 
        font-family: 'Courier New', monospace; color: #39FF14; height: 520px;
    }}
    .signal-box {{
        margin-top: 30px;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        text-transform: uppercase;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS ---
def fetch_data():
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        df['amount'] = df['amount'].astype(float)
        df['group'] = df.index // 4
        ohlc = df.groupby('group').agg({'price': ['first', 'max', 'min', 'last'], 'amount': 'sum'})
        ohlc.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return ohlc, df['price'].iloc[0]
    except:
        return pd.DataFrame(), 1261324.0

ohlc_data, precio_actual = fetch_data()
rsi_val = 42.5 # Simulación de RSI Neutro

# --- 4. LÓGICA DE SEÑAL IA ---
def get_action(rsi):
    if rsi <= 35: return "COMPRA (BUY)", "rgba(57, 255, 20, 0.2)", "#39FF14", "Precio bajo. ¡Es hora de comprar!"
    elif rsi >= 65: return "VENDE (SELL)", "rgba(255, 0, 255, 0.2)", "#ff00ff", "Precio alto. Toma ganancias."
    else: return "ESPERA (HOLD)", "rgba(0, 242, 255, 0.2)", "#00f2ff", "Mercado estable. Mantén la posición."

label, bg_color, text_color, pensamiento = get_action(rsi_val)

# --- 5. INTERFAZ ---
st.markdown('<div class="main-title">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# KPIs
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi-card"><small>BTC/MXN</small><br><b style="color:#00f2ff; font-size:20px;">${precio_actual:,.0f}</b></div>', unsafe_allow_html=True)
k2.markdown('<div class="kpi-card"><small>MXN BALANCE</small><br><b style="color:#ffffff; font-size:20px;">$115.59</b></div>', unsafe_allow_html=True)
k3.markdown('<div class="kpi-card"><small>IA STATUS</small><br><b style="color:#39FF14; font-size:20px;">ACTIVATED</b></div>', unsafe_allow_html=True)
k4.markdown('<div class="kpi-card"><small>META 10K</small><br><b style="color:#ff00ff; font-size:20px;">1.16%</b></div>', unsafe_allow_html=True)

st.write("")
col_main, col_ia = st.columns([2.5, 1])

with col_main:
    # Velas Japonesas
    if not ohlc_data.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
        )])
        fig.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # Indicadores
    c1, c2 = st.columns(2)
    with c1:
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=rsi_val, title={'text': "RSI STATUS"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "white"}, 'steps': [{'range': [0, 35], 'color': "#39FF14"}, {'range': [65, 100], 'color': "#ff00ff"}]}))
        fig_rsi.update_layout(height=230, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"})
        st.plotly_chart(fig_rsi, use_container_width=True)
    with c2:
        st.markdown(f"""
            <div class="signal-box" style="background:{bg_color}; border: 2px solid {text_color}; color:{text_color};">
                <small style="color:white;">RECOMENDACIÓN IA:</small><br>{label}
            </div>
        """, unsafe_allow_html=True)

with col_ia:
    # Consola Cerebro Mahora
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 MAHORA v2.0</h3>
            <hr style="border-color:#333">
            <div style="font-size:13px; line-height:1.6;">
                [{ahora}] >> ESCANEANDO MERCADO...<br>
                [{ahora}] >> RSI: {rsi_val} (NEUTRO)<br>
                <br>
                <b style="color:#ffffff;">>> PENSAMIENTO:</b><br>
                "{pensamiento}"
                <br><br>
                <hr style="border-color:#333">
                <p style="font-size:11px; color:#888;">Objetivo: Canadá 🇨🇦<br>Meta: $10,000 USD</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
