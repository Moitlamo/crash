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
    # Core Strategy Inputs
    bt_col1, bt_col2, bt_col3, bt_col4 = st.columns(4)
    starting_balance = bt_col1.number_input("Starting Balance (BWP)", value=1000.0, step=100.0)
    base_bet = bt_col2.number_input("Base Bet (BWP)", value=10.0, step=1.0)
    bt_target = bt_col3.number_input("Auto-Cashout Target", value=2.00, step=0.10)
    loss_multiplier = bt_col4.number_input("Bet Multiplier on Loss", value=1.0, step=0.1, help="1.0 = Flat bet. 2.0 = Double bet (Martingale).")

    # Risk Management Inputs
    st.write("### 🛡️ Risk Management (The Hit & Run Rules)")
    rm_col1, rm_col2 = st.columns(2)
    # These strings are now much shorter so GitHub won't break them!
    take_profit = rm_col1.number_input("Take Profit Target (BWP):", value=1200.0, step=100.0)
    stop_loss = rm_col2.number_input("Hard Stop Loss (BWP):", value=500.0, step=100.0)

    if st.button("Run Strategy Backtest", type="primary", use_container_width=True):
        balance = starting_balance
        current_bet = base_bet
        balance_history = [balance]
        
        end_reason = "Completed All Rounds"
        end_round = total_rounds

        # The Backtest Engine
        for i, tick in enumerate(st.session_state.market_history):
            if balance <= 0:
                end_reason = "💀 LIQUIDATED (Account Blown)"
                end_round = i
                break
            if balance <= stop_loss:
                end_reason = "🛑 STOP LOSS HIT (Capital Preserved)"
                end_round = i
                break
            if balance >= take_profit:
                end_reason = "🎯 TAKE PROFIT HIT (Walked Away a Winner)"
                end_round = i
                break
            
            actual_bet = min(current_bet, balance)
            balance -= actual_bet
            
            if tick >= bt_target:
                balance += actual_bet * bt_target
                current_bet = base_bet 
            else:
                current_bet = current_bet * loss_multiplier
                
            balance_history.append(balance)

        # --- Show Backtest Results ---
        st.write("### 📈 P&L Equity Curve")
        
        chart_data = pd.DataFrame(balance_history, columns=["Account Balance (BWP)"])
        st.line_chart(chart_data)
        
        final_balance = balance_history[-1]
        peak_balance = max(balance_history)
        
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("Ending Balance", f"BWP {final_balance:.2f}", f"{final_balance - starting_balance:.2f}")
        res_col2.metric("Peak Balance", f"BWP {peak_balance:.2f}")
        
        if "TAKE PROFIT" in end_reason:
            res_col3.success(f"**Status:** {end_reason} at round {end_round}")
        elif "STOP LOSS" in end_reason:
            res_col3.warning(f"**Status:** {end_reason} at round {end_round}")
        elif "LIQUIDATED" in end_reason:
            res_col3.error(f"**Status:** {end_reason} at round {end_round}")
        else:
            res_col3.info(f"**Status:** {end_reason}")
