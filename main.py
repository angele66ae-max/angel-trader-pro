import streamlit as st
import pandas as pd
import numpy as np
import time
import hmac
import hashlib
import requests
from datetime import datetime

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="MAHORASHARK AI")

BITSO_API_KEY = "TU_API_KEY"
BITSO_API_SECRET = "TU_SECRET"

BASE_URL = "https://api.bitso.com"

# ---------- FONDO ----------
fondo_url = "https://i.postimg.cc/gJSbdJ5f/Captura-de-pantalla-2026-03-14-005126.png"

st.markdown(f"""
<style>

.stApp{{
background: linear-gradient(rgba(0,0,0,0.85),rgba(0,0,0,0.85)),url("{fondo_url}");
background-size:cover;
background-attachment:fixed;
}}

.card{{
background:rgba(15,20,25,0.9);
border:1px solid #00f2ff;
border-radius:10px;
padding:20px;
box-shadow:0 0 15px #00f2ff33;
}}

.metric{{
font-size:28px;
color:#00f2ff;
font-weight:bold;
}}

</style>
""", unsafe_allow_html=True)

# ---------- SESION ----------
if "log" not in st.session_state:
    st.session_state.log = []

if "price_history" not in st.session_state:
    st.session_state.price_history = []

if "ai_on" not in st.session_state:
    st.session_state.ai_on = False

# ---------- FUNCIONES BITSO ----------

def get_price():

    url = f"{BASE_URL}/v3/ticker/?book=btc_mxn"

    r = requests.get(url)

    data = r.json()

    return float(data["payload"]["last"])


def get_balance():

    nonce = str(int(time.time()*1000))

    path="/v3/balance/"

    message = nonce+"GET"+path

    signature = hmac.new(
        BITSO_API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Authorization": f"Bitso {BITSO_API_KEY}:{nonce}:{signature}"
    }

    r=requests.get(BASE_URL+path,headers=headers)

    return r.json()


def place_order(side, amount):

    nonce=str(int(time.time()*1000))

    path="/v3/orders"

    body = {
        "book":"btc_mxn",
        "side":side,
        "type":"market",
        "major":amount
    }

    body_json = str(body).replace("'","\"")

    message = nonce+"POST"+path+body_json

    signature = hmac.new(
        BITSO_API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    headers={
        "Authorization":f"Bitso {BITSO_API_KEY}:{nonce}:{signature}",
        "Content-Type":"application/json"
    }

    r=requests.post(BASE_URL+path,headers=headers,data=body_json)

    return r.json()

# ---------- RSI ----------
def rsi(data,period=14):

    series=pd.Series(data)

    delta=series.diff()

    gain=(delta.where(delta>0,0)).rolling(period).mean()

    loss=(-delta.where(delta<0,0)).rolling(period).mean()

    rs=gain/loss

    return 100-(100/(1+rs))

# ---------- TITULO ----------
st.title("⛩️ MAHORASHARK AI TRADER")

# ---------- PRECIO ----------
price=get_price()

st.session_state.price_history.append(price)

price_series=pd.Series(st.session_state.price_history)

# ---------- RSI ----------
if len(price_series)>15:
    rsi_value=rsi(price_series).iloc[-1]
else:
    rsi_value=50

# ---------- PANEL ----------
col1,col2,col3,col4=st.columns(4)

with col1:
    st.markdown('<div class="card">BTC PRICE</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="metric">${price:,.2f} MXN</div>',unsafe_allow_html=True)

with col2:
    st.markdown('<div class="card">RSI</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="metric">{rsi_value:.2f}</div>',unsafe_allow_html=True)

with col3:

    if st.session_state.ai_on:
        status="GENERANDO"
    else:
        status="PAUSADO"

    st.markdown('<div class="card">ESTADO IA</div>',unsafe_allow_html=True)
    st.markdown(f'<div class="metric">{status}</div>',unsafe_allow_html=True)

with col4:

    st.markdown('<div class="card">META</div>',unsafe_allow_html=True)
    st.progress(116/10000)

# ---------- BOTONES ----------

c1,c2=st.columns(2)

with c1:

    if st.button("🚀 ACTIVAR IA"):
        st.session_state.ai_on=True
        st.session_state.log.append("IA ACTIVADA")

with c2:

    if st.button("⛔ DETENER IA"):
        st.session_state.ai_on=False
        st.session_state.log.append("IA DETENIDA")

# ---------- IA TRADING ----------

if st.session_state.ai_on:

    if rsi_value<30:

        st.session_state.log.append("IA DETECTA SOBREVENTA -> COMPRA")

        # place_order("buy",0.00001)

    elif rsi_value>70:

        st.session_state.log.append("IA DETECTA SOBRECOMPRA -> VENDE")

        # place_order("sell",0.00001)

    else:

        st.session_state.log.append("IA ANALIZANDO MERCADO")

# ---------- GRAFICA ----------
st.subheader("Mercado BTC")

chart_df=pd.DataFrame({"BTC":price_series})

st.line_chart(chart_df)

# ---------- LOGS ----------
st.subheader("Cerebro IA")

st.code("\n".join(st.session_state.log[-10:]))

# ---------- REFRESH ----------
time.sleep(5)
st.rerun()
