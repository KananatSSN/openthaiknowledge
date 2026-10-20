"""Theory 3.1-3.3: equation (1) gives k P_m cos(...) = omega rho0 v_m cos(...), so the pressure wave is in phase with the velocity and P_m = rho0 c v_m; equation (2) likewise gives rho_m = rho0 v_m/c and P_m/rho_m = c^2. Adapted: rho0, c and v_m (mm/s) vary; returns P_m in Pa."""


def solve(density=1.2, sound=340.0, velocity=50.0):
    return density * sound * velocity * 1e-3


def check(density=1.2, sound=340.0, velocity=50.0):
    # Differentiate v = v_m sin(kx - wt) numerically at x = t = 0 and use
    # dP/dx = k P_m (in phase) = -rho0 dv/dt.
    from math import pi, sin

    k = 2 * pi
    w = k * sound
    vm = velocity * 1e-3
    h = 1e-9
    dvdt = (vm * sin(-w * h) - vm * sin(w * h)) / (2 * h)
    return -density * dvdt / k


PARAMS = {"density": 1.2, "sound": 340.0, "velocity": 50.0}
VARIANTS = [{"velocity": 200.0}, {"density": 1000.0, "sound": 1480.0}, {"sound": 330.0}]
ANSWER = 20.400000000000002
TOL = 1e-6
