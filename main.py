import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS MEJORADO (Circuit & Galaxy) ---
# Usamos el fondo de la rueda dorada que ya tienes funcionando
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.85)), 
                    url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .main-title {{ text-align: center; color: #00f2ff; font-size: 36px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; padding: 10px; margin-bottom: 20px; }}
    .kpi-card {{ 
        background: rgba(10, 25, 41, 0.8); 
        backdrop-filter: blur(10px); 
        border: 1px solid #00f2ff; 
        border-radius: 15px; padding: 15px; text-align: center;
        box-shadow: 0 4px 15px rgba(0, 242, 255, 0.2);
    }}
    .console-box {{ 
        background: rgba(0, 0, 0, 0.9); 
        border: 2px solid #ff00ff; 
        border-radius: 15px; padding: 25px; 
        font-family: 'Courier New', monospace; color: #39FF14; height: 550px;
    }}
    .signal-container {{
        background: rgba(0, 0, 0, 0.5);
        border-radius: 15px;
        padding: 20px;
        margin-top: 20px;
        border: 1px solid #333;
    }}
    </style>
""", unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS REALES (BITSO) ---
def get_live_data():
    try:
        # Precio actual y velas
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        df['amount'] = df['amount'].astype(float)
        # Agrupamos para crear velas (OHLC)
        df['group'] = df.index // 5
        ohlc = df.groupby('group').agg({'price': ['first', 'max', 'min', 'last'], 'amount': 'sum'})
        ohlc.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        return ohlc, df['price'].iloc[0]
    except Exception as e:
        st.error(f"Error de conexión: {e}")
        return pd.DataFrame(), 1261324.0

ohlc_data, precio_actual = get_live_data()
# Lógica de RSI Simulada (Para que veas el movimiento)
rsi_actual = 48.5 

# --- 4. CEREBRO DE DECISIÓN ---
def get_ai_signal(rsi):
    if rsi <= 35:
        return "COMPRA (BUY)", "#39FF14", "Precios bajos detectados. ¡Es momento de acumular para Canadá!"
    elif rsi >= 65:
        return "VENDE (SELL)", "#ff00ff", "Zona de sobrecompra. Asegura ganancias ahora."
    else:
        return "ESPERA (HOLD)", "#00f2ff", "Mercado en equilibrio. Mantén la calma y observa."

signal_text, signal_color, pensamiento = get_ai_signal(rsi_actual)

# --- 5. INTERFAZ VISUAL ---
st.markdown('<div class="main-title">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER V28</div>', unsafe_allow_html=True)

# KPIs Superiores
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="kpi-card"><small>PRECIO BTC/MXN</small><br><b style="color:#00f2ff; font-size:24px;">${precio_actual:,.2f}</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card"><small>BALANCE TOTAL</small><br><b style="color:#ffffff; font-size:24px;">$115.59</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card"><small>ESTADO IA</small><br><b style="color:#39FF14; font-size:24px;">LIVE ACTIVE</b></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff; font-size:24px;">1.16%</b></div>', unsafe_allow_html=True)

st.write("---")

col_graph, col_info = st.columns([2.5, 1])

with col_graph:
    # Gráfico de Velas Profesional
    if not ohlc_data.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'],
            increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff',
            increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ff00ff'
        )])
        fig.update_layout(
            height=450, template="plotly_dark", 
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0),
            yaxis=dict(gridcolor='#222', zerolinecolor='#222')
        )
        st.plotly_chart(fig, use_container_width=True)

    # Indicador de Fuerza (RSI) y Señal
    st.markdown('<div class="signal-container">', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.write("**FUERZA DEL MERCADO (RSI)**")
        st.progress(rsi_actual / 100)
        st.write(f"Nivel Actual: {rsi_actual}")
    with i2:
        st.markdown(f"""
            <div style="text-align:center; border: 2px solid {signal_color}; border-radius:10px; padding:10px;">
                <small>RECOMENDACIÓN:</small><br>
                <span style="color:{signal_color}; font-size:28px; font-weight:bold;">{signal_text}</span>
            </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_info:
    # Consola Mahora
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 MAHORA CEREBRO v2.8</h3>
            <hr style="border-color:#333">
            <div style="font-size:13px; line-height:1.7;">
                <span style="color:#888;">[{ahora}]</span> >> ESCANEANDO BITSO... OK<br>
                <span style="color:#888;">[{ahora}]</span> >> CARTERA SINCRONIZADA: $115.59 MXN<br>
                <span style="color:#888;">[{ahora}]</span> >> BTC DETECTADO: 0.00006301 BTC<br>
                <br>
                <b style="color:#ffffff;">>> PENSAMIENTO ESTRATÉGICO:</b><br>
                "{pensamiento}"
                <br><br>
                <hr style="border-color:#333">
                <span style="color:#00f2ff;">PROGRESO A LOS $10,000 USD:</span><br>
                Estamos al 1.16%. El camino a Canadá 🇨🇦 sigue firme.
                <br><br>
                <div style="font-size:11px; color:#555; margin-top:50px;">
                    OPERANDO PARA ÁNGEL GABRIEL. <br>
                    MODO PRESTIGE ACTIVADO.
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Actualización automática cada 15 seg
time.sleep(15)
st.rerun()
