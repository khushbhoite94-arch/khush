from app.strategy.pullback import Pullback

prices = []

price = 1.1000

for i in range(80):

    price += 0.0003

    prices.append(price)

prices[-1] -= 0.0004

strategy = Pullback()

print(strategy.signal(prices))