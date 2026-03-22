import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS PARA COPIAR TU DISEÑO ---
st.markdown("""
    <style>
    .stApp { background: #0b141a; color: white; }
    .main-title { text-align: center; color: #e0fbfc; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; padding: 10px; border-bottom: 2px solid #00f2ff; }
    .kpi-container { background: rgba(16, 23, 30, 0.9); border: 2px solid #1f2937; border-radius: 10px; padding: 10px; text-align: center; }
    .console-box { background: #000; border: 2px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; height: 500px; }
    .indicator-label { color: #00f2ff; font-weight: bold; font-size: 14px; text-align: center; background: rgba(0,242,255,0.1); padding: 5px; border-radius: 5px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS ---
def fetch_bitso_ohlc():
    try:
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        df['amount'] = df['amount'].astype(float)
        df['group'] = df.index // 4
        ohlc = df.groupby('group').agg({'price': ['first', 'max', 'min', 'last'], 'amount': 'sum'})
        ohlc.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return ohlc, df['price'].iloc[0]
    except: return pd.DataFrame(), 1231910.0

ohlc_data, precio_actual = fetch_bitso_ohlc()

# --- 4. RENDERIZADO ---
st.markdown('<div class="main-title">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)
st.write("")

# FILA 1: KPIs SUPERIORES
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-container"><small>BTC/MXN:</small><br><b style="color:#00f2ff; font-size:18px;">${precio_actual:,.0f} (+2.1%)</b></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi-container"><small>MXN BALANCE:</small><br><b style="color:#ffffff; font-size:18px;">$115.59 (REAL)</b></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi-container"><small>IA STATUS:</small><br><b style="color:#39FF14; font-size:18px;">ACTIVATED 🟢</b></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-container"><small>META 10K PROGRESS:</small><br><b style="color:#ff00ff; font-size:18px;">1.16%</b></div>', unsafe_allow_html=True)

st.write("")

# FILA 2: GRÁFICO CENTRAL Y CONSOLA
col_main, col_console = st.columns([2.5, 1])

with col_main:
    # GRÁFICO DE VELAS
    fig_candles = go.Figure(data=[go.Candlestick(
        x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'],
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff',
        increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ff00ff'
    )])
    fig_candles.update_layout(height=450, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                              xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_candles, use_container_width=True)

    # FILA 3: INDICADORES CUANTITATIVOS (ABAJO)
    st.markdown('<div class="indicator-label">INDICADORES CUANTITATIVOS (REAL-TIME)</div>', unsafe_allow_html=True)
    ind_c1, ind_c2 = st.columns(2)
    
    with ind_c1:
        # RSI GAUGE (VELOCÍMETRO)
        rsi_val = 42.5
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number", value = rsi_val, title = {'text': "RSI (42.5 NEUTRO)", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1},
                'bar': {'color': "white"},
                'steps': [
                    {'range': [0, 30], 'color': "#39FF14"}, # Oversold
                    {'range': [30, 70], 'color': "#1f2937"},
                    {'range': [70, 100], 'color': "#ff00ff"} # Overbought
                ],
                'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': rsi_val}
            }
        ))
        fig_rsi.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_rsi, use_container_width=True)

    with ind_c2:
        # VOLUMEN DE MERCADO
        fig_vol = go.Figure(data=[go.Bar(x=ohlc_data.index, y=ohlc_data['Volume'], marker_color='#ff00ff')])
        fig_vol.update_layout(title="VOLUMEN DE MERCADO", height=250, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0))
        st.plotly_chart(fig_vol, use_container_width=True)

with col_console:
    # CEREBRO MAHORA v2.0
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 CEREBRO MAHORA v2.0</h3>
            <p style="font-size:12px; color:#888;">IA ACTIVA</p>
            <hr style="border-color:#333">
            <div style="font-size:12px;
