"""Part 1,17: mercury inside inverted tube stands10mm above open bath; atmospheric750mmHg. Trapped gas pressure740mmHg, not vacuum."""


def solve(atmosphere=750, height=10):
    return atmosphere - height


def check(atmosphere=750, height=10):
    # Pressures at a common level 1000mm below bath surface must match.
    lo, hi = 0.0, float(atmosphere)
    for _ in range(100):
        gas = (lo + hi) / 2
        inside = gas + height + 1000
        outside = atmosphere + 1000
        if inside < outside:
            lo = gas
        else:
            hi = gas
    return (lo + hi) / 2


PARAMS = {"atmosphere": 750, "height": 10}
VARIANTS = [{"height": 25}, {"atmosphere": 760}, {"height": 100}]
ANSWER = 740
