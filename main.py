import streamlit as st
import time, hashlib, hmac, json, requests
import plotly.graph_objects as go

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(layout="wide", page_title="SHARK AI: PRESTIGE CENTER", page_icon="🦈")

# Estilo de lujo
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&display=swap');
    .stApp { background-color: #000000; color: #ffffff; }
    .main-title { font-family: 'Orbitron', sans-serif; color: #00f2ff; text-align: center; font-size: 35px; text-shadow: 0 0 10px #00f2ff; margin-bottom: 30px; }
    .metric-box { background: #0a0a0a; border: 1px solid #1a1a1a; border-radius: 10px; padding: 20px; }
    .ai-logs { background: #050505; border: 1px solid #00ff00; border-radius: 5px; padding: 10px; height: 300px; overflow-y: auto; color: #00ff00; font-family: monospace; }
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
ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']
precio_actual = float(ticker['last'])
balance_data = bitso_api("GET", "/v3/balance")
usd_real = next((i['available'] for i in balance_data['payload']['balances'] if i['currency'] == 'usd'), "0")

# --- DISEÑO DE LA TERMINAL ---
st.markdown('<div class="main-title">🦈 IA DE TIBURÓN: TERMINAL DE PRESTIGIO</div>', unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-box"><p style="color:cyan; font-size:12px;">MERCADO DE BTC</p><h2 style="margin:0;">{precio_actual:,.0f} $</h2><p style="color:gray; font-size:10px;">USD</p></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-box"><p style="color:magenta; font-size:12px;">SALDO DISPONIBLE</p><h2 style="margin:0;">{float(usd_real):.2f} $</h2><p style="color:gray; font-size:10px;">USD</p></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-box"><p style="color:green; font-size:12px;">MOTOR DE IA</p><h2 style="margin:0;">ACTIVOS</h2><p style="color:gray; font-size:10px;">v10.1 CORE</p></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-box"><p style="color:white; font-size:12px;">OBJETIVO SUV</p><h2 style="margin:0;">90.2%</h2><div style="background:#333; height:5px; border-radius:5px;"><div style="background:cyan; width:90.2%; height:5px; border-radius:5px;"></div></div></div>', unsafe_allow_html=True)

st.write("")

col_left, col_right = st.columns([2, 1])

with col_left:
    # Gráfica de análisis en vivo
    fig = go.Figure(go.Scatter(y=[precio_actual*0.999, precio_actual], fill='tozeroy', line=dict(color='cyan', width=2)))
    fig.update_layout(paper_bgcolor='black', plot_bgcolor='black', height=350, margin=dict(l=0,r=0,t=0,b=0), yaxis=dict(showgrid=False), xaxis=dict(showgrid=False))
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    st.markdown('<p style="font-size:18px;">🕵️ PENSAMIENTOS DE LA IA</p>', unsafe_allow_html=True)
    if "logs" not in st.session_state: st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] SISTEMA INICIADO. OPERADOR: PAVO FREE FIRE"]
    
    if st.button("🚀 DEPLOY AI"):
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
