import streamlit as st
import random
import time

st.set_page_config(page_title="The Cattle Drive Slots", page_icon="🎰", layout="centered")

st.title("🎰 The Cattle Drive: 3x3 Slots")
st.write("Press SPIN to test the weighted probability matrix.")

# --- 1. The Mathematical Weights ---
# We don't use pure randomness. We use "weights" to control the house edge.
# The total adds up to 100% for easy math.
symbols = ["🐄", "🚐", "🦓", "🦁", "💎"]
weights = [45, 30, 15, 8, 2] # Diamonds only have a 2% chance of appearing!

# The Payout Table (Multiplier based on your bet)
payouts = {
    "🐄": 2.0,   # 3 Cows pays 2x
    "🚐": 5.0,   # 3 Combis pays 5x
    "🦓": 15.0,  # 3 Zebras pays 15x
    "🦁": 50.0,  # 3 Lions pays 50x
    "💎": 250.0  # 3 Diamonds pays 250x
}

def spin_reel():
    """Generates a single reel spin based on our rigged weights."""
    return random.choices(symbols, weights=weights, k=3)

# --- 2. The Game UI ---
st.divider()

col_bet, col_spin = st.columns([1, 1])
with col_bet:
    bet_amount = st.number_input("Bet Amount (BWP):", min_value=1.0, value=10.0, step=1.0)
with col_spin:
    st.write("") # Spacing
    spin_button = st.button("🎰 SPIN THE REELS", type="primary", use_container_width=True)

# Custom CSS to make the slot symbols massive
st.markdown("""
    <style>
    .slot-machine { font-size: 80px; text-align: center; letter-spacing: 20px; line-height: 1.2; }
    .win-text { color: #2ecc71; font-size: 30px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

if spin_button:
    with st.spinner("Spinning..."):
        time.sleep(0.5) # Fake delay for suspense
        
        # Generate the 3x3 Grid
        row1 = spin_reel()
        row2 = spin_reel()
        row3 = spin_reel()
        
        # Display the Grid
        st.markdown(f'<div class="slot-machine">{row1[0]} {row1[1]} {row1[2]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="slot-machine">{row2[0]} {row2[1]} {row2[2]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="slot-machine">{row3[0]} {row3[1]} {row3[2]}</div>', unsafe_allow_html=True)
        
        st.divider()
        
        # --- 3. The Payout Logic ---
        # For this basic version, we only check the MIDDLE row (Payline 1)
        if row2[0] == row2[1] == row2[2]:
            winning_symbol = row2[0]
            multiplier = payouts[winning_symbol]
            winnings = bet_amount * multiplier
            
            st.balloons()
            st.markdown(f'<div class="win-text">🎉 JACKPOT! 3 {winning_symbol} matched!</div>', unsafe_allow_html=True)
            st.success(f"You won BWP {winnings:.2f} ({multiplier}x multiplier)")
        else:
            st.error("No match on the center line. Try again!")
