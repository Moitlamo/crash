import streamlit as st
import random
import time

# I added layout="wide" so the columns have plenty of room to breathe!
st.set_page_config(page_title="The Combi Race", page_icon="🚐", layout="wide")

# --- 1. Set up Session State (Memory) ---
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.00 
if 'history' not in st.session_state:
    st.session_state.history = [] 

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Race")
st.markdown(f"### 💰 Current Balance: BWP {st.session_state.balance:.2f}")
st.divider()

# --- 2. Split the Layout into Left (Game) and Right (History) Columns ---
# [3, 1] means the left column is 3 times wider than the right column
main_col, history_col = st.columns([3, 1])

# --- RIGHT COLUMN: Vertical History ---
with history_col:
    st.write("### ⏱️ Past Crashes")
    if st.session_state.history:
        # Loop through the history and stack them
        for crash in reversed(st.session_state.history):
            if crash >= 10.00:
                color = "#FFD700" 
            elif crash >= 2.00:
                color = "#4CAF50" 
            else:
                color = "#F44336" 
                
            # By using a <div> with margin-bottom, these perfectly stack on top of each other
            st.markdown(
                f"<div style='background-color: {color}; color: white; padding: 8px; "
                f"border-radius: 6px; margin-bottom: 8px; text-align: center; "
                f"font-weight: bold; font-size: 18px; box-shadow: 1px 1px 3px rgba(0,0,0,0.2);'>"
                f"{crash}x</div>", 
                unsafe_allow_html=True
            )
    else:
        st.write("No rounds played yet.")

# --- LEFT COLUMN: Main Game Engine ---
with main_col:
    st.write("Set your target multiplier and see if the combi makes it!")
    
    # Input Fields (Nested inside the main column)
    col1, col2 = st.columns(2)
    
    with col1:
        max_bet = float(st.session_state.balance) if st.session_state.balance > 0 else 1.0
        bet_amount = st.number_input("Bet Amount (BWP)", min_value=1.0, max_value=max_bet, value=10.0, step=1.0)

    with col2:
        auto_cashout = st.number_input("Target Multiplier (x)", min_value=1.01, value=2.00, step=0.1)

    # Game Logic
    if st.button("Start The Engine", use_container_width=True):
        if bet_amount > st.session_state.balance:
            st.error("Insufficient funds! Please refresh the page.")
        else:
            st.session_state.balance -= bet_amount
            crash = generate_crash_point()
            
            # Placeholders
            multiplier_display = st.empty()
            status_message = st.empty()
            
            current_multiplier = 1.00
            
            while current_multiplier < crash:
                # Increased the font size slightly so it stands out in the wider column
                multiplier_display.markdown(f"<h1 style='text-align: center; color: green; font-size: 70px;'>{current_multiplier:.2f}x</h1>", unsafe_allow_html=True)
                time.sleep(0.05) 
                current_multiplier += 0.05 + (current_multiplier * 0.01)
                
                if current_multiplier >= auto_cashout:
                    current_multiplier = auto_cashout
                    break 
                    
            # Win/Loss Resolution
            if auto_cashout <= crash:
                winnings = bet_amount * auto_cashout
                st.session_state.balance += winnings 
                
                multiplier_display.markdown(f"<h1 style='text-align: center; color: #FFD700; font-size: 70px;'>Cashed out at {auto_cashout:.2f}x!</h1>", unsafe_allow_html=True)
                status_message.success(f"🎉 You won! Payout: BWP {winnings:.2f}. The Combi eventually crashed at {crash}x.")
            else:
                multiplier_display.markdown(f"<h1 style='text-align: center; color: red; font-size: 70px;'>💥 CRASHED AT {crash}x 💥</h1>", unsafe_allow_html=True)
                status_message.error(f"💀 You lost BWP {bet_amount:.2f}. The Combi crashed early.")
            
            # Update History
            st.session_state.history.append(crash)
            st.session_state.history = st.session_state.history[-20:]
            
            time.sleep(2) 
            st.rerun()
