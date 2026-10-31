from app.ai.ai_engine import AIEngine


def valid_candles(count=50):
    candles = []
    for index in range(count):
        close = 100.0 + index * 0.1
        candles.append({
            "open": close - 0.05,
            "high": close + 0.1,
            "low": close - 0.1,
            "close": close,
        })
    return candles


def test_validate_rejects_too_few_candles():
    assert AIEngine.validate(valid_candles(49)) is False


def test_validate_rejects_invalid_ohlc():
    candles = valid_candles()
    candles[-1]["high"] = candles[-1]["low"] - 1
    assert AIEngine.validate(candles) is False


def test_invalid_input_fails_closed():
    engine = AIEngine()
    result = engine.process([])
    assert result["action"] == "WAIT"
    assert result["decision"]["action"] == "WAIT"
    assert engine.total_predictions == 0


def test_process_returns_buy_only_when_strategy_and_decision_agree():
    engine = AIEngine()
    candles = valid_candles()

    engine.smart_money.analyze = lambda data: {
        "direction": "BUY",
        "confidence": 85,
    }
    engine.strategy_engine.calculate = lambda closes, data: {
        "signal": "BUY",
        "confidence": 82,
        "strategy": "test",
    }
    engine.decision_engine.decide = lambda data: {
        "action": "BUY",
        "confidence": 85,
        "trade": {
            "direction": "BUY",
            "entry": data[-1]["close"],
            "stop_loss": data[-1]["close"] - 1,
            "take_profit": data[-1]["close"] + 2,
        },
    }
    engine.statistics_engine.analyze = lambda data: {"sample_size": len(data)}

    result = engine.process(candles)

    assert result["action"] == "BUY"
    assert result["decision"]["action"] == "BUY"
    assert result["statistics"]["sample_size"] == 50


def test_process_waits_when_signals_conflict():
    engine = AIEngine()
    candles = valid_candles()

    engine.smart_money.analyze = lambda data: {
        "direction": "BUY",
        "confidence": 85,
    }
    engine.strategy_engine.calculate = lambda closes, data: {
        "signal": "SELL",
        "confidence": 82,
    }
    engine.decision_engine.decide = lambda data: {"action": "BUY"}
    engine.statistics_engine.analyze = lambda data: {}

    result = engine.process(candles)

    assert result["action"] == "WAIT"
    assert result["decision"]["reason"] == "NO_AGREEMENT"
