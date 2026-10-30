from app.strategy.ema_crossover import EMACrossover

prices = []

price = 1.1000

for _ in range(100):

    price += 0.0003

    prices.append(price)

strategy = EMACrossover()

print(strategy.signal(prices))