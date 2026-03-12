import requests
import time
from config import API_KEY, API_SECRET

def obtener_datos_btc():
    url = "https://api.bitso.com/v3/ticker/?book=btc_mxn"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            precio = float(data['payload']['last'])
            return precio
        else:
            print(f"Error: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

print("Iniciando la aplicación...")

while True:
    precio_actual = obtener_datos_btc()
    if precio_actual:
        print(f"¡Conexión exitosa! El precio actual de Bitcoin es: ${precio_actual:,.2f} MXN")
        # Aquí agregarías tu lógica de compra. Por ejemplo, puedes llamar a otra función que verifique si se cumplen tus condiciones y mande la orden.
    else:
        print("No se pudo obtener el precio. Reintentando...")
    time.sleep(10)  # Espera 10 segundos
