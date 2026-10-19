"""MC2 figure: thin diverging lens f_lens=-f, incident ray at height h; paraxial change in direction magnitude h/f radians. Incident ray need not be parallel. Adaptation explicitly asks slope-angle change in paraxial approximation."""

from fractions import Fraction


def solve(height=1, focal=10, object_distance=30):
    return Fraction(height) / Fraction(focal)


def check(height=1, focal=10, object_distance=30):
    # Independent virtual axial image construction for a finite real object.
    u = Fraction(object_distance)
    image = -1 / (1 / Fraction(focal) + 1 / u)
    slope_in = Fraction(height) / u
    slope_out = -Fraction(height) / image
    return slope_out - slope_in


PARAMS = {"height": 1, "focal": 10, "object_distance": 30}
VARIANTS = [{"height": 2}, {"focal": 20}, {"object_distance": 50}]
ANSWER = Fraction(1, 10)
