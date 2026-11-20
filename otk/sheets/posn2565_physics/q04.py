"""MC4 figure: concentric metal spheres; the inner (radius R1) holds -Q; the outer (radius R2) is earthed and carries induced +Q on its inner surface. V_outer - V_inner = kQ(1/R1 - 1/R2) (answer 2). Units: nC, cm, volts, k = 9e9."""

K = 9e9


def solve(charge=2, inner=3, outer=6):
    q = charge * 1e-9
    return K * q * (1 / (inner / 100) - 1 / (outer / 100))


def check(charge=2, inner=3, outer=6):
    # Integrate the field between the spheres (inner charge only, Gauss) from
    # R1 to R2 by Simpson's rule; the outer sphere is at zero potential.
    q = -charge * 1e-9
    a, b = inner / 100, outer / 100
    n = 2000
    h = (b - a) / n
    total = 0.0
    for k in range(n + 1):
        r = a + k * h
        w = 1 if k in (0, n) else (4 if k % 2 else 2)
        total += w * K * q / (r * r)
    v_inner = total * h / 3  # V(R1) - V(R2) = integral of E dr
    return 0 - v_inner


PARAMS = {"charge": 2, "inner": 3, "outer": 6}
VARIANTS = [{"charge": 5, "inner": 2, "outer": 10}, {"inner": 4, "outer": 5}, {"charge": 1, "outer": 9}]
TOL = 1e-9
ANSWER = 300.0
