"""Theory 2.1-2.2, 2.7: dry air rising adiabatically keeps T proportional to p^(2/7) (gamma = 7/5), so T1 = T0 (p1/p0)^(2/7) = 279 K = 5.94 C for 20.0 C at 100 kPa and 84.2 kPa. Adapted: the ground temperature (C) and both pressures (kPa) vary; returns Celsius."""


def solve(ground=20.0, base=100.0, station=84.2):
    return (ground + 273.15) * (station / base) ** (2 / 7) - 273.15


def check(ground=20.0, base=100.0, station=84.2, steps=20000):
    # integrate dT/dp = (1 - 1/gamma) T/p with gamma = c_p/c_V = 7/5
    t, p = ground + 273.15, base
    dp = (base - station) / steps
    for _ in range(steps):
        k1 = (2 / 7) * t / p
        k2 = (2 / 7) * (t - k1 * dp) / (p - dp)
        t -= dp * (k1 + k2) / 2
        p -= dp
    return t - 273.15


PARAMS = {"ground": 20.0, "base": 100.0, "station": 84.2}
VARIANTS = [{"ground": 30.0}, {"station": 70.0}, {"base": 101.3}]
ANSWER = 5.943997444741342
TOL = 1e-6
