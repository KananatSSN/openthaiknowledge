"""MC2 figure: pendulum of length l with a peg on the vertical a distance p l below the pivot; small swings. Half a cycle on each length: T = pi sqrt(l/g) + pi sqrt((1 - p) l/g), i.e. (1 + sqrt(1 - p))/2 of 2 pi sqrt(l/g); p = 1/2 gives (sqrt2 + 1)/sqrt8 (answer 1)."""

from math import pi, sqrt


def solve(peg=0.5):
    return (1 + sqrt(1 - peg)) / 2


def check(peg=0.5, length=1.0, g=10.0):
    # Integrate the small-angle motion: length l on the left (angle < 0),
    # (1 - p) l on the right; time one full cycle from the lowest point.
    def half_period(effective):
        angle, rate, t, dt = 0.0, 1e-3, 0.0, 1e-5
        started = False
        while True:
            rate -= g / effective * angle * dt
            angle += rate * dt
            t += dt
            if angle > 0:
                started = True
            elif started:
                return t

    full = half_period(length) + half_period((1 - peg) * length)
    return full / (2 * pi * sqrt(length / g))


PARAMS = {"peg": 0.5}
VARIANTS = [{"peg": 0.75}, {"peg": 5 / 9}, {"peg": 16 / 25}]
TOL = 1e-4
ANSWER = 0.8535533905932737
