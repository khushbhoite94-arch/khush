from app.ai.ai_engine import AIEngine


engine = AIEngine()


candles = []

price = 1.1000

for i in range(60):

    candles.append({

        "open": price,

        "high": price + 0.0010,

        "low": price - 0.0010,

        "close": price + 0.0005,

        "volume": 1000,

    })

    price += 0.0003


result = engine.process(candles)

print("=" * 80)
print(result)
print("=" * 80)