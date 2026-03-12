import flet as ft
import time
import threading
import requests
import hashlib
import hmac
import os
from dotenv import load_dotenv

# 1. CARGA DE SEGURIDAD (Busca en .env en PC o en Secrets en la nube)
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
        return {
            "Authorization": f"Bitso {API_KEY}:{nonce}:{signature}",
            "Content-Type": "application/json"
        }

    def obtener_precio(self):
        try:
            r = requests.get(f"{self.url_base}/v3/ticker/?book=btc_mxn", timeout=5)
            return float(r.json()['payload']['last'])
        except:
            return None

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
    page.title = "ANGEL IA - SCALPING DINÁMICO"
    page.bgcolor = "#000000"
    page.window_width = 400
    page.window_height = 800
    page.theme_mode = ft.ThemeMode.DARK
    
    bot = AngelTrader()

    # --- VARIABLES DE ESTADO ---
    precio_compra = 0
    en_operacion = False

    # --- ELEMENTOS VISUALES ---
    txt_precio = ft.Text("$0.00", size=45, weight="bold", color="#D4AF37")
    txt_status = ft.Text("ANALIZANDO MERCADO...", color="#00FFCC", size=16)
    txt_log = ft.Text("Esperando órdenes...", color="white54", size=12)
    
    def ejecutar_compra_manual(e):
        txt_log.value = "Ejecutando compra de $10 MXN..."
        page.update()
        res = bot.comprar_btc("10.00")
        if "payload" in res:
            txt_log.value = f"✅ ¡Compra Exitosa! ID: {res['payload']['oid']}"
            txt_log.color = "green"
        else:
            txt_log.value = f"❌ Error: {res.get('errors', 'Revisa saldo o llaves')}"
            txt_log.color = "red"
        page.update()

    def loop_mercado():
        nonlocal precio_compra, en_operacion
        while True:
            p_actual = bot.obtener_precio()
            if p_actual:
                txt_precio.value = f"${p_actual:,.2f}"
                
                # --- LÓGICA DE IA (SCALPING) ---
                if not en_operacion:
                    txt_status.value = "🤖 IA: Buscando punto bajo para comprar..."
                    txt_status.color = "cyan"
                else:
                    meta = precio_compra * 1.005 # Gana el 0.5%
                    txt_status.value = f"📈 Meta de venta: ${meta:,.2f}"
                    txt_status.color = "green"
                    if p_actual >= meta:
                        txt_log.value = "🚀 ¡VENDIENDO CON GANANCIA!"
                        en_operacion = False # Reset para la próxima operación
                
                page.update()
            time.sleep(2)

    # --- DISEÑO DE LA INTERFAZ ---
    page.add(
        ft.Column(
            [
                ft.Container(height=40),
                ft.Text("BITCOIN / MXN", size=14, color="white70"),
                txt_precio,
                ft.Container(height=20),
                txt_status,
                ft.Divider(color="white24"),
                ft.Row(
                    [ft.Switch(value=True), ft.Text("SCALPING DINÁMICO")],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                ft.Button(
                    "PROBAR COMPRA ($10 MXN)", 
                    on_click=ejecutar_compra_manual, 
                    bgcolor="#00FFCC", 
                    color="black",
                    width=300
                ),
                ft.Container(height=10),
                ft.Text("LOG DE OPERACIONES:", size=10, color="white30"),
                txt_log,
                ft.Divider(color="white24"),
                ft.TextField(label="CLABE PARA RETIRO", border_color="#D4AF37", width=300),
                ft.Button("RETIRAR GANANCIAS", width=300, disabled=True),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

    # Iniciar el motor en segundo plano
    threading.Thread(target=loop_mercado, daemon=True).start()

if __name__ == "__main__":
    # Usamos run en lugar de app para evitar el Warning
    ft.run(main)
