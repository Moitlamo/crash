# 2. We write the Frontend (HTML + JavaScript) as a Python string
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
                // Notice we ONLY check if it crashed. We no longer care if you cashed out!
                if (crashed) return;
                
                currentMulti += 0.05 + (currentMulti * 0.01);
                
                if (currentMulti >= crashPoint) {{
                    // CRASH LOGIC
                    currentMulti = crashPoint;
                    crashed = true;
                    display.innerText = currentMulti.toFixed(2) + "x";
                    display.style.color = "#F44336"; // Turn Red
                    
                    // Final message changes depending on if you clicked the button earlier
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
                cashOutValue = currentMulti; // Lock in the exact number you clicked on
                
                // Update the status text, but leave the multiplier green so it keeps going!
                status.innerText = "🎉 Cashed Out at " + cashOutValue.toFixed(2) + "x! (Watching Combi...)";
                btn.disabled = true; // Gray out the button so you can't click twice
            }}
        </script>
    </body>
    </html>
    """
