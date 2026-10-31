import pytest

from app.execution.paper_executor import PaperExecutor


def executor_without_dynamic_stops(starting_balance=10_000.0):
    executor = PaperExecutor(starting_balance=starting_balance)
    # Isolate the fixed stop-loss / take-profit behavior in these tests.
    executor.break_even.trigger_rr = 1_000_000
    executor.trailing.distance = 1_000_000
    return executor


def test_buy_trade_closes_at_stop_loss():
    executor = executor_without_dynamic_stops()
    opened = executor.buy("TEST", 0.001, 100.0, 99.0, 103.0)

    finished = executor.update(98.0)

    assert len(finished) == 1
    assert finished[0]["status"] == "CLOSED"
    assert finished[0]["exit_price"] == 99.0
    assert finished[0]["profit"] == -100.0
    assert executor.get_balance() == 9_900.0
    assert executor.get_open_positions() == []


def test_buy_trade_closes_at_take_profit():
    executor = executor_without_dynamic_stops()
    executor.buy("TEST", 0.001, 100.0, 99.0, 103.0)

    finished = executor.update(104.0)

    assert len(finished) == 1
    assert finished[0]["exit_price"] == 103.0
    assert finished[0]["profit"] == 300.0
    assert executor.get_balance() == 10_300.0


def test_sell_trade_closes_at_stop_loss():
    executor = executor_without_dynamic_stops()
    executor.sell("TEST", 0.001, 100.0, 102.0, 97.0)

    finished = executor.update(103.0)

    assert len(finished) == 1
    assert finished[0]["exit_price"] == 102.0
    assert finished[0]["profit"] == -200.0
    assert executor.get_balance() == 9_800.0


def test_sell_trade_closes_at_take_profit():
    executor = executor_without_dynamic_stops()
    executor.sell("TEST", 0.001, 100.0, 102.0, 97.0)

    finished = executor.update(96.0)

    assert len(finished) == 1
    assert finished[0]["exit_price"] == 97.0
    assert finished[0]["profit"] == 300.0
    assert executor.get_balance() == 10_300.0


def test_repeated_partial_close_does_not_realize_profit_twice():
    executor = executor_without_dynamic_stops()
    opened = executor.buy("TEST", 0.001, 100.0, 99.0, 103.0)

    first = executor.partial_close(opened["id"], 101.0, 0.5)
    balance_after_first_close = executor.get_balance()

    second = executor.partial_close(opened["id"], 102.0, 0.5)

    assert first is not None
    assert second is None
    assert executor.get_balance() == balance_after_first_close == 10_050.0
    assert executor.statistics()["realized_profit"] == 50.0


def test_reset_restores_original_starting_balance():
    executor = executor_without_dynamic_stops(starting_balance=10_000.0)
    opened = executor.buy("TEST", 0.001, 100.0, 99.0, 103.0)
    executor.close_trade(opened["id"], 101.0)

    executor.reset()

    assert executor.get_balance() == 10_000.0
    assert executor.get_equity() == 10_000.0
    assert executor.get_open_positions() == []
    assert executor.get_closed_positions() == []
