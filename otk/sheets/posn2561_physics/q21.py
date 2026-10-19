"""Written1: rocket from rest has NET upward acceleration9.8m/s^2 for10s then engine stops; thereafter free fall underg9.8. Apex980m. Acceleration is net, not thrust/mass."""


def solve(acceleration=9.8, time=10, g=9.8):
    return acceleration * time * time / 2 + (acceleration * time) ** 2 / (2 * g)


def check(acceleration=9.8, time=10, g=9.8):
    # Integrate each constant-acceleration phase by midpoint quadrature.
    steps = 1000
    dt = time / steps
    height = sum(acceleration * (i + 0.5) * dt * dt for i in range(steps))
    speed = acceleration * time
    coast = speed / g
    dt = coast / steps
    height += sum((speed - g * (i + 0.5) * dt) * dt for i in range(steps))
    return height


PARAMS = {"acceleration": 9.8, "time": 10, "g": 9.8}
VARIANTS = [{"acceleration": 10, "g": 10}, {"time": 5}, {"acceleration": 4.9}]
ANSWER = 980.0
