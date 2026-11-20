"""Theory 3.6: the momentum density rho v = (rho0 + rho_m sin)(v_m sin) averages to rho_m v_m/2 = rho0 v_m^2/(2c) = 2<K>/c. Adapted: rho0, c and v_m (mm/s) vary; returns it in units of 1e-6 kg/(m^2 s)."""


def solve(density=1.2, sound=340.0, velocity=50.0):
    return density * (velocity * 1e-3) ** 2 / (2 * sound) * 1e6


def check(density=1.2, sound=340.0, velocity=50.0):
    from math import pi, sin

    vm = velocity * 1e-3
    rho_m = density * vm / sound
    n = 4000
    total = 0.0
    for i in range(n):
        s = sin(2 * pi * (i + 0.5) / n)
        total += (density + rho_m * s) * vm * s
    return total / n * 1e6


PARAMS = {"density": 1.2, "sound": 340.0, "velocity": 50.0}
VARIANTS = [{"velocity": 200.0}, {"density": 1000.0, "sound": 1480.0}, {"sound": 330.0}]
ANSWER = 4.411764705882353
TOL = 1e-9
