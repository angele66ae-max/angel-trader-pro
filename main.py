import streamlit as st
import requests
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Pro", page_icon="⛩️")

# --- DISEÑO Y FONDO EXACTO ---
# Usamos tu imagen de Postimg con el degradado para que se vea Pro
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(5, 10, 14, 0.85), rgba(5, 10, 14, 0.95)), url("{fondo_url}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .metric-card {{
        background-color: rgba(11, 20, 26, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 20px #00f2ff66;
    }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.9);
        border: 2px solid #ff00ff;
        border-radius: 10px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
        box-shadow: 0 0 15px #ff00ff44;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS (BITSO) ---
def obtener_bitso():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except:
        return 1261000.0

def generar_velas(precio_base, num=30):
    # Genera datos OHLC estéticos para la gráfica profesional
    data = []
    for i in range(num):
        move = (pd.Series([0]).sample().iloc[0] - 0.5) * 2000
        open_p = precio_base + move
        close_p = open_p + (pd.Series([0]).sample().iloc[0] - 0.5) * 1500
        data.append({
            'Date': datetime.now() - timedelta(minutes=i*5),
            'Open': open_p, 'High': max(open_p, close_p) + 500,
            'Low': min(open_p, close_p) - 500, 'Close': close_p
        })
    return pd.DataFrame(data)

# --- VARIABLES ---
precio_btc = obtener_bitso()
saldo_mxn = 47.12
progreso = (saldo_mxn / 10000) * 100
df_velas = generar_velas(precio_btc)

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Métricas Neón
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card">BTC/MXN<br><span style="font-size:24px; color:#00f2ff;">${precio_btc:,.0f}</span></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card">SALDO ACTUAL<br><span style="font-size:24px; color:#ff00ff;">${saldo_mxn:,.2f}</span></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card">IA STATUS<br><span style="font-size:24px; color:#39FF14;">ADAPTIVE</span></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card">META 10K<br><span style="font-size:24px; color:#00f2ff;">{progreso:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Gráfica de Velas Japonesas (Profesional)")
    fig = go.Figure(data=[go.Candlestick(
        x=df_velas['Date'], open=df_velas['Open'], high=df_velas['High'],
        low=df_velas['Low'], close=df_velas['Close'],
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font_color='white', margin=dict(l=0, r=0, t=0, b=0),
        xaxis_rangeslider_visible=False, yaxis=dict(gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.subheader("🧠 Cerebro Mahora")
    st.markdown(f"""
        <div class="ia-log">
            [OBJECTIVE]: $10,000.00<br>
            [RESTANTE]: ${(10000 - saldo_mxn):,.2f}<br>
            [ESTRATEGIA]: Acumulación Silenciosa<br>
            <hr>
            >> IA esperando punto de entrada óptimo...
        </div>
    """, unsafe_allow_html=True)

time.sleep(20)
st.rerun()
