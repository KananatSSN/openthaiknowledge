"""Theory 1.2 (b): the drag C_d (1/2) rho v^2 pi r^2 decelerates the meteor at a = C_d rho v^2 pi r^2/(2m). Adapted: C_d, rho, v (km/s), r and m vary; returns the deceleration in m/s^2."""

from math import pi


def solve(drag=1.0, density=0.1, speed=15.0, radius=0.5, mass=1500.0):
    return drag * density * (speed * 1e3) ** 2 * pi * radius**2 / (2 * mass)


def check(drag=1.0, density=0.1, speed=15.0, radius=0.5, mass=1500.0):
    # Step the speed over a tiny time and difference it.
    v = speed * 1e3
    dt = 1e-9
    after = v - drag * 0.5 * density * v * v * pi * radius**2 / mass * dt
    return (v - after) / dt


PARAMS = {"drag": 1.0, "density": 0.1, "speed": 15.0, "radius": 0.5, "mass": 1500.0}
VARIANTS = [{"drag": 0.5}, {"mass": 10000.0, "radius": 1.0}, {"speed": 25.0}]
ANSWER = 5890.486225480862
TOL = 1e-6
