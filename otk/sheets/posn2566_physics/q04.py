"""MC4 figure: a liquid drop (mass m, radius r) moving at v splats on a rigid wall without rebounding. Its momentum m v is removed in the time its far side takes to reach the wall, 2r/v, so the average force is m v^2/(2r) (answer 4). Grams, m/s, cm -> newtons."""


def solve(mass=10, speed=4, radius=2):
    return mass / 1000 * speed**2 / (2 * radius / 100)


def check(mass=10, speed=4, radius=2):
    # Time-domain: while the drop crosses the wall plane at speed v, the
    # layer arriving at time t has cross-section pi(r^2 - x^2), x = v t - r;
    # it stops there, so F(t) = rho * area * v^2. Average F over 2r/v.
    r = radius / 100
    density = mass / 1000 / (4 / 3 * 3.141592653589793 * r**3)
    duration = 2 * r / speed
    n = 20000
    dt = duration / n
    total = 0.0
    for k in range(n):
        x = speed * (k + 0.5) * dt - r
        total += density * 3.141592653589793 * (r * r - x * x) * speed**2 * dt
    return total / duration


PARAMS = {"mass": 10, "speed": 4, "radius": 2}
VARIANTS = [{"speed": 10}, {"mass": 4, "radius": 1}, {"mass": 30, "speed": 2, "radius": 3}]
TOL = 1e-6
ANSWER = 4.0
