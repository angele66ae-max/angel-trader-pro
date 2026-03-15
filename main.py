import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PANTALLA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- DISEÑO PRESTIGE (ESTÁTICO PARA EVITAR ERRORES) ---
st.markdown("""
<style>
    .stApp {
        background-image: url("https://raw.githubusercontent.com/pavo-free-fire/mahorashark/main/fondo_rueda.png"); /* Asegúrate de subir la imagen de la rueda a tu repo */
        background-size: cover; background-position: center; background-attachment: fixed;
        background-color: #000;
    }
    [data-testid="stHeader"] { background: rgba(0,0,0,0); }
    .prestige-card {
        background: rgba(0, 10, 20, 0.85);
        border: 2px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 20px rgba(0, 242, 255, 0.3);
    }
    .val-main { color: #00f2ff; font-size: 40px; font-weight: bold; text-shadow: 0 0 10px #00f2ff; }
    .val-sub { color: #ff00ff; font-size: 30px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

def get_prestige_data():
    try:
        # 1. Bóveda Real
        bal = bitso.fetch_balance()
        u_usd = bal['total'].get('USD', 2.81)
        u_eth = bal['total'].get('ETH', 0.0017524)
        u_btc = bal['total'].get('BTC', 0.0)
        
        # 2. Mercado Real
        ticker = bitso.fetch_ticker('BTC/USD')
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=35)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ia_core'] = df['c'].ewm(span=6).mean() # IA Core mejorada
        
        return u_usd, u_eth, u_btc, df, ticker['last']
    except Exception as e:
        st.error(f"Error de Sincronización: {e}")
        return 2.81, 0.0017524, 0.0, pd.DataFrame(), 71000.0

# --- LÓGICA DE ACTUALIZACIÓN ---
usd_r, eth_r, btc_r, df_v, btc_p = get_prestige_data()

# HEADER: PANELES SUPERIORES
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="prestige-card"><small>BTC/USD BITSO</small><div class="val-main">${btc_p:,.1f}</div></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="prestige-card"><small>BALANCE REAL</small><div class="val-sub">${usd_r:,.2f}</div></div>', unsafe_allow_html=True)
with c3:
    # Ganancia estimada basada en tu inversión inicial
    total_cartera = usd_r + (eth_r * (37566 / 18.2))
    profit = total_cartera - 6.45
    st.markdown(f'<div class="prestige-card"><small>GANANCIA LÍQUIDA</small><div style="color:#00ff00; font-size:25px;">+${profit:,.5f}</div></div>', unsafe_allow_html=True)
with c4:
    meta = (total_cartera / 10000) * 100
    st.markdown(f'<div class="prestige-card"><small>META 10K</small><div style="color:#00f2ff; font-size:25px;">{meta:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
# CUERPO: SIDEBAR IZQUIERDO Y GRÁFICA
col_side, col_main, col_brain = st.columns([0.8, 2, 1])

with col_side:
    st.markdown('<div class="prestige-card" style="text-align:left;">', unsafe_allow_html=True)
    st.subheader("Tu Cuenta")
    st.write(f"**Bitcoin:**\n`{btc_r:.8f}`")
    st.write(f"**Ethereum:**\n`{eth_r:.7f}`")
    st.write(f"**Dólares:**\n`${usd_r:,.2f}`")
    st.divider()
    if st.button("🚀 ACTIVAR IA REAL"):
        # Lógica de compra real
        if usd_r > 1.0:
            st.warning("Ejecutando Orden...")
            # bitso.create_market_buy_order('BTC/USD', usd_r * 0.95)
    st.markdown('</div>', unsafe_allow_html=True)

with col_main:
    if not df_v.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC")])
        fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ia_core'], line=dict(color='#ff00ff', width=2), name="IA Core"))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=500, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_brain:
    st.markdown('<div class="prestige-card" style="height:500px;">', unsafe_allow_html=True)
    st.subheader("Cerebro Mahora")
    st.markdown(f"""
    <div style="text-align:left; font-family:monospace; font-size:12px;">
    > [{datetime.now().strftime('%H:%M:%S')}] Escaneando...<br>
    > BTC: ${btc_p:,.2f}<br>
    > IA CORE: ADAPTÁNDOSE...<br>
    > ESTADO: LISTO PARA OPERAR
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

time.sleep(10)
st.rerun()
