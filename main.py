import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
import base64
from datetime import datetime

# --- CONFIGURACIÓN DE GALAXY ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: THE WHEEL")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- CARGADOR DE VIDEO OPTIMIZADO ---
def get_video_bg_html():
    video_file = "Ajustes_de_Video_y_Sugerencias.mp4"
    try:
        with open(video_file, "rb") as f:
            data = f.read()
            b64_video = base64.b64encode(data).decode()
        return f'''
            <video autoplay loop muted playsinline id="mahora-bg">
                <source src="data:video/mp4;base64,{b64_video}" type="video/mp4">
            </video>
            <style>
                #mahora-bg {{
                    position: fixed; right: 0; bottom: 0;
                    min-width: 100%; min-height: 100%;
                    z-index: -1; filter: brightness(0.4) contrast(1.1);
                    object-fit: cover;
                }}
                .stApp {{ background: transparent; }}
                .glass-box {{
                    background: rgba(0, 0, 0, 0.75);
                    border: 1px solid #00f2ff;
                    border-radius: 15px; padding: 25px; text-align: center;
                    box-shadow: 0 0 20px rgba(0, 242, 255, 0.2);
                }}
                .money {{ font-size: 55px; color: #00ff00; font-weight: bold; text-shadow: 0 0 15px #00ff00; }}
            </style>
        '''
    except:
        return '<style>.stApp { background: black; }</style>'

st.markdown(get_video_bg_html(), unsafe_allow_html=True)

# --- LÓGICA DE DATOS (RECOLECTANDO TUS 116.1 MXN) ---
def fetch_mahora_wealth():
    try:
        # Balance real de tus monedas
        bal = bitso.fetch_balance()
        btc_p = bitso.fetch_ticker('BTC/USD')['last']
        
        # Calculamos el valor real en USD de tu cartera
        total_usd = bal['total'].get('USD', 2.81)
        eth_val = bal['total'].get('ETH', 0.0017524)
        # Sumamos Ether y USD (Tus $6.81 USD totales)
        cartera_total = total_usd + (eth_val * (37566 / 18.2)) 
        
        # Datos para la gráfica
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ema'] = df['c'].ewm(span=7).mean()

        return cartera_total, df, btc_p, bal['total']
    except:
        return 6.81, pd.DataFrame(), 71000.0, {}

# --- RENDERIZADO DE INTERFAZ ---
total_w, df_v, btc_current, my_assets = fetch_mahora_wealth()

# HEADER: BALANCE DE PODER
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="glass-box"><h6>VALOR TOTAL (USD)</h6><div class="money">${total_w:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    ganancia = total_w - 6.45
    st.markdown(f'<div class="glass-box"><h6>GANANCIA REAL</h6><div style="font-size:40px; color:#ffd700;">+${ganancia:,.5f}</div></div>', unsafe_allow_html=True)
with c3:
    meta = (total_w / 10000) * 100
    st.markdown(f'<div class="glass-box"><h6>META SUV 10K</h6><div style="font-size:40px; color:#00f2ff;">{meta:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # Gráfica transparente para ver la rueda de fondo
    if not df_v.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC")])
        fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ema'], line=dict(color='#ff00ff', width=2), name="IA Core"))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=480, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    # Desglose Real de Monedas
    st.markdown('<div class="glass-box" style="text-align:left; height:480px;">', unsafe_allow_html=True)
    st.subheader("Bóveda Mahora")
    st.write(f"**Ether:** {my_assets.get('ETH', 0.0017524):.7f}")
    st.write(f"**Dólares:** ${my_assets.get('USD', 2.81):,.2f}")
    st.write(f"**Bitcoin:** {my_assets.get('BTC', 0.0000039):.8f}")
    st.divider()
    st.metric("PRECIO BTC", f"${btc_current:,.2f}")
    st.code(f"ESTADO: {datetime.now().strftime('%H:%M:%S')}\nADAPTACIÓN AL VACÍO", language="bash")
    if st.button("🔥 FORZAR RE-SINCRONIZACIÓN"): st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(5)
st.rerun()
