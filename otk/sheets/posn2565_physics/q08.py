"""MC8 figure: uniform heavy rope of mass M hangs from O, where it is horizontal, to A, where it makes theta with the horizontal. Horizontal tension H = Mg cot theta (answer 1). Newtons, g = 10; angle given by its sine."""

from math import asinh, sinh, sqrt


def solve(mass=3, sine=0.6, g=10):
    cosine = sqrt(1 - sine * sine)
    return mass * g * cosine / sine


def check(mass=3, sine=0.6, g=10):
    # Catenary y = c cosh(x/c) with weight per length w = 1: the slope at A is
    # sinh(x_A/c) = tan(theta), arc length from O is c sinh(x_A/c), and H = w c.
    # Fix the arc length to M g (w = 1 N/m), solve for c by bisection.
    tan_a = sine / sqrt(1 - sine * sine)
    lo, hi = 1e-6, 1e6
    for _ in range(300):
        c = (lo + hi) / 2
        x_a = c * asinh(tan_a)
        if c * sinh(x_a / c) < mass * g:
            lo = c
        else:
            hi = c
    c = (lo + hi) / 2
    return c  # H = w c with w = 1 N/m


PARAMS = {"mass": 3, "sine": 0.6, "g": 10}
VARIANTS = [{"sine": 0.8}, {"mass": 12, "sine": 5 / 13}, {"mass": 1, "sine": 0.5}]
ANSWER = 40.0
