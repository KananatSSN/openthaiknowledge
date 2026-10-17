"""Part2,2 figure: F pushes M right on smooth horizontal floor; m contacts right vertical wall of M. Static friction holds m up. Minimum force=(M+m)g/mu."""


def solve(big=3, small=1, mu=0.5, g=9.8):
    return (big + small) * g / mu


def check(big=3, small=1, mu=0.5, g=9.8):
    lo, hi = 0.0, 1.0

    def supports(force):
        a = force / (big + small)
        normal = force - big * a
        return mu * normal >= small * g

    while not supports(hi):
        hi *= 2
    for _ in range(100):
        force = (lo + hi) / 2
        if supports(force):
            hi = force
        else:
            lo = force
    return (lo + hi) / 2


PARAMS = {"big": 3, "small": 1, "mu": 0.5, "g": 9.8}
VARIANTS = [{"big": 5}, {"mu": 0.25}, {"small": 2}]
ANSWER = 78.4
