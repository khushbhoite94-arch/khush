from app.indicators.rsi import RSI

prices = [
100,
101,
102,
103,
104,
105,
106,
107,
108,
109,
110,
111,
112,
113,
114,
115,
116,
117,
118,
119,
120,
121,
122,
123,
124,
125,
124,
123,
122,
121,
120,
119,
118,
117,
116,
115,
114,
113
]

rsi = RSI()

print()

print("RSI =", rsi.calculate(prices))

print()