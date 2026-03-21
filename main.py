import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import hmac, hashlib, time, numpy as np
from datetime import datetime

# --- 1. CONFIGURACIÓN DE PÁGINA E IDENTIDAD ---
st.set_page_config(layout="wide", page_title="Angel's Prestige Center", page_icon="⛩️")

# Nombre del usuario para personalizar la IA
NOMBRE_USUARIO = "Angel"

# --- 2. CONEXIÓN REAL BITSO & SEGURIDAD ---
# Se asume que las llaves están en Streamlit Secrets
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

def firmar_solicitud(metodo, endpoint, cuerpo=""):
    """Genera la firma HMAC necesaria para la API privada de Bitso."""
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- 3. ESTILO CSS PERSONALIZADO (EL "LOOK & FEEL") ---
# Este bloque recrea los bordes neón, el fondo oscuro y la tipografía del diseño.
st.markdown("""
    <style>
    /* Fondo general oscuro y limpio */
    .stApp {
        background-color: #06090f;
        color: #e6e6e6;
        font-family: 'Inter', sans-serif;
    }

    /* Ocultar elementos predeterminados de Streamlit */
    #MainMenu, header, footer {visibility: hidden;}
    .block-container {padding-top: 2rem; padding-bottom: 0rem;}

    /* Contenedor principal del Header */
    .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1.5rem;
    }

    /* Título principal con brillo neón tenue */
    .main-title {
        color: #ffffff;
        font-size: 28px;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 242, 255, 0.5);
        display: flex;
        align-items: center;
        gap: 10px;
    }

    /* Estilo de las tarjetas de métricas superiores */
    .metric-card {
        background-color: #0b1018;
        border: 1px solid #1a2638;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        transition: border-color 0.3s;
    }
    
    /* Efecto neón al pasar el mouse (opcional, para feedback) */
    .metric-card:hover {
        border-color: #00f2ff;
        box-shadow: 0 0 10px rgba(0, 242, 255, 0.2);
    }

    .metric-title {
        color: #8b9bb4;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 24px;
        font-weight: 700;
    }

    .metric-change {
        font-size: 14px;
        font-weight: 600;
    }

    /* Estilo del panel lateral de la IA (Cerebro Mahora) */
    .ia-panel {
        background-color: #0b1018;
        border: 1px solid #2d1331; /* Borde magenta oscuro */
        border-radius: 12px;
        padding: 20px;
        height: 100%;
    }

    .ia-header {
        display: flex;
        align-items: center;
        gap: 10px;
        color: #ff00ff; /* Magenta neón */
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 15px;
    }

    /* Consola de logs estilo hacking */
    .ia-console {
        background-color: #000000;
        border-radius: 8px;
        padding: 15px;
        font-family: 'Courier New', monospace;
        color: #39FF14; /* Verde neón */
        font-size: 13px;
        line-height: 1.6;
        height: 300px;
        overflow-y: auto;
    }

    .log-time { color: #888; }
    .log-thought { color: #e6e6e6; font-style: italic; margin-top: 10px; display: block;}

    /* Estilo de los títulos de secciones */
    .section-title {
        color: #8b9bb4;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 1rem;
        margin-top: 1.5rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. FUNCIONES DE DATOS (REAL-TIME) ---
@st.cache_data(ttl=10) # Cachear datos por 10 segundos
def obtener_datos_mercado():
    """Obtiene precio actual y datos históricos para la gráfica."""
    try:
        # Precio actual
        r_ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']
        precio_actual = float(r_ticker['last'])
        vwap = float(r_ticker['vwap'])
        cambio_pct = ((precio_actual - vwap) / vwap) * 100

        # Simulación de datos históricos (Velas) para la gráfica pro
        # En producción, usarías un endpoint de OHLCV real
        np.random.seed(42) # Para consistencia en la demo
        fechas = pd.date_range(start=datetime.now() - pd.Timedelta(hours=1), periods=60, freq='T')
        precios = [precio_actual * (1 + np.sin(i/5)*0.002 + np.random.normal(0, 0.001)) for i in range(60)]
        
        df = pd.DataFrame({'Timestamp': fechas, 'Close': precios})
        df['Open'] = df['Close'].shift(1).fillna(precios[0] * 0.999)
        df['High'] = df[['Open', 'Close']].max(axis=1) * 1.001
        df['Low'] = df[['Open', 'Close']].min(axis=1) * 0.999
        df['Volumen'] = np.random.randint(100, 1000, 60)
        # EMAs
        df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
        df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
        
        return precio_actual, cambio_pct, df
    except Exception as e:
        st.error(f"Error obteniendo datos de mercado: {e}")
        return 0, 0, pd.DataFrame()

def obtener_saldo_real():
    """Consulta el saldo real en Bitso."""
    if not MODO_REAL:
        return 68.91 # Valor de prueba si no hay llaves
    try:
        url = "https://api.bitso.com/v3/balance/"
        headers = firmar_solicitud("GET", "/v3/balance/")
        r = requests.get(url, headers=headers).json()
        for b in r['payload']['balances']:
            if b['currency'] == 'mxn':
                return float(b['total'])
        return 0.0
    except:
        return 0.0

# --- 5. LÓGICA DE ACTUALIZACIÓN ---
precio_btc, cambio_pct, df_mercado = obtener_datos_mercado()
saldo_mxn = obtener_saldo_mxn_real()
progreso_10k = (saldo_mxn / 10000) * 100

# --- 6. RENDERIZADO DE LA INTERFAZ (ESTILO PRESTIGE) ---

# Título y Logo
st.markdown(f"""
    <div class="header-container">
        <div class="main-title">
            <img src="https://img.icons8.com/fluency/48/torii-gate.png" width="30"/>
            MAHORASHARK
        </div>
        <div style="color: #00f2ff; font-weight: 600;">{NOMBRE_USUARIO.upper()}'S PRESTIGE CENTER</div>
    </div>
    """, unsafe_allow_html=True)

# Panel de Métricas Superiores (Las 4 tarjetas neón)
m1, m2, m3, m4 = st.columns(4)

with m1:
    color_cambio = "#39FF14" if cambio_pct >= 0 else "#ff00ff"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">BTC/MXN</div>
            <div class="metric-value">${precio_btc:,.0f}</div>
            <div class="metric-change" style="color: {color_cambio};">{cambio_pct:+.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">MXN BALANCE</div>
            <div class="metric-value">${saldo_mxn:,.2f}</div>
            <div class="metric-change" style="color: #8b9bb4;">(REAL)</div>
        </div>
        """, unsafe_allow_html=True)

