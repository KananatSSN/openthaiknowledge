"""MC20: fixed object-screen separation25cm, convex lens f6cm. Two positions u10,v15 and u15,v10. Magnified REAL image selectsu10. Adaptation preserves the magnification condition; source contains no physical diagram to attach."""

from math import sqrt


def solve(distance=25, focal=6):
    if distance <= 4 * focal:
        raise ValueError("requires distinct real image positions")
    return (distance - sqrt(distance**2 - 4 * focal * distance)) / 2


def check(distance=25, focal=6):
    lo, hi = focal * (1 + 1e-10), distance / 2
    for _ in range(100):
        u = (lo + hi) / 2
        predicted_image = focal * u / (u - focal)
        actual_image = distance - u
        if predicted_image > actual_image:
            lo = u
        else:
            hi = u
    u = (lo + hi) / 2
    assert (distance - u) / u > 1
    return u


PARAMS = {"distance": 25, "focal": 6}
VARIANTS = [
    {"distance": 50, "focal": 12},
    {"distance": 36, "focal": 8},
    {"distance": 45, "focal": 10},
]
ANSWER = 10.0
