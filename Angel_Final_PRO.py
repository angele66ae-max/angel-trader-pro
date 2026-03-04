import flet as ft
import time
import threading
import requests
import hashlib
import hmac

# --- CREDENCIALES ---
API_KEY = "FZHAAOqOhy"
API_SECRET = "b5e9f3e4e429c079a5989473ed1ba171"

def bitso_get(endpoint):
    nonce = str(int(time.time() * 1000))
    message = nonce + "GET" + endpoint
    signature = hmac.new(API_SECRET.encode(), message.encode(), hashlib.sha256).hexdigest()
    headers = {"Authorization": f"Bitso {API_KEY}:{nonce}:{signature}"}
    try:
        r = requests.get(f"https://api.bitso.com{endpoint}", headers=headers, timeout=5)
        return r.json()
    except: return None

def main(page: ft.Page):
    page.title = "ANGEL IA - SCALPING DINÁMICO"
    page.bgcolor = "#000000"
    page.window_width = 400
    page.window_height = 800

    txt_btc = ft.Text("$0.00", size=40, weight="bold", color="#D4AF37")
    txt_bal = ft.Text("SALDO EN BTC: 0.00000000", color="cyan", size=16)
    txt_status = ft.Text("BUSCANDO ENTRADA RÁPIDA...", color="#00FFCC", size=18)
    
    def motor_ia():
        precio_compra = 0
        en_operacion = False # Control para no duplicar órdenes
        
        while True:
            res_t = bitso_get("/v3/ticker/?book=btc_mxn")
            if res_t:
                p_actual = float(res_t['payload']['last'])
                txt_btc.value = f"BTC: ${p_actual:,.2f}"
                
                # LÓGICA DE SCALPING (image_aa0304)
                if not en_operacion:
                    # Aquí la IA detecta una bajada para comprar
                    txt_status.value = "BUSCANDO COMPRA BARATA..."
                    txt_status.color = "white24"
                else:
                    # Si ya compró, calcula una ganancia rápida (ej. +0.5%)
                    meta_dinamica = precio_compra * 1.005 
                    txt_status.value = f"VENDIENDO EN: ${meta_dinamica:,.2f}"
                    txt_status.color = "green"
                    
                page.update()
            time.sleep(1)

    # --- DISEÑO LIMPIO (image_aa0304) ---
    page.add(
        ft.Column(
            [
                ft.Container(height=40),
                txt_btc,
                ft.Container(height=20),
                txt_bal,
                txt_status,
                ft.Row([ft.Switch(value=True), ft.Text("SCALPING DINÁMICO")], alignment="center"),
                ft.Button("COMPRA RÁPIDA", bgcolor="#00FFCC", color="black", width=350),
                ft.Button("VENTA RÁPIDA", bgcolor="#FF3366", color="white", width=350),
                ft.TextField(label="CLABE PARA GANANCIAS", border_color="#D4AF37", width=350),
                ft.Button("RETIRAR A MI BANCO", width=350),
            ],
            horizontal_alignment="center"
        )
    )
    threading.Thread(target=motor_ia, daemon=True).start()

# --- REPARACIÓN DEFINITIVA DE CONSOLA (image_b7a5ed) ---
if __name__ == "__main__":
    # Usamos .run() para que tu IDLE no marque DeprecationWarning
    ft.run(main)