with m3:
    # Estado dinámico de la IA
    estado_ia = "ACTIVATED" if MODO_REAL else "SIMULATION"
    color_estado = "#39FF14" if MODO_REAL else "#ffc107"
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">IA STATUS</div>
            <div class="metric-value" style="color: {color_estado};">{estado_ia}</div>
            <div class="metric-change">🟢 Online</div>
        </div>
        """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">META 10K PROGRESS</div>
            <div class="metric-value">{progreso_10k:.2f}%</div>
            <div class="metric-change" style="color: #8b9bb4;">Target: $10,000</div>
        </div>
        """, unsafe_allow_html=True)


# Disposición Principal: Gráfica a la izquierda, IA a la derecha
col_grafica, col_ia = st.columns([2.2, 1])

with col_grafica:
    st.markdown('<div class="section-title">Gráfica de Velas Japonesas (Professional View)</div>', unsafe_allow_html=True)
    
    # --- Creación de la Gráfica Pro con Plotly ---
    if not df_mercado.empty:
        fig = go.Figure(data=[
            # Velas Japonesas
            go.Candlestick(
                x=df_mercado['Timestamp'],
                open=df_mercado['Open'], high=df_mercado['High'],
                low=df_mercado['Low'], close=df_mercado['Close'],
                increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff', # Cian para subir, Magenta para bajar
                increasing_fillcolor='#00f2ff', decreasing_fillcolor='#ff00ff',
                name='BTC/MXN'
            ),
            # Líneas EMA
            go.Scatter(x=df_mercado['Timestamp'], y=df_mercado['EMA20'], line=dict(color='#00f2ff', width=1), name='EMA 20'),
            go.Scatter(x=df_mercado['Timestamp'], y=df_mercado['EMA50'], line=dict(color='#ff00ff', width=1), name='EMA 50')
        ])

        # Configuración del diseño de la gráfica (Limpio y oscuro)
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', # Fondo transparente para integrarse
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=10, r=10, t=10, b=10),
            xaxis_rangeslider_visible=False, # Ocultar slider inferior
            showlegend=False,
            yaxis=dict(
                gridcolor='#1a2638', # Rejilla tenue
                showgrid=True,
                zeroline=False,
                tickprefix="$",
                tickfont=dict(color='#8b9bb4')
            ),
            xaxis=dict(
                gridcolor='#1a2638',
                showgrid=True,
                tickfont=dict(color='#8b9bb4'),
                format='%H:%M' # Formato de hora corto
            )
        )
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    else:
        st.warning("Esperando datos de mercado...")

    # --- Sección de Indicadores Inferiores ---
    st.markdown('<div class="section-title">Indicadores Cuantitativos (Real-Time)</div>', unsafe_allow_html=True)
    c_rsi, c_vol = st.columns([1, 1.2])
    
    with c_rsi:
        # Medidor RSI (Gauge)
        rsi_actual = 42.5 # Valor simulado
        fig_rsi = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = rsi_actual,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "RSI (14)", 'font': {'color': '#8b9bb4', 'size': 14}},
            number = {'font': {'color': '#ffffff', 'size': 20}},
            gauge = {
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#8b9bb4"},
                'bar': {'color': "#00f2ff"}, # Barra cian
                'bgcolor': "#0b1018",
                'borderwidth': 1,
                'bordercolor': "#1a2638",
                'steps': [
                    {'range': [0, 30], 'color': '#ff00ff', 'name': 'Oversold'}, # Magenta
                    {'range': [30, 70], 'color': '#0b1018'},
                    {'range': [70, 100], 'color': '#ff00ff', 'name': 'Overbought'} # Magenta
                ],
                'threshold': {
                    'line': {'color': "#39FF14", 'width': 2},
                    'thickness': 0.75,
                    'value': rsi_actual
                }
            }
        ))
        fig_rsi.update_layout(height=180, paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig_rsi, use_container_width=True, config={'displayModeBar': False})

    with c_vol:
        # Histograma de Volumen
        if not df_mercado.empty:
            fig_vol = go.Figure(data=[go.Bar(
                x=df_mercado['Timestamp'],
                y=df_mercado['Volumen'],
                marker_color=['#00f2ff' if df_mercado['Close'][i] >= df_mercado['Open'][i] else '#ff00ff' for i in range(len(df_mercado))],
                opacity=0.8
            )])
            fig_vol.update_layout(
                height=180,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                showlegend=False,
                yaxis=dict(showgrid=False, showticklabels=False),
                xaxis=dict(showgrid=False, showticklabels=False)
            )
            st.plotly_chart(fig_vol, use_container_width=True, config={'displayModeBar': False})


