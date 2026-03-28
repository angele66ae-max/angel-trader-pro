# --- MEJORA DEL RADAR (Copia esto en la sección del gráfico) ---
with col_radar:
    st.markdown("### 📊 RADAR TÁCTICO")
    try:
        m_req = requests.get("https://api.bitso.com/v3/trades/?book=btc_mxn", timeout=10).json()
        if 'payload' in m_req:
            precios = [float(t['price']) for t in m_req['payload']][::-1]
            avg_price = sum(precios) / len(precios)
            
            fig = go.Figure()
            # Gráfico de área neón
            fig.add_trace(go.Scatter(y=precios, fill='tozeroy', name='BTC',
                         line=dict(color='#00f2ff', width=3),
                         fillcolor='rgba(0, 242, 255, 0.1)'))
            
            # Línea de Promedio (Soporte)
            fig.add_trace(go.Scatter(y=[avg_price]*len(precios), 
                         line=dict(color='rgba(255, 255, 255, 0.3)', dash='dash'),
                         name='Promedio'))

            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', height=400, 
                              margin=dict(l=0,r=0,t=0,b=0), xaxis_visible=False,
                              showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
