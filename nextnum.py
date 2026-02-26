import streamlit as st
import random

st.set_page_config(page_title="Aviator Sniper Tracker", page_icon="🚐")

def generate_simulated_number():
    """Generates a number using the standard crash math (0.99 house edge)."""
    random_float = random.uniform(0, 1)
    return round(max(1.01, 0.99 / (1 - random_float)), 2)

st.title("🚐 Aviator Pattern Tracker")

# 1. Direct Streak Input
st.subheader("1. Current Game State")
manual_streak = st.number_input("How many blues are currently on the screen?", min_value=0, value=0, step=1)

# 2. Strategy Logic
st.divider()
st.subheader("2. Sniper Strategy Advice")

col1, col2 = st.columns(2)
col1.metric("Live Blue Streak", f"{manual_streak} Rounds")

if manual_streak >= 8:
    col2.success("🎯 CONDITION MET: SNIPER ENTRY")
    advice = "The 8-round drought has occurred. Statistically, the chance of the next round also being blue is low, though every round remains independent."
else:
    col2.warning("🕒 OBSERVATION MODE")
    advice = f"Continue watching the tape. You need {8 - manual_streak} more consecutive blues before entering."

st.info(advice)

# 3. Predict the 'Next' Outcome
st.divider()
if st.button("Generate Next Number Prediction", use_container_width=True, type="primary"):
    predicted_next = generate_simulated_number()
    
    # Large Display Logic
    color = "#3498db" if predicted_next < 2 else "#2ecc71"
    if predicted_next >= 10: color = "#9b59b6"
    
    st.markdown(f"""
        <div style="text-align: center; border: 2px solid #555; border-radius: 15px; padding: 30px; background-color: #1e1e1e;">
            <h2 style="color: white;">Simulated Next Number</h2>
            <p style="font-size: 100px; font-weight: bold; color: {color}; margin: 0;">
                {predicted_next}x
            </p>
            <p style="color: #aaa;"><i>(Math-based prediction for the next round)</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    # Result Analysis
    if manual_streak >= 8 and predicted_next >= 2.0:
        st.balloons()
        st.success(f"Profit! The {manual_streak}-streak was broken by a {predicted_next}x.")
    elif manual_streak >= 8 and predicted_next < 2.0:
        st.error(f"Drought Continued. The streak is now {manual_streak + 1} blues.")
