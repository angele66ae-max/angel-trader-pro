import streamlit as st
import pandas as pd
import ccxt
import time
from datetime import datetime
import plotly.graph_objects as go

# --- CONFIGURACIÓN DE INTERFAZ ---
st.set_page_config(layout="wide", page_title="MAHORASHARK PRESTIGE")

# --- CONEXIÓN API ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- ESTILO SIN PARPADEO ---
st.markdown("""
<style>
    .stApp { background-color: #050505; }
    .status-box {
        background: rgba(0, 255, 242, 0.05);
        border: 2px solid #00f2ff;
        border-radius: 15px; padding: 20px; text-align: center;
    }
    .money-text { color: #00ff00; font-size: 55px; font-weight: bold; text-shadow: 0 0 15px #00ff00; }
</style>
""", unsafe_allow_html=True)

def run_mahora_logic():
    try:
        # Balance real
        bal = bitso.fetch_balance()
        usd_val = bal['total'].get('USD', 2.81)
        
        # Datos de mercado
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=30)
        if not ohlcv: return None
        
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ema'] = df['c'].ewm(span=5).mean()
        
        # LÓGICA DE ACTIVACIÓN REAL
        precio_actual = df['c'].iloc[-1]
        target = df['ema'].iloc[-1]
        
        msg = "IA EN ESPERA..."
        if usd_val > 1.0 and precio_actual < target:
            bitso.create_market_buy_order('BTC/USD', usd_val)
            msg = "🔥 COMPRANDO BTC"
        elif bal['total'].get('BTC', 0) > 0.00001 and precio_actual > target:
            bitso.create_market_sell_order('BTC/USD', bal['total'].get('BTC'))
            msg = "⚡ VENDIENDO (PROFIT)"
            
        return usd_val, df, msg, precio_actual
    except Exception as e:
        st.warning(f"Sincronizando con Bitso... {e}")
        return None

# --- RENDERIZADO ---
data = run_mahora_logic()

if data:
    usd, df_v, status_msg, p_btc = data
    
    st.markdown(f"""
        <div class="status-box">
            <h2 style="color:white; margin:0;">MAHORASHARK LIQUIDITY</h2>
            <div class="money-text">${usd:,.6f}</div>
            <p style="color:#00f2ff;">ESTADO: {status_msg}</p>
        </div>
    """, unsafe_allow_html=True)

    st.write("")
    c1, c2 = st.columns([2, 1])
    
    with c1:
        # Escudo para el KeyError de la línea 83
        fig = go.Figure(data=[go.Candlestick(
            x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c']
        )])
        fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ema'], line=dict(color='#ff00ff')))
        fig.update_layout(template="plotly_dark", height=400, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.metric("PRECIO BTC", f"${p_btc:,.2f}")
        st.code(f"LOG: {datetime.now().strftime('%H:%M:%S')}\nMAHORA ADAPTADO")
        if st.button("RECARGAR MANUAL"): st.rerun()

# Pausa de 5 segundos para que no se ponga opaco tan seguido
time.sleep(5)
st.rerun()
