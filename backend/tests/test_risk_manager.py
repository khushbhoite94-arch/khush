from app.risk.risk_manager import RiskManager


def test_position_size_matches_paper_executor_contract_multiplier():
    manager = RiskManager(risk_percent=1.0, contract_size=100000)
    # 1% of 10,000 is 100; a 1.0 price stop at 100,000 units
    # per lot requires 0.001 lots to risk approximately 100.
    assert manager.calculate_position_size(10000, 100, 99) == 0.001


def test_buy_stop_loss_must_be_below_entry():
    result = RiskManager().evaluate(
        balance=10000,
        entry=100,
        stop_loss=101,
        side="BUY",
        open_positions=0,
    )
    assert result["allowed"] is False
    assert result["reason"] == "Stop loss is on the wrong side of entry"


def test_sell_stop_loss_must_be_above_entry():
    result = RiskManager().evaluate(
        balance=10000,
        entry=100,
        stop_loss=99,
        side="SELL",
        open_positions=0,
    )
    assert result["allowed"] is False
    assert result["reason"] == "Stop loss is on the wrong side of entry"
