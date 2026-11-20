"""Theory 3.7 figure: a blade of length 2r pressed with N spread evenly has friction mu N/(2r) per length; each half resists with torque integral of (mu N/(2r)) x dx from 0 to r, so the total is mu r N/2 and k = mu r/2. Adapted: mu and r (mm) vary; returns k in mm."""


def solve(mu=0.4, radius=3.0):
    return mu * radius / 2


def check(mu=0.4, radius=3.0, load=10.0):
    # Sum the friction torque over many small pieces of the blade.
    n = 2000
    piece = 2 * radius / n
    torque = sum(mu * load / (2 * radius) * piece * abs(-radius + (i + 0.5) * piece) for i in range(n))
    return torque / load


PARAMS = {"mu": 0.4, "radius": 3.0}
VARIANTS = [{"mu": 0.6}, {"radius": 5.0}, {"mu": 0.25, "radius": 2.0}]
ANSWER = 0.6000000000000001
TOL = 1e-9
