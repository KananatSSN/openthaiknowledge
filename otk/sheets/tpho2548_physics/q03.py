"""Theory 1.2: with M_B at rest, M_B takes the fraction 4 M_A M_B/(M_A + M_B)^2 of M_A's kinetic energy (M_A keeps ((M_B - M_A)/(M_A + M_B))^2). Adapted: numbers for the masses."""


def solve(mass_a=2, mass_b=3):
    return 4 * mass_a * mass_b / (mass_a + mass_b) ** 2


def check(mass_a=2, mass_b=3, speed=1.0):
    # Kinetic energies from the collision velocities, as 1 minus what A keeps.
    va = (mass_a - mass_b) * speed / (mass_a + mass_b)
    return 1 - va * va / (speed * speed)


PARAMS = {"mass_a": 2, "mass_b": 3}
VARIANTS = [{"mass_a": 3, "mass_b": 3}, {"mass_a": 1, "mass_b": 100}, {"mass_a": 7, "mass_b": 2}]
ANSWER = 0.96
TOL = 1e-9