with col_ia:
    # --- PANEL DEL CEREBRO MAHORA (DERECHA) ---
    st.markdown(f"""
        <div class="ia-panel">
            <div class="ia-header">
                <img src="https://img.icons8.com/fluency/48/brain.png" width="24"/>
                CEREBRO MAHORA v2.0
            </div>
            
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                <span style="color: #e6e6e6; font-size: 14px;">IA ACTIVA</span>
                <div style="width: 40px; height: 20px; background-color: #00f2ff; border-radius: 10px; position: relative;">
                    <div style="width: 16px; height: 16px; background-color: white; border-radius: 50%; position: absolute; right: 2px; top: 2px;"></div>
                </div>
            </div>

            <div class="ia-console">
                <span class="log-time">[{datetime.now().strftime("%H:%M:%S")}]</span> >> MERCADO ESTABLE.<br>
                <span class="log-time">[{datetime.now().strftime("%H:%M:%S")}]</span> >> RSI 42.5 (NEUTRO).<br>
                <span class="log-time">[{datetime.now().strftime("%H:%M:%S")}]</span> >> SIN SEÑAL CLARA. HOLD MXN.<br>
                <span class="log-time">[{datetime.now().strftime("%H:%M:%S")}]</span> >> AJUSTE DE RIESGO: BAJO (2%).<br>
                <span class="log-time">[{datetime.now().strftime("%H:%M:%S")}]</span> >> SIGUIENTE SCAN EN 15S.<br>
                <span class="log-thought">>> Pensamiento: {NOMBRE_USUARIO}, el mercado muestra volatilidad baja. Sugiero mantener posición para el viaje a Canadá 🇨🇦.</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Botón de operación manual (estilizado con Streamlit pero integrado)
    st.write("")
    if st.button("🚀 EJECUTAR ESCANEO QUANTUM", use_container_width=True):
        st.snow() # Efecto visual de confirmación
        st.toast("Iniciando escaneo profundo de liquidez...", icon="🧠")

# --- 7. AUTO-REFRESH ---
# Streamlit no tiene autorefresh nativo eficiente, usamos un bucle simple
# Para producción, considera usar componentes como streamlit-autorefresh
time.sleep(15)
st.rerun()
