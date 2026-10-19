"""MC2: Earth's radius halves while its mass stays the same; surface g becomes 4 times (answer 4). Adapted: mass scaled by mass_factor, radius by radius_factor; g' / g = mass_factor / radius_factor**2."""

G = 6.674e-11
EARTH_MASS = 5.97e24
EARTH_RADIUS = 6.371e6


def solve(mass_factor=1, radius_factor=0.5):
    return mass_factor / radius_factor**2


def check(mass_factor=1, radius_factor=0.5):
    # Newton's law with real constants, then the ratio of the two surface fields.
    old = G * EARTH_MASS / EARTH_RADIUS**2
    new = G * EARTH_MASS * mass_factor / (EARTH_RADIUS * radius_factor) ** 2
    return new / old


PARAMS = {"mass_factor": 1, "radius_factor": 0.5}
VARIANTS = [{"mass_factor": 2, "radius_factor": 2}, {"radius_factor": 1 / 3}, {"mass_factor": 3}]
ANSWER = 4.0
