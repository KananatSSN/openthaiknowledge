"""Theory 1.2 figure: as water starts to spill from the shorter end (height h), the trapped air pocket spans from the W's middle peak (at h) to its bottom; its pressure is P_a + rho g h from the short side and P_a + rho g (H - h) from the tall side, so H = 2h. Adapted: h (cm) varies; returns H in cm."""


def solve(height=20.0):
    return 2 * height


def check(height=20.0, rho=1000.0, g=9.8, air=1.0e5):
    # Bisect the tall-side level that balances the trapped air's pressure.
    pocket = air + rho * g * height / 100
    lo, hi = 0.0, 10 * height
    for _ in range(200):
        mid = (lo + hi) / 2
        if air + rho * g * (mid - height) / 100 < pocket:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"height": 20.0}
VARIANTS = [{"height": 12.0}, {"height": 35.0}, {"height": 8.0}]
ANSWER = 40.0
TOL = 1e-9
