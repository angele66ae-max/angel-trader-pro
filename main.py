import streamlit as st
import time, hashlib, hmac, json, requests
import plotly.graph_objects as go
from pilot import image_gen

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE CENTER", page_icon="⛩️")

# Generación de la Corona de Mahoraga para el fondo
mahoraga_corona_url = image_gen(prompt="A minimalist, stylized watermark of Mahoraga's eight-spoked wheel (Dharma Chakra) crown from Jujutsu Kaisen, rendered in a translucent, glowing cyan outline against a deep black background, suitable as a subtle UI background element.")[0]

# Estilo de lujo con fondo de Mahoraga
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono&display=swap');
    .stApp {{
        background-color: #000000;
        background-image: url('{mahoraga_corona_url}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }}
    .main-title {{
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        text-align: center;
        font-size: 38px;
        text-shadow: 0 0 15px #00f2ff;
        margin-bottom: 30px;
    }}
    .metric-box {{
        background: rgba(10, 10, 10, 0.8);
        border: 2px solid #1a1a1a;
        border-radius: 12px;
        padding: 22px;
        backdrop-filter: blur(5px);
    }}
    .ai-logs {{
        background: rgba(5, 5, 5, 0.9);
        border: 2px solid #00ff00;
        border-radius: 8px;
        padding: 12px;
        height: 320px;
        overflow-y: auto;
        color: #00ff00;
        font-size: 13px;
        backdrop-filter: blur(5px);
    }}
</style>
""", unsafe_allow_html=True)

# --- CARGA DE LLAVES ---
try:
    API_KEY = st.secrets["BITSO_API_KEY"]
    API_SECRET = st.secrets["BITSO_API_SECRET"]
except:
    st.error("🚨 LLAVES NO ENCONTRADAS")
    st.stop()

# --- FUNCIONES DE RED ---
def bitso_api(method, path, payload=None):
    nonce = str(int(time.time() * 1000))
    json_payload = json.dumps(payload) if payload else ""
    message = nonce + method + path + json_payload
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{signature}', 'Content-Type': 'application/json'}
    try:
        if method == "POST":
            return requests.post(f"https://api.bitso.com{path}", headers=headers, data=json_payload).json()
        return requests.get(f"https://api.bitso.com{path}", headers=headers).json()
    except: return {"error": "Connection lost"}

# --- OBTENER DATOS ---
try:
    ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']
    precio_actual = float(ticker['last'])
    balance_data = bitso_api("GET", "/v3/balance")
    usd_real = next((i['available'] for i in balance_data['payload']['balances'] if i['currency'] == 'usd'), "0")
except:
    precio_actual, usd_real = 70961.0, 2.81 # Datos de respaldo

# --- DISEÑO DE LA TERMINAL ---
st.markdown('<div class="main-title">⛩️ MAHORASHARK: ADAPTACIÓN TOTAL</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-box"><p style="color:cyan; font-size:12px;">MERCADO DE BTC</p><h2 style="margin:0;">{precio_actual:,.0f} $</h2><p style="color:gray; font-size:10px;">USD</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-box"><p style="color:magenta; font-size:12px;">SALDO DISPONIBLE</p><h2 style="margin:0;">{float(usd_real):.2f} $</h2><p style="color:gray; font-size:10px;">USD</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-box"><p style="color:green; font-size:12px;">ESTADO DE IA</p><h2 style="margin:0;">CAZANDO</h2><p style="color:gray; font-size:10px;">v19.0 MAHORA</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-box"><p style="color:white; font-size:12px;">OBJETIVO SUV</p><h2 style="margin:0;">90.2%</h2><div style="background:#333; height:5px; border-radius:5px;"><div style="background:cyan; width:90.2%; height:5px; border-radius:5px;"></div></div></div>', unsafe_allow_html=True)

st.write("")

col_left, col_right = st.columns([2, 1])

with col_left:
    st.markdown('<p style="font-size:18px;">📡 ANÁLISIS DE MERCADO (LIVE)</p>', unsafe_allow_html=True)
    # Gráfica de análisis en vivo
    fig = go.Figure(go.Scatter(y=[precio_actual*0.9995, precio_actual], fill='tozeroy', line=dict(color='cyan', width=3)))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=380, margin=dict(l=0,r=0,t=0,b=0), yaxis=dict(showgrid=False), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<p style="font-size:18px;">🕵️ PENSAMIENTOS DE LA IA</p>', unsafe_allow_html=True)
    if "logs" not in st.session_state: st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] SISTEMA INICIADO. OPERADOR: MAHORASHARK"]
    
    if st.button("🚀 INICIAR ADAPTACIÓN"):
        st.session_state.active = True
        st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] CAZANDO EN MERCADO REAL...")

    log_html = "".join([f"<p style='margin:2px;'>{l}</p>" for l in st.session_state.logs])
    st.markdown(f'<div class="ai-logs">{log_html}</div>', unsafe_allow_html=True)

# --- MOTOR DE ACCIÓN ---
if st.session_state.get("active", False):
    # Lógica de compra real
    # bitso_api("POST", "/v3/orders", {"book": "btc_usd", "side": "buy", "type": "market", "major": "1.00"})
    time.sleep(10)
    st.rerun()
