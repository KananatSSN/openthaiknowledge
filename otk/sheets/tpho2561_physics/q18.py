"""Theory 3.7: keeping the second-order term, -rho dv/dt adds omega rho_m v_m sin cos, so 2kB = omega rho_m v_m, B = P_m^2/(2 rho0 c^2), and the mean pressure exceeds P_a by B/2 = P_m^2/(4 rho0 c^2). Adapted: P_m (Pa), rho0 and c vary; returns the excess in mPa."""


def solve(amplitude=20.0, density=1.2, sound=340.0):
    return amplitude**2 / (4 * density * sound**2) * 1e3


def check(amplitude=20.0, density=1.2, sound=340.0):
    # Average B sin^2 over a period with B from 2kB = w rho_m v_m.
    from math import pi, sin

    vm = amplitude / (density * sound)
    rho_m = density * vm / sound
    k = 1.0
    w = k * sound
    B = w * rho_m * vm / (2 * k)
    n = 4000
    return sum(B * sin(2 * pi * (i + 0.5) / n) ** 2 for i in range(n)) / n * 1e3


PARAMS = {"amplitude": 20.0, "density": 1.2, "sound": 340.0}
VARIANTS = [{"amplitude": 100.0}, {"density": 1.29}, {"sound": 330.0, "amplitude": 50.0}]
ANSWER = 0.720876585928489
TOL = 1e-9
