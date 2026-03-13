import streamlit as st
import time
import hashlib
import hmac
import requests
import pandas as pd

# ---------------- CONFIG ----------------

st.set_page_config(
    page_title="SHARK SYSTEM v10",
    layout="wide"
)

# --------- API KEYS ---------

API_KEY = st.secrets.get("BITSO_API_KEY", "")
API_SECRET = st.secrets.get("BITSO_API_SECRET", "")

# --------- ESTILO NEON ---------

st.markdown("""
<style>

.stApp{
background-color:#040404;
color:#00d4ff;
}

.neon-box{
border:1px solid #bc13fe;
padding:20px;
border-radius:12px;
background:#111;
box-shadow:0 0 10px #bc13fe;
}

</style>
""", unsafe_allow_html=True)

# --------- FUNCION BITSO ---------

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

        r = requests.get(url, headers=headers, timeout=10)

        if r.status_code == 200:
            return r.json()

        return None

    except:
        return None


# --------- PRECIO ---------

def get_price(book):

    try:

        r = requests.get(
            f"https://api.bitso.com/v3/ticker/?book={book}",
            timeout=10
        ).json()

        return float(r["payload"]["last"])

    except:
        return 0


# --------- INTERFAZ ---------

st.title("🦈 SHARK SYSTEM v10")

st.write("Protocolo activo | Nodo conectado")

meta_suv = 1700000

col1, col2 = st.columns([1,2])

# --------- PANEL API ---------

with col1:

    st.subheader("📡 ESTADO DEL NODO")

    if API_KEY == "" or API_SECRET == "":

        st.error("Configura BITSO_API_KEY y BITSO_API_SECRET en Secrets")

        status_ok = False

    else:

        data = bitso_request("/v3/balance/")

        if data:

            st.success("🟢 Conectado a Bitso")

            balances = data["payload"]["balances"]

            status_ok = True

        else:

            st.error("🔴 No se pudo conectar a Bitso")

            status_ok = False


# --------- BALANCE ---------

with col2:

    st.subheader("🎯 META SUV $1.7M")

    saldo_total = 0
    tabla = []

    if status_ok:

        for b in balances:

            qty = float(b["total"])

            if qty > 0:

                coin = b["currency"].upper()

                if coin == "MXN":
                    price = 1
                else:
                    price = get_price(f"{coin.lower()}_mxn")

                valor = qty * price

                saldo_total += valor

                tabla.append({
                    "Moneda": coin,
                    "Cantidad": qty,
                    "Valor MXN": f"${valor:,.2f}"
                })

        df = pd.DataFrame(tabla)

        st.table(df)

        progreso = min(saldo_total/meta_suv,1)

        st.metric("Saldo Total",f"${saldo_total:,.2f} MXN")

        st.progress(progreso)

        faltante = meta_suv - saldo_total

        if faltante > 0:

            st.write(f"Faltan **${faltante:,.2f} MXN** para tu SUV")

        else:

            st.success("META ALCANZADA 🚀")

    else:

        st.warning("Esperando conexión con Bitso")


# --------- TICKERS ---------

st.divider()

st.subheader("📊 MERCADO")

c1,c2,c3 = st.columns(3)

btc = get_price("btc_mxn")
eth = get_price("eth_mxn")
usd = get_price("usd_mxn")

c1.metric("₿ BTC",f"${btc:,.0f} MXN")
c2.metric("Ξ ETH",f"${eth:,.0f} MXN")
c3.metric("💵 USD",f"${usd:,.2f} MXN")


# --------- REFRESH ---------

time.sleep(30)

st.rerun()
