import streamlit as st
import random

st.set_page_config(page_title="Aviator Pattern Tracker", page_icon="🚐")

def generate_simulated_number():
    """Generates a number using the standard crash math for comparison."""
    random_float = random.uniform(0, 1)
    return round(max(1.01, 0.99 / (1 - random_float)), 2)

st.title("🚐 Aviator Live Pattern Tracker")
st.write("Enter the last number you saw on Aviator to track the current 'Blue Streak'.")

# 1. Initialize session data
if 'real_history' not in st.session_state:
    st.session_state.real_history = []
if 'blue_streak' not in st.session_state:
    st.session_state.blue_streak = 0

# 2. Manual Input Section
with st.form("input_form", clear_on_submit=True):
    prev_num = st.number_input("Enter Last Aviator Number (e.g. 1.30):", min_value=1.00, step=0.01)
    submitted = st.form_submit_button("Log Number & Generate Prediction")

if submitted:
    # Update History
    st.session_state.real_history.insert(0, prev_num)
    
    # Update Blue Streak (numbers under 2.0x)
    if prev_num < 2.0:
        st.session_state.blue_streak += 1
    else:
        st.session_state.blue_streak = 0

# 3. The "Prediction" (Simulated Next Round)
st.divider()
st.subheader("Current Market Status")

col1, col2 = st.columns(2)
col1.metric("Current Blue Streak", f"{st.session_state.blue_streak} Rounds")

# Strategy Advice based on your 8-round wait rule
if st.session_state.blue_streak >= 8:
    col2.success("🎯 SNIPER ALERT: Wait Condition Met!")
    st.write("**Strategy:** The 8-blue wait is complete. Statistically, a green round is 'likely' soon (though not guaranteed).")
else:
    col2.warning("🕒 Observation Mode")
    st.write(f"**Strategy:** Continue waiting. You need {8 - st.session_state.blue_streak} more blues.")

# 4. The Simulated "Next" Result
# This shows what a fair RNG would produce next
predicted_next = generate_simulated_number()
st.markdown(f"""
    <div style="text-align: center; border: 2px solid #555; border-radius: 10px; padding: 20px;">
        <h3>Simulated Next Outcome</h3>
        <p style="font-size: 80px; font-weight: bold; color: {'#3498db' if predicted_next < 2 else '#2ecc71'};">
            {predicted_next}x
        </p>
        <p><i>(Based on Provably Fair Math)</i></p>
    </div>
""", unsafe_allow_html=True)

# 5. Visual Tape
st.divider()
st.write("**Recent Tape (Real Data):**", st.session_state.real_history[:15])
