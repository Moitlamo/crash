import streamlit as st
import random
import time

st.set_page_config(page_title="The Combi Race", page_icon="🚐")

# --- 1. Set up the Bankroll using Session State ---
# This ensures the balance doesn't reset to 1000 every time the page refreshes
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.00 

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Race")
st.write("Set your target multiplier and see if the combi makes it!")

# Display the player's current balance
st.markdown(f"### 💰 Current Balance: BWP {st.session_state.balance:.2f}")

# --- 2. Input Fields ---
col1, col2 = st.columns(2)

with col1:
    # Max bet is tied to their current balance
    bet_amount = st.number_input("Bet Amount (BWP)", min_value=1.0, max_value=float(st.session_state.balance), value=10.0, step=1.0)

with col2:
    auto_cashout = st.number_input("Target Multiplier (x)", min_value=1.01, value=2.00, step=0.1)

# --- 3. Game Logic ---
if st.button("Start The Engine"):
    if bet_amount > st.session_state.balance:
        st.error("Insufficient funds!")
    else:
        # Deduct the bet right when the round starts
        st.session_state.balance -= bet_amount
        
        crash = generate_crash_point()
        
        multiplier_display = st.empty()
        status_message = st.empty()
        
        current_multiplier = 1.00
        
        while current_multiplier < crash:
            multiplier_display.markdown(f"<h2 style='text-align: center; color: green;'>{current_multiplier:.2f}x</h2>", unsafe_allow_html=True)
            time.sleep(0.05) 
            current_multiplier += 0.05 + (current_multiplier * 0.01)
            
            if current_multiplier >= auto_cashout:
                current_multiplier = auto_cashout
                break 
                
        # --- Win/Loss Resolution ---
        if auto_cashout <= crash:
            winnings = bet_amount * auto_cashout
            profit = winnings - bet_amount
            # Add the original bet + profit back to the balance
            st.session_state.balance += winnings 
            
            multiplier_display.markdown(f"<h2 style='text-align: center; color: #FFD700;'>Cashed out at {auto_cashout:.2f}x!</h2>", unsafe_allow_html=True)
            status_message.success(f"🎉 You won! Payout: BWP {winnings:.2f}. The Combi eventually crashed at {crash}x.")
        else:
            multiplier_display.markdown(f"<h2 style='text-align: center; color: red;'>💥 CRASHED AT {crash}x 💥</h2>", unsafe_allow_html=True)
            status_message.error(f"💀 You lost BWP {bet_amount:.2f}. The Combi crashed early.")
        
        # We use st.rerun() to refresh the page so the new Account Balance shows up immediately at the top
        time.sleep(2) # Give the user 2 seconds to read the result before refreshing
        st.rerun() 

st.divider()
