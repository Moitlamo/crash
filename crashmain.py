import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Time-Session Analyzer", page_icon="🕒", layout="wide")

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🕒 Time-Session Crash Analyzer")
st.write("Analyze how the algorithm performs during specific windows of time.")

# --- 1. Session Setup ---
st.subheader("1. Configure Simulation Window")
t_col1, t_col2, t_col3 = st.columns(3)

with t_col1:
    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
with t_col2:
    end_time = st.time_input("End Time", value=datetime.strptime("11:00", "%H:%M").time())
with t_col3:
    rounds_per_min = st.slider("Rounds per minute", 1, 5, 3)

# Calculate total rounds based on time difference
start_dt = datetime.combine(datetime.today(), start_time)
end_dt = datetime.combine(datetime.today(), end_time)

# Handle overnight sessions
if end_dt <= start_dt:
    end_dt += timedelta(days=1)

duration_minutes = (end_dt - start_dt).total_seconds() / 60
total_rounds = int(duration_minutes * rounds_per_min)

st.info(f"Setting up a session of **{duration_minutes:.0f} minutes**. This will generate **{total_rounds} rounds**.")

if 'time_history' not in st.session_state:
    st.session_state.time_history = pd.DataFrame()

if st.button("Run Time-Session Simulation", use_container_width=True):
    data = []
    current_time = start_dt
    
    with st.spinner("Simulating the session..."):
        for _ in range(total_rounds):
            crash = generate_crash_point()
            data.append({
                "Time": current_time.strftime("%H:%M:%S"),
                "Crash": crash,
                "Type": "Pink (10x+)" if crash >= 10 else ("Green (2x+)" if crash >= 2 else "Blue (<2x)")
            })
            # Advance clock by roughly X seconds per round
            current_time += timedelta(seconds=(60/rounds_per_min))
        
        st.session_state.time_history = pd.DataFrame(data)

# --- 2. Analytics Dashboard ---
if not st.session_state.time_history.empty:
    df = st.session_state.time_history
    
    st.divider()
    st.subheader(f"📊 Market Report: {start_time.strftime('%H:%M')} to {end_time.strftime('%H:%M')}")
    
    # Show Chart
    st.write("**Visual Tape Reading**")
    st.line_chart(df.set_index("Time")["Crash"])
    
    # Statistical Summary
    col_a, col_b, col_c = st.columns(3)
    pinks = len(df[df["Crash"] >= 10])
    blues = len(df[df["Crash"] < 2])
    
    col_a.metric("Total Rounds", len(df))
    col_b.metric("Pink Spikes (10x+)", pinks)
    col_c.metric("Blue Rounds (<2x)", blues)

    # Strategy Insights
    st.write("### 🧠 Pattern Observation")
    # Finding the "quietest" period
    st.write(f"In this simulated hour, your best 'Pink' hit was **{df['Crash'].max()}x**.")
    
    # Backtest integration
    st.divider()
    st.subheader("🧪 Run Backtest on this Session")
    # (Same backtest logic as before can be applied here)
    if st.button("Run Flat-Bet Strategy on this Time Window"):
        balance = 1000.0
        for crash in df["Crash"]:
            balance -= 10
            if crash >= 2.0:
                balance += 20
        st.write(f"Final Balance after this session: **BWP {balance:.2f}**")
