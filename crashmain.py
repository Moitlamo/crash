import random
import time

def generate_crash_point():
    """Generates a crash multiplier heavily weighting lower numbers."""
    # This math creates the classic 'crash' probability curve
    random_float = random.uniform(0, 1)
    
    # If the random float is very close to 1, it creates a high multiplier
    # The max(1.01, ...) ensures the absolute minimum crash is 1.01x
    crash_point = max(1.01, 0.99 / (1 - random_float))
    
    # Let's cap the maximum possible multiplier at 1000x for safety
    return round(min(crash_point, 1000.00), 2)

def play_round():
    crash = generate_crash_point()
    print("🚦 Get ready...")
    time.sleep(1)
    print("🚀 The round has started!")
    
    current_multiplier = 1.00
    
    # Loop to simulate the rising multiplier
    while current_multiplier < crash:
        print(f"Current Multiplier: {current_multiplier:.2f}x")
        time.sleep(0.2) # Wait a fraction of a second to simulate time passing
        
        # Increase the multiplier (it accelerates slightly as it gets higher)
        current_multiplier += 0.05 + (current_multiplier * 0.01)
        
    print(f"\n💥 CRASHED at {crash}x! 💥")

# Run a test round
play_round()