from app.indicators.momentum import Momentum

prices = []

price = 1.1000

for _ in range(120):

    price += 0.0003

    prices.append(price)

m = Momentum()

print(m.calculate(prices))