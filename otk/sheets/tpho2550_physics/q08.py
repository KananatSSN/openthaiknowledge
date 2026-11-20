"""Theory 2.3.2: the falling mass M (string wound on the rim) drives the wheel to a terminal omega_f where Mg r0 omega_f = i^2 R with i = omega_f B r0^2/(2R): omega_f = 4MgR/(B^2 r0^3). Adapted: numbers; rad/s with g = 10."""


def solve(mass=0.1, field=0.5, radius=0.2, resistor=2, g=10):
    return 4 * mass * g * resistor / (field**2 * radius**3)


def check(mass=0.1, field=0.5, radius=0.2, resistor=2, g=10, inertia=1e-3):
    # Time-step the wheel: gravity torque against the magnetic torque on the
    # current, (1/2) i B r0^2, for thirty time constants of the approach.
    total = inertia + mass * radius**2
    drag = (field * radius**2) ** 2 / (4 * resistor)   # torque per unit omega
    tau = total / drag
    w, dt = 0.0, tau / 2000
    for _ in range(60000):
        i = w * field * radius**2 / (2 * resistor)
        torque = mass * g * radius - i * field * radius**2 / 2
        w += torque / total * dt
    return w


PARAMS = {"mass": 0.1, "field": 0.5, "radius": 0.2, "resistor": 2, "g": 10}
VARIANTS = [{"mass": 0.05}, {"field": 1.0, "radius": 0.3}, {"resistor": 0.5}]
ANSWER = 3999.999999999999
TOL = 1e-6
