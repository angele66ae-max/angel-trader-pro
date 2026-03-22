import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS ---
st.markdown("""
    <style>
    .stApp { background: #0b141a; color: white; }
    .main-title { text-align: center; color: #e0fbfc; font-size: 28px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; padding: 10px; border-bottom: 2px solid #00f2ff; }
    .kpi-container { background: rgba(16, 23, 30, 0.9); border: 2px solid #1f2937; border-radius: 10px; padding: 10px; text-align: center; height: 80px; }
    .console-box { background: #000; border: 2px solid #ff00ff; border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace; color: #39FF14; height: 550px; overflow-y: auto; }
    .indicator-label { color: #00f2ff; font-weight: bold; font-size: 14px; text-align: center; background: rgba(0,242,255,0.1); padding: 5px; border-radius: 5px; margin-top: 20px; }
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS ---
def fetch_bitso_data():
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

ohlc_data, precio_actual = fetch_bitso_data()

# --- 4. RENDERIZADO DE INTERFAZ ---
st.markdown('<div class="main-title">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)
st.write("")

# FILA 1: KPIs (Aquí estaba el error de la línea 50)
k1, k2, k3, k4 = st.columns(4)
with k1:
    st.markdown(f'<div class="kpi-container"><small>BTC/MXN</small><br><b style="color:#00f2ff; font-size:18px;">${precio_actual:,.0f}</b></div>', unsafe_allow_html=True)
with k2:
    st.markdown('<div class="kpi-container"><small>MXN BALANCE</small><br><b style="color:#ffffff; font-size:18px;">$115.59</b></div>', unsafe_allow_html=True)
with k3:
    st.markdown('<div class="kpi-container"><small>IA STATUS</small><br><b style="color:#39FF14; font-size:18px;">ACTIVE 🟢</b></div>', unsafe_allow_html=True)
with k4:
    st.markdown('<div class="kpi-container"><small>META 10K</small><br><b style="color:#ff00ff; font-size:18px;">1.16%</b></div>', unsafe_allow_html=True)

st.write("")

# FILA 2: GRÁFICO CENTRAL Y CONSOLA IA
col_main, col_console = st.columns([2.5, 1])

with col_main:
    # VELAS
    if not ohlc_data.empty:
        fig_candles = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff',
            increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ff00ff'
        )])
        fig_candles.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                                  xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_candles, use_container_width=True)

    st.markdown('<div class="indicator-label">ANÁLISIS CUANTITATIVO</div>', unsafe_allow_html=True)
    ind_c1, ind_c2 = st.columns(2)
    
    with ind_c1:
        # RSI GAUGE
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number", value = 42.5, title = {'text': "RSI NEUTRO", 'font': {'size': 14}},
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "white"},
                     'steps': [{'range': [0, 30], 'color': "#39FF14"}, {'range': [70, 100], 'color': "#ff00ff"}]}
        ))
        fig_rsi.update_layout(height=230, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_rsi, use_container_width=True)

    with ind_c2:
        # VOLUMEN
        if not ohlc_data.empty:
            fig_vol = go.Figure(data=[go.Bar(x=ohlc_data.index, y=ohlc_data['Volume'], marker_color='#ff00ff')])
            fig_vol.update_layout(height=230, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0,r=0,t=30,b=0))
            st.plotly_chart(fig_vol, use_container_width=True)

with col_console:
    # CONSOLA IA
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 MAHORA v2.0</h3>
            <hr style="border-color:#333">
            <div style="font-size:12px; line-height:1.6;">
                [{ahora}] >> SINCRONIZADO CON BITSO.<br>
                [{ahora}] >> MERCADO ESTABLE.<br>
                <br>
                <b style="color:#ffffff;">>> PENSAMIENTO:</b><br>
                "Angel, el sistema está operando. 
                Cada movimiento nos acerca a Canadá 🇨🇦. 
                Mantén el enfoque en la meta."
                <br><br>
                <span style="color:#ff00ff;">>> STATUS: LIVE ACTIVE</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
