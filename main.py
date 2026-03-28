import streamlit as st
import time

def render_mahoraga_wheel(factor=32, speed=10):
    # Definición de colores según tu Design System
    cyan = "#00F2FF"
    purple = "#8A2BE2"
    
    # CSS dinámico para la rotación y el gradiente
    st.markdown(f"""
    <style>
        .wheel-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 20px;
            background: #0A0E14;
            border: 1px solid {cyan}33;
            border-radius: 4px;
        }}
        
        .outer-ring {{
            width: 180px;
            height: 180px;
            border-radius: 50%;
            border: 2px solid {purple};
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            box-shadow: 0 0 20px {purple}44;
            animation: spin {speed}s linear infinite;
        }}
        
        /* Segmentos Radiales (Los 8 radios de la rueda) */
        .spoke {{
            position: absolute;
            width: 2px;
            height: 90px;
            background: linear-gradient(to top, {cyan}, transparent);
            transform-origin: bottom center;
            bottom: 50%;
        }}
        
        .spoke:nth-child(1) {{ transform: rotate(0deg); }}
        .spoke:nth-child(2) {{ transform: rotate(45deg); }}
        .spoke:nth-child(3) {{ transform: rotate(90deg); }}
        .spoke:nth-child(4) {{ transform: rotate(135deg); }}
        .spoke:nth-child(5) {{ transform: rotate(180deg); }}
        .spoke:nth-child(6) {{ transform: rotate(225deg); }}
        .spoke:nth-child(7) {{ transform: rotate(270deg); }}
        .spoke:nth-child(8) {{ transform: rotate(315deg); }}

        .inner-hub {{
            width: 60px;
            height: 60px;
            background: #0A0E14;
            border: 2px solid {cyan};
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 2;
            box-shadow: inset 0 0 10px {cyan};
        }}

        .rudder-icon {{
            font-size: 30px;
            color: {cyan};
            text-shadow: 0 0 10px {cyan};
        }}

        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to {{ transform: rotate(360deg); }}
        }}
        
        .factor-label {{
            margin-top: 15px;
            font-family: 'monospace';
            color: {cyan};
            font-size: 12px;
            letter-spacing: 2px;
        }}
    </style>
    
    <div class="wheel-container">
        <div class="outer-ring">
            <div class="spoke"></div><div class="spoke"></div>
            <div class="spoke"></div><div class="spoke"></div>
            <div class="spoke"></div><div class="spoke"></div>
            <div class="spoke"></div><div class="spoke"></div>
            <div class="inner-hub">
                <span class="rudder-icon">☸</span>
            </div>
        </div>
        <div class="factor-label">ADAPTATION FACTOR: {factor}</div>
    </div>
    """, unsafe_allow_html=True)

# Ejecución de prueba
render_mahoraga_wheel(factor=32, speed=5)
