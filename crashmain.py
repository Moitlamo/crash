import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Frequency & Sniper Analyzer", page_icon="🎯", layout="wide")

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🎯 Frequency Distribution & Sniper Analyzer")
st.write("Understand the rarity of multipliers and test your entry strategies.")

# --- 1. Session Setup ---
st.subheader("1. Configure Market Session")
t_col1, t_col2, t_col3 = st.columns(3)

with t_col1:
    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
with t_col2:
    end_time = st.time_input("End Time", value=datetime.strptime("11:00", "%H:%M").time())
with t_col3:
    rounds_per_min = st.slider("Rounds per min", 1, 5, 3)

start_dt = datetime.combine(datetime.today(), start_time)
end_dt = datetime.combine(datetime.today(), end_time)
if end_dt <= start_dt: end_dt += timedelta(days=1)

if 'session_df' not in st.session_state:
    st.session_state.session_df = pd.DataFrame()

if st.button("Generate Session & Analyze Frequency", use_container_width=True):
    data = []
    current_time = start_dt
    duration_minutes = (end_dt - start_dt).total_seconds() / 60
    total_rounds = int(duration_minutes * rounds_per_min)
    
    for _ in range(total_rounds):
        crash = generate_crash_point()
        data.append({"Time": current_time.strftime("%H:%M:%S"), "Crash": crash})
        current_time += timedelta(seconds=(60/rounds_per_min))
    st.session_state.session_df = pd.DataFrame(data)

# --- 2. Frequency Table & Histogram ---
if not st.session_state.session_df.empty:
    df = st.session_state.session_df
    st.divider()
    st.subheader("📊 Multiplier Frequency Distribution")
    
    # Categorize the data
    bins = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 1000]
    labels = ["1x-2x", "2x-3x", "3x-4x", "4x-5x", "5x-6x", "6x-7x", "7x-8x", "8x-9x", "9x-10x", "10x+"]
    df['Range'] = pd.cut(df['Crash'], bins=bins, labels=labels, right=False)
    freq_counts = df['Range'].value_counts().reindex(labels).reset_index()
    freq_counts.columns = ['Multiplier Range', 'Occurrences']

    col_chart, col_table = st.columns([2, 1])
    
    with col_chart:
        st.write("**Occurrences per Range**")
        st.bar_chart(freq_counts.set_index('Multiplier Range'))
        
    with col_table:
        st.write("**Detailed Frequency Count**")
        st.table(freq_counts)
        st.info("Notice how the '9x-10x' range is significantly smaller than the '1x-2x' range.")

# --- 3. Sniper Backtester ---
    st.divider()
    st.subheader("🧪 3. Sniper Strategy Test")
    s_col1, s_col2, s_col3 = st.columns(3)
    base_bet = s_col1.number_input("Bet (BWP)", value=10.0)
    sniper_target = s_col2.number_input("Cashout Target (x)", value=2.0)
    wait_rounds = s_col3.number_input("Wait for 'X' Blues first:", value=8)

    if st.button("Run Sniper Test"):
        balance = 1000.0
        balance_history = [balance]
        blue_streak = 0
        
        for crash in df["Crash"]:
            if blue_streak < wait_rounds:
                if crash < 2.0: blue_streak += 1
                else: blue_streak = 0
            else:
                balance -= base_bet
                if crash >= sniper_target:
                    balance += (base_bet * sniper_target)
                    blue_streak = 0
                else: pass
            balance_history.append(balance)
            
        st.metric("Final Balance", f"BWP {balance:.2f}")
        st.line_chart(balance_history)
