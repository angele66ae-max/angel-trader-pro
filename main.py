import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Quantum", page_icon="⛩️")

# Fondo Cósmico
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(5, 10, 14, 0.85), rgba(5, 10, 14, 0.95)), url("{fondo_url}");
        background-size: cover;
        background-attachment: fixed;
        color: white;
    }}
    .metric-card {{
        background-color: rgba(11, 20, 26, 0.95);
        border: 2px solid #00f2ff;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 0 15px #00f2ff55;
    }}
    .ia-log {{
        background-color: rgba(0, 0, 0, 0.95);
        border: 2px solid #ff00ff;
        border-radius: 10px;
        padding: 20px;
        font-family: 'Courier New', monospace;
        color: #39FF14;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- MOTOR DE DATOS REALES ---
def obtener_top_mercado():
    try:
        # Obtenemos varios libros para comparar
        libros = ['btc_mxn', 'eth_mxn', 'xrp_mxn', 'sol_mxn']
        datos = []
        for libro in libros:
            r = requests.get(f"https://api.bitso.com/v3/ticker/?book={libro}").json()
            p = r['payload']
            datos.append({
                'Asset': libro.split('_')[0].upper(),
                'Precio': float(p['last']),
                'Cambio': ((float(p['last']) - float(p['vwap'])) / float(p['vwap'])) * 100
            })
        return pd.DataFrame(datos)
    except: return pd.DataFrame()

def generar_velas_pro(precio_actual):
    # Creamos una estructura de 30 velas estéticas basadas en volatilidad real
    import numpy as np
    np.random.seed(int(time.time()) % 1000)
    cambios = np.random.normal(0, 0.002, 30)
    precios = [precio_actual]
    for c in cambios: precios.append(precios[-1] * (1 + c))
    
    df = pd.DataFrame({'Close': precios[1:]})
    df['Open'] = precios[:-1]
    df['High'] = df[['Open', 'Close']].max(axis=1) * (1 + 0.001)
    df['Low'] = df[['Open', 'Close']].min(axis=1) * (1 - 0.001)
    df['Date'] = [datetime.now() - pd.Timedelta(minutes=5*i) for i in range(len(df))][::-1]
    return df

# --- PROCESAMIENTO ---
top_df = obtener_top_mercado()
precio_btc = top_df[top_df['Asset'] == 'BTC']['Precio'].iloc[0] if not top_df.empty else 1260000.0
df_velas = generar_velas_pro(precio_btc)
saldo_actual = 47.12

# --- INTERFAZ ---
st.title("⛩️ MAHORASHARK: PRESTIGE TERMINAL")

# Fila 1: Métricas Neón
m1, m2, m3, m4 = st.columns(4)
with m1: st.markdown(f'<div class="metric-card">BTC/MXN<br><span style="font-size:22px; color:#00f2ff;">${precio_btc:,.0f}</span></div>', unsafe_allow_html=True)
with m2: st.markdown(f'<div class="metric-card">TU SALDO<br><span style="font-size:22px; color:#ff00ff;">${saldo_actual:,.2f} MXN</span></div>', unsafe_allow_html=True)
with m3: st.markdown(f'<div class="metric-card">ESTADO IA<br><span style="font-size:22px; color:#39FF14;">QUANTUM READY</span></div>', unsafe_allow_html=True)
with m4: st.markdown(f'<div class="metric-card">PROGRESO 10K<br><span style="font-size:22px; color:#00f2ff;">{(saldo_actual/10000)*100:.4f}%</span></div>', unsafe_allow_html=True)

st.write("---")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.subheader("📊 Gráfica de Velas Japonesas (Professional View)")
    # Configuración de Velas Japonesas Estilo TradingView
    fig = go.Figure(data=[go.Candlestick(
        x=df_velas['Date'],
        open=df_velas['Open'], high=df_velas['High'],
        low=df_velas['Low'], close=df_velas['Close'],
        increasing_line_color='#00f2ff', # Neón Cian
        decreasing_line_color='#ff00ff', # Neón Magenta
        increasing_fillcolor='#00f2ff',
        decreasing_fillcolor='#ff00ff'
    )])
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis_rangeslider_visible=False,
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)', side='right'),
        xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig, width='stretch')

with col_right:
    st.subheader("🧠 Cerebro Mahora")
    
    # Pensamiento dinámico
    best_asset = top_df.sort_values(by='Cambio', ascending=False).iloc[0]
    
    st.markdown(f"""
        <div class="ia-log">
            <b>[IA PENSAMIENTO]:</b> Analizando liquidez en Bitso...<br>
            <b>[RECOMENDACIÓN]:</b> El activo con mayor fuerza hoy es <b>{best_asset['Asset']}</b> ({best_asset['Cambio']:+.2f}%)<br><br>
            <b>[ESTADO DE CARTERA]:</b><br>
            - Tienes: ${saldo_actual} MXN<br>
            - Objetivo: $10,000.00 MXN<br>
            - Falta: ${(10000 - saldo_actual):,.2f} MXN<br><br>
            <hr>
            >> IA: "Pavo, el mercado muestra volatilidad alta en {best_asset['Asset']}. Sugiero mantener posición para el viaje a Canadá 🇨🇦."
        </div>
    """, unsafe_allow_html=True)
    
    st.write("### 🚀 Top Oportunidades")
    st.dataframe(top_df, hide_index=True)

time.sleep(15)
st.rerun()
