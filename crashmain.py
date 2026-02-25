import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="Algorithm Analyzer", page_icon="📊", layout="wide")

def generate_crash_point():
    """The core RNG engine."""
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("📊 Crash Pattern Analyzer")
st.write("Simulate thousands of rounds instantly to uncover the algorithm's statistical distribution.")

# --- Inputs ---
col1, col2 = st.columns(2)
with col1:
    total_rounds = st.number_input("Number of rounds to simulate:", min_value=100, max_value=1000000, value=10000, step=1000)
with col2:
    # This lets you change the target you want to analyze without changing the code!
    target_multiplier = st.number_input("Target Multiplier to Analyze (e.g., 3.00):", min_value=1.01, value=3.00, step=0.10)

if st.button("Run Deep Analysis", use_container_width=True):
    with st.spinner(f"Generating and analyzing {total_rounds} rounds..."):
        
        # 1. Generate the massive dataset instantly
        market_history = [generate_crash_point() for _ in range(total_rounds)]
        
        # 2. Calculate the core statistics
        crashes_under_2 = sum(1 for x in market_history if x < 2.00)
        crashes_over_2 = sum(1 for x in market_history if x >= 2.00)
        crashes_over_10 = sum(1 for x in market_history if x >= 10.00)
        crashes_at_1_01 = sum(1 for x in market_history if x == 1.01)
        
        # Calculate the longest brutal losing streak (under 2.00x)
        max_red_streak = 0
        current_streak = 0
        for tick in market_history:
            if tick < 2.00:
                current_streak += 1
                if current_streak > max_red_streak:
                    max_red_streak = current_streak
            else:
                current_streak = 0

        # 3. Display the results
        st.divider()
        st.subheader("Statistical Breakdown")
        
        col_a, col_b, col_c, col_d = st.columns(4)
        col_a.metric("Win Rate (≥2.00x)", f"{(crashes_over_2 / total_rounds) * 100:.2f}%")
        col_b.metric("Loss Rate (<2.00x)", f"{(crashes_under_2 / total_rounds) * 100:.2f}%")
        col_c.metric("Huge Crash (≥10.00x)", f"{(crashes_over_10 / total_rounds) * 100:.2f}%")
        col_d.metric("Instant Death (1.01x)", f"{(crashes_at_1_01 / total_rounds) * 100:.2f}%")
        
        st.error(f"⚠️ **Longest Red Streak:** The algorithm crashed under 2.00x for **{max_red_streak} rounds in a row.**")
        
        # 4. The Target Gap Analyzer
        st.divider()
        st.subheader(f"🎯 {target_multiplier:.2f}x Target Gap Analysis")
        
        gaps = []
        current_gap = 0
        hits = 0
        
        # Loop through our simulated history to count the gaps between hits
        for tick in market_history:
            if tick >= target_multiplier:
                gaps.append(current_gap)
                current_gap = 0
                hits += 1
            else:
                current_gap += 1
                
        if hits > 0:
            avg_gap = sum(gaps) / len(gaps)
            max_gap = max(gaps)
            
            gap_col1, gap_col2, gap_col3 = st.columns(3)
            gap_col1.metric(f"Total {target_multiplier:.2f}x Hits", f"{hits:,}")
            gap_col2.metric("Average Gap (Rounds)", f"{avg_gap:.1f}")
            gap_col3.metric("Longest Drought (Rounds)", f"{max_gap}")
            
            st.warning(f"💡 **Insight:** While a {target_multiplier:.2f}x hits every {avg_gap:.1f} rounds on average, the longest waiting period was **{max_gap} rounds in a row** without hitting it.")
        else:
            st.write(f"A {target_multiplier:.2f}x never hit in this simulation.")

        # 5. Visualize the Volatility
        st.divider()
        st.subheader("Volatility Chart (Last 200 Rounds)")
        chart_data = pd.DataFrame(market_history[-200:], columns=["Crash Multiplier"])
        st.line_chart(chart_data)
