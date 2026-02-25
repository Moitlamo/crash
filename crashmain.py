import streamlit as st
import random
import time

st.set_page_config(page_title="The Combi Race", page_icon="🚐")

# --- 1. Set up Session State (Memory) ---
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.00 
if 'history' not in st.session_state:
    st.session_state.history = [] # Creates an empty list to store past crashes

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Race")
st.write("Set your target multiplier and see if the combi makes it!")

# Display the player's current balance
st.markdown(f"### 💰 Current Balance: BWP {st.session_state.balance:.2f}")

# --- 2. Display the Crash History ---
if st.session_state.history:
    st.write("**Past Crashes:**")
    history_html = ""
    
    # We use reversed() so the absolute newest crash shows up on the far left
    for crash in reversed(st.session_state.history):
        # Color coding the badges based on how high the combi went
        if crash >= 10.00:
            color = "#FFD700" # Gold for massive crashes
        elif crash >= 2.00:
            color = "#4CAF50" # Green for safe/moderate crashes
        else:
            color = "#F44336" # Red for early crashes (under 2x)
            
        # This creates the visual "pills" or badges for the numbers
        history_html += f"<span style='background-color: {color}; color: white; padding: 4px 8px; border-radius: 4px; margin-right: 5px; font-weight: bold;'>{crash}x</span>"
        
    st.markdown(history_html, unsafe_allow_html=True)
    st.write("") # Just adds a little bit of spacing below the history bar

# --- 3. Input Fields ---
col1, col2 = st.columns(2)

with col1:
    # Adding a safety check so the max bet doesn't break if balance hits 0
    max_bet = float(st.session_state.balance) if st.session_state.balance > 0 else 1.0
    bet_amount = st.number_input("Bet Amount (BWP)", min_value=1.0, max_value=max_bet, value=10.0, step=1.0)

with col2:
    auto_cashout = st.number_input("Target Multiplier (x)", min_value=1.01, value=2.00, step=0.1)

# --- 4. Game Logic ---
if st.button("Start The Engine"):
    if bet_amount > st.session_state.balance:
        st.error("Insufficient funds! Please refresh the page to restart your bankroll.")
    else:
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
            st.session_state.balance += winnings 
            
            multiplier_display.markdown(f"<h2 style='text-align: center; color: #FFD700;'>Cashed out at {auto_cashout:.2f}x!</h2>", unsafe_allow_html=True)
            status_message.success(f"🎉 You won! Payout: BWP {winnings:.2f}. The Combi eventually crashed at {crash}x.")
        else:
            multiplier_display.markdown(f"<h2 style='text-align: center; color: red;'>💥 CRASHED AT {crash}x 💥</h2>", unsafe_allow_html=True)
            status_message.error(f"💀 You lost BWP {bet_amount:.2f}. The Combi crashed early.")
        
        # --- Update the History ---
        # Add the final crash point to our memory bank
        st.session_state.history.append(crash)
        
        # Slice the list to ensure we ONLY keep the last 20 records
        st.session_state.history = st.session_state.history[-20:]
        
        time.sleep(2) 
        st.rerun() 

st.divider()
