"""MC11 figure: top branch R then 2R, bottom branch 3R then 4R (R and 3R on the left); both branches lie across battery E; C joins the two branch midpoints. Steady DC: |V_top - V_bottom| = E(2/3 - 4/7) = 2E/21, so Q = (2/21) C E (answer 1). Returns Q / (C E) for resistances r1..r4 in units of R."""


def solve(r1=1, r2=2, r3=3, r4=4):
    return abs(r2 / (r1 + r2) - r4 / (r3 + r4))


def check(r1=1, r2=2, r3=3, r4=4):
    # Nodal equations with the capacitor open: unknown midpoint potentials T, B,
    # left rail at E = 1 and right rail at 0. Solve each by bisection on KCL.
    def node(left, right):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            v = (lo + hi) / 2
            net_in = (1 - v) / left - v / right
            if net_in > 0:
                lo = v
            else:
                hi = v
        return (lo + hi) / 2

    return abs(node(r1, r2) - node(r3, r4))


PARAMS = {"r1": 1, "r2": 2, "r3": 3, "r4": 4}
VARIANTS = [{"r1": 2, "r2": 1}, {"r3": 1, "r4": 1}, {"r1": 5, "r2": 3, "r3": 2, "r4": 6}]
ANSWER = 0.09523809523809523
