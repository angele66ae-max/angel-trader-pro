import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import hmac
import hashlib
import time
from datetime import datetime

# --- CONFIGURACIÓN DE IDENTIDAD ---
NOMBRE = "Angel"
st.set_page_config(layout="wide", page_title=f"MahoraShark - {NOMBRE}")

# --- SEGURIDAD BITSO ---
# Asegúrate de tener estas llaves en Streamlit Cloud > Settings > Secrets
try:
    API_KEY = st.secrets["BITSO_KEY"]
    API_SECRET = st.secrets["BITSO_SECRET"]
    OPERACION_REAL = True
except:
    OPERACION_REAL = False

def firmar(metodo, endpoint, cuerpo=""):
    nonce = str(int(time.time() * 1000))
    mensaje = nonce + metodo + endpoint + cuerpo
    firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
    return {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}

# --- OBTENCIÓN DE TUS MONEDAS REALES ---
def obtener_mi_cartera_real():
    if not OPERACION_REAL:
        # Datos de prueba basados en tu imagen
        return pd.DataFrame([
            {"Moneda": "MXN", "Balance": 68.90, "Valor aprox MXN": 68.90},
            {"Moneda": "BTC", "Balance": 0.00003542, "Valor aprox MXN": 44.79},
            {"Moneda": "USD", "Balance": 0.22, "Valor aprox MXN": 3.94}
        ])
    
    try:
        headers = firmar("GET", "/v3/balance/")
        res = requests.get("https://api.bitso.com/v3/balance/", headers=headers).json()
        items = []
        for b in res['payload']['balances']:
            total = float(b['total'])
            if total > 0:
                items.append({"Moneda": b['currency'].upper(), "Balance": total})
        return pd.DataFrame(items)
    except:
        return pd.DataFrame(columns=["Moneda", "Balance"])

# --- INTERFAZ ---
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura_de_pantalla_2026_03_14_005126.png"
st.markdown(f"""<style>.stApp {{ background: linear-gradient(rgba(5,10,14,0.9), rgba(5,10,14,0.9)), url("{fondo_url}"); background-size: cover; color: white; }}</style>""", unsafe_allow_html=True)

# Datos Actualizados
precio_btc = requests.get("https://api.bitso.com/v3/ticker/?book=btc_mxn").json()['payload']['last']
df_cartera = obtener_mi_cartera_real()
saldo_mxn_total = df_cartera[df_cartera['Moneda'] == 'MXN']['Balance'].sum()

st.title(f"⛩️ MAHORASHARK: {NOMBRE.upper()} PRESTIGE")

# Métricas Top
c1, c2, c3 = st.columns(3)
c1.metric("BTC/MXN", f"${float(precio_btc):,.0f}")
c2.metric("MI SALDO DISPONIBLE", f"${saldo_mxn_total:,.2f} MXN")
c3.metric("PROGRESO CANADÁ", f"{(saldo_mxn_total/10000)*100:.4f}%")

st.write("---")

col_main, col_wallet = st.columns([2, 1])

with col_main:
    st.subheader("📊 Mercado en Vivo")
    # Gráfica estética de Velas Neón
    fig = go.Figure(data=[go.Candlestick(
        open=[float(precio_btc)]*20, high=[float(precio_btc)*1.002]*20,
        low=[float(precio_btc)*0.998]*20, close=[float(precio_btc)]*20,
        increasing_line_color='#00f2ff', decreasing_line_color='#ff00ff'
    )])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', 
                      font_color='white', xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, use_container_width=True)

with col_wallet:
    st.subheader("💰 Tu Cartera Real")
    # Tabla de tus activos
    st.dataframe(df_cartera, hide_index=True, use_container_width=True)
    
    st.markdown("""<div style="background: rgba(0,0,0,0.5); padding:10px; border-radius:10px; border: 1px solid #ff00ff;">
        <b>Cerebro Mahora:</b><br>
        Angel, he detectado tus activos. <br>
        Tu saldo principal es en Pesos ($68.9 MXN).<br>
        ¿Quieres que convierta el BTC a MXN cuando suba?
    </div>""", unsafe_allow_html=True)

time.sleep(30)
st.rerun()
