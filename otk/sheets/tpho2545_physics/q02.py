"""Theory I.2a figure: rod ef slides at v0 across rails L apart in field B; the emf is v0 L B whatever the rod's tilt theta. Volts."""

from math import radians, tan


def solve(speed=4, separation=0.5, field=0.2, tilt=30):
    return speed * separation * field


def check(speed=4, separation=0.5, field=0.2, tilt=30):
    # Flux through the circuit: the polygon from the resistor end (x = 0) to
    # the tilted rod, by the shoelace formula, at two nearby times.
    def area(x):
        shift = separation * tan(radians(tilt))
        pts = [(0.0, 0.0), (x, 0.0), (x + shift, separation), (0.0, separation)]
        return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2

    dt = 1e-6
    x0 = 1.0
    return field * (area(x0 + speed * dt) - area(x0)) / dt

PARAMS = {"speed": 4, "separation": 0.5, "field": 0.2, "tilt": 30}
VARIANTS = [{"tilt": 0}, {"speed": 10, "field": 0.5}, {"tilt": 60, "separation": 1.2}]
ANSWER = 0.4
