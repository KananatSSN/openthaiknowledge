"""Theory 1.4 figure: a ball (1.0 g, 0.010 C) fired at 1.0 m/s along x at height h = 1.0 m; above h/2 a field 0.50 N/C along x acts. Falling h/2 takes sqrt(h/g), so v_x = v0 + (qE/m) sqrt(h/g) = 2.58 m/s and v_y = -sqrt(gh) = -3.16 m/s; |v| = 4.08 m/s. Adapted: numbers vary; returns the speed in m/s with g = 10."""

from math import sqrt


def solve(mass=1e-3, charge=0.01, field=0.5, speed=1.0, height=1.0, g=10):
    t = sqrt(height / g)
    vx = speed + charge * field / mass * t
    vy = g * t
    return sqrt(vx * vx + vy * vy)


def check(mass=1e-3, charge=0.01, field=0.5, speed=1.0, height=1.0, g=10):
    # Step the motion from y = h down to y = h/2.
    y, vx, vy, dt = height, speed, 0.0, 1e-6
    while y > height / 2:
        vx += charge * field / mass * dt
        vy -= g * dt
        y += vy * dt
    return sqrt(vx * vx + vy * vy)


PARAMS = {"mass": 1e-3, "charge": 0.01, "field": 0.5, "speed": 1.0, "height": 1.0, "g": 10}
VARIANTS = [{"field": 1.0}, {"height": 2.0, "speed": 3.0}, {"mass": 2e-3}]
ANSWER = 4.081945327924957
TOL = 1e-5
