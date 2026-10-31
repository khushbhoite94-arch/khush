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


def test_paper_trade_rejects_stop_loss_on_wrong_side():
    engine = AIEngine()
    result = engine.paper_trade({
        "direction": "BUY",
        "entry": 100.0,
        "stop_loss": 101.0,
        "take_profit": 103.0,
    })
    assert result["status"] == "REJECTED"
    assert "wrong side" in result["reason"]
    assert engine.total_trades == 0



def test_paper_trade_rejects_take_profit_on_wrong_side():
    engine = AIEngine()
    result = engine.paper_trade({
        "direction": "BUY",
        "entry": 100.0,
        "stop_loss": 99.0,
        "take_profit": 99.5,
    })
    assert result["status"] == "REJECTED"
    assert "take-profit" in result["reason"]
    assert engine.total_trades == 0


def test_paper_executor_manual_close_pnl_matches_contract_multiplier():
    engine = AIEngine(starting_balance=10000.0)
    opened = engine.paper_executor.buy("TEST", 0.001, 100.0, 99.0, 102.0)
    closed = engine.paper_executor.close_trade(opened["id"], 101.0)

    assert closed["profit"] == 100.0
    assert engine.paper_executor.get_balance() == 10100.0
    assert engine.paper_executor.statistics()["closed_positions"] == 1



def test_partial_close_realizes_pnl_and_final_close_preserves_total():
    engine = AIEngine(starting_balance=10000.0)
    opened = engine.paper_executor.buy("TEST", 0.001, 100.0, 99.0, 103.0)

    partial = engine.paper_executor.partial_close(
        opened["id"], current_price=101.0, percentage=0.5
    )

    assert partial["lot_size"] == 0.0005
    assert partial["realized_partial_profit"] == 50.0
    assert engine.paper_executor.get_balance() == 10050.0
    assert engine.paper_executor.statistics()["realized_profit"] == 50.0

    closed = engine.paper_executor.close_trade(opened["id"], 102.0)

    assert closed["profit"] == 100.0
    assert engine.paper_executor.get_balance() == 10150.0
    assert engine.paper_executor.statistics()["realized_profit"] == 150.0


def test_partial_close_rejects_invalid_price_or_percentage():
    engine = AIEngine()
    opened = engine.paper_executor.buy("TEST", 0.001, 100.0, 99.0, 103.0)

    assert engine.paper_executor.partial_close(opened["id"], 0, 0.5) is None
    assert engine.paper_executor.partial_close(opened["id"], 101, 1.0) is None
    assert engine.paper_executor.get_balance() == 10000.0
    assert opened["lot_size"] == 0.001
