"""Short13 figure: a parallel beam of intensity I1 passes a converging lens f1, then a diverging lens f2 = -f1/2 placed so the beam leaves parallel. Its width halves, so I2/I1 = 4. Adapted: f1 = k |f2|; ratio k^2."""


def solve(ratio=2):
    return ratio**2


def check(ratio=2):
    # Paraxial trace of a marginal ray through the afocal pair (f1 = ratio,
    # f2 = -1, separation f1 + f2), then compare beam radii.
    f1, f2 = float(ratio), -1.0
    y, s = 1.0, 0.0
    s -= y / f1
    y += s * (f1 + f2)
    s -= y / f2
    assert abs(s) < 1e-12
    return (1.0 / y) ** 2


PARAMS = {"ratio": 2}
VARIANTS = [{"ratio": 3}, {"ratio": 1.5}, {"ratio": 4}]
ANSWER = 4
