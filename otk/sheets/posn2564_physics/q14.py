"""MC14: ideal gas at constant T, small change: dP/dV = -P/V (answer 2). Returns the slope in kPa per litre."""


def solve(pressure=100, volume=2):
    return -pressure / volume


def check(pressure=100, volume=2):
    # Boyle's law PV = const, central finite difference.
    product = pressure * volume
    h = 1e-6 * volume
    return (product / (volume + h) - product / (volume - h)) / (2 * h)


PARAMS = {"pressure": 100, "volume": 2}
VARIANTS = [{"pressure": 150, "volume": 3}, {"volume": 5}, {"pressure": 80, "volume": 0.5}]
TOL = 1e-6
ANSWER = -50.0
