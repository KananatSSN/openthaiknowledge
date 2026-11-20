"""Theory 2 (a) figure: the gas stops flowing when B's pressure equals A's, which the weight on A's light piston fixes at P_B = mg/a in the vacuum around the cylinders. Adapted: m (kg) and a (cm^2) vary; returns P_B in kPa with g = 9.8."""


def solve(mass=5.0, area=50.0, g=9.8):
    return mass * g / (area * 1e-4) / 1e3


def check(mass=5.0, area=50.0, g=9.8):
    # Bisect the pressure that holds A's piston still.
    lo, hi = 0.0, 1e9
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid * area * 1e-4 < mass * g:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2 / 1e3


PARAMS = {"mass": 5.0, "area": 50.0, "g": 9.8}
VARIANTS = [{"mass": 12.0}, {"area": 20.0}, {"mass": 2.0, "area": 80.0}]
ANSWER = 9.8
TOL = 1e-9
