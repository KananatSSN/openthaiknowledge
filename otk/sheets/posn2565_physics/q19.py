"""MC19 figure: a light ball (mass m, volume V) tied to the bottom of a water tank; the string snaps. Initial upward acceleration (rho V / m - 1) g (answer 4), with no drag and no added mass. Grams, cm^3, g = 10."""


def solve(mass=2, volume=10, density=1, g=10):
    return (density * volume / mass - 1) * g


def check(mass=2, volume=10, density=1, g=10):
    # Before the cut: tension T = buoyancy - weight. After the cut the net
    # force is exactly the vanished tension, upward.
    buoyancy = density * volume / 1000 * g
    weight = mass / 1000 * g
    tension = buoyancy - weight
    return tension / (mass / 1000)


PARAMS = {"mass": 2, "volume": 10, "density": 1, "g": 10}
VARIANTS = [{"mass": 5}, {"mass": 3, "volume": 12}, {"volume": 40, "mass": 8}]
ANSWER = 40.0
