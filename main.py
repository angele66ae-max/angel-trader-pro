import streamlit as st
import time
import requests
import hashlib
import hmac
import json
import pandas as pd

# ---------- CONFIG ----------
st.set_page_config(layout="wide", page_title="SHARK AI TRADER")

# ---------- API ----------
API_KEY = st.secrets.get("BITSO_API_KEY","")
API_SECRET = st.secrets.get("BITSO_API_SECRET","")

BASE_URL = "https://api.bitso.com"

# ---------- ESTILO ----------
st.markdown("""
<style>
.stApp {background-color:#050505;color:#00eaff;}
.block-container {padding-top:2rem;}
</style>
""", unsafe_allow_html=True)

st.title("🦈 SHARK AI TRADER")

# ---------- SESSION ----------
if "auto_trading" not in st.session_state:
    st.session_state.auto_trading = False

# ---------- PRECIO ----------
def get_price(book="btc_mxn"):
    try:
        r = requests.get(f"{BASE_URL}/v3/ticker/?book={book}")
        return float(r.json()["payload"]["last"])
    except:
        return 0

# ---------- TRADES ----------
def get_trades():
    try:
        r = requests.get(f"{BASE_URL}/v3/trades/?book=btc_mxn&limit=100")
        df = pd.DataFrame(r.json()["payload"])
        df["price"] = df["price"].astype(float)
        return df
    except:
        return pd.DataFrame()

# ---------- RSI ----------
def calculate_rsi(series, period=14):

    delta = series.diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# ---------- ORDEN ----------
def crear_orden(side, amount):

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

# ---------- PANEL ----------
col1,col2,col3=st.columns(3)

precio=get_price()

df=get_trades()

if not df.empty:

    rsi=calculate_rsi(df["price"])
    rsi_actual=float(rsi.iloc[-1])

else:
    rsi_actual=0

col1.metric("BTC PRECIO",f"${precio:,.0f} MXN")
col2.metric("RSI",round(rsi_actual,2))
col3.metric("IA ACTIVA","SI" if st.session_state.auto_trading else "NO")

# ---------- BOTONES ----------
b1,b2,b3=st.columns(3)

if b1.button("🤖 Activar IA"):
    st.session_state.auto_trading=True

if b2.button("⛔ Detener IA"):
    st.session_state.auto_trading=False

if b3.button("🟢 Comprar $100 BTC"):
    r=crear_orden("buy",100)
    st.write(r)

# ---------- IA AUTOMATICA ----------
if st.session_state.auto_trading:

    st.success("IA OPERANDO")

    if rsi_actual<30:

        st.write("🟢 IA COMPRA BTC")
        crear_orden("buy",100)

    elif rsi_actual>70:

        st.write("🔴 IA VENDE BTC")
        crear_orden("sell",100)

    else:

        st.write("⏳ IA esperando señal")

else:

    st.warning("IA DESACTIVADA")

# ---------- REFRESH ----------
time.sleep(20)
st.rerun()
