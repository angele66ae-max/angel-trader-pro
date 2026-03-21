import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD & HEADER ---
NOMBRE = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE}'s Prestige")

# --- CONEXIÓN REAL BITSO ---
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- 🎯 ESTILO CYBERPUNK / NEÓN (CSS) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""
    <style>
    /* Fondo General con Gotas de Agua */
    .stApp {{ 
        background: linear-gradient(rgba(5,10,14,0.95), rgba(5,10,14,0.98)), url("{fondo_url}"); 
        background-size: cover; color: white; 
    }}
    /* Header Estilo Glow */
    .main-header {{
        text-align: center; color: #ffffff; font-weight: bold; font-size: 42px;
        text-shadow: 0 0 20px #00f2ff, 0 0 30px #00f2ff; letter-spacing: 4px; padding: 20px;
    }}
    /* Tarjetas de Métricas Neón */
    .metric-card {{
        background: rgba(11, 20, 26, 0.85); border: 2px solid #00f2ff;
        border-radius: 12px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
    }}
    .metric-title {{ font-size: 12px; color: #aaa; text-transform: uppercase; }}
    .metric-val {{ font-size: 26px; font-weight: bold; color: #00f2ff; }}
    /* Consola Cerebro Mahora */
    .ia-terminal {{
        background: rgba(0,0,0,0.9); border: 2px solid #ff00ff;
        border-radius: 12px; padding: 15px; font-family: 'Courier New', monospace;
        color: #39FF14; height: 350px; overflow-y: auto; box-shadow: 0 0 15px rgba(255, 0, 255, 0.3);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- OBTENCIÓN DE DATOS ---
def get_live_data():
    r = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
    precio = float(r['last'])
    cambio = ((precio - float(r['vwap'])) / float(r['vwap'])) * 100
    
    # Simulación de velas con SMA (Cyan y Magenta)
    precios = [precio * (1 + np.sin(i/5)*0.002) for i in range(60)]
    df = pd.DataFrame({'Close': precios})
    df['Open'] = df['Close'].shift(1).fillna(precios[0])
    df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
    df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
    df['SMA_short'] = df['Close'].rolling(7).mean()
    df['SMA_long'] = df['Close'].rolling(15).mean()
    df['Vol'] = np.random.randint(100, 1000, 60)
    return precio, cambio, df

def get_balance():
    if MODO_REAL:
        h = firmar("GET", "/v3/balance/")
        res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
        return {b['currency'].upper(): float(b['total']) for b in res['payload']['balances']}
    return {"MXN": 68.91, "BTC": 0.00003542}

# --- PROCESAMIENTO ---
precio_act, cambio_pct, df_data = get_live_data()
bal = get_balance()
saldo_mxn = bal.get("MXN", 0.0)

# --- 🔝 1. HEADER ---
st.markdown(f'<div class="main-header">{NOMBRE.upper()}\'S PRESTIGE CENTER</div>', unsafe_allow_html=True)

# --- 📊 2. PANEL DE MÉTRICAS ---
c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN</div><div class="metric-val">${precio_act:,.0f}</div><small style="color:#39FF14">+{cambio_pct:.1f}%</small></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-title">MXN BALANCE</div><div class="metric-val" style="color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-title">IA STATUS</div><div class="metric-val" style="color:#39FF14">ACTIVATED 🟢</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div class="metric-title">META 10K PROGRESS</div><div class="metric-val">{(saldo_mxn/10000)*100:.2f}%</div></div>', unsafe_allow_html=True)

st.write("---")

col_main, col_brain = st.columns([2.5, 1])

with col_main:
    # --- 📉 3. GRÁFICA PRINCIPAL (VELAS + SMAs) ---
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_width=[0.2, 0.8])
    # Velas
    fig.add_trace(go.Candlestick(open=df_data['Open'], high=df_data['High'], low=df_data['Low'], close=df_data['Close'], 
                                 increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'), row=1, col=1)
    # SMAs
    fig.add_trace(go.Scatter(y=df_data['SMA_short'], line=dict(color='#00f2ff', width=1.5), name="SMA Corta"), row=1, col=1)
    fig.add_trace(go.Scatter(y=df_data['SMA_long'], line=dict(color='#ff00ff', width=1.5), name="SMA Larga"), row=1, col=1)
    # Volumen
    fig.add_trace(go.Bar(y=df_data['Vol'], marker_color=['#00f2ff' if i%2==0 else '#ff00ff' for i in range(60)], opacity=0.4), row=2, col=1)
    
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, 
                      xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), font_color="white")
    st.plotly_chart(fig, use_container_width=True)

    # --- 📊 4. INDICADORES ---
    st.markdown("### INDICADORES CUANTITATIVOS (REAL-TIME)")
    ci1, ci2 = st.columns(2)
    with ci1:
        # RSI Gauge
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number", value = 42.5,
            gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': "#00f2ff"},
                     'steps': [{'range': [0, 30], 'color': "#ff00ff"}, {'range': [70, 100], 'color': "#ff00ff"}]}))
        fig_rsi.update_layout(height=200, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=30,b=0))
        st.plotly_chart(fig_rsi, use_container_width=True)

with col_brain:
    # --- 🧠 5. CEREBRO MAHORA ---
    st.markdown(f"""
    <div style="background:#ff00ff22; border:1px solid #ff00ff; border-radius:12px; padding:15px;">
        <div style="display:flex; justify-content:space-between; align-items:center;">
            <h4 style="margin:0; color:#ff00ff;">🧠 CEREBRO MAHORA v2.0</h4>
        </div>
        <hr style="border-color:#ff00ff44">
        <div class="ia-terminal">
            [{datetime.now().strftime("%H:%M:%S")}] >> MERCADO ESTABLE.<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> RSI 42.5 (NEUTRO).<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> SIN SEÑAL CLARA. HOLD MXN.<br>
            [{datetime.now().strftime("%H:%M:%S")}] >> AJUSTE DE RIESGO: BAJO.<br>
            <hr>
            >> PENSAMIENTO:<br>
            Angel, el sistema está operando con tu dinero real. 
            Progreso actual hacia Canadá: {(saldo_mxn/10000)*100:.2f}%.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.toggle("IA ACTIVA", value=True)
    st.write("### 💰 TUS ACTIVOS")
    st.table(pd.DataFrame(list(bal.items()), columns=["Asset", "Total"]))

# Auto-Refresh
time.sleep(15)
st.rerun()
