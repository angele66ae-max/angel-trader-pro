import flet as ft
import time
import threading
import requests
import hashlib
import hmac
import os
from dotenv import load_dotenv

# Cargamos seguridad
load_dotenv()
API_KEY = os.getenv("BITSO_API_KEY")
API_SECRET = os.getenv("BITSO_API_SECRET")

class AngelTrader:
    def __init__(self):
        self.url_base = "https://api.bitso.com"

    def firmar_solicitud(self, metodo, endpoint, payload=""):
        nonce = str(int(time.time() * 1000))
        message = nonce + metodo + endpoint + payload
        signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
        return {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}", "Content-Type": "application/json"}

    def obtener_precio(self):
        try:
            r = requests.get(f"{self.url_base}/v3/ticker/?book=btc_mxn")
            return float(r.json()['payload']['last'])
        except: return None

    def comprar_btc(self, monto_mxn):
        endpoint = "/v3/orders/"
        payload = f'{{"book":"btc_mxn","side":"buy","type":"market","major":"{monto_mxn}"}}'
        headers = self.firmar_solicitud("POST", endpoint, payload)
        try:
            r = requests.post(f"{self.url_base}{endpoint}", data=payload, headers=headers)
            return r.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

def main(page: ft.Page):
    page.title = "ANGEL IA - TRADING BOT"
    page.bgcolor = "#000000"
    bot = AngelTrader()

    txt_precio = ft.Text("$0.00", size=45, weight="bold", color="#D4AF37")
    txt_log = ft.Text("Esperando órdenes...", color="white54")

    def ejecutar_compra(e):
        txt_log.value = "Ejecutando compra de $10 MXN..."
        page.update()
        res = bot.comprar_btc("10.00")
        if "payload" in res:
            txt_log.value = f"✅ Compra Exitosa! ID: {res['payload']['oid']}"
            txt_log.color = "green"
        else:
            txt_log.value = f"❌ Error: {res.get('errors', 'Desconocido')}"
            txt_log.color = "red"
        page.update()

    def loop_precio():
        while True:
            p = bot.obtener_precio()
            if p: txt_precio.value = f"${p:,.2f}"
            page.update()
            time.sleep(2)

    page.add(
        ft.Container(height=50),
        ft.Column([
            ft.Text("BITCOIN / MXN", size=15, color="white70"),
            txt_precio,
            ft.Divider(),
            # CAMBIO: Ahora usamos ft.Button en lugar de ft.ElevatedButton
            ft.Button("PROBAR COMPRA ($10 MXN)", on_click=ejecutar_compra, bgcolor="#00FFCC", color="black"),
            txt_log
        ], horizontal_alignment="center")
    )
    
    threading.Thread(target=loop_precio, daemon=True).start()

# CAMBIO: Ahora usamos ft.run() en lugar de ft.app()
if __name__ == "__main__":
    ft.run(main)
def motor_ia():
        precio_compra = 0
        en_operacion = False
        
        while True:
            p_actual = bot.obtener_precio()
            if p_actual:
                txt_precio.value = f"${p_actual:,.2f}"
                
                # --- LÓGICA DE TRADING ---
                if not en_operacion:
                    # Ejemplo: Si el precio baja de un umbral, COMPRA
                    # Por ahora lo dejamos manual con el botón, pero aquí
                    # programaremos la detección de "caídas" de precio.
                    txt_status.value = "🤖 IA: Analizando punto de entrada..."
                else:
                    # Si ya compró, calcula una ganancia del 0.5%
                    meta = precio_compra * 1.005
                    if p_actual >= meta:
                        txt_status.value = f"🚀 ¡META ALCANZADA! Vendiendo en ${p_actual:,.2f}"
                        # Aquí ejecutaría bot.vender_btc()
                
                page.update()
            time.sleep(2)
