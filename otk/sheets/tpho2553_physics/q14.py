"""Lab 2 figures 1-2: student 3 models the seiche as the centre of mass of the water shifting under the pressure difference of the tilted surface, T = 2 pi sqrt(L^2/(12 g H)). Adapted: tank length L and depth H in cm; seconds with g = 9.8."""

from math import pi, sqrt


def solve(length=51.0, depth=5.0, g=9.8):
    return 2 * pi * sqrt((length / 100) ** 2 / (12 * g * depth / 100))


def check(length=51.0, depth=5.0, g=9.8):
    # Student 3's model as energies: tilt the flat surface by x at the walls;
    # the hydrostatic potential energy (numerical sum over columns) gives the
    # stiffness, and the water's kinetic energy is that of its centre of mass,
    # which shifts sideways in proportion to x.
    L, H = length / 100, depth / 100
    n = 4000
    def potential(x):
        # surface y = H + x (2u/L - 1), u in [0, L]; PE per unit width
        total = 0.0
        for i in range(n):
            u = (i + 0.5) * L / n
            h = H + x * (2 * u / L - 1)
            total += 0.5 * g * h * h * L / n
        return total

    def com_shift(x):
        mass = H * L
        moment = 0.0
        for i in range(n):
            u = (i + 0.5) * L / n
            h = H + x * (2 * u / L - 1)
            moment += h * (u - L / 2) * L / n
        return moment / mass

    h = 1e-4
    stiffness = (potential(h) - 2 * potential(0) + potential(-h)) / h**2   # per rho per width
    shift = com_shift(h) / h                                            # dX/dx
    mass = H * L
    return 2 * pi * sqrt(mass * shift**2 / stiffness)


PARAMS = {"length": 51.0, "depth": 5.0, "g": 9.8}
VARIANTS = [{"depth": 2.0}, {"length": 30.0, "depth": 8.0}, {"depth": 10.0}]
ANSWER = 1.321482393942073
TOL = 1e-4
