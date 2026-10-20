"""Theory 2.3: thermally insulated, displaced down by y the gas (helium, gamma = 5/3) is compressed adiabatically by y(A - a): to first order the net upward force is P0 gamma (A - a)^2 y/V0. Adapted: numbers; newtons."""


def solve(pressure=1.049e5, volume=0.002, big=0.05, small=0.01, shift=0.001, gamma=5 / 3):
    return pressure * gamma * (big - small) ** 2 * shift / volume


def check(pressure=1.049e5, volume=0.002, big=0.05, small=0.01, shift=0.001, gamma=5 / 3):
    # Exact adiabatic pressure change, linearised by a tiny displacement and
    # scaled to the given one.
    h = shift * 1e-4
    p = pressure * (volume / (volume - h * (big - small))) ** gamma
    return (p - pressure) * (big - small) * shift / h


PARAMS = {"pressure": 1.049e5, "volume": 0.002, "big": 0.05, "small": 0.01, "shift": 0.001, "gamma": 5 / 3}
VARIANTS = [{"shift": 0.002}, {"volume": 0.005}, {"big": 0.03, "small": 0.02}]
ANSWER = 139.86666666666667
TOL = 1e-4
