"""Theory 2.4: the wire's temperature levels off where dT/dt = 0, T = Ta + i^2 rho/(2 alpha pi^2 r^3). Adapted: alpha (W/cm^2 C) and Ta given with the paper's wire; C."""

from math import pi


def solve(current=10, resistivity=11.5e-6, radius=0.1, alpha=1e-4, room=25):
    return room + current**2 * resistivity / (2 * alpha * pi**2 * radius**3)


def check(current=10, resistivity=11.5e-6, radius=0.1, alpha=1e-4, room=25, heat=0.23, density=7.3):
    # Integrate the 2.3 equation (RK4) for many time constants.
    gain = current**2 * resistivity / (pi**2 * radius**4 * heat * density)
    k = 2 * alpha / (heat * radius * density)

    def f(t):
        return gain - k * (t - room)

    temperature, dt = room, 0.05 / k
    for _ in range(2000):
        a = f(temperature)
        b = f(temperature + dt / 2 * a)
        c = f(temperature + dt / 2 * b)
        d = f(temperature + dt * c)
        temperature += dt / 6 * (a + 2 * b + 2 * c + d)
    return temperature


PARAMS = {"current": 10, "resistivity": 11.5e-6, "radius": 0.1, "alpha": 1e-4, "room": 25}
VARIANTS = [{"current": 5}, {"alpha": 5e-4, "room": 30}, {"radius": 0.2}]
ANSWER = 607.596805943442
TOL = 1e-6
