"""MC2 figure: uniform rod M, length L, horizontal on supports A (L/4 from the left end) and B (right end). Just after B is pulled away the rod pivots about A: N_A = Mg (L^2/12)/(L^2/12 + d^2) with d = L/2 - pL the pivot-to-centre distance; p = 1/4 gives 4Mg/7 (answer 1). Returns N_A in newtons, g = 10."""


def solve(mass=7, fraction=0.25, g=10):
    d = 0.5 - fraction
    return mass * g * (1 / 12) / (1 / 12 + d * d)


def check(mass=7, fraction=0.25, g=10, length=1.0):
    # Moment of inertia about A by summing 20000 slices, then the angular
    # acceleration from the weight's torque and N = M(g - a_cm).
    n = 20000
    inertia = 0.0
    for k in range(n):
        x = length * (k + 0.5) / n - fraction * length
        inertia += mass / n * x * x
    d = (0.5 - fraction) * length
    alpha = mass * g * d / inertia
    return mass * (g - alpha * d)


PARAMS = {"mass": 7, "fraction": 0.25, "g": 10}
VARIANTS = [{"fraction": 0.0}, {"fraction": 1 / 3}, {"mass": 3, "fraction": 0.125}]
TOL = 1e-6
ANSWER = 40.0
