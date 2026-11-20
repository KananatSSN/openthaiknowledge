"""Short26 figure: E1 (positive plate up) in series with R1 to the top node; E2 (positive plate up) straight across the top node and the bottom wire; R2 also across them. i1 flows right through R1, i2 down through R2. Top node sits at E2, so i1/i2 = R2 (E1 - E2) / (R1 E2)."""


def solve(e1=12, e2=4, r1=2, r2=3):
    return r2 * (e1 - e2) / (r1 * e2)


def check(e1=12, e2=4, r1=2, r2=3):
    # Two mesh currents (left loop J1 clockwise through E1,R1,E2; right loop J2
    # clockwise through E2,R2), solved by Cramer's rule. i1 = J1, i2 = J2.
    # Left:  E1 - J1 R1 - E2 = 0 ; right: E2 - J2 R2 = 0
    a = [[r1, 0.0], [0.0, r2]]
    b = [e1 - e2, e2]
    det = a[0][0] * a[1][1] - a[0][1] * a[1][0]
    j1 = (b[0] * a[1][1] - a[0][1] * b[1]) / det
    j2 = (a[0][0] * b[1] - b[0] * a[1][0]) / det
    return j1 / j2


PARAMS = {"e1": 12, "e2": 4, "r1": 2, "r2": 3}
VARIANTS = [{"e1": 9, "e2": 6}, {"r1": 5, "r2": 1}, {"e1": 20, "e2": 5, "r1": 4, "r2": 6}]
ANSWER = 3.0
