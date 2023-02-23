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

# Function to calculate the RSI

def calculate_rsi(prices, lenght):
    deltas = np.diff(prices)
    seed = deltas[:lenght + 1]
    up = seed[seed >= 0].sum() / lenght
    down = -seed[seed < 0].sum() / lenght
    rs = up / down
    rsi = np.zeros_like(prices)
    rsi[:lenght] = 100. - 100. / (1. + rs)

    for i in range(lenght, len(prices)):
        delta = deltas[i - 1]
        if delta > 0:
            upval = delta
            downval = 0.
        else:
            upval = 0.
            downval = -delta

        up = (up * (lenght - 1) + upval) / lenght
        down = (down * (lenght - 1) + downval) / lenght

        rs = up / down
        rsi[i] = 100. - 100. / (1. + rs)
        rsi = np.around(rsi, decimals=2)

    return rsi/100

# Set up the exchange, the symbol and the period of time.

exchange = ccxt.binance()
symbol = 'BTCUSDT'
period = 1000
smoothness = 0.2

# Get the last close, highest and lowest prices.
prices = exchange.fetch_ohlcv(symbol, timeframe='1h', limit=period)

open_prices = np.array([candle[1] for candle in prices])

closing_prices = np.array([candle[4] for candle in prices])

highest_prices = np.array([candle[2] for candle in prices])

lowest_prices = np.array([candle[3] for candle in prices])

# Inputs. Can be changed if you want different results.
length = 35
mass = smoothness
g = calculate_rsi(closing_prices, length)

# Calculate the variables used to calculate the kinetic/potential energy
close_ema = ema(closing_prices, length)
high_ema = ema(highest_prices, length)
low_ema = ema(lowest_prices, length)
h = high_ema - low_ema
price_change = np.diff(close_ema)

# Calculate the kinetic and the potential energy

kinetic_energy = (0.5 * mass * np.power(price_change, 2))
kinetic_energy = np.around(kinetic_energy, decimals=2)
kinetic_energy = kinetic_energy.tolist()
kinetic_energy.insert(-1, kinetic_energy[-2])

potential_energy = (mass * g * h[0:])

# Set up the range of data we have.
date = []
for i in range(closing_prices.size):
    date.append(i)

# Plot the data in three differents charts.
# Chart 1
fig, (ax, ax1, ax2) = plt.subplots(3, 1, sharex=True)
ax.plot(date, closing_prices)
ax.set_title(f"Last {period} Closing Entries")

# Chart 2
ax1.plot(date, potential_energy)
ax1.set_title("Potential Energy")

# Chart 3
ax2.plot(date, kinetic_energy)
ax2.set_title("Kinetic Energy")
plt.show()


# One Dimensional Situations
# Calculate the variables used to calculate the kinetic/potential energy
h = np.max(closing_prices) - np.min(closing_prices)
g = calculate_rsi(closing_prices, length)
v = np.diff(closing_prices)

# Calculate the kinetic and the potential energy

kinetic_energy = (0.5 * mass * np.power(v, 2))
kinetic_energy = np.around(kinetic_energy, decimals=2)
kinetic_energy = kinetic_energy.tolist()
kinetic_energy.insert(-1, kinetic_energy[-2])
potential_energy = (mass * g * h)

# Chart 1
fig, (ax, ax1, ax2) = plt.subplots(3, 1, sharex=True)
ax.plot(date, closing_prices)
ax.set_title(f"Last {period} Closing Entries")

# Chart 2
ax1.plot(date, potential_energy)
ax1.set_title("Potential Energy")

# Chart 3
ax2.plot(date, kinetic_energy)
ax2.set_title("Kinetic Energy")
plt.show()
