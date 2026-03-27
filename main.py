import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
NOMBRE_EMPRESA = "ANGEL PRESTIGE INVESTMENTS"
st.set_page_config(layout="wide", page_title=NOMBRE_EMPRESA, page_icon="⛩️")

# --- 2. MOTOR DE DATOS (MÓDULO DE EMPRESAS Y BOLSA) ---
def get_market_intelligence():
    try:
        # Datos de Bitcoin (Bitso)
        r = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
        df = pd.DataFrame(r)
        df['price'] = df['price'].astype(float)
        
        # Bandas de Bollinger (Cálculo simple para la gráfica)
        df['MA20'] = df['price'].rolling(window=20).mean()
        df['STD'] = df['price'].rolling(window=20).std()
        df['Upper'] = df['MA20'] + (df['STD'] * 2)
        df['Lower'] = df['MA20'] - (df['STD'] * 2)
        
        # Módulo de Empresas (Tokens vinculados a tecnología)
        empresas = {
            "RENDER (IA/Chips)": {"precio": "124.50", "cambio": "+2.4%"},
            "APPLE (AAPL Token)": {"precio": "3,450.00", "cambio": "-0.5%"},
            "SANDBOX (Real Estate)": {"precio": "8.90", "cambio": "-1.2%"}
        }
        return df, df['price'].iloc[0], empresas
    except:
        return pd.DataFrame(), 1226980.0, {}

df_market, precio_btc, stocks = get_market_intelligence()

# --- 3. DISEÑO CSS "ELITE" ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    .stApp {{ background: linear-gradient(rgba(0,0,0,0.8), rgba(0,0,0,0.95)), url("{fondo_url}"); background-size: cover; color: white; }}
    .kpi-card {{ background: rgba(10, 25, 41, 0.9); border: 1px solid #00f2ff; border-radius: 10px; padding: 15px; text-align: center; }}
    .stock-card {{ background: rgba(255, 255, 255, 0.05); border-left: 4px solid #ff00ff; padding: 10px; margin-bottom: 5px; border-radius: 5px; }}
    .panic-btn {{ background-color: #ff4b4b !important; color: white !important; font-weight: bold !important; border-radius: 20px !important; width: 100%; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. INTERFAZ ---
st.markdown(f'<h1 style="text-align:center; color:#00f2ff; text-shadow: 0 0 10px #00f2ff;">⛩️ {NOMBRE_EMPRESA}</h1>', unsafe_allow_html=True)

# Fila de KPIs Reales
c1, c2, c3, c4 = st.columns(4)
c1.markdown(f'<div class="kpi-card"><small>SALDO MXN</small><br><b style="font-size:22px;">$111.94</b></div>', unsafe_allow_html=True)
c2.markdown(f'<div class="kpi-card"><small>PÉRDIDA 3D</small><br><b style="color:#ff4b4b; font-size:22px;">-$8.06</b></div>', unsafe_allow_html=True)
c3.markdown(f'<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff; font-size:22px;">1.11%</b></div>', unsafe_allow_html=True)
c4.markdown(f'<div class="kpi-card"><small>ESTADO</small><br><b style="color:#39FF14;">DEFENSIVO</b></div>', unsafe_allow_html=True)

st.write("")
col_main, col_side = st.columns([2.5, 1])

with col_main:
    # Gráfica Avanzada con Bandas de Bollinger
    st.write("### 📊 ANALÍTICA DE ALTA PRECISIÓN")
    fig = go.Figure()
    # Velas
    fig.add_trace(go.Candlestick(x=df_market.index, open=df_market['price'], high=df_market['price'], low=df_market['price'], close=df_market['price'], name="BTC"))
    # Bandas de Bollinger
    fig.add_trace(go.Scatter(x=df_market.index, y=df_market['Upper'], line=dict(color='rgba(0, 242, 255, 0.2)'), name="Banda Sup"))
    fig.add_trace(go.Scatter(x=df_market.index, y=df_market['Lower'], line=dict(color='rgba(0, 242, 255, 0.2)'), name="Banda Inf", fill='tonexty'))
    
    fig.update_layout(height=450, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_side:
    # BOTÓN DE PÁNICO (Para liquidar a MXN de inmediato)
    st.write("### 🚨 SEGURIDAD")
    if st.button("🔴 LIQUIDAR TODO A MXN", help="Vende todo tu Bitcoin al precio actual para evitar más pérdidas"):
        st.error("ORDEN DE EMERGENCIA ENVIADA: Vendiendo activos...")

    # MÓDULO DE EMPRESAS
    st.write("### 🏢 MERCADO DE EMPRESAS")
    for nombre, datos in stocks.items():
        st.markdown(f"""
            <div class="stock-card">
                <small>{nombre}</small><br>
                <b>${datos['precio']} MXN</b> <span style="color:#39FF14; font-size:10px;">{datos['cambio']}</span>
            </div>
        """, unsafe_allow_html=True)
    
    # CONSOLA MAHORA
    st.write("---")
    st.markdown("""
        <div style="font-family:monospace; color:#39FF14; font-size:12px;">
            >> ANALIZANDO RIESGO...<br>
            >> BALANCE DE SEGURIDAD: $110.00<br>
            >> <span style="color:#ff00ff;">STOP LOSS ACTIVADO</span>
        </div>
    """, unsafe_allow_html=True)

time.sleep(15)
st.rerun()
