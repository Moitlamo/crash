import streamlit as st
import random
import time

st.set_page_config(page_title="The Combi Race", page_icon="🚐", layout="wide")

# --- 1. Set up Session State (Memory) ---
if 'balance' not in st.session_state:
    st.session_state.balance = 1000.00 
if 'history' not in st.session_state:
    st.session_state.history = [] 
if 'balance_history' not in st.session_state:
    st.session_state.balance_history = [1000.00]
# NEW: Memory bank specifically for plotting the crash trend
if 'all_crashes' not in st.session_state:
    st.session_state.all_crashes = []

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Race")
st.markdown(f"### 💰 Current Balance: BWP {st.session_state.balance:.2f}")
st.divider()

# --- 2. Split the Layout ---
main_col, history_col = st.columns([3, 1])

# --- RIGHT COLUMN: Vertical History (Last 20) ---
with history_col:
    st.write("### ⏱️ Past 20 Crashes")
    if st.session_state.history:
        for crash in reversed(st.session_state.history):
            if crash >= 10.00:
                color = "#FFD700" 
            elif crash >= 2.00:
                color = "#4CAF50" 
            else:
                color = "#F44336" 
                
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        max_bet = float(st.session_state.balance) if st.session_state.balance > 0 else 1.0
        bet_amount = st.number_input("Bet Amount (BWP)", min_value=1.0, max_value=max_bet, value=10.0, step=1.0)

    with col2:
        auto_cashout = st.number_input("Target Multiplier (x)", min_value=1.01, value=2.00, step=0.1)

    if st.button("Start The Engine", use_container_width=True):
        if bet_amount > st.session_state.balance:
            st.error("Insufficient funds! Please refresh the page.")
        else:
            st.session_state.balance -= bet_amount
            crash = generate_crash_point()
            
            multiplier_display = st.empty()
            status_message = st.empty()
            
            current_multiplier = 1.00
            
            while current_multiplier < crash:
                multiplier_display.markdown(f"<h1 style='text-align: center; color: green; font-size: 70px;'>{current_multiplier:.2f}x</h1>", unsafe_allow_html=True)
                time.sleep(0.05) 
                current_multiplier += 0.05 + (current_multiplier * 0.01)
                
                if current_multiplier >= auto_cashout:
                    current_multiplier = auto_cashout
                    break 
                    
            if auto_cashout <= crash:
                winnings = bet_amount * auto_cashout
                st.session_state.balance += winnings 
                
                multiplier_display.markdown(f"<h1 style='text-align: center; color: #FFD700; font-size: 70px;'>Cashed out at {auto_cashout:.2f}x!</h1>", unsafe_allow_html=True)
                status_message.success(f"🎉 You won! Payout: BWP {winnings:.2f}. The Combi eventually crashed at {crash}x.")
            else:
                multiplier_display.markdown(f"<h1 style='text-align: center; color: red; font-size: 70px;'>💥 CRASHED AT {crash}x 💥</h1>", unsafe_allow_html=True)
                status_message.error(f"💀 You lost BWP {bet_amount:.2f}. The Combi crashed early.")
            
            # --- Update Memories ---
            st.session_state.history.append(crash)
            st.session_state.history = st.session_state.history[-20:]
            
            st.session_state.balance_history.append(st.session_state.balance)
            
            # NEW: Add the crash point to our long-term chart history
            st.session_state.all_crashes.append(crash)
            
            time.sleep(2) 
            st.rerun() 

st.divider()

# --- 3. The Analytics Section ---
st.write("### 📈 Performance & Market Analytics")

# Create two columns side-by-side for our charts
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.write("**Crash Multiplier Trend**")
    st.write("Analyze the volatility of past rounds.")
    if st.session_state.all_crashes:
        # Plot the crash history
        st.line_chart(st.session_state.all_crashes)
    else:
        st.write("Play a round to generate chart data.")

with chart_col2:
    st.write("**Account Bankroll (BWP)**")
    st.write("Track your profit and loss curve.")
    # Plot the bankroll history
    st.line_chart(st.session_state.balance_history)
