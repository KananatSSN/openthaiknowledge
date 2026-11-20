"""Lab part 3: T_pendulum^2 is proportional to the string length, so a line through the origin (least squares) gives the slope; the length at which the pendulum period equals the torsion period T_t is l_m = T_t^2/slope (0.46/0.0381 = 12 cm in the solution). Adapted with synthetic periods (cm, s) and the torsion time for 50 swings; returns l_m in cm."""


def solve(lengths=(15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0), periods=(0.77, 0.83, 0.88, 0.91, 0.98, 1.02, 1.07), time50=33.97):
    sq = [t * t for t in periods]
    slope = sum(x * y for x, y in zip(lengths, sq)) / sum(x * x for x in lengths)
    return (time50 / 50) ** 2 / slope


def check(lengths=(15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0), periods=(0.77, 0.83, 0.88, 0.91, 0.98, 1.02, 1.07), time50=33.97):
    # Minimise the squared residuals over the slope by golden section, then
    # bisect the length whose fitted T^2 matches the torsion period's square.
    sq = [t * t for t in periods]

    def cost(s):
        return sum((y - s * x) ** 2 for x, y in zip(lengths, sq))

    lo, hi = 0.0, 1.0
    r = (5**0.5 - 1) / 2
    for _ in range(200):
        a, b = hi - r * (hi - lo), lo + r * (hi - lo)
        if cost(a) < cost(b):
            hi = b
        else:
            lo = a
    slope = (lo + hi) / 2
    target = (time50 / 50) ** 2
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if slope * mid < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"lengths": (15.0, 18.0, 20.0, 22.0, 25.0, 28.0, 30.0), "periods": (0.77, 0.83, 0.88, 0.91, 0.98, 1.02, 1.07), "time50": 33.97}
VARIANTS = [{"time50": 30.0}, {"periods": (0.78, 0.85, 0.90, 0.94, 1.00, 1.06, 1.10)}, {"lengths": (10.0, 14.0, 18.0, 22.0, 26.0, 30.0, 34.0)}]
ANSWER = 12.122055632154545
TOL = 1e-8
