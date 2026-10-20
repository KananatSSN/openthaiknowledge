"""Theory 1(g): with the pulley's inertia I_C, r(T' - T) = I_C a(0)/r, so T' = mg + (m r^2 + I_C) v0^2/(H r^2). Adapted: numbers for m, r, I_C, v0, H; newtons with g = 10."""


def solve(mass=2, radius=0.1, inertia=0.01, speed=2, height=4, g=10):
    return mass * g + (mass * radius**2 + inertia) * speed**2 / (height * radius**2)


def check(mass=2, radius=0.1, inertia=0.01, speed=2, height=4, g=10):
    # Free bodies: the mass gives T from a (a from the geometry by a second
    # difference), the pulley's angular acceleration a/r needs the torque
    # (T' - T) r.
    from math import sqrt

    def y(t):
        return sqrt((speed * t) ** 2 + height**2) - height

    h = 1e-4
    a = (y(h) - 2 * y(0) + y(-h)) / (h * h)
    tension = mass * (g + a)
    torque = inertia * a / radius
    return tension + torque / radius


PARAMS = {"mass": 2, "radius": 0.1, "inertia": 0.01, "speed": 2, "height": 4, "g": 10}
VARIANTS = [{"inertia": 0}, {"radius": 0.05, "inertia": 0.002}, {"speed": 4, "height": 2}]
ANSWER = 23.0
TOL = 1e-6
