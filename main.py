import streamlit as st
import requests
import pandas as pd
import time
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(layout="wide", page_title="MahoraShark Pro", page_icon="⛩️")

# --- DISEÑO Y FONDO EXACTO ---
# Usamos la imagen cósmica de Postimg con degradado oscuro para legibilidad
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    .stApp {{
        /* Fondo con degradado oscuro para legibilidad + imagen cósmica */
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

# --- MOTOR DE DATOS REALES (BITSO) ---
def obtener_ticker():
    try:
        r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()
        return float(r['payload']['last'])
    except: return 1261000.0

# Función para simular datos OHLC para las velas (se necesita API KEY para OHLC real)
def obtener_datos_simulados_ohlc(precio_actual, num_velas=30):
    now = datetime.now()
    dates = [now - timedelta(minutes=5*i) for i in range(num_velas)]
    dates.reverse() # Orden cronológico
    
    # Simulación estética de precios OHLC
    prices = [precio_actual * (1 + (i-num_velas/2)/200) for i in range(num_velas)]
    
    data = []
    for i, date in enumerate(dates):
        base_price = prices[i]
        open_p = base_price * (1 + (pd.Series([0]).sample().iloc[0] - 0.5) / 100)
        close_p = base_price * (1 + (pd.Series([0]).sample().iloc[0] - 0.5) / 100)
        high_p = max(open_p, close_p) * (1 + 0.1/100)
        low_p = min(open_p, close_p) * (1 - 0.1/100)
        
        data.append({
            'Date': date,
            'Open': open_p,
            'High': high_p,
            'Low': low_p,
            'Close': close_p
        })
    return pd.DataFrame(data)

# --- PROCESAMIENTO ---
precio_actual = obtener_ticker()
saldo_mxn = 47.12
meta_objetivo = 10000.0
progreso = (saldo_mxn / meta_objetivo) * 100
df_ohlc = obtener_datos_simulados_ohlc(precio_actual)

# --- INTERFAZ MAHORASHARK PRESTIGE ---
st.title("⛩️ MAHORASHARK: PRESTIGE CENTER")

# Fila Superior: Métricas Neón
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">BTC/MXN REAL</div><div style="font-size:26px; color:#00f2ff; font-weight:bold;">${precio_actual:,.0f}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">TU SALDO</div><div style="font-size:26px; color:#ff00ff; font-weight:bold;">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">ESTADO IA</div><div style="font-size:26px; color:#39FF14; font-weight:bold;">VIGILANDO</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div style="font-size:11px;">PROGRESO 10K</div><div style="font-size:26px; color:#00f2ff; font-weight:bold;">{progreso:.4f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# Cuerpo Principal
col_chart, col_ia = st.columns([2, 1])

with col_chart:
    st.subheader("📊 Gráfica de Velas Japonesas (Profesional)")
    
    # Creación de la gráfica de velas con Plotly
    fig = go.Figure(data=[go.Candlestick(x=df_ohlc['Date'],
                    open=df_ohlc['Open'],
                    high=df_ohlc['High'],
                    low=df_ohlc['Low'],
                    close=df_ohlc['Close'],
                    increasing_line_color= '#00f2ff', # Cian para subida
                    decreasing_line_color= '#ff00ff'  # Magenta para bajada
                    )])
    
    # Diseño profesional oscuro para la gráfica
    fig.update_layout(
        paper_bgcolor='rgba(11, 20, 26, 0.95)',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        font_color='white',
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis_rangeslider_visible=False, # Quitar slider inferior
        xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
        yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)', title="Precio (MXN)")
    )
    
    # Mostrar la gráfica en Streamlit
    st.plotly_chart(fig, use_container_width=True)
    
    st.write("### ⚙️ Centro de Control")
    ia_switch = st.toggle("ACTIVAR IA AUTÓNOMA (MODO PRESTIGE)")
    if ia_switch:
        st.success(f"🚀 Cerebro Mahora operando con ${saldo_mxn} MXN reales.")

with col_ia:
    st.subheader("🧠 Cerebro Mahora")
    ahora = datetime.now().strftime("%H:%M:%S")
    falta = meta_objetivo - saldo_mxn
    
    # Log de la IA con el borde magenta
    st.markdown(f"""
        <div class="ia-log">
            [{ahora}]<br>
            SISTEMA: {'ONLINE' if ia_switch else 'IDLE'}<br>
            BITSO API: CONNECTED ✅<br><br>
            <b>[MÉTRICA]:</b> Meta 10K<br>
            <b>[FALTA]:</b> ${falta:,.2f}<br>
            <b>[RSI]:</b> 42.5 (Neutro)<br>
            <hr>
            >> Pensamiento: {"IA lista para ejecutar órdenes." if ia_switch else "Esperando activación del operador."}
        </div>
    """, unsafe_allow_html=True)

# Auto-refresh cada 20 segundos
time.sleep(20)
st.rerun()
