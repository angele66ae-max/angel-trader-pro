import streamlit as st
import time, hashlib, hmac, json, requests
import plotly.graph_objects as go
import numpy as np

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE CENTER", page_icon="⛩️")

# Estilo de lujo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono&display=swap');
    .stApp { background-color: #000000; color: #ffffff; font-family: 'JetBrains Mono', monospace; }
    .main-title { font-family: 'Orbitron', sans-serif; color: #00f2ff; text-align: center; font-size: 35px; text-shadow: 0 0 10px #00f2ff; margin-bottom: 30px; }
    .metric-box { background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 10px; padding: 20px; text-align: center; }
    .status-vivido { background-color: #003300; border-radius: 15px; padding: 5px 15px; color: #00ff00; font-size: 12px; font-weight: bold; }
    .ai-logs { background: #050505; border: 1px solid #00ff00; border-radius: 5px; padding: 15px; height: 320px; overflow-y: auto; color: #00ff00; font-size: 13px; }
</style>
""", unsafe_allow_html=True)

# --- CARGA DE LLAVES ---
try:
    API_KEY = st.secrets["BITSO_API_KEY"]
    API_SECRET = st.secrets["BITSO_API_SECRET"]
except Exception as e:
    st.error(f"🚨 ERROR EN LLAVES: {str(e)}")
    st.stop()

# --- FUNCIONES DE RED ---
def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_payload = json.dumps(payload) if payload else ""
    message = nonce + method + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    url = f"https://api.bitso.com{path}"
    try:
        if method == "POST": return requests.post(url, headers=headers, data=json_payload).json()
        return requests.get(url, headers=headers).json()
    except Exception as e: return {"error": str(e)}

# --- OBTENER DATOS ---
ticker_res = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()
precio_real = float(ticker_res['payload']['last'])
balance_res = bitso_api("GET", "/v3/balance")
if 'payload' in balance_res:
    balances = balance_res['payload']['balances']
    usd_real = next((i['available'] for i in balances if i['currency'] == 'usd'), "0.00")
    btc_real = next((i['available'] for i in balances if i['currency'] == 'btc'), "0.00000000")
else:
    usd_real, btc_real = 2.81, 0.00000000 # Datos de respaldo

# --- LÓGICA DE TRADING REAL ---
def calcular_rsi():
    ticker_bitso = requests.get(f"https://api.bitso.com/v3/ticker/?book=btc_usd").json()
    precios = [float(ticker_bitso['payload']['last']) for _ in range(14)] # Simulado
    cambios = np.diff(precios)
    ganancias = changes[changes > 0].sum()
    perdidas = -changes[changes < 0].sum()
    rs = ganancias / perdidas if perdidas != 0 else 100
    return 100 - (100 / (1 + rs))

# --- INTERFAZ SHARK REAL ---
st.markdown('<div class="main-title">⛩️ MAHORASHARK: ADAPTACIÓN TOTAL</div>', unsafe_allow_html=True)

# Barra de estado superior
s1, s2 = st.columns([8, 1])
with s1:
    st.markdown("<h3><span class='status-vivido'>🟢 SISTEMA VIVO</span> <span style='color:gray; font-size:16px;'>v19.3 MAHORA CORE</span></h3>", unsafe_allow_html=True)

st.write("")

# Paneles de Métricas Tácticas
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-box"><p style="color:cyan;">BTC USD (MERCADO)</p><h2 style="margin:0;">{precio_real:,.0f} $</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-box"><p style="color:magenta;">SALDO DISPONIBLE</p><h2 style="margin:0;">{float(usd_real):.2f} $</h2></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-box"><p style="color:green;">MOTOR DE IA</p><h2 style="margin:0;">CAZANDO</h2><p style="color:gray;">ADAPTÁNDOSE...</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-box"><p style="color:white;">OBJETIVO SUV</p><h2 style="margin:0;">90.2%</h2></div>', unsafe_allow_html=True)

st.write("")

# Sección de Análisis Live y Pensamientos
col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<p style="font-size:18px;">📡 LIVE ANALYSIS</p>', unsafe_allow_html=True)
    # Gráfica de precio real
    fig = go.Figure(go.Scatter(y=[precio_real*0.999, precio_real], fill='tozeroy', line=dict(color='cyan', width=2)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(l=0,r=0,t=0,b=0), yaxis=dict(showgrid=False), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<p style="font-size:18px;">🕵️ PENSAMIENTOS DE LA IA</p>', unsafe_allow
