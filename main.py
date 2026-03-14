import streamlit as st
import time, hashlib, hmac, json, requests
import plotly.graph_objects as go

# --- CONFIGURACIÓN TÁCTICA ---
st.set_page_config(layout="wide", page_title="MAHORASHARK: PRESTIGE CENTER", page_icon="⛩️")

# Imagen de la Corona de Mahoraga (Dharma Wheel)
# Usamos una URL de imagen estable para evitar el error de 'pilot'
mahoraga_url = "https://w0.peakpx.com/wallpaper/639/940/HD-wallpaper-mahoraga-crown-anime-jujutsu-kaisen.jpg"

st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700&family=JetBrains+Mono&display=swap');
    .stApp {{
        background: linear-gradient(rgba(0,0,0,0.85), rgba(0,0,0,0.85)), url('{mahoraga_url}');
        background-size: cover;
        background-position: center;
        color: #ffffff;
        font-family: 'JetBrains Mono', monospace;
    }}
    .main-title {{
        font-family: 'Orbitron', sans-serif;
        color: #00f2ff;
        text-align: center;
        font-size: 35px;
        text-shadow: 0 0 15px #00f2ff;
    }}
    .metric-box {{
        background: rgba(15, 15, 15, 0.9);
        border: 1px solid #333;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
    }}
    .ai-logs {{
        background: rgba(0, 0, 0, 0.9);
        border: 1px solid #00ff00;
        color: #00ff00;
        padding: 15px;
        height: 300px;
        overflow-y: auto;
        font-size: 13px;
    }}
</style>
""", unsafe_allow_html=True)

# --- CARGA DE LLAVES ---
try:
    API_KEY = st.secrets["BITSO_API_KEY"]
    API_SECRET = st.secrets["BITSO_API_SECRET"]
except Exception as e:
    st.error("🚨 ERROR EN SECRETS: Revisa tu configuración")
    st.stop()

# --- MOTOR DE RED ---
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
    except: return {"error": "OFFLINE"}

# --- OBTENER DATOS ---
ticker = requests.get("https://api.bitso.com/v3/ticker/?book=btc_usd").json()['payload']
precio_actual = float(ticker['last'])
balance_data = bitso_api("GET", "/v3/balance")
usd_real = next((i['available'] for i in balance_data['payload']['balances'] if i['currency'] == 'usd'), "0")

# --- INTERFAZ ---
st.markdown('<div class="main-title">⛩️ MAHORASHARK: TERMINAL DE PRESTIGIO</div>', unsafe_allow_html=True)
st.write("")

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f'<div class="metric-box"><p style="color:cyan;">BTC USD</p><h2>{precio_actual:,.0f}</h2></div>', unsafe_allow_html=True)
with c2:
    st.markdown(f'<div class="metric-box"><p style="color:magenta;">SALDO REAL</p><h2>${float(usd_real):.2f}</h2></div>', unsafe_allow_html=True)
with c3:
    st.markdown('<div class="metric-box"><p style="color:green;">IA CORE</p><h2>ADAPTANDO</h2></div>', unsafe_allow_html=True)
with c4:
    st.markdown('<div class="metric-box"><p style="color:white;">SUV META</p><h2>90.2%</h2></div>', unsafe_allow_html=True)

st.write("")
col_l, col_r = st.columns([2, 1])

with col_l:
    fig = go.Figure(go.Scatter(y=[precio_actual*0.999, precio_actual], fill='tozeroy', line=dict(color='cyan')))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=350, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

with col_r:
    st.subheader("🕵️ PENSAMIENTOS")
    if "logs" not in st.session_state: 
        st.session_state.logs = [f"[{time.strftime('%H:%M:%S')}] SISTEMA INICIADO. OPERADOR: MAHORASHARK"]
    
    if st.button("🚀 INICIAR ADAPTACIÓN"):
        st.session_state.active = True
        st.session_state.logs.insert(0, f"[{time.strftime('%H:%M:%S')}] CAZANDO CON SALDO DE ${usd_real} USD")

    log_html = "".join([f"<p style='margin:2px;'>{l}</p>" for l in st.session_state.logs])
    st.markdown(f'<div class="ai-logs">{log_html}</div>', unsafe_allow_html=True)

if st.session_state.get("active", False):
    time.sleep(10)
    st.rerun()
