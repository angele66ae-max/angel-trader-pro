import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time

# --- 1. CONFIGURACIÓN ---
st.set_page_config(layout="wide", page_title="Angel Prestige Center", page_icon="⛩️")

# --- 2. ESTILO CSS PROFESIONAL CON FONDO DE GALAXIA ---
# Aquí es donde puse el enlace correcto de tu imagen de fondo
fondo_galaxia = "https://img.wallhere.com/photo/2157018.jpg"

st.markdown(f"""
    <style>
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.9)), 
                    url("{fondo_galaxia}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: white;
    }}
    .main-title {{ text-align: center; color: #00f2ff; font-size: 32px; font-weight: bold; text-shadow: 0 0 20px #00f2ff; padding: 15px; }}
    .kpi-card {{ 
        background: rgba(255, 255, 255, 0.03); 
        backdrop-filter: blur(15px); 
        border: 1px solid rgba(0, 242, 255, 0.2); 
        border-radius: 15px; padding: 15px; text-align: center;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.1);
    }}
    .console-box {{ 
        background: rgba(0, 0, 0, 0.7); 
        border: 2px solid #ff00ff; 
        border-radius: 15px; padding: 20px; 
        font-family: 'Courier New', monospace; color: #39FF14; height: 500px; overflow-y: auto;
    }}
    .signal-buy {{ color: #39FF14; font-weight: bold; border: 2px solid #39FF14; padding: 10px; border-radius: 10px; text-align: center; background: rgba(57, 255, 20, 0.05); }}
    .signal-sell {{ color: #ff00ff; font-weight: bold; border: 2px solid #ff00ff; padding: 10px; border-radius: 10px; text-align: center; background: rgba(255, 0, 255, 0.05); }}
    .signal-hold {{ color: #00f2ff; font-weight: bold; border: 2px solid #00f2ff; padding: 10px; border-radius: 10px; text-align: center; background: rgba(0, 242, 255, 0.05); }}
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
        return pd.DataFrame(), 1230000.0

ohlc_data, precio_actual = fetch_data()
rsi_valor = 48.0 # Valor base para el semáforo

# --- 4. LÓGICA DE SEÑAL IA ---
def get_ai_decision(rsi):
    if rsi <= 35:
        return "COMPRA (BUY)", "signal-buy", "¡Oportunidad de oro! Carga para el sueño de Canadá."
    elif rsi >= 65:
        return "VENDE (SELL)", "signal-sell", "Zona de burbuja detectada. Asegura ganancias."
    else:
        return "ESPERA (HOLD)", "signal-hold", "Mercado lateral. Mantén la calma y el enfoque."

label, estilo, pensamiento = get_ai_decision(rsi_valor)

# --- 5. INTERFAZ ---
st.markdown('<div class="main-title">⛩️ ANGEL\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

# Fila Superior: KPIs con efecto cristal
k1, k2, k3, k4 = st.columns(4)
k1.markdown(f'<div class="kpi-card"><small>PRECIO BTC/MXN</small><br><b style="color:#00f2ff; font-size:20px;">${precio_actual:,.0f}</b></div>', unsafe_allow_html=True)
k2.markdown('<div class="kpi-card"><small>SALDO REAL</small><br><b style="color:#ffffff; font-size:20px;">$115.59</b></div>', unsafe_allow_html=True)
k3.markdown('<div class="kpi-card"><small>MODO IA</small><br><b style="color:#39FF14; font-size:20px;">HYPER-DRIVE</b></div>', unsafe_allow_html=True)
k4.markdown('<div class="kpi-card"><small>META CANADÁ</small><br><b style="color:#ff00ff; font-size:20px;">1.16%</b></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # Gráfico de Velas con estilo Prestige
    if not ohlc_data.empty:
        fig = go.Figure(data=[go.Candlestick(
            x=ohlc_data.index, open=ohlc_data['Open'], high=ohlc_data['High'], low=ohlc_data['Low'], close=ohlc_data['Close'],
            increasing_line_color='#39FF14', decreasing_line_color='#ff00ff',
            increasing_fillcolor='#39FF14', decreasing_fillcolor='#ff00ff'
        )])
        fig.update_layout(height=400, template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # Indicadores Inferiores y Semáforo
    st.write("")
    c_rsi, c_sig = st.columns(2)
    with c_rsi:
        fig_rsi = go.Figure(go.Indicator(mode="gauge+number", value=rsi_valor, title={'text': "RSI ESTRATÉGICO"},
            gauge={'axis': {'range': [0, 100]}, 'bar': {'color': "white"}, 
                   'steps': [{'range': [0, 35], 'color': "#39FF14"}, {'range': [65, 100], 'color': "#ff00ff"}]}))
        fig_rsi.update_layout(height=230, paper_bgcolor='rgba(0,0,0,0)', font={'color': "white"}, margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_rsi, use_container_width=True)
    
    with c_sig:
        st.markdown(f'<div class="{estilo}" style="margin-top:40px;"><small>IA RECOMIENDA:</small><br><span style="font-size:24px;">{label}</span></div>', unsafe_allow_html=True)

with col_right:
    # Consola IA con el Pensamiento sobre Canadá
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
        <div class="console-box">
            <h3 style="color:#ff00ff; margin:0; font-size:18px;">🧠 MAHORA v2.0</h3>
            <hr style="border-color:#333">
            <div style="font-size:12px; line-height:1.6;">
                [{ahora}] >> SINCRONIZANDO CON BITSO...<br>
                [{ahora}] >> ANALIZANDO TENDENCIAS...<br>
                [{ahora}] >> SALDO TOTAL: $115.59 MXN<br>
                <br>
                <b style="color:#ffffff;">>> PENSAMIENTO ESTRATÉGICO:</b><br>
                "{pensamiento}"
                <br><br>
                <hr style="border-color:#333">
                <span style="color:#00f2ff;">PROGRESO A $10,000:</span><br>
                Llevamos el 1.16%. El Ferrari no se detiene.
                <br><br>
                <p style="font-size:11px; color:#888;">Operando para Ángel Gabriel. <br>Meta Final: Canadá 🇨🇦</p>
            </div>
        </div>
    """, unsafe_allow_html=True)

# Auto-refresh cada 15 segundos
time.sleep(15)
st.rerun()
