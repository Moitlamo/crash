import streamlit as st
import random
import time

# Set up the page layout with a localized theme
st.set_page_config(page_title="The Combi Race", page_icon="🚐")

def generate_crash_point():
    """Generates the random crash multiplier."""
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Race")
st.write("Place your bet, set your target, and cash out before the combi crashes!")

# Create two columns for the input fields
col1, col2 = st.columns(2)

with col1:
    # Input for the bet amount
    bet_amount = st.number_input("Bet Amount (BWP)", min_value=1.0, value=10.0, step=1.0)

with col2:
    # Input for the target multiplier
    auto_cashout = st.number_input("Auto Cash Out (x)", min_value=1.01, value=2.00, step=0.1)

# Create a button to start the round
if st.button("Start The Engine"):
    crash = generate_crash_point()
    
    # Placeholders for the multiplier animation and the final result message
    multiplier_display = st.empty()
    status_message = st.empty()
    
    current_multiplier = 1.00
    
    # Loop to simulate the combi speeding up
    while current_multiplier < crash:
        multiplier_display.markdown(f"<h2 style='text-align: center; color: green;'>{current_multiplier:.2f}x</h2>", unsafe_allow_html=True)
        time.sleep(0.05) # Made it slightly faster for a smoother animation
        current_multiplier += 0.05 + (current_multiplier * 0.01)
        
        # Stop the animation early if the player hits their cash out target!
        if current_multiplier >= auto_cashout:
            current_multiplier = auto_cashout
            break 
            
    # --- Determine Win or Loss ---
    if auto_cashout <= crash:
        # WIN LOGIC
        winnings = bet_amount * auto_cashout
        profit = winnings - bet_amount
        multiplier_display.markdown(f"<h2 style='text-align: center; color: #FFD700;'>Cashed out at {auto_cashout:.2f}x!</h2>", unsafe_allow_html=True)
        status_message.success(f"🎉 You won! Payout: BWP {winnings:.2f} (Profit: BWP {profit:.2f}). The Combi eventually crashed at {crash}x.")
    else:
        # LOSS LOGIC
        multiplier_display.markdown(f"<h2 style='text-align: center; color: red;'>💥 CRASHED AT {crash}x 💥</h2>", unsafe_allow_html=True)
        status_message.error(f"💀 You lost BWP {bet_amount:.2f}. The Combi crashed before reaching your {auto_cashout}x target.")

st.divider()
