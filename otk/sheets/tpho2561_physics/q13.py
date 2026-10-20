"""Theory 2.8-2.9: m = A1 A2 f1 f2 h/(u g) (e cancels), so the relative errors add as dh/h + df1/f1 + df2/f2 + du/u + dg/g = 1.2e-8 + 1.7e-9 + 4.4e-9 = 1.8e-8. Adapted: the relative errors of h, u and g (units of 1e-9) vary; returns dm/m in units of 1e-8."""


def solve(planck=12.0, speed=1.7, gravity=4.4, clock=1e-6):
    return (planck + speed + gravity + 2 * clock) / 10


def check(planck=12.0, speed=1.7, gravity=4.4, clock=1e-6):
    # Perturb each quantity in the worst direction and compare masses.
    h, f1, f2, u, g = 1.0, 1.0, 1.0, 1.0, 1.0
    base = f1 * f2 * h / (u * g)
    worst = (f1 * (1 + clock * 1e-9)) * (f2 * (1 + clock * 1e-9)) * (h * (1 + planck * 1e-9)) / ((u * (1 - speed * 1e-9)) * (g * (1 - gravity * 1e-9)))
    return (worst / base - 1) / 1e-8


PARAMS = {"planck": 12.0, "speed": 1.7, "gravity": 4.4, "clock": 1e-6}
VARIANTS = [{"planck": 5.0}, {"gravity": 10.0}, {"speed": 3.0, "planck": 8.0}]
ANSWER = 1.8100002
TOL = 1e-6
