"""Theory 1.2 c): through the side wall 2 pi r h of a 30 cm tall, 3.0 cm radius flask (e1 = e2 = 0.08, 25 C outside), 500 g of ice at 0 C needs 0.5 x 336 kJ, taking 5.39e5 s = 6.24 days. Adapted: the ice mass (g), the emissivity and the outside temperature (Celsius) vary; returns the time in days."""

from math import pi


def solve(ice=500.0, emissivity=0.08, warm=25.0, height=30.0, radius=3.0):
    from otk.sheets.tpho2561_physics import q04

    flow = q04.solve(outer=emissivity, inner=emissivity, warm=warm)
    area = 2 * pi * radius * 1e-2 * height * 1e-2
    return ice * 1e-3 * 336e3 / (flow * area) / 86400


def check(ice=500.0, emissivity=0.08, warm=25.0, height=30.0, radius=3.0):
    from otk.sheets.tpho2561_physics import q04

    flow = q04.check(outer=emissivity, inner=emissivity, warm=warm)
    # melt in steps of one hour
    remaining, hours = ice * 1e-3 * 336e3, 0.0
    power = flow * 2 * pi * radius * 1e-2 * height * 1e-2
    while remaining > power * 3600:
        remaining -= power * 3600
        hours += 1
    return (hours + remaining / (power * 3600)) / 24


PARAMS = {"ice": 500.0, "emissivity": 0.08, "warm": 25.0, "height": 30.0, "radius": 3.0}
VARIANTS = [{"ice": 300.0}, {"emissivity": 0.05}, {"warm": 35.0}]
ANSWER = 6.241984980197193
TOL = 1e-6
