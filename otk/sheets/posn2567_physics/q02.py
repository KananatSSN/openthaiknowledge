"""Short2 figure: launched at 30 deg above the horizontal; the incline OA falls 30 deg below it. Range along the incline OP = 2u^2/g, and the velocity at P makes phi = 30 deg with the incline. Returns (OP in m, phi in degrees) for g = 10."""

from math import atan2, cos, degrees, radians, sin, tan


def solve(speed=10, g=10):
    return 2 * speed * speed / g, 30.0


def check(speed=10, g=10):
    # Step the flight until the path crosses the incline, then measure.
    up, down = radians(30), radians(30)
    vx, vy = speed * cos(up), speed * sin(up)
    dt, t = 1e-6, 0.0
    while True:
        t += dt
        x, y = vx * t, vy * t - g * t * t / 2
        if y < -x * tan(down):
            break
    distance = (x * x + y * y) ** 0.5
    heading = atan2(vy - g * t, vx)  # negative: below the horizontal
    phi = degrees(abs(heading) - down)
    return distance, phi


PARAMS = {"speed": 10, "g": 10}
VARIANTS = [{"speed": 20}, {"speed": 5}, {"speed": 15, "g": 9.8}]
TOL = 1e-4
ANSWER = (20.0, 30.0)
