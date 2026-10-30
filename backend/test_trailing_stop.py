from app.execution.trailing_stop import TrailingStop

trade = {
    "direction": "BUY",
    "entry": 1.1000,
    "stop_loss": 1.0980,
}

ts = TrailingStop(distance=0.0010)

print(trade)

trade = ts.apply(trade, 1.1050)

print(trade)

trade = ts.apply(trade, 1.1070)

print(trade)