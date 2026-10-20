"""Theory 2.3 figure: a square loop (side L, each side resistance r, mass m) slides on smooth rails touching them at the midpoints of ab and cd; a resistor R joins the rails. Both vertical sides carry emf vBL, as two cells of internal resistance 2r in parallel (emf vBL, internal r), so I = (BLv0/(r + R)) e^(-B^2 L^2 t/(m (r + R))). Adapted: numbers for B, L, v0, m, r, R, t; amperes."""

from math import exp


def solve(field=0.5, side=0.2, speed=4, mass=0.01, wire=1, resistor=3, time=0.4):
    total = wire + resistor
    return field * side * speed / total * exp(-(field * side) ** 2 * time / (mass * total))


def check(field=0.5, side=0.2, speed=4, mass=0.01, wire=1, resistor=3, time=0.4):
    # Solve the two-loop circuit by nodal analysis at each step: left half
    # (emf, 2r) and right half (emf, 2r) in parallel across R; force on both
    # vertical sides; Euler steps for the velocity.
    v, dt = float(speed), time / 200000

    def current(v):
        emf = v * field * side
        # node voltage U across R: (emf - U)/(2r) * 2 = U/R
        u = 2 * emf / (2 * wire) / (2 / (2 * wire) + 1 / resistor)
        return u / resistor

    for _ in range(200000):
        v -= current(v) * side * field / mass * dt
    return current(v)


PARAMS = {"field": 0.5, "side": 0.2, "speed": 4, "mass": 0.01, "wire": 1, "resistor": 3, "time": 0.4}
VARIANTS = [{"time": 0}, {"field": 1, "resistor": 1}, {"mass": 0.05, "wire": 0.5}]
ANSWER = 0.09048374180359596
TOL = 1e-4
