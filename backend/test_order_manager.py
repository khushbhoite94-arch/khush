from app.execution.order_manager import OrderManager

manager = OrderManager()

order = manager.create(

    direction="BUY",

    symbol="EURUSD",

    entry=1.1000,

    stop_loss=1.0980,

    take_profit=1.1040,

    lot_size=0.10,

)

print(manager.statistics())

manager.execute(order)

print(manager.statistics())