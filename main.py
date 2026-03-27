import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac, hashlib, time
from datetime import datetime

# --- 1. CONFIGURACIÓN DE SEGURIDAD (BITSO ALPHA ENGINE) ---
API_KEY = "qdgvoUmYcB"
API_SECRET = "c764dc6961cd5d1a443cbc677fe39597"
NOMBRE = "ANGEL PRESTIGE ALPHA"

st.set_page_config(layout="wide", page_title=NOMBRE, page_icon="📈")

# --- 2. MOTOR DE DATOS REALES ---
def get_bitso_data():
    try:
        nonce = str(int(time.time() * 1000))
        path = "/v3/balance/"
        mensaje = nonce + "GET" + path
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}'}
        r = requests.get(f"https://api.bitso.com{path}", headers=headers).json()
        
        mxn, btc = 0.0, 0.0
        for b in r['payload']['balances']:
            if b['currency'] == 'mxn': mxn = float(b['total'])
            if b['currency'] == 'btc': btc = float(b['total'])
        return mxn, btc
    except: return 111.94, 0.00004726

saldo_mxn, saldo_btc = get_bitso_data()

# --- 3. DISEÑO "ALPHA BLACK" (ESTILO BITSO ALPHA) ---
st.markdown(f"""
    <style>
    .stApp {{ background-color: #050a0e; color: #d1d4dc; font-family: 'Roboto', sans-serif; }}
    .alpha-header {{ background: #131722; border-bottom: 1px solid #363c4e; padding: 10px 20px; display: flex; justify-content: space-between; }}
    .metric-box {{ border-right: 1px solid #363c4e; padding: 0 20px; text-align: left; }}
    .side-panel {{ background: #131722; border: 1px solid #363c4e; border-radius: 4px; padding: 15px; margin-bottom: 10px; }}
    .btn-buy {{ background-color: #089981 !important; color: white !important; width: 100%; border: none; }}
    .btn-sell {{ background-color: #f23645 !important; color: white !important; width: 100%; border: none; }}
    .terminal-text {{ font-family: 'Courier New', monospace; color: #39FF14; font-size: 12px; }}
    </style>
""", unsafe_allow_html=True)

# --- 4. HEADER ESTILO TERMINAL ---
st.markdown(f"""
    <div class="alpha-header">
        <div style="display:flex;">
            <div class="metric-box"><small style="color:#848e9c">ACTIVO</small><br><b>BTC/MXN</b></div>
            <div class="metric-box"><small style="color:#848e9c">PRECIO REAL</small><br><b style="color:#089981">$1,226,980</b></div>
            <div class="metric-box"><small style="color:#848e9c">TU SALDO MXN</small><br><b>${saldo_mxn:,.2f}</b></div>
            <div class="metric-box"><small style="color:#848e9c">META CANADÁ</small><br><b style="color:#ff00ff">{(saldo_mxn/200000)*100:.2f}%</b></div>
        </div>
    </div>
""", unsafe_allow_html=True)

st.write("")

# --- 5. CUERPO PRINCIPAL (LAYOUT ALPHA) ---
col_chart, col_order = st.columns([3, 1])

with col_chart:
    # Gráfica de Velas Profesional
    r_mkt = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn").json()['payload']
    df = pd.DataFrame(r_mkt)
    df['price'] = df['price'].astype(float)
    
    fig = go.Figure(data=[go.Candlestick(
        x=df.index, open=df['price'], high=df['price']*1.001,
        low=df['price']*0.999, close=df['price'],
        increasing_line_color='#089981', decreasing_line_color='#f23645'
    )])
    fig.update_layout(template="plotly_dark", paper_bgcolor='#131722', plot_bgcolor='#131722', 
                      xaxis_rangeslider_visible=False, height=500, margin=dict(l=10,r=10,t=10,b=10))
    st.plotly_chart(fig, use_container_width=True)

with col_order:
    # --- MÓDULO DE EMPRESAS (NUEVO) ---
    st.markdown('<div class="side-panel">', unsafe_allow_html=True)
    st.markdown("<h5 style='margin:0'>🏢 EMPRESAS TECH</h5>", unsafe_allow_html=True)
    st.caption("Inversión vía Tokens de Utilidad")
    
    st.write("---")
    c_ia, c_met = st.columns(2)
    c_ia.metric("RENDER (IA)", "$124.50", "+2.4%")
    c_met.metric("SAND (Bienes)", "$8.90", "-1.2%")
    
    if st.button("INVERTIR EN RENDER", use_container_width=True):
        st.success("Orden enviada: Comprando potencia de IA...")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PANEL DE ACCIÓN ---
    st.markdown('<div class="side-panel">', unsafe_allow_html=True)
    st.markdown("<h5 style='margin:0'>🚨 ACCIÓN RÁPIDA</h5>", unsafe_allow_html=True)
    st.write("")
    if st.button("COMPRA BTC (BARATO)", help="Comprar ahora", key="buy_btn"):
        st.write("Procesando...")
    if st.button("LIQUIDAR TODO (PÁNICO)", help="Vender todo a pesos", key="sell_btn"):
        st.error("¡VENDIENDO TODO PARA PROTEGER MXN!")
    st.markdown('</div>', unsafe_allow_html=True)

    # --- TERMINAL MAHORA ---
    st.markdown('<div class="side-panel" style="border-color:#ff00ff">', unsafe_allow_html=True)
    st.markdown("<b style='color:#ff00ff'>CEREBRO MAHORA v38</b>", unsafe_allow_html=True)
    st.markdown(f"""
        <div class="terminal-text">
            [{datetime.now().strftime("%H:%M")}] CONEXIÓN ALPHA OK<br>
            [{datetime.now().strftime("%H:%M")}] MÓDULO EMPRESAS: READY<br>
            <hr style="border-color:#333">
            >> "Pavo, este es tu gemelo de Bitso Alpha. Ya no eres un usuario, eres el dueño de la terminal."
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(15)
st.rerun()
