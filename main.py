import requests

# Función para comprar acciones SIN librerías pesadas
def comprar_bolsa_directo(symbol, monto_usd):
    url = "https://api.alpaca.markets/v2/orders"
    headers = {
        "APCA-API-KEY-ID": "AK2MF7RHHRDWLLX6R47FPZE32J",
        "APCA-API-SECRET-KEY": "4pDdU6jCS3zA7QB1aK4d68FTG6MobAgJnvh8vGTsMj47",
        "Content-Type": "application/json"
    }
    data = {
        "symbol": symbol,
        "notional": str(monto_usd), # Compra por dinero, no por acciones completas
        "side": "buy",
        "type": "market",
        "time_in_force": "day"
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()

# En tu botón de la interfaz:
if st.button(f"🚀 Ejecutar Compra Real de {stock_fav}"):
    resultado = comprar_bolsa_directo(stock_fav, 5) # Intenta comprar $5 USD
    st.write(resultado)
