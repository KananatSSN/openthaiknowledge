"""Lab 1 (parallel-plate capacitor) parts 2-3: with X_C >> R the current is I = V omega C, and C = (kappa eps0/d) A, so kappa eps0/d = I/(2 pi f V A). Adapted: one synthetic reading of V_rms, I_rms and plate area A at 50 Hz; F/m^2."""

from math import pi


def solve(voltage=10, current=5e-5, area=0.06, frequency=50):
    return current / (2 * pi * frequency * voltage * area)


def check(voltage=10, current=5e-5, area=0.06, frequency=50):
    # Bisect on kappa eps0/d until the capacitor's reactance (with the 200 ohm
    # series resistor, negligible here) draws the measured current.
    def drawn(per_area):
        c = per_area * area
        z = abs(complex(200, -1 / (2 * pi * frequency * c)))
        return voltage / z

    lo, hi = 1e-15, 1.0
    for _ in range(300):
        mid = (lo * hi) ** 0.5
        lo, hi = (mid, hi) if drawn(mid) < current else (lo, mid)
    return lo


PARAMS = {"voltage": 10, "current": 5e-5, "area": 0.06, "frequency": 50}
VARIANTS = [{"area": 0.03}, {"voltage": 20, "current": 1e-4}, {"current": 2e-5, "area": 0.1}]
ANSWER = 2.652582384864922e-07
TOL = 1e-6
