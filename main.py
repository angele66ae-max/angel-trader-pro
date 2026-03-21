with c_side:
    ahora = datetime.now().strftime("%H:%M:%S")
    
    # --- LÓGICA DE INTELIGENCIA ARTIFICIAL (AUTO-PILOT) ---
    # Simulamos un RSI para la decisión (en el futuro esto será real)
    rsi_ia = 42 # Valor base
    status_ia = "ESCANEO QUANTUM"
    color_status = "#39FF14" # Verde Neón

    if rsi_ia < 35:
        status_ia = "⚠️ COMPRANDO (BARATO)"
        color_status = "#00f2ff" # Cian
        # enviar_orden("buy", activo_actual, "15.00") # <--- GATILLO DE COMPRA
    elif rsi_ia > 65:
        status_ia = "💰 VENDIENDO (GANANCIA)"
        color_status = "#ff00ff" # Magenta
        # enviar_orden("sell", activo_actual, "0.0001") # <--- GATILLO DE VENTA

    st.markdown(f"""
        <div style="background:rgba(255,0,255,0.1); border:1.5px solid #ff00ff; border-radius:10px; padding:15px;">
            <h4 style="color:#ff00ff; margin:0; font-size:16px;">🧠 CEREBRO MAHORA v8.5</h4>
            <div class="ia-terminal">
                [{ahora}] >> MODO: AUTO-PILOT ON<br>
                [{ahora}] >> ACTIVO: {activo_actual.upper()}<br>
                [{ahora}] >> STATUS: <span style="color:{color_status}">{status_ia}</span><br>
                <hr style="border-color:#333">
                >> PENSAMIENTO:<br>
                Angel, el Ferrari está en pista. Si detecto que {activo_actual.split('_')[0].upper()} sube, 
                venderé automáticamente para asegurar los pesos para Canadá 🇨🇦.
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    st.write("")
    # Selector de monto para cuando tú quieras disparar manualmente
    monto_op = st.number_input("Monto Manual MXN", min_value=10.0, value=20.0)
    
    col_buy, col_sell = st.columns(2)
    with col_buy:
        if st.button(f"🚀 COMPRAR", use_container_width=True):
            res = enviar_orden("buy", activo_actual, str(monto_op))
            st.toast(f"Compra: {res}")
    with col_sell:
        if st.button(f"💰 VENDER", use_container_width=True):
            # Para vender necesitas saldo en el activo, esto es manual por ahora
            st.toast("Calculando saldo para vender...")

# --- 7. CIERRE DEL MOTOR ---
time.sleep(20)
st.rerun()
