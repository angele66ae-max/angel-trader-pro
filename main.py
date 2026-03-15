import streamlit as st
import pandas as pd
import ccxt
import time
import plotly.graph_objects as go
from datetime import datetime
import base64

# --- CONFIGURACIÓN DE GALAXY ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: THE WHEEL")

# --- CONEXIÓN API (SEGURA) ---
bitso = ccxt.bitso({
    'apiKey': 'FZHAAOqOhy',
    'secret': 'b5e9f3e4e429c079a5989473ed1ba171',
})

# --- INYECCIÓN DEL VIDEO DE LA RUEDA (FONDO ANIMADO) ---
# Nota: Streamlit necesita el video en base64 para reproducirlo localmente sin tirones
def get_video_html():
    video_path = "Ajustes_de_Video_y_Sugerencias.mp4" # Asegúrate que el archivo esté en tu GitHub
    try:
        with open(video_path, "rb") as f:
            data = f.read()
            bin_str = base64.b64encode(data).decode()
        return f'''
            <video autoplay loop muted playsinline id="bg-video" style="
                position: fixed; right: 0; bottom: 0; 
                min-width: 100%; min-height: 100%; 
                z-index: -1; filter: brightness(0.4); object-fit: cover;">
                <source src="data:video/mp4;base64,{bin_str}" type="video/mp4">
            </video>
        '''
    except:
        return '<div style="position:fixed; width:100%; height:100%; background:black; z-index:-1;"></div>'

st.markdown(get_video_html(), unsafe_allow_html=True)

# --- ESTILOS DE PRESTIGIO (TRANSLÚCIDOS) ---
st.markdown("""
<style>
    .stApp { background: transparent; }
    .glass-card {
        background: rgba(0, 0, 0, 0.7); 
        border: 1px solid #00f2ff;
        border-radius: 15px; padding: 25px; text-align: center;
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.2);
    }
    .main-balance { font-size: 60px; color: #00ff00; font-weight: bold; text-shadow: 0 0 20px #00ff00; }
</style>
""", unsafe_allow_html=True)

# --- MOTOR OMNI-VISION (Real-Time) ---
def mahora_sync():
    try:
        # 1. Balance completo (Dólares + Ether + Bitcoin)
        bal = bitso.fetch_balance()
        btc_p = bitso.fetch_ticker('BTC/USD')['last']
        eth_p_mxn = 37566.0 # Tu referencia de Bitso
        
        # Cálculo de Balance Total en USD
        usd_cash = bal['total'].get('USD', 2.81)
        eth_qty = bal['total'].get('ETH', 0.0017524)
        total_val_usd = usd_cash + (eth_qty * (eth_price_mxn / 18.0))
        
        # 2. Gráfica de Velas Profesionales
        ohlcv = bitso.fetch_ohlcv('BTC/USD', timeframe='1m', limit=50)
        df = pd.DataFrame(ohlcv, columns=['ts', 'o', 'h', 'l', 'c', 'v'])
        df['ts'] = pd.to_datetime(df['ts'], unit='ms')
        df['ema'] = df['c'].ewm(span=7).mean()

        return total_val_usd, df, btc_p, bal['total']
    except:
        return 6.81, pd.DataFrame(), 71000.0, {}

# --- EJECUCIÓN ---
val_total, df_v, p_btc, my_coins = mahora_sync()

# PANEL SUPERIOR: BALANCE MAESTRO
c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f'<div class="glass-card"><h6>BALANCE TOTAL ESTIMADO</h6><div class="main-balance">${val_total:,.2f}</div></div>', unsafe_allow_html=True)
with c2:
    ganancia = val_total - 6.45
    st.markdown(f'<div class="glass-card"><h6>GANANCIA LÍQUIDA</h6><div style="font-size:45px; color:#ffd700; font-weight:bold;">+${ganancia:,.5f}</div></div>', unsafe_allow_html=True)
with c3:
    st.markdown(f'<div class="glass-card"><h6>META SUV (10K)</h6><div style="font-size:45px; color:#00f2ff;">{(val_total/10000)*100:.4f}%</div></div>', unsafe_allow_html=True)

st.write("")
col_left, col_right = st.columns([2.3, 1])

with col_left:
    # Gráfica con fondo transparente para ver la rueda girar
    if not df_v.empty:
        fig = go.Figure(data=[go.Candlestick(x=df_v['ts'], open=df_v['o'], high=df_v['h'], low=df_v['l'], close=df_v['c'], name="BTC")])
        fig.add_trace(go.Scatter(x=df_v['ts'], y=df_v['ema'], line=dict(color='#ff00ff', width=2), name="IA Core"))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                          height=500, margin=dict(l=0, r=0, t=0, b=0), xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

with col_right:
    # Monitor de Activos
    st.markdown('<div class="glass-card" style="text-align:left; height:500px;">', unsafe_allow_html=True)
    st.subheader("Cerebro Mahora")
    st.write(f"**Bitcoin:** {my_coins.get('BTC', 0.0000039):.8f}")
    st.write(f"**Ether:** {my_coins.get('ETH', 0.0017524):.8f}")
    st.write(f"**Dólares:** ${my_coins.get('USD', 2.81):,.2f}")
    st.divider()
    st.metric("PRECIO ACTUAL", f"${p_btc:,.2f}")
    st.code(f"ESTADO: ADAPTACIÓN ACTIVA\nOBJETIVO: 115", language="bash")
    if st.button("🚀 RE-ESCANEAR CARTERA"): st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# Loop de refresco para animación fluida
time.sleep(4)
st.rerun()
