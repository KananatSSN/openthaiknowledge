"""Theory 3.1 (g)-(h): the stopped water reaches P = P_a + rho v u + rho u^2 and can hold a column h' = (P - P_a)/(rho g) = v u/g + u^2/g = v sqrt(2 h0/g) + 2 h0. Adapted: h0 and v vary; returns h' in metres with g = 9.8."""

from math import sqrt


def solve(head=2.0, sound=1480.0, g=9.8):
    u = sqrt(2 * g * head)
    return sound * u / g + u * u / g


def check(head=2.0, sound=1480.0, g=9.8):
    # Bisect the column height whose hydrostatic pressure matches the jump
    # rho (v + u) u found from the momentum balance.
    from otk.sheets.tpho2557_physics._shared import bisect

    u = sqrt(2 * g * head)
    jump = 1000 * (sound + u) * u
    return bisect(lambda h: 1000 * g * h - jump, 0.0, 1e5)


PARAMS = {"head": 2.0, "sound": 1480.0, "g": 9.8}
VARIANTS = [{"head": 5.0}, {"sound": 1400.0}, {"head": 0.8}]
ANSWER = 949.5373161999111
TOL = 1e-9
