"""Short1 figure: A is the top of a vertical circle of centre C; B is on the circle level with C. Sliding from rest along the smooth chord AB takes 2 sqrt(R/g); free fall from A to C takes sqrt(2R/g); ratio sqrt2. Adapted: compare with free fall through k R; ratio sqrt(2/k)."""

from math import sqrt


def solve(depth=1):
    return sqrt(2 / depth)


def check(depth=1, radius=10.0, g=10.0):
    # Step the slide along the chord from the top to the level of C, and time
    # a free fall through depth*R, both by small time steps.
    def timed(length, accel):
        dt, s, v, t = 1e-5, 0.0, 0.0, 0.0
        while s < length:
            v += accel * dt
            s += v * dt
            t += dt
        return t - (s - length) / v

    chord = radius * sqrt(2)
    slide = timed(chord, g * radius / chord)  # g cos(angle to vertical)
    fall = timed(depth * radius, g)
    return slide / fall


PARAMS = {"depth": 1}
VARIANTS = [{"depth": 2}, {"depth": 0.5}, {"depth": 1.5}]
TOL = 1e-4
ANSWER = 1.4142135623730951
