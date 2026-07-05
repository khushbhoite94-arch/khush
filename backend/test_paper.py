from app.execution.paper_executor import PaperExecutor

engine = PaperExecutor()

trade = engine.buy(
    symbol="EURUSD",
    lot=0.10,
    entry=1.17000,
    sl=1.16900,
    tp=1.17200,
)

print(trade)

closed = engine.close_trade(
    trade["id"],
    1.17150,
)

print(closed)

print(engine.get_balance())