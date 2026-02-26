import streamlit as st
import random
import time

# Page styling for that "Casino" feel
st.set_page_config(page_title="Combi Number Reveal", page_icon="🚐", layout="centered")

def generate_crash_point():
    """The core engine generating the next outcome."""
    random_float = random.uniform(0, 1)
    # The math: 0.99 / (1 - rand) creates the crash curve
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

st.title("🚐 The Combi Next Number")
st.write("Click below to reveal the next generated multiplier in the sequence.")

# Custom CSS for the "Big Font" display
st.markdown("""
    <style>
    .big-font {
        font-size:120px !important;
        font-weight: bold;
        text-align: center;
        margin-top: -20px;
    }
    .blue { color: #3498db; }
    .green { color: #2ecc71; }
    .pink { color: #9b59b6; }
    </style>
    """, unsafe_allow_html=True)

# Initialize a history list in session state to track the tape
if 'history' not in st.session_state:
    st.session_state.history = []

# The "Next Number" Trigger
if st.button("Reveal Next Number", use_container_width=True, type="primary"):
    with st.spinner('Generating...'):
        time.sleep(0.5) # Adding a slight delay for suspense
        next_val = generate_crash_point()
        st.session_state.history.insert(0, next_val) # Add to the top of the list

# Display the Current Number
if st.session_state.history:
    latest = st.session_state.history[0]
    
    # Determine color based on rarity/value
    color_class = "blue"
    if latest >= 10:
        color_class = "pink"
    elif latest >= 2:
        color_class = "green"
    
    # BIG FONT DISPLAY
    st.markdown(f'<p class="big-font {color_class}">{latest}x</p>', unsafe_allow_html=True)
    
    # Simple logic for your advantage
    if latest < 2.0:
        st.info(f"This was a **Blue** (High Occurrence). Current Blue Streak: {sum(1 for x in st.session_state.history if x < 2.0)} total blues recorded.")
    elif latest >= 10:
        st.balloons()
        st.success("🔥 **PINK SPIKE!** This is a rare high-value number.")

# Display the Recent Tape (History)
st.divider()
st.subheader("Recent Tape History")
st.write(st.session_state.history[:10]) # Show the last 10 numbers
