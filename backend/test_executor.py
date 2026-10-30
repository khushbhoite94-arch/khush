from app.execution.executor import ExecutionEngine

engine = ExecutionEngine()

trade = engine.buy(

    symbol="EURUSD",

    lot=0.10,

    entry=1.1000,

    sl=1.0980,

    tp=1.1040,

)

print(engine.statistics())

engine.update(1.1040)

print(engine.statistics())