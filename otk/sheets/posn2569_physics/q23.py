"""Part2 item 13 figure: C1 holding q is switched onto C2, C3, C4 (uncharged, in parallel); C1 keeps q C1/(C1 + C2 + C3 + C4)."""


def solve(charge=20, c1=2, c2=1, c3=1, c4=1):
    return charge * c1 / (c1 + c2 + c3 + c4)


def check(charge=20, c1=2, c2=1, c3=1, c4=1):
    # Bisect on the common voltage so the total charge is conserved.
    lo, hi = 0.0, charge / c1
    for _ in range(200):
        v = (lo + hi) / 2
        if v * (c1 + c2 + c3 + c4) < charge:
            lo = v
        else:
            hi = v
    return (lo + hi) / 2 * c1


PARAMS = {"charge": 20, "c1": 2, "c2": 1, "c3": 1, "c4": 1}
VARIANTS = [{"c2": 3, "c3": 2}, {"charge": 60, "c1": 5, "c4": 4}, {"c1": 1}]
ANSWER = 8.0
