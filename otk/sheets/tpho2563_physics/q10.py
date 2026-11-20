"""Theory 2.4, 2.7: dry air cooling at alpha = 2 g mu/(7R) reaches pressure p at z = (T0/alpha)[1 - (p/p0)^(2/7)]: 1.44e3 m at 84.2 kPa and 2.90e3 m at 70.0 kPa from 20.0 C and 100 kPa. Adapted: the ground temperature (C) and the pressures (kPa) vary; returns metres."""


def solve(ground=20.0, base=100.0, station=84.2):
    alpha = 2 * 9.81 * 29.0e-3 / (7 * 8.31)
    return (ground + 273.15) / alpha * (1 - (station / base) ** (2 / 7))


def check(ground=20.0, base=100.0, station=84.2):
    from otk.sheets.tpho2563_physics._shared import adiabatic_climb

    return adiabatic_climb(ground + 273.15, base, station)[0]


PARAMS = {"ground": 20.0, "base": 100.0, "station": 84.2}
VARIANTS = [{"station": 70.0}, {"ground": 30.0}, {"station": 90.0}]
ANSWER = 1437.0235660996825
TOL = 1e-6
