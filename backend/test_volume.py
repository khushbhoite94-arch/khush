from app.indicators.volume import Volume

volumes = [

    100,

    102,

    99,

    101,

    105,

    98,

    100,

    101,

    103,

    99,

    100,

    101,

    98,

    99,

    104,

    103,

    100,

    101,

    102,

    250,

]

v = Volume()

print(v.calculate(volumes))