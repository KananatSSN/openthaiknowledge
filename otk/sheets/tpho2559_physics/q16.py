"""Theory 3.3: the work F1 L(theta0 - theta_n) minus the friction work 2 n pi k(Mg + F1) becomes (1/2) I omega^2, so omega = sqrt((2/I)(F1 L(theta0 - theta_n) - 2 n pi k (Mg + F1))). Adapted: F1 (N), n, M (kg), k (mm) and I (kg cm^2) vary with L = 25 cm, r = 3 mm, theta0 = 70 degrees; returns omega in rad/s with g = 9.8."""

from math import acos, cos, exp, pi, radians, sqrt


def solve(force=30.0, turns=3, mass=1.0, k=0.3, inertia=10.0, arm=25.0, radius=3.0, angle=70.0, g=9.8):
    t0 = radians(angle)
    tn = acos(cos(t0) * exp(2 * turns * pi * radius / (arm * 10)))
    work = force * arm * 1e-2 * (t0 - tn) - 2 * turns * pi * k * 1e-3 * (mass * g + force)
    return sqrt(2 * work / (inertia * 1e-4))


def check(force=30.0, turns=3, mass=1.0, k=0.3, inertia=10.0, arm=25.0, radius=3.0, angle=70.0, g=9.8):
    # Integrate the torque F1 r/tan(theta) - k(Mg + F1) over the unwinding angle.
    from otk.sheets.tpho2559_physics._drill import spin_up

    return spin_up(force, radians(angle), turns, radius * 1e-3, arm * 1e-2, mass, inertia * 1e-4, k * 1e-3, g)


PARAMS = {"force": 30.0, "turns": 3, "mass": 1.0, "k": 0.3, "inertia": 10.0, "arm": 25.0, "radius": 3.0, "angle": 70.0, "g": 9.8}
VARIANTS = [{"force": 40.0}, {"turns": 2, "inertia": 20.0}, {"k": 0.2, "mass": 2.0}]
ANSWER = 31.014032111840432
TOL = 1e-6
