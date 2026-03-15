import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# CONEXIÓN BITSO
bitso = ccxt.bitso({
    'apiKey': 'TU_API_KEY',
    'secret': 'TU_SECRET'
})

# ESTILO
st.markdown("""
<style>
.stApp { background:#000; color:white; }

.metric-card{
background:rgba(0,255,242,0.05);
border:1px solid #00f2ff;
border-radius:15px;
padding:20px;
text-align:center;
box-shadow:0 0 15px rgba(0,242,255,0.2);
}

.main-balance{
font-size:60px;
color:#00ff00;
font-weight:bold;
text-shadow:0 0 20px #00ff00;
}
</style>
""", unsafe_allow_html=True)


def get_full_portfolio():

    try:

        balance = bitso.fetch_balance()

        total_mxn = 0

        btc_price = bitso.fetch_ticker('BTC/MXN')['last']
        eth_price = bitso.fetch_ticker('ETH/MXN')['last']

        # MXN directo
        total_mxn += balance['total'].get('MXN', 0)

        # ETH a MXN
        eth_amt = balance['total'].get('ETH', 0)
        total_mxn += eth_amt * eth_price

        # BTC a MXN
        btc_amt = balance['total'].get('BTC', 0)
        total_mxn += btc_amt * btc_price

        # GRÁFICA
        ohlcv = bitso.fetch_ohlcv('BTC/MXN', timeframe='1m', limit=50)

        df = pd.DataFrame(ohlcv, columns=['ts','o','h','l','c','v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')

        df['sma'] = df['c'].rolling(window=7).mean()

        return total_mxn, df, btc_price

    except Exception as e:

        st.error(f"Error de conexión: {e}")
        return 0, pd.DataFrame(), 0


total_val, df_v, btc_p = get_full_portfolio()

# PANEL
c1,c2,c3 = st.columns(3)

with c1:

    st.markdown(f"""
    <div class="metric-card">
    <h4>BALANCE TOTAL (MXN)</h4>
    <div class="main-balance">${total_val:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:

    ganancia = total_val - 116

    st.markdown(f"""
    <div class="metric-card">
    <h4>GANANCIA LÍQUIDA</h4>
    <div style="font-size:40px;color:#ffd700;">
    ${ganancia:,.2f}
    </div>
    </div>
    """, unsafe_allow_html=True)

with c3:

    progreso = (total_val / 200000) * 100

    st.markdown(f"""
    <div class="metric-card">
    <h4>META 200K MXN</h4>
    <div style="font-size:40px;color:#00f2ff;">
    {progreso:.4f}%
    </div>
    </div>
    """, unsafe_allow_html=True)

# GRÁFICA
if not df_v.empty:

    fig = go.Figure(data=[go.Candlestick(
        x=df_v['ts'],
        open=df_v['o'],
        high=df_v['h'],
        low=df_v['l'],
        close=df_v['c']
    )])

    fig.add_trace(go.Scatter(
        x=df_v['ts'],
        y=df_v['sma'],
        line=dict(color='#00f2ff', width=2)
    ))

    fig.update_layout(
        template="plotly_dark",
        height=500,
        margin=dict(l=0,r=0,t=0,b=0),
        xaxis_rangeslider_visible=False
    )

    st.plotly_chart(fig, use_container_width=True)

# IA
st.subheader("Cerebro Mahora")

st.code(f"""
[{datetime.now().strftime('%H:%M:%S')}] Escaneando Portfolio...
> BTC Precio: ${btc_p:,.2f} MXN
> Valor total cartera: ${total_val:,.2f}
> Estado: Analizando mercado
""")

time.sleep(5)
st.rerun()
