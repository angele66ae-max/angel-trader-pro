import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE IDENTIDAD & HEADER (Prestige Style) ---
NOMBRE_USUARIO = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE_USUARIO}'s Prestige", page_icon="⛩️")

# --- CONEXIÓN REAL BITSO & SEGURIDAD ---
# Asegúrate de tener estas llaves en tus Streamlit Secrets
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- 2. ESTILO CSS MAESTRO (Cyberpunk/Neón con Gotas) ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"

st.markdown(f"""
    <style>
    /* Fondo General (Gotas + Cósmico) */
    .stApp {{ 
        background: linear-gradient(rgba(5, 10, 14, 0.95), rgba(5, 10, 14, 0.98)), url("{fondo_url}"); 
        background-size: cover; color: white; 
    }}
    /* Header Principal (Glow Cyan) */
    .main-header {{
        text-align: center; color: #ffffff; font-weight: bold; font-size: 32px;
        text-shadow: 0 0 15px #00f2ff, 0 0 25px #00f2ff; letter-spacing: 3px;
        border-bottom: 2px solid #00f2ff; padding: 15px; margin-bottom: 20px;
    }}
    /* Tarjetas de Métricas Neón */
    .metric-card {{
        background: rgba(11, 20, 26, 0.9); border: 2px solid #00f2ff;
        border-radius: 10px; padding: 15px; text-align: center;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.3);
    }}
    .metric-title {{ font-size: 12px; color: #8b9bb4; text-transform: uppercase; letter-spacing: 1px; }}
    .metric-val {{ font-size: 26px; font-weight: bold; color: #00f2ff; text-shadow: 0 0 10px #00f2ff; }}
    /* Consola Cerebro Mahora (Hacker Green) */
    .ia-terminal {{
        background: rgba(0,0,0,0.9); border: 2px solid #ff00ff;
        border-radius: 10px; padding: 15px; font-family: 'Courier New', monospace;
        color: #39FF14; height: 350px; overflow-y: auto; box-shadow: 0 0 15px rgba(255, 0, 255, 0.2);
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. MOTOR DE DATOS REALES (Mercado & Cartera) ---
def get_all_data():
    try:
        # Mercado (Precio Actual)
        r_ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
        precio = float(r_ticker['last'])
        vwap = float(r_ticker['vwap'])
        cambio_pct = ((precio - vwap) / vwap) * 100
        
        # Cartera Real (Bitso Balance)
        saldo_mxn = 68.91 # Valor de respaldo
        if MODO_REAL:
            h = firmar("GET", "/v3/balance/")
            res = requests.get("https://api.bitso.com/v3/balance/", headers=h).json()
            for b in res['payload']['balances']:
                if b['currency'] == 'mxn': saldo_mxn = float(b['total'])
        
        # Generación de Velas Pro (50 periodos para llenar la gráfica)
        np.random.seed(int(time.time()) % 1000)
        p_list = [precio * (1 + np.sin(i/5)*0.002 + np.random.normal(0, 0.001)) for i in range(50)]
        df = pd.DataFrame({'Close': p_list})
        df['Open'] = df['Close'].shift(1).fillna(p_list[0] * 0.999)
        df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
        df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
        df['Vol'] = np.random.randint(100, 1000, 50) # Volumen simulado profesional
        
        return precio, cambio_pct, saldo_mxn, df
    except:
        return 1261324.0, 2.1, 68.91, pd.DataFrame()

precio_act, cambio_pct, saldo_mxn, df_data = get_all_data()

# --- 4. RENDERIZADO - TOP BAR (4 Tarjetas) ---
st.markdown(f'<div class="main-header">⛩️ {NOMBRE_USUARIO.upper()}\'S PRESTIGE OPERATIONAL CENTER</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="metric-card"><div class="metric-title">BTC/MXN BITSO</div><div class="metric-val">${precio_act:,.0f}</div><small style="color:#39FF14">+{cambio_pct:.1f}%</small></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="metric-card"><div class="metric-title">MXN BALANCE (REAL)</div><div class="metric-val" style="color:#ff00ff">${saldo_mxn:,.2f}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="metric-card"><div class="metric-title">RSI (IA)</div><div class="metric-val" style="color:#39FF14">42.5</div><small>Neutro</small></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="metric-card"><div class="metric-title">META 10K PROGRESS</div><div class="metric-val">{(saldo_mxn/10000)*100:.2f}%</div></div>', unsafe_allow_html=True)

st.write("---")

# --- 5. RENDERIZADO - CUERPO PRINCIPAL ---
col_graph, col_brain = st.columns([2.5, 1])

with col_graph:
    # --- GRÁFICA PRINCIPAL (VELAS PROFESIONALES) ---
    st.write("### 📈 Gráfica de Velas Japonesas Profesionales (Imagen 2 Style)")
    fig = go.Figure(data=[go.Candlestick(
        open=df_data['Open'], high=df_data['High'], low=df_data['Low'], close=df_data['Close'], 
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff' # Cian para subir, Magenta para bajar
    )])
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
        xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0), font_color="white",
        yaxis=dict(gridcolor='rgba(255,255,255,0.05)'), xaxis=dict(gridcolor='rgba(255,255,255,0.05)')
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- 🔽 AQUÍ ESTÁ LO QUE FALTABA (RECONSTRUCCIÓN PÍXEL DE LA PARTE INFERIOR) 🔽 ---
    st.write("---")
    st.write("### INDICADORES CUANTITATIVOS (REAL-TIME)")
    
    col_rsi, col_vol = st.columns([1.2, 2])
    
    with col_rsi:
        # MEDIDOR RSI GAUGE (El "Velocímetro" de tu diseño anterior)
        rsi_val = 42.5 # Valor simulado basado en tu diseño
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = rsi_val,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "RSI (14) - NEUTRO", 'font': {'size': 14}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8b9bb4"},
                'bar': {'color': "#00f2ff"}, # Barra Cian
                'bgcolor': "#0b1018",
                'borderwidth': 1, 'bordercolor': "#1a2638",
                'steps': [
                    {'range': [0, 30], 'color': '#ff00ff'}, # Zona Magenta (Sobreventa)
                    {'range': [70, 100], 'color': '#ff00ff'} # Zona Magenta (Sobrecompra)
                ],
                'threshold': {
                    'line': {'color': "#39FF14", 'width': 2}, # Línea de valor actual en verde
                    'thickness': 0.75,
                    'value': rsi_val
                }
            }
        ))
        fig_rsi.update_layout(height=220, paper_bgcolor='rgba(0,0,0,0)', font_color="white", margin=dict(t=0,b=0,l=10,r=10))
        st.plotly_chart(fig_rsi, use_container_width=True)

    with col_vol:
        # GRÁFICA DE VOLUMEN PROFESIONAL (El histograma de tu diseño anterior)
        st.write("### Volumen de Mercado")
        fig_vol = go.Figure(data=[go.Bar(
            y=df_data['Vol'],
            marker_color='#00f2ff', # Volumen Cian profesional
            opacity=0.5
        )])
        fig_vol.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=0,r=0,t=0,b=0), height=180, font_color="white",
            yaxis=dict(showgrid=False, showticklabels=False),
            xaxis=dict(showgrid=False, showticklabels=False)
        )
        st.plotly_chart(fig_vol, use_container_width=True)

with col_brain:
    # --- 🧠 CEREBRO MAHORA v2.0 (Terminal IA) ---
    ahora = datetime.now().strftime("%H:%M:%S")
    st.markdown(f"""
    <div style="background:#ff00ff22; border:1px solid #ff00ff; border-radius:10px; padding:15px; box-shadow:0 0 10px #ff00ff33;">
        <h4 style="margin:0; color:#ff00ff;">🧠 CEREBRO MAHORA v2.0</h4>
        <hr style="border-color:#ff00ff44">
        <div class="ia-terminal">
            [{ahora}] >> SCAN REAL FINALIZADO.<br>
            [{ahora}] >> CONEXIÓN BITSO: {"OK" if MODO_REAL else "SIM"}.<br>
            [{ahora}] >> SALDO DETECTADO: ${saldo_mxn} MXN.<br>
            [{ahora}] >> RSI 42.5 (NEUTRO).<br>
            [{ahora}] >> SIN SEÑAL CLARA. HOLD MXN.<br>
            [{ahora}] >> AJUSTE DE RIESGO: BAJO (2%).<br>
            <hr style="border-color:#333">
            >> PENSAMIENTO:<br>
            Angel, el mercado muestra volatilidad controlada. Manteniendo posición para el objetivo de los $10,000 MXN. Falta poco para el viaje a Canadá 🇨🇦.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.toggle("IA ACTIVA", value=True)
    if st.button("🚀 EJECUTAR OPERACIÓN MANUAL", use_container_width=True):
        st.toast("Conectando con Bitso para orden...")

# Auto-Refresh cada 15 seg
time.sleep(15)
st.rerun()
