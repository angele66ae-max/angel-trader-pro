import streamlit as st
import time
import requests
import hashlib
import hmac
import json
import pandas as pd

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="SHARK AI TERMINAL")

# ---------- API ----------
API_KEY = st.secrets.get("BITSO_API_KEY","")
API_SECRET = st.secrets.get("BITSO_API_SECRET","")

BASE_URL = "https://api.bitso.com"

# ---------- ESTILO CINE ----------
st.markdown("""
<style>

.stApp{
background: radial-gradient(circle at top,#050505,#000000);
color:#00eaff;
font-family:monospace;
}

.title{
font-size:50px;
text-align:center;
color:#00eaff;
text-shadow:0 0 20px #00eaff;
}

.card{
background:#0b0b0b;
border:1px solid #00eaff;
border-radius:10px;
padding:20px;
box-shadow:0 0 15px #00eaff;
}

button[kind="secondary"]{
background:#00eaff;
color:black;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🦈 SHARK AI TRADING TERMINAL</div>',unsafe_allow_html=True)

# ---------- SESSION ----------
if "ai_on" not in st.session_state:
    st.session_state.ai_on=False

# ---------- PRECIO ----------
def get_price():
    r=requests.get(f"{BASE_URL}/v3/ticker/?book=btc_mxn")
    return float(r.json()["payload"]["last"])

# ---------- TRADES ----------
def get_trades():
    r=requests.get(f"{BASE_URL}/v3/trades/?book=btc_mxn&limit=100")
    df=pd.DataFrame(r.json()["payload"])
    df["price"]=df["price"].astype(float)
    return df

# ---------- RSI ----------
def rsi(series,period=14):

    delta=series.diff()

    gain=delta.clip(lower=0)
    loss=-delta.clip(upper=0)

    avg_gain=gain.rolling(period).mean()
    avg_loss=loss.rolling(period).mean()

    rs=avg_gain/avg_loss

    return 100-(100/(1+rs))

# ---------- ORDEN ----------
def order(side,amount):

    path="/v3/orders"

    nonce=str(int(time.time()*1000))

    order={
        "book":"btc_mxn",
        "side":side,
        "type":"market",
        "major":amount
    }

    body=json.dumps(order)

    message=nonce+"POST"+path+body

    signature=hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    headers={
        "Authorization":f"Bitso {API_KEY}:{nonce}:{signature}",
        "Content-Type":"application/json"
    }

    r=requests.post(BASE_URL+path,headers=headers,data=body)

    return r.json()

# ---------- DATOS ----------
df=get_trades()

precio=get_price()

rsi_actual=float(rsi(df["price"]).iloc[-1])

# ---------- PANEL ----------
c1,c2,c3=st.columns(3)

with c1:
    st.metric("BTC PRICE",f"${precio:,.0f} MXN")

with c2:
    st.metric("RSI",round(rsi_actual,2))

with c3:
    estado="ACTIVA" if st.session_state.ai_on else "OFF"
    st.metric("AI STATUS",estado)

# ---------- BOTONES ----------
b1,b2,b3=st.columns(3)

if b1.button("🤖 ACTIVAR IA"):
    st.session_state.ai_on=True

if b2.button("🛑 DETENER IA"):
    st.session_state.ai_on=False

if b3.button("🟢 COMPRAR $100"):
    st.write(order("buy",100))

# ---------- IA ----------
st.divider()

if st.session_state.ai_on:

    st.success("IA OPERANDO EN MERCADO")

    if rsi_actual<30:

        st.write("🟢 IA COMPRA BTC")
        order("buy",100)

    elif rsi_actual>70:

        st.write("🔴 IA VENDE BTC")
        order("sell",100)

    else:

        st.write("⏳ IA ANALIZANDO MERCADO")

else:

    st.warning("IA DESACTIVADA")

# ---------- HISTORIAL ----------
st.divider()

st.subheader("📊 HISTORIAL DE TRADES")

st.line_chart(df["price"])

# ---------- REFRESH ----------
time.sleep(15)
st.rerun()
