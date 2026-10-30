from app.ai.confidence import Confidence

signals = [

    {

        "signal": "BUY",

        "confidence": 85,

    },

    {

        "signal": "BUY",

        "confidence": 90,

    },

    {

        "signal": "SELL",

        "confidence": 70,

    },

]

engine = Confidence()

print(

    engine.calculate(

        signals

    )

)