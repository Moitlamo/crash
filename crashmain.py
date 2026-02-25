import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Algorithm Analyzer", page_icon="📊", layout="wide")

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("📊 Crash Pattern & Strategy Analyzer")
st.write("Simulate thousands of rounds instantly and test your risk management strategies.")

# --- 1. Generate Market Data ---
st.subheader("1. Generate Market History")
col1, col2 = st.columns(2)
with col1:
    total_rounds = st.number_input("Number of rounds to simulate:", min_value=100, max_value=1000000, value=10000, step=1000)
with col2:
    target_multiplier = st.number_input("Target Multiplier to Analyze (e.g., 3.00):", min_value=1.01, value=3.00, step=0.10)

# We use session state to save the market history so the backtester can use it
if 'market_history' not in st.session_state:
    st.session_state.market_history = []

if st.button("Generate & Analyze Tick Data", use_container_width=True):
    with st.spinner(f"Generating {total_rounds} rounds..."):
        st.session_state.market_history = [generate_crash_point() for _ in range(total_rounds)]
        
        market_history = st.session_state.market_history
        crashes_under_2 = sum(1 for x in market_history if x < 2.00)
        crashes_over_2 = sum(1 for x in market_history if x >= 2.00)
        
        max_red_streak = 0
        current_streak = 0
        for tick in market_history:
            if tick < 2.00:
                current_streak += 1
                if current_streak > max_red_streak:
                    max_red_streak = current_streak
            else:
                current_streak = 0

        st.divider()
        st.success("✅ Market Data Generated!")
        st.write(f"**Win Rate (≥2.00x):** {(crashes_over_2 / total_rounds) * 100:.2f}% | **Longest Red Streak:** {max_red_streak} rounds")


# --- 2. The Strategy Backtester ---
st.divider()
st.subheader("🧪 2. Strategy Backtester")
st.write("Run a betting system through the generated history to see your Profit & Loss (P&L) curve.")

if not st.session_state.market_history:
    st.warning("⚠️ Please click 'Generate & Analyze Tick Data' above before running a backtest.")
else:
    bt_col1, bt_col2, bt_col3, bt_col4 = st.columns(4)
    starting_balance = bt_col1.number_input("Starting Balance (BWP)", value=1000.0, step=100.0)
    base_bet = bt_col2.number_input("Base Bet (BWP)", value=10.0, step=1.0)
    bt_target = bt_col3.number_input("Auto-Cashout Target", value=2.00, step=0.10)
    loss_multiplier = bt_col4.number_input("Bet Multiplier on Loss", value=1.0, step=0.1, help="1.0 = Flat bet. 2.0 = Double bet after loss (Martingale).")

    if st.button("Run Strategy Backtest", type="primary", use_container_width=True):
        balance = starting_balance
        current_bet = base_bet
        balance_history = [balance]
        busted_round = -1

        # The Backtest Engine
        for i, tick in enumerate(st.session_state.market_history):
            if balance <= 0:
                busted_round = i
                break # Account blown, stop trading
            
            # You can't bet more money than you have in your account
            actual_bet = min(current_bet, balance)
            balance -= actual_bet
            
            if tick >= bt_target:
                # WIN: Add profits and reset the bet size to normal
                balance += actual_bet * bt_target
                current_bet = base_bet 
            else:
                # LOSS: Multiply the next bet based on your risk rules
                current_bet = current_bet * loss_multiplier
                
            balance_history.append(balance)

        # --- Show Backtest Results ---
        st.write("### 📈 P&L Equity Curve")
        
        # Draw the chart
        chart_data = pd.DataFrame(balance_history, columns=["Account Balance (BWP)"])
        st.line_chart(chart_data)
        
        # Show final metrics
        final_balance = balance_history[-1]
        peak_balance = max(balance_history)
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Ending Balance", f"BWP {final_balance:.2f}", f"{final_balance - starting_balance:.2f}")
        res_col2.metric("Peak Balance (Highest Point)", f"BWP {peak_balance:.2f}")
        
        if busted_round != -1:
            res_col3.metric("Status", "💀 LIQUIDATED")
            st.error(f"**Margin Call:** Your account was completely wiped out on round **{busted_round}**.")
            st.write("This usually happens when a long 'red streak' forces your bet size higher than your available margin.")
        else:
            res_col3.metric("Status", "✅ SURVIVED")
