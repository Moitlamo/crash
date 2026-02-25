import streamlit as st
import random
import time

# Set up the page layout
st.set_page_config(page_title="Crash Simulator", page_icon="🚀")

def generate_crash_point():
    """Generates the random crash multiplier."""
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

# The Web UI
st.title("🚀 Crash Game Engine")
st.write("Click the button below to simulate a round.")

# Create a button to start the game
if st.button("Start Round"):
    crash = generate_crash_point()
    
    # st.empty() creates a placeholder on the web page that we can update in real-time
    multiplier_display = st.empty()
    
    current_multiplier = 1.00
    
    # Loop to simulate the rising multiplier
    while current_multiplier < crash:
        # Update the placeholder with the current number
        multiplier_display.markdown(f"<h2 style='text-align: center; color: green;'>{current_multiplier:.2f}x</h2>", unsafe_allow_html=True)
        
        time.sleep(0.1) # Controls the speed of the counter
        current_multiplier += 0.05 + (current_multiplier * 0.01)
        
    # Once the loop finishes (it crashes), update the text to red
    multiplier_display.markdown(f"<h2 style='text-align: center; color: red;'>💥 CRASHED AT {crash}x 💥</h2>", unsafe_allow_html=True)

st.divider()
st.write("Ready to test your strategies without risking the bankroll.")
