"""Theory 2.1 (b): the vapour's partial pressure P1 - P0 T1/T0 at T1 counts n_W = (P1 - P0 T1/T0) V/(R T1) moles, a liquid volume M_W n_W/rho spread over the sphere's 4 pi r^2 = (36 pi)^(1/3) V^(2/3), so the film was M_W V^(1/3)(P1 - P0 T1/T0)/((36 pi)^(1/3) rho R T1) thick. Adapted: V (L), P0 and P1 (kPa) and the temperatures (Celsius) vary; returns the thickness in micrometres."""

from math import pi


def solve(volume=1.0, pressure=100.0, final=129.0, start=27.0, end=100.0, R=8.314):
    T0, T1 = start + 273.15, end + 273.15
    V = volume * 1e-3
    vapour = (final - pressure * T1 / T0) * 1e3
    return 0.018 * V ** (1 / 3) * vapour / ((36 * pi) ** (1 / 3) * 1000 * R * T1) * 1e6


def check(volume=1.0, pressure=100.0, final=129.0, start=27.0, end=100.0, R=8.314):
    # Moles of each gas, the liquid's volume, and the sphere's radius by bisection.
    from otk.sheets.tpho2558_physics._shared import bisect

    T0, T1 = start + 273.15, end + 273.15
    V = volume * 1e-3
    gas = pressure * 1e3 * V / (R * T0)
    total = final * 1e3 * V / (R * T1)
    water = (total - gas) * 0.018 / 1000
    radius = bisect(lambda r: 4 / 3 * pi * r**3 - V, 0.0, 10.0)
    return water / (4 * pi * radius**2) * 1e6


PARAMS = {"volume": 1.0, "pressure": 100.0, "final": 129.0, "start": 27.0, "end": 100.0, "R": 8.314}
VARIANTS = [{"final": 135.0}, {"volume": 5.0, "final": 131.0}, {"end": 120.0, "final": 140.0}]
ANSWER = 0.5613476713503127
TOL = 1e-9
