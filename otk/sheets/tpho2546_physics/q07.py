"""Theory 2.3: with heat loss alpha x (surface area) x (T - Ta), dT/dt = i^2 rho/(pi^2 r^4 c D) - 2 alpha (T - Ta)/(c r D). Adapted: alpha (W/cm^2 C) and T - Ta given; returns dT/dt in C/s with the paper's wire."""

from math import pi


def solve(current=10, resistivity=11.5e-6, radius=0.1, heat=0.23, density=7.3, alpha=1e-4, excess=50):
    gain = current**2 * resistivity / (pi**2 * radius**4 * heat * density)
    return gain - 2 * alpha * excess / (heat * radius * density)


def check(current=10, resistivity=11.5e-6, radius=0.1, heat=0.23, density=7.3, alpha=1e-4, excess=50, length=5.0):
    # Energy balance for a wire of explicit length: P_in - P_loss = m c dT/dt.
    area = pi * radius**2
    power = current**2 * resistivity * length / area
    loss = alpha * (2 * pi * radius * length) * excess
    return (power - loss) / (density * area * length * heat)


PARAMS = {"current": 10, "resistivity": 11.5e-6, "radius": 0.1, "heat": 0.23, "density": 7.3, "alpha": 1e-4, "excess": 50}
VARIANTS = [{"excess": 0}, {"alpha": 2e-4, "excess": 100}, {"current": 20, "radius": 0.2}]
ANSWER = 0.634421448413868
TOL = 1e-9
