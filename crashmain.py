import streamlit as st
import streamlit.components.v1 as components
import random

st.set_page_config(page_title="The Combi Race", page_icon="🚐", layout="wide")

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Race (Real-Time Edition)")
st.write("Click the green CASH OUT button before the combi crashes!")
st.divider()

# 1. The Python Backend generates the secure crash point
if st.button("Start Next Round", use_container_width=True):
    crash_target = generate_crash_point()
    
    # 2. The Frontend (HTML + JavaScript) 
    # Notice how this is indented to line up exactly under 'crash_target'
    custom_game_ui = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; text-align: center; color: white; background-color: #0E1117; }}
            #multiplier {{ font-size: 80px; font-weight: bold; color: #4CAF50; margin-top: 20px; }}
            #status {{ font-size: 24px; margin-top: 10px; height: 30px; color: #FFD700; }}
            .btn {{ 
                background-color: #4CAF50; color: white; padding: 15px 32px; 
                text-align: center; font-size: 24px; font-weight: bold; border-radius: 8px;
                border: none; cursor: pointer; margin-top: 20px; width: 50%; box-shadow: 0px 4px 6px rgba(0,0,0,0.3);
            }}
            .btn:active {{ transform: scale(0.98); }}
            .btn:disabled {{ background-color: #555; cursor: not-allowed; }}
        </style>
    </head>
    <body>
        <div id="multiplier">1.00x</div>
        <div id="status">Speeding up...</div>
        <button id="cashout-btn" class="btn" onclick="cashOut()">CASH OUT NOW</button>

        <script>
            let currentMulti = 1.00;
            let crashed = false;
            let cashedOut = false;
            let cashOutValue = 0.00;
            
            // The Python variable is injected right here:
            let crashPoint = {crash_target}; 
            
            let display = document.getElementById("multiplier");
            let status = document.getElementById("status");
            let btn = document.getElementById("cashout-btn");

            // The animation loop
            let gameLoop = setInterval(() => {{
                if (crashed) return;
                
                currentMulti += 0.05 + (currentMulti * 0.01);
                
                if (currentMulti >= crashPoint) {{
                    // CRASH LOGIC
                    currentMulti = crashPoint;
                    crashed = true;
                    display.innerText = currentMulti.toFixed(2) + "x";
                    display.style.color = "#F44336"; // Turn Red
                    
                    if (cashedOut) {{
                        status.innerText = "💥 CRASHED! But you safely secured " + cashOutValue.toFixed(2) + "x.";
                    }} else {{
                        status.innerText = "💥 CRASHED! You were too late.";
                    }}
                    
                    btn.disabled = true;
                    clearInterval(gameLoop);
                }} else {{
                    display.innerText = currentMulti.toFixed(2) + "x";
                }}
            }}, 50);

            // The button click logic
            function cashOut() {{
                if (crashed || cashedOut) return;
                
                cashedOut = true;
                cashOutValue = currentMulti; 
                
                status.innerText = "🎉 Cashed Out at " + cashOutValue.toFixed(2) + "x! (Watching Combi...)";
                btn.disabled = true; 
            }}
        </script>
    </body>
    </html>
    """

    # 3. We use Streamlit Components to render our mini JavaScript game
    components.html(custom_game_ui, height=400)
