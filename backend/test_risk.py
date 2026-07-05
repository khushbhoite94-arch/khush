from app.risk.risk_manager import RiskManager

risk = RiskManager(risk_percent=1)

lot = risk.calculate_lot(

    balance=10000,

    stop_loss_points=200,

    pip_value=10

)

print()
print("Lot Size:", lot)
print()