"""Theory 2.3: with m2 at the midpoint, eliminating omega between the whole system and m1 alone gives (m1/(m1 + m2)) sin^2(beta)/cos(beta) = sin(alpha) tan(beta) - tan(alpha) sin(beta) + tan(alpha) sin(alpha), so A = m1/(m1 + m2), B = 1, C = -1, D = 1. Adapted: the masses vary; returns (A, B, C, D)."""


def solve(m1=2.0, m2=1.0):
    return (m1 / (m1 + m2), 1.0, -1.0, 1.0)


def check(m1=2.0, m2=1.0):
    # Solve Newton's laws for beta at three upper angles, then find A, C, D
    # with B = 1 from the three equations A s - C u - D w = v (Cramer's rule).
    from math import cos, sin, tan

    from otk.sheets.tpho2554_physics._spin import beta_fixed

    a_max = 0.9 * m1 / (m1 + m2)          # need sin(alpha) < m1/(m1 + m2)
    rows = []
    for frac in (0.3, 0.6, 0.9):
        alpha = frac * a_max
        beta = beta_fixed(alpha, m1, m2)
        rows.append((sin(beta) ** 2 / cos(beta), tan(alpha) * sin(beta), tan(alpha) * sin(alpha), sin(alpha) * tan(beta)))
    # A s + C' u + D' w = v with C' = -C, D' = -D
    def det(m):
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1])
                - m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0])
                + m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))
    M = [[s, u, w] for s, u, w, _ in rows]
    rhs = [v for *_, v in rows]
    d = det(M)
    sol = []
    for j in range(3):
        Mj = [row[:] for row in M]
        for i in range(3):
            Mj[i][j] = rhs[i]
        sol.append(det(Mj) / d)
    A, Cp, Dp = sol
    return (A, 1.0, -Cp, -Dp)


PARAMS = {"m1": 2.0, "m2": 1.0}
VARIANTS = [{"m1": 1.0}, {"m1": 5.0, "m2": 3.0}, {"m2": 0.5}]
ANSWER = (0.6666666666666666, 1.0, -1.0, 1.0)
TOL = 1e-6
