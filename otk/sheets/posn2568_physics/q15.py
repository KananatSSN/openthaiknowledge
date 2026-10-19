"""Short15 figure: a rubber cord of length l and radius r is stretched by dl; dr/r = k dl/l with k = 1/2 gives dV = pi r^2 l (1 - 2k) dl/l = 0 to first order. Adapted: any k; returns dV / pi in cm^3."""


def solve(radius=1, change=2, ratio=0.5):
    return radius**2 * (1 - 2 * ratio) * change


def check(radius=1, change=2, ratio=0.5, length=100.0):
    # Exact volumes with a tiny stretch, scaled back up (first order).
    eps = 1e-7
    dl = change * eps
    dr = ratio * radius * dl / length
    before = radius**2 * length
    after = (radius - dr) ** 2 * (length + dl)
    return (after - before) / eps


PARAMS = {"radius": 1, "change": 2, "ratio": 0.5}
VARIANTS = [{"ratio": 0.25}, {"radius": 2, "ratio": 0}, {"change": 5, "ratio": 1 / 3}]
TOL = 1e-5
ANSWER = 0.0
