"""Theory 1.3: at the best intermediate mass m = sqrt(M_A M_B) the fraction of M_A's energy reaching M_B is 16 M_A M_B m^2/((M_A + m)^2 (m + M_B)^2) = 16 M_A M_B/(sqrt M_A + sqrt M_B)^4. Adapted: numbers for M_A and M_B."""

from math import sqrt


def solve(mass_a=2, mass_b=8):
    return 16 * mass_a * mass_b / (sqrt(mass_a) + sqrt(mass_b)) ** 4


def check(mass_a=2, mass_b=8, speed=1.0):
    # Run the two collisions with velocities and compare kinetic energies.
    m = sqrt(mass_a * mass_b)
    v_mid = 2 * mass_a * speed / (mass_a + m)
    v_b = 2 * m * v_mid / (m + mass_b)
    return mass_b * v_b**2 / (mass_a * speed**2)


PARAMS = {"mass_a": 2, "mass_b": 8}
VARIANTS = [{"mass_a": 3, "mass_b": 3}, {"mass_a": 1, "mass_b": 81}, {"mass_a": 9, "mass_b": 4}]
ANSWER = 0.7901234567901231
TOL = 1e-9
