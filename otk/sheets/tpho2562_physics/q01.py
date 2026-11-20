"""Theory 1.1-1.2: water of density rho crossing a section A at speed v carries momentum rho A v^2 per second, so a layer h1 deep in a channel L wide entering the jump at v1 carries rho L h1 v1^2. Adapted: the channel width (m), depth (cm) and speed (m/s) vary; returns newtons."""


def solve(density=1000.0, width=0.5, depth=2.0, speed=3.0):
    return density * width * depth * 1e-2 * speed**2


def check(density=1000.0, width=0.5, depth=2.0, speed=3.0):
    # the mass crossing in a short time dt, times its speed, over dt
    dt = 1e-3
    mass = density * width * depth * 1e-2 * speed * dt
    return mass * speed / dt


PARAMS = {"density": 1000.0, "width": 0.5, "depth": 2.0, "speed": 3.0}
VARIANTS = [{"depth": 5.0}, {"speed": 1.5}, {"width": 2.0}]
ANSWER = 90.0
TOL = 1e-9
