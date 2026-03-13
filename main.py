import time
import requests
import hashlib
import hmac
import json
import pandas as pd

# --- API KEYS ---
API_KEY = "TU_API_KEY"
API_SECRET = "TU_API_SECRET"

BASE_URL = "https://api.bitso.com"

# ---------- PRECIOS ----------
def get_price(book="btc_mxn"):
    r = requests.get(f"{BASE_URL}/v3/ticker/?book={book}")
    data = r.json()
    return float(data["payload"]["last"])

# ---------- HISTORIAL ----------
def get_trades():
    r = requests.get(f"{BASE_URL}/v3/trades/?book=btc_mxn&limit=100")
    trades = r.json()["payload"]
    df = pd.DataFrame(trades)
    df["price"] = df["price"].astype(float)
    return df

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
def crear_orden(side, amount_mxn):

    path = "/v3/orders"
    nonce = str(int(time.time()*1000))

    order = {
        "book": "btc_mxn",
        "side": side,
        "type": "market",
        "major": amount_mxn
    }

    body = json.dumps(order)

    message = nonce + "POST" + path + body

    signature = hmac.new(
        API_SECRET.encode(),
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    headers = {
        "Authorization": f"Bitso {API_KEY}:{nonce}:{signature}",
        "Content-Type": "application/json"
    }

    r = requests.post(
        BASE_URL + path,
        headers=headers,
        data=body
    )

    return r.json()

# ---------- LOOP PRINCIPAL ----------

while True:

    print("Analizando mercado...")

    df = get_trades()

    rsi = calculate_rsi(df["price"])
    rsi_actual = rsi.iloc[-1]

    precio = get_price()

    print("Precio BTC:", precio)
    print("RSI:", rsi_actual)

    if rsi_actual < 30:

        print("🟢 COMPRA AUTOMÁTICA")
        respuesta = crear_orden("buy", 100)   # compra 100 MXN
        print(respuesta)

    elif rsi_actual > 70:

        print("🔴 VENTA AUTOMÁTICA")
        respuesta = crear_orden("sell", 100)
        print(respuesta)

    else:

        print("⏳ Esperando señal...")

    time.sleep(60)
