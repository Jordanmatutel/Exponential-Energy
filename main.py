import ccxt
import numpy as np
import matplotlib.pyplot as plt

# Function to calculate the EMA

def ema(values, ema_length):
    alpha = 2 / (ema_length + 1)
    ema = np.zeros(len(values))
    ema[0] = values[0]
    for i in range(1, len(values)):
        ema[i] = alpha * values[i] + (1 - alpha) * ema[i-1]
    return ema

# Set up the exchange, the symbol and the period of time.

exchange = ccxt.binance()
symbol = 'BTC/USDT'
period = 1000

# Get the last close, highest and lowest prices.
prices = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=period)

closing_prices = np.array([candle[4] for candle in prices])

highest_prices = np.array([candle[2] for candle in prices])

lowest_prices = np.array([candle[3] for candle in prices])

# Inputs. Can be changed if you want different results.
length = 100
mass = 1
g = 1

# Calculate the variables used to calculate the kinetic/potential energy
close_ema = ema(closing_prices, length)
high_ema = ema(highest_prices, length)
low_ema = ema(lowest_prices, length)
h = high_ema - low_ema
price_change = np.diff(close_ema)

# Calculate the kinetic and the potential energy

kinetic_energy = (0.5 * mass * np.power(price_change, 2))/100
kinetic_energy = np.around(kinetic_energy, decimals=2)
potential_energy = mass * g * h[1:]

# Set up the range of data we have.
date = []
date1 = []
for i in range(closing_prices.size):
    date.append(i)
for i in range(potential_energy.size):
    date1.append(i)

# Calculate the EMA of the Potential Energy.
ema1 = ema(potential_energy,25)

# Plot the data in two differents charts.
# Chart 1
fig, (ax, ax1, ax2) = plt.subplots(3, 1, sharex=True)
ax.plot(date, closing_prices)
ax.set_title("Last 100 Closing Entries")

# Chart 2
ax1.plot(date1, potential_energy)
ax1.plot(date1, ema1)
ax1.set_title("Potential Energy Size")

# Chart 3
ax2.plot(date1, kinetic_energy)
ax2.set_title("Kinetic Energy Size")
plt.show()
