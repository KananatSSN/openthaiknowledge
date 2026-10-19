"""Short3 figure: m at u compresses a light spring fixed to M at rest on a smooth floor; at closest approach both move at m u/(m + M)."""


def solve(small=2, big=3, speed=10):
    return small * speed / (small + big)


def check(small=2, big=3, speed=10, k=100.0):
    # Simulate the spring contact and record m's speed at maximum compression.
    x1, v1, x2, v2, dt = 0.0, float(speed), 0.0, 0.0, 1e-6
    best_gap, at = 0.0, speed
    while True:
        compression = x1 - x2
        force = k * compression
        v1 -= force / small * dt
        v2 += force / big * dt
        x1 += v1 * dt
        x2 += v2 * dt
        if x1 - x2 > best_gap:
            best_gap, at = x1 - x2, v1
        elif x1 - x2 < best_gap - 1e-9:
            return at


PARAMS = {"small": 2, "big": 3, "speed": 10}
VARIANTS = [{"big": 1}, {"small": 5, "big": 1, "speed": 6}, {"speed": 3}]
TOL = 1e-4
ANSWER = 4.0
