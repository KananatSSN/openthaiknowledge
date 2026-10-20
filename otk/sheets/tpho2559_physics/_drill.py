"""Shared model for problem 3 (pump drill): the rope angle theta(phi) obeys d(theta)/d(phi) = -r/(L tan theta) while it winds (phi measured as rope winds), so cos(theta_n) = cos(theta0) e^(2 n pi r/L). The beam is massless: 2T sin(theta) = F1 and the rope's torque on the shaft is 2T cos(theta) r."""

from math import tan


def wind(theta0, turns, radius, arm, steps=20000):
    """theta after winding `turns` turns, by RK4 on d(theta)/d(phi)."""
    from math import pi

    def f(t):
        return -radius / (arm * tan(t))

    t = theta0
    h = 2 * pi * turns / steps
    for _ in range(steps):
        k1 = f(t)
        k2 = f(t + h / 2 * k1)
        k3 = f(t + h / 2 * k2)
        k4 = f(t + h * k3)
        t += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
    return t


def spin_up(force, theta0, turns, radius, arm, mass, inertia, k, g=9.8, steps=20000):
    """omega when the rope has fully unwound, integrating I omega d(omega) = net torque d(phi)."""
    from math import pi, sqrt

    thetas = [theta0]
    t = theta0
    h = 2 * pi * turns / steps
    for _ in range(steps):
        def f(x):
            return -radius / (arm * tan(x))
        k1 = f(t)
        k2 = f(t + h / 2 * k1)
        k3 = f(t + h / 2 * k2)
        k4 = f(t + h * k3)
        t += h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
        thetas.append(t)
    # unwinding runs the list backwards; torque F1 r/tan(theta) - k(Mg + F1)
    energy = 0.0
    for i in range(steps):
        a, b = thetas[i], thetas[i + 1]
        mid = (a + b) / 2
        energy += (force * radius / tan(mid) - k * (mass * g + force)) * h
    return sqrt(2 * energy / inertia)
