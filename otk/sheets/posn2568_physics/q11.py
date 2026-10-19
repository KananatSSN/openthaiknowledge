"""Short11 figure: a bucket of water (depth h, density rho, open to air) is hauled up with acceleration a; bottom pressure P_a + rho (g + a) h. Pascals."""


def solve(depth=0.5, accel=2, atmosphere=1e5, density=1000, g=10):
    return atmosphere + density * (g + accel) * depth


def check(depth=0.5, accel=2, atmosphere=1e5, density=1000, g=10, area=0.01):
    # Newton's second law for the water column: (P - P_a) A - m g = m a.
    mass = density * area * depth
    return atmosphere + mass * (g + accel) / area


PARAMS = {"depth": 0.5, "accel": 2, "atmosphere": 1e5, "density": 1000, "g": 10}
VARIANTS = [{"accel": 0}, {"depth": 1.2, "accel": 5}, {"accel": -3}]
ANSWER = 106000.0
