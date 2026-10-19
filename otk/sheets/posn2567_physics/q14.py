"""Short14: lensmaker 1/f = (mu - 1)(1/R1 + 1/R2); a small rise d mu gives df/f = -d mu/(mu - 1)."""


def solve(index=1.5, change=0.01):
    return -change / (index - 1)


def check(index=1.5, change=0.01, r1=0.2, r2=0.3):
    # Central difference of the relative change, scaled to `change`.
    focal = lambda mu: 1 / ((mu - 1) * (1 / r1 + 1 / r2))
    h = 1e-7
    rate = (focal(index + h) - focal(index - h)) / (2 * h) / focal(index)
    return rate * change


PARAMS = {"index": 1.5, "change": 0.01}
VARIANTS = [{"index": 1.6, "change": 0.03}, {"index": 1.25}, {"index": 2, "change": 0.05}]
TOL = 1e-7
ANSWER = -0.02
