import streamlit as st
import random
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="Drought & Peak Analyzer", page_icon="🕒", layout="wide")

def generate_crash_point():
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🕒 Time-Session & Drought Analyzer")
st.write("Identify exactly when the 'Peak' ends and the 'Drought' begins.")

# --- 1. Session Setup ---
st.subheader("1. Simulation Window")
t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    start_time = st.time_input("Start Time", value=datetime.strptime("10:00", "%H:%M").time())
with t_col2:
    end_time = st.time_input("End Time", value=datetime.strptime("11:00", "%H:%M").time())
with t_col3:
    rounds_per_min = st.slider("Rounds per min", 1, 5, 3)
with t_col4:
    analysis_target = st.number_input("Target for Drought (x)", value=3.0, step=0.5)

start_dt = datetime.combine(datetime.today(), start_time)
end_dt = datetime.combine(datetime.today(), end_time)
if end_dt <= start_dt: end_dt += timedelta(days=1)

duration_minutes = (end_dt - start_dt).total_seconds() / 60
total_rounds = int(duration_minutes * rounds_per_min)

if 'time_history' not in st.session_state:
    st.session_state.time_history = pd.DataFrame()

if st.button("Analyze Session", use_container_width=True):
    data = []
    current_time = start_dt
    
    # Drought Tracking Variables
    max_drought = 0
    current_drought = 0
    drought_start_time = start_dt
    final_max_drought_start = start_dt

    for _ in range(total_rounds):
        crash = generate_crash_point()
        
        # Drought Logic
        if crash < analysis_target:
            if current_drought == 0:
                drought_start_time = current_time
            current_drought += 1
        else:
            if current_drought > max_drought:
                max_drought = current_drought
                final_max_drought_start = drought_start_time
            current_drought = 0

        data.append({
            "Timestamp": current_time,
            "Time": current_time.strftime("%H:%M:%S"),
            "Crash": crash,
            "Is_Target": 1 if crash >= analysis_target else 0,
            "Is_Pink": 1 if crash >= 10 else 0
        })
        current_time += timedelta(seconds=(60/rounds_per_min))
    
    st.session_state.time_history = pd.DataFrame(data)
    st.session_state.max_drought = max_drought
    st.session_state.drought_time = final_max_drought_start.strftime("%H:%M:%S")

# --- 2. Results Dashboard ---
if not st.session_state.time_history.empty:
    df = st.session_state.time_history
    
    st.divider()
    
    # 2.1 Peak & Drought Metrics
    m1, m2, m3 = st.columns(3)
    
    # Find Peak (10-min window)
    df_idx = df.set_index('Timestamp')
    peak_val = df_idx['Is_Pink'].resample('10T').sum().max()
    
    m1.metric("Peak Intensity", f"{peak_val:.0f} Pinks", help="Most 10x hits in a 10-min block")
    m2.metric("Longest Drought", f"{st.session_state.max_drought} Rounds", help=f"Consecutive rounds under {analysis_target}x")
    m3.metric("Drought Start Time", st.session_state.drought_time)

    # 2.2 Visual Timeline
    st.write(f"### 📈 Session Multiplier Timeline")
    st.line_chart(df.set_index("Time")["Crash"])

    # 2.3 Detailed Insights
    st.divider()
    st.write("### 🧠 Strategist's View")
    
    col_left, col_right = st.columns(2)
    with col_left:
        st.info(f"""
        **The Drought Alert:**
        Your longest drought was **{st.session_state.max_drought} rounds**. 
        If you were using a Martingale (doubling) strategy starting at BWP 1, 
        you would have needed **BWP {2**st.session_state.max_drought:.0f}** just to place the next bet. This is why Martingale fails.
        """)
    
    with col_right:
        win_rate = (len(df[df["Crash"] >= analysis_target]) / len(df)) * 100
        st.success(f"""
        **The Profit Opportunity:**
        Even with a **{win_rate:.1f}% win rate**, a 'Sniper' 
        waiting for the end of a drought could have 
        capitalized on the Peak Periods.
        """)
