import streamlit as st
import random
import pandas as pd

# Set up the page
st.set_page_config(page_title="Algorithm Analyzer", page_icon="📊", layout="wide")

def generate_crash_point():
    """The core RNG engine."""
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("📊 Crash Pattern Analyzer")
st.write("Simulate thousands of rounds instantly to uncover the algorithm's statistical distribution.")

# Allow the user to choose the sample size
total_rounds = st.number_input("Number of rounds to simulate:", min_value=100, max_value=1000000, value=10000, step=1000)

if st.button("Run Deep Analysis", use_container_width=True):
    with st.spinner("Generating and analyzing tick data..."):
        
        # 1. Generate the massive dataset instantly
        market_history = [generate_crash_point() for _ in range(total_rounds)]
        
        # 2. Calculate the core statistics
        crashes_under_2 = sum(1 for x in market_history if x < 2.00)
        crashes_over_2 = sum(1 for x in market_history if x >= 2.00)
        crashes_over_10 = sum(1 for x in market_history if x >= 10.00)
        crashes_at_1_01 = sum(1 for x in market_history if x == 1.01)
        
        # Calculate the longest brutal losing streak (consecutive crashes under 2.00x)
        max_red_streak = 0
        current_streak = 0
        for tick in market_history:
            if tick < 2.00:
                current_streak += 1
                if current_streak > max_red_streak:
                    max_red_streak = current_streak
            else:
                current_streak = 0

        # 3. Display the results using Streamlit UI components
        st.divider()
        st.subheader("Statistical Breakdown")
        
        # st.columns makes the data look like a professional dashboard
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Win Rate (≥2.00x)", f"{(crashes_over_2 / total_rounds) * 100:.2f}%")
        col2.metric("Loss Rate (<2.00x)", f"{(crashes_under_2 / total_rounds) * 100:.2f}%")
        col3.metric("Huge Crash (≥10.00x)", f"{(crashes_over_10 / total_rounds) * 100:.2f}%")
        col4.metric("Instant Death (1.01x)", f"{(crashes_at_1_01 / total_rounds) * 100:.2f}%")
        
        st.error(f"⚠️ **Longest Red Streak:** In this simulation, the algorithm crashed under 2.00x for **{max_red_streak} rounds in a row.**")
        
        st.divider()
        
        # 4. Visualize the Volatility
        st.subheader("Volatility Chart (Last 200 Rounds)")
        st.write("Here is a slice of what the raw trend looks like on a line chart.")
        
        # We only chart the last 200 rounds so the web browser doesn't freeze trying to draw 10,000 lines!
        chart_data = pd.DataFrame(market_history[-200:], columns=["Crash Multiplier"])
        st.line_chart(chart_data)
