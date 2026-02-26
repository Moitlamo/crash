import MetaTrader5 as mt5
import pandas as pd
from datetime import datetime

# 1. Initialize connection to the MT5 terminal
if not mt5.initialize():
    print("Initialization failed. Ensure MT5 is open and logged in.")
    mt5.shutdown()
    quit()

print("Successfully connected to MT5!")

# 2. Define the symbol and timeframe
# Note: Ensure this string matches EXACTLY how it appears in your MT5 Market Watch
symbol = "Volatility 25 (1s) Index" 
timeframe = mt5.TIMEFRAME_M1 # 1-minute candles

# Ensure the symbol is active in the Market Watch window
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select {symbol}. Please check the symbol name and your broker connection.")
    mt5.shutdown()
    quit()

# 3. Fetch the last 10 candles
print(f"Fetching data for {symbol}...")
rates = mt5.copy_rates_from_pos(symbol, timeframe, 0, 10)

if rates is None:
    print("Failed to fetch data. No rates returned.")
else:
    # 4. Convert the raw data into a Pandas DataFrame for easier analysis
    df = pd.DataFrame(rates)
    
    # MT5 returns time in Unix seconds; convert it to a readable datetime format
    df['time'] = pd.to_datetime(df['time'], unit='s')
    
    # Display the essential columns
    print("\nLatest Market Data:")
    print(df[['time', 'open', 'high', 'low', 'close', 'tick_volume']])

# 5. Clean up and shut down the connection
mt5.shutdown()
