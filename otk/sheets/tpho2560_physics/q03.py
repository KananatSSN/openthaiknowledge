"""Theory 1.2.3: the cycle's work is the triangle's area (1/2)(V_B - V_A)(p_A - p_C) = 200 J and heat enters on AB ((5/2) p_A dV = 4000 J) and CA ((3/2) V_A dp = 150 J), so e = 200/4150 = 4.8%. Adapted: p_A (atm), V_A (L), the volume ratio and T_min vary with T_A = 400 K; returns e in percent (1 atm taken as 1.013e5 Pa, which cancels)."""


def solve(pressure=10.0, volume=0.4, ratio=5.0, hot=400.0, cold=300.0):
    drop = pressure * (1 - cold / hot)
    work = 0.5 * (ratio - 1) * volume * drop
    heat = 2.5 * pressure * (ratio - 1) * volume + 1.5 * volume * drop
    return 100 * work / heat


def check(pressure=10.0, volume=0.4, ratio=5.0, hot=400.0, cold=300.0):
    from otk.sheets.tpho2560_physics._shared import cycle

    work, heat = cycle(pressure, volume, ratio, hot, cold, steps=4000)
    return 100 * work / heat


PARAMS = {"pressure": 10.0, "volume": 0.4, "ratio": 5.0, "hot": 400.0, "cold": 300.0}
VARIANTS = [{"ratio": 3.0}, {"cold": 200.0}, {"pressure": 6.0, "ratio": 8.0}]
ANSWER = 4.819277108433735
TOL = 1e-6
