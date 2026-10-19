"""MC1 figure: a ring of mass m slides loosely down a hanging rope with acceleration a; friction m(g - a) (answer 4). Newtons, g = 10."""


def solve(mass=2, accel=6, g=10):
    return mass * (g - accel)


def check(mass=2, accel=6, g=10):
    # Bisect on the friction until Newton's second law gives the observed a.
    lo, hi = 0.0, mass * g
    for _ in range(200):
        f = (lo + hi) / 2
        if (mass * g - f) / mass > accel:
            lo = f
        else:
            hi = f
    return (lo + hi) / 2


PARAMS = {"mass": 2, "accel": 6, "g": 10}
VARIANTS = [{"accel": 2}, {"mass": 5, "accel": 9}, {"mass": 0.5, "accel": 0}]
ANSWER = 8
