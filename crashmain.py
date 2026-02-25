import random

def generate_crash_point():
    """The exact same engine powering The Combi Race."""
    random_float = random.uniform(0, 1)
    crash_point = max(1.01, 0.99 / (1 - random_float))
    return round(min(crash_point, 1000.00), 2)

# --- 1. Generate the Tick Data ---
total_rounds = 100000
print(f"Generating and analyzing {total_rounds:,} rounds...")

# This creates a massive list of 100,000 crash points instantly
market_history = [generate_crash_point() for _ in range(total_rounds)]

# --- 2. Analyze the Statistics ---
# Count occurrences
crashes_under_2 = sum(1 for x in market_history if x < 2.00)
crashes_over_2 = sum(1 for x in market_history if x >= 2.00)
crashes_over_10 = sum(1 for x in market_history if x >= 10.00)
crashes_at_1_01 = sum(1 for x in market_history if x == 1.01)

# Find the longest brutal losing streak (consecutive crashes under 2.00x)
max_red_streak = 0
current_streak = 0

for tick in market_history:
    if tick < 2.00:
        current_streak += 1
        if current_streak > max_red_streak:
            max_red_streak = current_streak
    else:
        current_streak = 0

# --- 3. Print the Market Report ---
print("\n--- 📊 ALGORITHM ANALYSIS REPORT ---")
print(f"Total Rounds Simulated: {total_rounds:,}")
print("-" * 35)
print(f"Win Rate (Target 2.00x): {(crashes_over_2 / total_rounds) * 100:.2f}%")
print(f"Loss Rate (Under 2.00x): {(crashes_under_2 / total_rounds) * 100:.2f}%")
print("-" * 35)
print(f"Frequency of 10.00x+: {(crashes_over_10 / total_rounds) * 100:.2f}%")
print(f"Frequency of INSTANT CRASH (1.01x): {(crashes_at_1_01 / total_rounds) * 100:.2f}%")
print("-" * 35)
print(f"⚠️ LONGEST RECORDED RED STREAK: {max_red_streak} rounds in a row under 2.00x")
