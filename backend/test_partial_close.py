from app.execution.partial_close import PartialClose

trade = {
    "lot_size": 1.00,
    "partial_closed": False,
}

pc = PartialClose()

print(trade)

trade = pc.apply(trade)

print(trade)