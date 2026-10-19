"""MC1: A = B 2^(-(m v^2 / C)) with m in kg and v in m/s. The exponent must be dimensionless, so C carries the units of m v^2: kg m^2 s^-2 = joule (answer 1). Adapted: the exponent holds m^a v^b; returns C's SI exponents (kg, m, s) = (a, b, -b)."""

from itertools import product


def solve(mass_power=1, speed_power=2):
    return (mass_power, speed_power, -speed_power)


def check(mass_power=1, speed_power=2):
    # Brute-force the (kg, m, s) exponents that leave the exponent dimensionless.
    top = (mass_power, speed_power, -speed_power)
    found = [c for c in product(range(-6, 7), repeat=3) if all(t - x == 0 for t, x in zip(top, c))]
    assert len(found) == 1
    return found[0]


PARAMS = {"mass_power": 1, "speed_power": 2}
VARIANTS = [{"speed_power": 1}, {"mass_power": 2, "speed_power": 3}, {"speed_power": 4}]
ANSWER = (1, 2, -2)
