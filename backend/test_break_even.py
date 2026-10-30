from app.execution.break_even import BreakEven

trade = {
    "direction": "BUY",
    "entry": 1.1000,
    "stop_loss": 1.0980,
}

be = BreakEven()

print(be.ready(trade, 1.1025))

trade = be.apply(trade, 1.1025)

print(trade)