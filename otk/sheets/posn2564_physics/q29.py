"""Short29 figure: wedge ABC, mass M, on smooth level ground; m slides down smooth face AB (angle theta at B) with speed v relative to the wedge. Both start at rest. Horizontal momentum gives V = m v cos theta / (m + M), wedge recoiling left. Cosine given."""

from math import sqrt


def solve(small=1, big=4, speed=5, cosine=0.8):
    return small * speed * cosine / (small + big)


def check(small=1, big=4, speed=5, cosine=0.8, g=10):
    # Newton's laws for constant accelerations: unknowns N, A (wedge, left) and
    # s (block along the face, relative). Block: horizontal m(s cos - A) = N sin,
    # vertical m(-s sin) = N cos - m g; wedge: M A = N sin. Solve, then V/v = A/s.
    sine = sqrt(1 - cosine * cosine)
    # From the wedge equation N = M A / sin; substitute into the other two.
    # m s cos - m A = M A  ->  s = A (m + M) / (m cos)
    # -m s sin = M A cos / sin - m g  -> linear in A.
    coeff = small * sine * (small + big) / (small * cosine) + big * cosine / sine
    accel_wedge = small * g / coeff
    accel_rel = accel_wedge * (small + big) / (small * cosine)
    normal = big * accel_wedge / sine
    assert normal > 0
    return speed * accel_wedge / accel_rel


PARAMS = {"small": 1, "big": 4, "speed": 5, "cosine": 0.8}
VARIANTS = [{"cosine": 0.6}, {"small": 2, "big": 3, "speed": 10}, {"big": 1, "cosine": 0.5}]
ANSWER = 0.8
