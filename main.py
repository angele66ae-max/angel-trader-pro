import streamlit as st
import time
import requests
import hashlib
import hmac
import pandas as pd
import plotly.graph_objects as go

# ---------- CONFIG ----------

st.set_page_config(
    page_title="SHARK AI v11",
    layout="wide"
)

# ---------- API ----------

API_KEY = st.secrets.get("BITSO_API_KEY", "")
API_SECRET = st.secrets.get("BITSO_API_SECRET", "")

# ---------- ESTILO ----------

st.markdown("""
<style>
.stApp{
background-color:#050505;
color:#00d4ff;
}
</style>
""", unsafe_allow_html=True)

# ---------- BITSO REQUEST ----------

def bitso_request(path):

    nonce = str(int(time.time()*1000))

    message = nonce + "GET" + path

    signature = hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Authorization": f"Bitso {API_KEY}:{nonce}:{signature}"
    }

    url = "https://api.bitso.com" + path

    try:

        r = requests.get(url, headers=headers)

        if r.status_code == 200:
            return r.json()

    except:
        pass

    return None

# ---------- PRECIO ----------

def get_price(book):

    try:

        r = requests.get(
            f"https://api.bitso.com/v3/ticker/?book={book}"
        ).json()

        return float(r["payload"]["last"])

    except:
        return 0

# ---------- OHLC ----------

def get_candles():

    url = "https://api.bitso.com/v3/trades/?book=btc_mxn&limit=100"

    r = requests.get(url).json()

    trades = r["payload"]

    df = pd.DataFrame(trades)

    df["price"] = df["price"].astype(float)

    df["date"] = pd.to_datetime(df["created_at"])

    df = df.sort_values("date")

    return df

# ---------- RSI ----------

def calculate_rsi(data, period=14):

    delta = data.diff()

    gain = delta.clip(lower=0)

    loss = -1*delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()

    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    rsi = 100 - (100/(1+rs))

    return rsi

# ---------- INTERFAZ ----------

st.title("🦈 SHARK AI v11")

meta = 1700000

col1, col2 = st.columns([1,2])

# ---------- BALANCE ----------

with col1:

    st.subheader("📡 BITSO NODE")

    if API_KEY == "" or API_SECRET == "":
        st.error("Configura tus secrets")

    else:

        data = bitso_request("/v3/balance/")

        if data:

            st.success("Conectado")

            balances = data["payload"]["balances"]

            total = 0
            tabla = []

            for b in balances:

                qty = float(b["total"])

                if qty > 0:

                    coin = b["currency"].upper()

                    price = 1 if coin=="MXN" else get_price(f"{coin.lower()}_mxn")

                    valor = qty * price

                    total += valor

                    tabla.append({
                        "Moneda": coin,
                        "Cantidad": qty,
                        "MXN": valor
                    })

            df = pd.DataFrame(tabla)

            st.table(df)

            progreso = min(total/meta,1)

            st.metric("Saldo Total",f"${total:,.2f}")

            st.progress(progreso)

        else:

            st.error("No se pudo conectar a Bitso")

# ---------- GRAFICO ----------

with col2:

    st.subheader("📈 BTC ANALYSIS")

    df = get_candles()

    rsi = calculate_rsi(df["price"])

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["date"],
            y=df["price"],
            mode="lines",
            name="BTC"
        )
    )

    st.plotly_chart(fig, use_container_width=True)

    rsi_actual = rsi.iloc[-1]

    st.metric("RSI",round(rsi_actual,2))

    if rsi_actual < 30:
        st.success("🟢 IA SIGNAL: COMPRA")

    elif rsi_actual > 70:
        st.error("🔴 IA SIGNAL: VENDE")

    else:
        st.warning("🟡 IA SIGNAL: ESPERA")

# ---------- TICKERS ----------

st.divider()

c1,c2,c3 = st.columns(3)

c1.metric("BTC",f"${get_price('btc_mxn'):,.0f} MXN")
c2.metric("ETH",f"${get_price('eth_mxn'):,.0f} MXN")
c3.metric("USD",f"${get_price('usd_mxn'):,.2f} MXN")

# ---------- REFRESH ----------

time.sleep(30)
st.rerun()
