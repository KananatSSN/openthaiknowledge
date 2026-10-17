"""MC2 figure: monkey64kg on left rope end, counterweight34kg right, ideal fixed pulley. Monkey descends6m from rest while holding end without sliding. g9.8, final speed6m/s."""

from math import sqrt
import numpy as np


def solve(heavy=64, light=34, height=6, g=9.8):
    if heavy <= light:
        raise ValueError("left mass must descend")
    return sqrt(2 * g * height * (heavy - light) / (heavy + light))


def check(heavy=64, light=34, height=6, g=9.8):
    # Independently solve the two Newton equations, then integrate acceleration.
    tension, acceleration = np.linalg.solve([[1, heavy], [1, -light]], [heavy * g, light * g])
    assert tension > 0 and acceleration > 0
    lo, hi = 0.0, 1 + 2 * height / acceleration
    for _ in range(100):
        time = (lo + hi) / 2
        if acceleration * time * time / 2 < height:
            lo = time
        else:
            hi = time
    return float(acceleration * (lo + hi) / 2)


PARAMS = {"heavy": 64, "light": 34, "height": 6, "g": 9.8}
VARIANTS = [{"height": 3}, {"heavy": 60, "light": 20}, {"light": 24}]
ANSWER = 6.000000000000001
