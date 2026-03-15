import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
import base64
from datetime import datetime

# --- CONFIGURACIÓN DE GALAXY ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: FINAL ADAPTATION")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- MOTOR DE VIDEO (The Eternal Wheel) ---
def load_mahoraga_wheel():
    video_file = "Ajustes_de_Video_y_Sugerencias.mp4"
    try:
        with open(video_file, "rb") as f:
            data = f.read()
            b64 = base64.b64encode(data).decode()
        return f'''
            <video autoplay loop muted playsinline id="bg-video">
                <source src="data:video/mp4;base64,{b64}" type="video/mp4">
            </video>
            <style>
                #bg-video {{
                    position: fixed; right: 0; bottom: 0;
                    min-width: 100%; min-height: 100%;
                    z-index: -1; filter: brightness(0.4) contrast(1.1);
                    object-fit: cover;
                }}
                .stApp {{ background: transparent; }}
                .mahora-card {{
                    background: rgba(0, 10, 20, 0.85);
                    border: 1px solid #00f2ff;
                    border-radius: 12px; padding: 20px;
                    box-shadow: 0 0 15px rgba(0, 242, 255, 0.4);
                    margin-bottom: 10px;
                }}
                .glow-val {{ color: #00ff00; font-size: 45px; font-weight: bold; text-shadow: 0 0 10px #00ff00; }}
            </style>
        '''
    except:
        return '<style>.stApp { background: #0b0e11; }</style>'

st.markdown(load_mahoraga_wheel(), unsafe_allow_html=True)

# --- SINCRONIZACIÓN DE RIQUEZA (Omni-Vision) ---
def sync_wealth():
    try:
        bal = bitso.fetch_balance()
        btc_tick = bitso.fetch_ticker('BTC/USD')
        
        # Datos de tu cartera real
        usd_amt = bal['total'].get('USD', 2.81)
        eth_amt = bal['total'].get('ETH', 0.0017524)
        # Conversión a valor total USD ($6.42 estimado)
        total_usd = usd_amt + (eth_amt * (37566 / 18.2))
        
        # Datos de mercado para IA Core
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=45)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ema'] = df['c'].ewm(span=7).mean()

        return total_usd, df, btc_tick['last'], bal['total']
    except:
        return 6.42, pd.DataFrame(), 71550.0, {}

# --- RENDERIZADO ---
wealth, market_df, price_btc, my_coins = sync_wealth()

# HEADER: STATUS DE ADAPTACIÓN
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="mahora-card"><small>VALOR TOTAL (USD)</small><div class="glow-val">${wealth:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    ganancia = wealth - 6.45
    color = "#ffd700" if ganancia >= 0 else "#ff4b4b"
    st.markdown(f'<div class="mahora-card"><small>GANANCIA LÍQUIDA</small><div style="font-size:35px; color:{color}; font-weight:bold;">${ganancia:,.5f}</div></div>', unsafe_allow_html=True)
with c3:
    meta_prog = (wealth / 10000) * 100
    st.markdown(f'<div class="mahora-card"><small>PROGRESO META 10K</small><div style="font-size:35px; color:#00f2ff;">{meta_prog:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.5, 1])

with col_left:
    # Gráfica de Velas con la IA Core (Magenta)
    if not market_df.empty:
        fig = go.Figure(data=[go.Candlestick(x=market_df['ts'], open=market_df['o'], high=market_df['h'], low=market_df['l'], close=market_df['c'], name="BTC/USD")])
        fig.add_trace(go.Scatter(x=market_df['ts'], y=market_df['ema'], line=dict(color='#ff00ff', width=2), name="IA Core"))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=450, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    # Bóveda Mahora Detallada
    st.markdown('<div class="mahora-card" style="text-align:left;">', unsafe_allow_html=True)
    st.subheader("Bóveda Mahora")
    st.write(f"**Ether:** `{my_coins.get('ETH', 0.0017524):.7f}`")
    st.write(f"**Dólares:** `${my_coins.get('USD', 2.81):,.2f}`")
    st.write(f"**BTC:** `{my_coins.get('BTC', 0.0000000):.8f}`")
    st.divider()
    st.metric("PRECIO BTC", f"${price_btc:,.2f}")
    st.code(f"MAHORA LOG:\n{datetime.now().strftime('%H:%M:%S')} - ADAPTADO")
    if st.button("🔄 RE-SINCRONIZAR"): st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(5)
st.rerun()
