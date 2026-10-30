from app.execution.position_manager import PositionManager

pm = PositionManager()

trade = {
    "id": "1",
    "direction": "BUY",
    "entry": 1.1000,
    "lot_size": 0.10,
}

pm.open(trade)

print(pm.statistics())

pm.close("1", 1.1020)

print(pm.statistics())