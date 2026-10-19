"""MC24: surface waves v^2 = lambda g/(2 pi) + 2 pi S/(lambda rho). For small lambda only the tension term stays, f = v/lambda gives lambda^(3/2) f = constant (answer 3). Adapted: two capillary waves; return f2/f1 = (lambda1/lambda2)^(3/2)."""

from math import pi, sqrt

TENSION = 0.073
DENSITY = 1000


def solve(ratio=4):
    """ratio = lambda1 / lambda2."""
    return ratio**1.5


def check(ratio=4):
    # Absolute frequencies of two very short waves from the tension term alone.
    freq = lambda lam: sqrt(2 * pi * TENSION / (lam * DENSITY)) / lam
    lam1 = 1e-4
    return freq(lam1 / ratio) / freq(lam1)


PARAMS = {"ratio": 4}
VARIANTS = [{"ratio": 0.25}, {"ratio": 9}, {"ratio": 4 / 9}]
ANSWER = 8.0
