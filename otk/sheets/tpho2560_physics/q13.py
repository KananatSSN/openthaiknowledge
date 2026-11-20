"""Theory 3 A.2-A.4 figures 3.2-3.4: two long wires 2R apart with opposite currents give B = (mu0 I/2 pi R)(2 + 2x^2/R^2) near the axis, so B = mu0 I/(pi R) on it; N dipoles of length D each turn the beam by 2 pi/N on radius rho = mv/(qB) = ND/(2 pi), so I = 2 pi^2 R m v/(mu0 N D q) = 1.14e4 A for 4.0 MeV protons, D = 2.0 m, R = 5.0 cm, N = 10. Adapted: E (MeV), D (m), R (cm) and N vary; returns I in kA."""

from math import pi, sqrt

MU0, Q, M = 4e-7 * pi, 1.6e-19, 1.67e-27


def solve(energy=4.0, length=2.0, radius=5.0, count=10):
    v = sqrt(2 * energy * 1e6 * Q / M)
    return 2 * pi**2 * radius * 1e-2 * M * v / (MU0 * count * length * Q) / 1e3


def check(energy=4.0, length=2.0, radius=5.0, count=10):
    # Field at the centre from the two wires by Biot-Savart (finite length D,
    # summed in segments), then bisect the current that bends the beam 2 pi/N
    # over the dipole's length.
    from otk.sheets.tpho2560_physics._shared import bisect

    v = sqrt(2 * energy * 1e6 * Q / M)
    R = radius * 1e-2
    n = 2000

    def field(current):
        total = 0.0
        for i in range(n):
            z = -length / 2 + (i + 0.5) * length / n
            total += 2 * MU0 * current / (4 * pi) * R * (length / n) / (R * R + z * z) ** 1.5
        return total

    def bend(current):
        return Q * field(current) * length / (M * v) - 2 * pi / count

    return bisect(bend, 0.0, 1e7) / 1e3


PARAMS = {"energy": 4.0, "length": 2.0, "radius": 5.0, "count": 10}
VARIANTS = [{"count": 20}, {"energy": 9.0}, {"radius": 3.0, "length": 3.0}]
ANSWER = 11.347576610028359
TOL = 5e-3
