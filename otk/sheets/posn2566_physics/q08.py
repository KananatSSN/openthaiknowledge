"""MC8 figure: picture a: source E with internal r feeding two resistors in parallel; I is the current in one. Picture b: the same source with a single x carries the same I. For branches R1 (other) and R2 (the one with I): x = R2 + r R2 / R1; equal R gives x = r + R (answer 2). Ohms."""


def solve(internal=2, other=6, branch=6):
    return branch + internal * branch / other


def check(internal=2, other=6, branch=6, emf=12):
    # Solve picture a by nodal analysis, then bisect x in picture b.
    lo, hi = 0.0, emf
    for _ in range(200):
        v = (lo + hi) / 2
        if (emf - v) / internal > v / other + v / branch:
            lo = v
        else:
            hi = v
    current = (lo + hi) / 2 / branch
    lo, hi = 0.0, 1e6
    for _ in range(200):
        x = (lo + hi) / 2
        if emf / (internal + x) > current:
            lo = x
        else:
            hi = x
    return (lo + hi) / 2


PARAMS = {"internal": 2, "other": 6, "branch": 6}
VARIANTS = [{"other": 3}, {"internal": 1, "other": 4, "branch": 12}, {"branch": 2}]
TOL = 1e-9
ANSWER = 8.0
