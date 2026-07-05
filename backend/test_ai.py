from app.ai.decision_engine import DecisionEngine

engine = DecisionEngine()

decision = engine.decide(

    strategy_signal="BUY",

    rsi=55,

    macd={
        "macd": 1.8,
        "signal": 1.2,
        "histogram": 0.6,
    }

)

print()
print(decision)
print()