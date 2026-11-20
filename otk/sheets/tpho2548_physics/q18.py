"""Lab 1 part 4: a sheet of thickness d with measured kappa eps0/d has dielectric constant kappa = (kappa eps0/d) d/eps0. Adapted: synthetic kappa eps0/d (F/m^2) and thickness (micrometres), eps0 = 8.854e-12 F/m."""


def solve(per_area=2e-7, thickness=100, eps0=8.854e-12):
    return per_area * thickness * 1e-6 / eps0


def check(per_area=2e-7, thickness=100, eps0=8.854e-12):
    # A 1 m^2 plate: build C from kappa and compare with the measured C.
    lo, hi = 0.0, 1e6
    for _ in range(200):
        kappa = (lo + hi) / 2
        c = kappa * eps0 * 1.0 / (thickness * 1e-6)
        lo, hi = (kappa, hi) if c < per_area else (lo, kappa)
    return lo


PARAMS = {"per_area": 2e-7, "thickness": 100, "eps0": 8.854e-12}
VARIANTS = [{"thickness": 50}, {"per_area": 5e-7}, {"per_area": 1e-7, "thickness": 200}]
ANSWER = 2.25886604924328
TOL = 1e-9
