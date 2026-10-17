"""MC8 figure/text: launch30m/s at30deg, horizontal balloon distance30sqrt3m, both start ground level. Balloon starts FROM REST with constant upward acceleration. Meeting t2s, required a5.2m/s². Printed least acceleration actually gives one exact acceleration for fixed launch data; adaptation asks that acceleration."""


def solve(speed=30, distance_coeff=30, g=9.8):
    return speed * speed / (2 * distance_coeff) - g


def check(speed=30, distance_coeff=30, g=9.8):
    # Integrate vertical projectile motion by midpoint steps until x=d*sqrt3.
    time = 2 * distance_coeff / speed
    dt = time / 1000
    y = 0.0
    vy = speed / 2
    for _ in range(1000):
        y += (vy - g * dt / 2) * dt
        vy -= g * dt
    lo, hi = 0.0, 1 + speed**2 / distance_coeff
    for _ in range(100):
        acceleration = (lo + hi) / 2
        if acceleration * time * time / 2 < y:
            lo = acceleration
        else:
            hi = acceleration
    return (lo + hi) / 2


PARAMS = {"speed": 30, "distance_coeff": 30, "g": 9.8}
VARIANTS = [{"speed": 40, "distance_coeff": 40}, {"g": 10}, {"distance_coeff": 25}]
ANSWER = 5.199999999999999
