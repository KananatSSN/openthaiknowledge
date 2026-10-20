"""Lab 2 item 4: each turn of the spring has the same mass, so the linear density is inversely proportional to a turn's stretched length; with lambda0 at the top (turn length l0) and lambdan at the bottom (ln), beta2 = (lambda0/6 + lambdan/2)/(lambda0 + lambdan). Adapted: l0 and ln (mm) vary; returns beta2."""


def solve(top=12.0, bottom=6.0):
    lam0, lamn = 1 / top, 1 / bottom
    return (lam0 / 6 + lamn / 2) / (lam0 + lamn)


def check(top=12.0, bottom=6.0):
    # Equation (2)'s model: density linear in position from lambda0 at the
    # fixed top to lambdan at the mass, every point moving in proportion to
    # its distance from the top; kinetic-energy share by the midpoint rule.
    lam0, lamn = 1 / top, 1 / bottom
    n = 20000
    mass = ke = 0.0
    for i in range(n):
        s = (i + 0.5) / n
        lam = lam0 + (lamn - lam0) * s
        mass += lam / n
        ke += lam * s * s / n
    return ke / mass


PARAMS = {"top": 12.0, "bottom": 6.0}
VARIANTS = [{"top": 8.0}, {"top": 20.0, "bottom": 5.0}, {"top": 6.0}]
ANSWER = 0.38888888888888884
TOL = 1e-8
