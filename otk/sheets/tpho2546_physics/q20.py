"""Lab 2, part 2.1: a spherical cavity gives the same moment of inertia in both hangings (I1' = I2' = rho a^5/6 - 8 pi rho b^5/15); a cylindrical one does not (I1 = rho a^5/6 - pi rho a b^4/2, I2 = rho a^5/6 - pi rho a^3 b^2/12 - pi rho a b^4/4 < I1). Adapted: the two moments of inertia from synthetic periods; returns 'sphere' or 'cylinder'."""

from math import pi


def solve(side=4, density=8.5, first=1436.425, second=1436.425):
    return "sphere" if abs(first - second) <= 1e-3 * first else "cylinder"


def check(side=4, density=8.5, first=1436.425, second=1436.425):
    # Test the cylinder hypothesis: take b from hanging (a), predict hanging
    # (b), and see whether the prediction matches the measurement.
    full = density * side**5 / 6
    b4 = 2 * (full - first) / (pi * density * side)
    b = b4**0.25
    predicted = full - pi * density * side**3 * b * b / 12 - pi * density * side * b4 / 4
    if abs(predicted - second) <= 1e-3 * first and abs(first - second) > 1e-3 * first:
        return "cylinder"
    return "sphere"


PARAMS = {"side": 4, "density": 8.5, "first": 1436.425, "second": 1436.425}
VARIANTS = [{"first": 1397.26, "second": 1281.544}, {"side": 5, "first": 4318.934, "second": 4318.934}, {"first": 1180.293, "second": 995.038}]
ANSWER = 'sphere'
