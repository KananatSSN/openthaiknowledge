"""Theory 2.2 (d): the pellet gains speed while the push exceeds the drag, so the best barrel ends where (F + P_a A)(L/(L + D))^gamma = f + P_a A: D = L[((F + P_a A)/(f + P_a A))^(1/gamma) - 1]. Adapted: L0 (cm), F, f (N) and A (cm^2) vary with P_a = 1.0e5 Pa and gamma = 1.4; returns D in cm."""


def solve(rest=30.0, grip=10.0, slide=0.5, area=1.0, gamma=1.4, air=1.0e5):
    A = area * 1e-4
    L = rest * (air * A / (grip + air * A)) ** (1 / gamma)
    return L * (((grip + air * A) / (slide + air * A)) ** (1 / gamma) - 1)


def check(rest=30.0, grip=10.0, slide=0.5, area=1.0, gamma=1.4, air=1.0e5):
    # Maximise the work done over the barrel length numerically.
    from otk.sheets.tpho2558_physics._popgun import push, start_gap
    from otk.sheets.tpho2558_physics._shared import golden_max, simpson

    A = area * 1e-4
    gap = start_gap(rest * 1e-2, grip, A, gamma, air)
    best = golden_max(lambda D: simpson(lambda x: push(x, gap, grip, A, slide, gamma, air), 0.0, D, 400), 1e-6, 2.0, 120)
    return best * 100


PARAMS = {"rest": 30.0, "grip": 10.0, "slide": 0.5, "area": 1.0, "gamma": 1.4, "air": 1.0e5}
VARIANTS = [{"grip": 20.0}, {"slide": 2.0}, {"rest": 40.0, "area": 0.5}]
ANSWER = 10.687299827512637
TOL = 1e-5
