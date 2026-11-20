"""Theory 3.1 figure (a): a thin shell of radius xi and thickness d xi in a uniformly charged ball (density rho) gives the potential dV = rho xi d xi/eps0 at any point inside it (r < xi). Adapted: returns dV in units of rho/eps0 (lengths in m)."""

from math import cos, pi, sin, sqrt


def solve(shell=0.5, thickness=0.01, point=0.2):
    return shell * thickness


def check(shell=0.5, thickness=0.01, point=0.2):
    # Coulomb's law summed over the shell's rings (Simpson in the polar
    # angle), with rho = eps0 = 1.
    n = 2000
    h = pi / n
    total = 0.0
    for k in range(n + 1):
        a = k * h
        ring = 2 * pi * shell**2 * thickness * sin(a)
        dist = sqrt(shell**2 + point**2 - 2 * shell * point * cos(a))
        weight = 1 if k in (0, n) else (4 if k % 2 else 2)
        total += weight * ring / (4 * pi * dist)
    return total * h / 3


PARAMS = {"shell": 0.5, "thickness": 0.01, "point": 0.2}
VARIANTS = [{"point": 0}, {"shell": 2, "thickness": 0.05, "point": 1.5}, {"point": 0.45}]
ANSWER = 0.005
TOL = 1e-6
