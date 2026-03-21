import streamlit as st
import requests
import time
import hmac, hashlib, numpy as np
from datetime import datetime

# --- 1. IDENTIDAD ---
NOMBRE_USUARIO = "Angel"
LISTA_ACTIVOS = ["btc_mxn", "nvda_mxn", "googl_mxn"]
API_KEY = st.secrets.get("BITSO_KEY")
API_SECRET = st.secrets.get("BITSO_SECRET")
MODO_REAL = True if API_KEY and API_SECRET else False

# --- 2. MOTOR DE EJECUCIÓN (GATILLO) ---
def ejecutar_orden(side, libro, monto_nominal):
    if not MODO_REAL: return "SIMULACIÓN: Orden de " + side
    try:
        nonce = str(int(time.time() * 1000))
        endpoint = "/v3/orders/"
        # Para vender usamos 'major' (la cripto/acción) y para comprar 'nominal' (pesos)
        cuerpo = f'{{"book": "{libro}", "side": "{side}", "type": "market", "nominal": "{monto_nominal}"}}'
        mensaje = nonce + "POST" + endpoint + cuerpo
        firma = hmac.new(API_SECRET.encode(), mensaje.encode(), hashlib.sha256).hexdigest()
        headers = {'Authorization': f'Bitso {API_KEY}:{nonce}:{firma}', 'Content-Type': 'application/json'}
        r = requests.post(f"https://api.bitso.com{endpoint}", headers=headers, data=cuerpo).json()
        return r
    except Exception as e: return str(e)

# --- 3. LÓGICA DE LA IA (DECISIÓN SOLA) ---
def cerebro_mahora(precio_actual, rsi, activo):
    # LÓGICA DE COMPRA (Barato)
    if rsi < 30:
        res = ejecutar_orden("buy", activo, "20.00") # Compra $20 MXN
        return f"🟢 COMPRA AUTOMÁTICA: {res}"
    
    # LÓGICA DE VENTA (Caro / Ganancia)
    elif rsi > 70:
        # Aquí vendería lo que tengas acumulado de ese activo
        # Nota: Para vender necesitas especificar cuánto de la moneda tienes
        return "🔴 ZONA DE VENTA: Precio alto, detectando ganancias..."
    
    return "😴 ESPERANDO OPORTUNIDAD..."

# --- 4. INTERFAZ PRESTIGE ---
st.title(f"⛩️ {NOMBRE_USUARIO.upper()} - AUTO-PILOT ON")

# Simulamos el escaneo de todos tus activos
for activo in LISTA_ACTIVOS:
    # 1. Obtener precio real
    try:
        data = requests.get(f"https://api.bitso.com/v3/ticker/?book={activo}").json()['payload']
        precio = float(data['last'])
        rsi_simulado = np.random.randint(25, 75) # Aquí iría el cálculo real del RSI
        
        # 2. La IA decide y ejecuta SOLA
        decision = cerebro_mahora(precio, rsi_simulado, activo)
        
        # 3. Mostrar en pantalla con estilo
        col1, col2, col3 = st.columns([1, 1, 2])
        col1.metric(activo.upper(), f"${precio:,.2f}")
        col2.metric("RSI", rsi_simulado)
        col3.write(f"🤖 **Log:** {decision}")
    except:
        st.error(f"Error conectando con {activo}")

# --- 5. REFRESCO AUTOMÁTICO (EL CORAZÓN DEL BOT) ---
# Esto hace que el bot se "despierte" cada 30 segundos, vea el precio y decida si compra o vende
st.write("---")
st.caption("Refrescando sistema en 30 segundos... La IA nunca duerme.")
time.sleep(30)
st.rerun()
