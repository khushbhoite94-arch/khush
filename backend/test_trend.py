from app.indicators.trend import Trend

prices = []

price = 1.1000

for _ in range(100):

    price += 0.0004

    prices.append(price)

trend = Trend().calculate(prices)

print(trend)