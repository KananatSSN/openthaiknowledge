"""Written5 graph: tennisball50g incoming8m/s, bat force oppositeincoming piecewise linear(0ms,100N),(10ms,200N),(15ms,0). Impulse2Ns, outgoing32m/s. Horizontal brief contact, neglect other impulse."""

from fractions import Fraction


def solve(mass_g=50, incoming=8, first_force=100, peak=200, rise_ms=10, fall_ms=5):
    impulse = Fraction((first_force + peak) * rise_ms + peak * fall_ms, 2000)
    return impulse / Fraction(mass_g, 1000) - incoming


def check(mass_g=50, incoming=8, first_force=100, peak=200, rise_ms=10, fall_ms=5):
    velocity = -float(incoming)
    for start, end, duration in ((first_force, peak, rise_ms), (peak, 0, fall_ms)):
        dt = duration / 1000 / 1000
        for i in range(1000):
            force = start + (end - start) * (i + 0.5) / 1000
            velocity += force * dt / (mass_g / 1000)
    return velocity


PARAMS = {"mass_g": 50, "incoming": 8, "first_force": 100, "peak": 200, "rise_ms": 10, "fall_ms": 5}
VARIANTS = [{"mass_g": 100}, {"incoming": 10}, {"peak": 300}]
ANSWER = Fraction(32, 1)
