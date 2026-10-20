"""Theory 1.3(i) figure: a small solid sphere (r << R) rolls without slipping from height h into a vertical loop of radius R; it just goes round when mg = mv^2/R at the top, so mgh = (7/10)mv^2 + 2mgR gives h = 2.7R. Adapted: R given; metres."""


def solve(loop=1.0, g=10):
    return 2.7 * loop


def check(loop=1.0, g=10):
    # Bisect on h: does the normal force at the top stay non-negative?
    def top_normal(h):
        v2 = (h - 2 * loop) * g / 0.7
        return v2 / loop - g

    lo, hi = 0.0, 100 * loop
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if top_normal(mid) < 0 else (lo, mid)
    return hi


PARAMS = {"loop": 1.0, "g": 10}
VARIANTS = [{"loop": 0.3}, {"loop": 2.5}, {"g": 9.8}]
ANSWER = 2.7
TOL = 1e-9
