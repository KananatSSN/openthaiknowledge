"""Theory 2(a) figure: an inverted steel tank (height L) lowered to the river bed fills a fraction k with water; Boyle's law Pa L A = (Pa + rho g (h - kL))(1 - k) L A gives h = kL + k Pa/((1 - k) rho g); with L = 8.0 m and k = 1/2, h = 4.0 + 10.13 = 14.1 m. Adapted: L and k given; metres with Pa = 1.013e5 Pa, rho g = 1.0e4 N/m^3."""


def solve(length=8.0, fraction=0.5, pa=1.013e5, rho_g=1.0e4):
    return fraction * length + fraction * pa / ((1 - fraction) * rho_g)


def check(length=8.0, fraction=0.5, pa=1.013e5, rho_g=1.0e4):
    # Bisect on the depth: lower the tank and solve for the water level
    # inside from Boyle's law, until the fill fraction matches.
    def filled(depth):
        lo, hi = 0.0, 1.0
        for _ in range(200):
            k = (lo + hi) / 2
            inside = pa * 1 / (1 - k)
            outside = pa + rho_g * (depth - k * length)
            lo, hi = (k, hi) if inside < outside else (lo, k)
        return lo

    lo, hi = 0.0, 1e4
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if filled(mid) < fraction else (lo, mid)
    return lo


PARAMS = {"length": 8.0, "fraction": 0.5, "pa": 1.013e5, "rho_g": 1.0e4}
VARIANTS = [{"fraction": 0.25}, {"length": 5, "fraction": 0.6}, {"length": 10, "fraction": 0.2}]
ANSWER = 14.13
TOL = 1e-6
