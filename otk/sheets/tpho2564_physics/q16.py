"""Theory 3.1 d): 2.7 J per breath at 10 breaths a minute is 9.26 kcal a day (1 cal = 4.2 J); if that is 30% of what the diaphragm spends, the diaphragm uses 30.9 kcal a day. Adapted: the work per breath (J), breathing rate (per minute) and efficiency (%) vary; returns kcal per day."""


def solve(work=2.7, rate=10.0, share=30.0):
    return work * rate * 24 * 60 / 4.2e3 / (share / 100)


def check(work=2.7, rate=10.0, share=30.0):
    # diaphragm power in watts, then a day's energy in kilocalories
    power = work / (share / 100) * rate / 60
    return power * 86400 / 4200


PARAMS = {"work": 2.7, "rate": 10.0, "share": 30.0}
VARIANTS = [{"rate": 15.0}, {"share": 25.0}, {"work": 3.2}]
ANSWER = 30.85714285714286
TOL = 1e-9
