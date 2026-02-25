import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Sniper Strategy Analyzer", page_icon="🎯", layout="wide")

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🎯 The Sniper: Time-Session & Strategy Backtester")
st.write("Analyze market sessions and test 'Waiting' strategies to find your edge.")

# --- 1. Session Setup ---
st.subheader("1. Configure Market Session")
t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
with t_col2:
    end_time = st.time_input("End Time", value=datetime.strptime("11:00", "%H:%M").time())
with t_col3:
    rounds_per_min = st.slider("Rounds per min", 1, 5, 3)
with t_col4:
    drought_target = st.number_input("Target for Drought (x)", value=2.0, step=0.1)

start_dt = datetime.combine(datetime.today(), start_time)
end_dt = datetime.combine(datetime.today(), end_time)
if end_dt <= start_dt: end_dt += timedelta(days=1)

duration_minutes = (end_dt - start_dt).total_seconds() / 60
total_rounds = int(duration_minutes * rounds_per_min)

if 'session_df' not in st.session_state:
    st.session_state.session_df = pd.DataFrame()

if st.button("Generate Session Data", use_container_width=True):
    data = []
    current_time = start_dt
    for _ in range(total_rounds):
        crash = generate_crash_point()
        data.append({"Timestamp": current_time, "Time": current_time.strftime("%H:%M:%S"), "Crash": crash})
        current_time += timedelta(seconds=(60/rounds_per_min))
    st.session_state.session_df = pd.DataFrame(data)

# --- 2. Sniper Backtester ---
if not st.session_state.session_df.empty:
    st.divider()
    st.subheader("🧪 2. Sniper Backtest Settings")
    
    s_col1, s_col2, s_col3, s_col4 = st.columns(4)
    start_bal = s_col1.number_input("Starting Balance (BWP)", value=1000.0)
    base_bet = s_col2.number_input("Bet Amount (BWP)", value=10.0)
    sniper_target = s_col3.number_input("Cashout Target (x)", value=2.0)
    wait_rounds = s_col4.number_input("Wait for 'X' Blues first:", min_value=0, value=8, help="How many rounds under 2.0x must pass before you place your first bet?")

    if st.button("Run Sniper Backtest", type="primary", use_container_width=True):
        balance = start_bal
        balance_history = [balance]
        blue_streak = 0
        bets_placed = 0
        wins = 0
        
        for crash in st.session_state.session_df["Crash"]:
            # Logic: If we haven't reached our 'wait' yet, just observe
            if blue_streak < wait_rounds:
                if crash < 2.0:
                    blue_streak += 1
                else:
                    blue_streak = 0 # Reset if a green hits before our wait is over
                balance_history.append(balance)
                continue
            
            # If we are here, the 'Wait' condition is met. Place a bet!
            bets_placed += 1
            balance -= base_bet
            
            if crash >= sniper_target:
                balance += (base_bet * sniper_target)
                wins += 1
                blue_streak = 0 # Reset after a win
            else:
                # If we lose, we keep betting until a win or account blown
                # Alternatively, you could reset the wait here.
                pass
            
            balance_history.append(balance)
            if balance <= 0: break

        # --- Results ---
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Final Balance", f"BWP {balance:.2f}")
        res_col2.metric("Total Bets Placed", bets_placed)
        res_col3.metric("Win Rate on Entry", f"{(wins/bets_placed*100 if bets_placed > 0 else 0):.1f}%")

        st.line_chart(balance_history)
        st.info(f"By waiting for {wait_rounds} blues, you avoided thousands of potential losses, but you also sat out for most of the session. This is the 'Sniper' trade-off.")
