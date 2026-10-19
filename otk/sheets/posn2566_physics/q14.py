"""MC14 figure: water spinning with its cup at omega; the surface is the paraboloid y = (omega^2/2g) x^2 + h (answer 3). Adapted: the rise above the centre at radius x, in cm."""


def solve(omega=10, radius=4, g=10):
    x = radius / 100
    return omega**2 * x * x / (2 * g) * 100


def check(omega=10, radius=4, g=10):
    # Integrate the surface slope dy/dx = omega^2 x / g (effective gravity
    # tilt) from the axis out to x by the trapezoid rule.
    n = 10000
    x_end = radius / 100
    h = x_end / n
    rise = 0.0
    for k in range(n):
        a, b = k * h, (k + 1) * h
        rise += (omega**2 * a / g + omega**2 * b / g) / 2 * h
    return rise * 100


PARAMS = {"omega": 10, "radius": 4, "g": 10}
VARIANTS = [{"omega": 20, "radius": 5}, {"radius": 10}, {"omega": 6, "radius": 8}]
ANSWER = 0.8
