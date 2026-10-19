"""Short19 figure: uniform slenderrod length2l falls fromnearlyvertical rest on perfectlysmooth horizontalfloor. Lowerend slides, CM horizontalmomentum remainszero. In limiting initialtilt0, CM speed justbeforehorizontal=sqrt(3gl/2). The lowerendpoint is not fixed. General initialanglefromvertical allowed."""

from math import sqrt, cos, radians


def solve(half_length=1, g=10, initial_angle=0):
    return sqrt(1.5 * g * half_length * cos(radians(initial_angle)))


def check(half_length=1, g=10, initial_angle=0):
    # Simpson integrate the actual rod's rotational inertia about its CM.
    count = 1000
    ds = 2 * half_length / count
    moment = 0.0
    for i in range(count + 1):
        coordinate = -half_length + i * ds
        weight = 1 if i in (0, count) else (4 if i % 2 else 2)
        moment += weight * coordinate**2 * ds / (6 * half_length)
    available = g * half_length * cos(radians(initial_angle))
    lo, hi = 0.0, 100.0
    for _ in range(100):
        speed = (lo + hi) / 2
        omega = speed / half_length  # geometric ground-contact constraint at horizontal
        kinetic = speed**2 / 2 + moment * omega**2 / 2
        if kinetic < available:
            lo = speed
        else:
            hi = speed
    return (lo + hi) / 2


PARAMS = {"half_length": 1, "g": 10, "initial_angle": 0}
VARIANTS = [{"half_length": 2}, {"g": 9.8}, {"initial_angle": 30}]
ANSWER = 3.872983346207417
