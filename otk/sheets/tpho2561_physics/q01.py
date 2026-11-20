"""Theory 1.1 a) figure 1: to retrace its path the mass must hit the beam end along the beam's normal, i.e. at theta0 from the vertical; it then flies to the other end, L cos(theta0) away at the same height, so L cos(theta0) = v^2 sin(2 theta0)/g and L = 2 v^2 sin(theta0)/g. Adapted: v and theta0 (degrees) vary; returns L in metres with g = 9.8."""

from math import radians, sin


def solve(speed=3.0, angle=30.0, g=9.8):
    return 2 * speed**2 * sin(radians(angle)) / g


def check(speed=3.0, angle=30.0, g=9.8):
    # Fly the mass from one end (velocity along the normal) until it returns
    # to its launch height; the horizontal distance is L cos(theta0).
    from math import cos

    t0 = radians(angle)
    vx, vy = speed * sin(t0), speed * cos(t0)
    x = y = 0.0
    dt = 1e-6
    while True:
        x += vx * dt
        y += vy * dt - 0.5 * g * dt * dt
        vy -= g * dt
        if y < 0:
            break
    return x / cos(t0)


PARAMS = {"speed": 3.0, "angle": 30.0, "g": 9.8}
VARIANTS = [{"speed": 5.0}, {"angle": 45.0}, {"angle": 20.0, "speed": 2.0}]
ANSWER = 0.9183673469387753
TOL = 1e-5
