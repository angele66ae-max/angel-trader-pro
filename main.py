# --- MÓDULO DE FUEGO: EJECUCIÓN REAL ---
def ejecutar_panico_real(monto_btc):
    if not MODO_REAL:
        return "Simulación: Venta de emergencia activada."
    
    try:
        nonce = str(int(time.time() * 1000))
        path = "/v3/orders/"
        # Vende todo tu BTC al precio de mercado para rescatar tus pesos
        payload = f'{{"book":"btc_mxn","side":"sell","type":"market","major":"{monto_btc}"}}'
        
        mensaje = nonce + "POST" + path + payload
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}'}
        
        r = requests.post(f"https://api.bitso.com{path}", headers=headers, data=payload).json()
        return r
    except Exception as e:
        return f"Falla en el sistema: {str(e)}"
