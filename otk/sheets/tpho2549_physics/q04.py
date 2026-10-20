"""Theory 1.3(ii): at B, level with the loop's centre, N = mv^2/R with (7/10)mv^2 = mg(h - R); from h = 2.7R, N = (17/7)mg ~ 2.4mg. Adapted: numbers for m, R and h; newtons with g = 10."""


def solve(mass=0.2, loop=1.0, height=2.7, g=10):
    return mass * (10 / 7) * g * (height - loop) / loop


def check(mass=0.2, loop=1.0, height=2.7, g=10, radius=1e-6):
    # Energy with explicit translational and rotational parts for a sphere of
    # radius r, then the centripetal requirement at B.
    inertia = 0.4 * mass * radius**2
    # m g (h - R) = 1/2 m v^2 + 1/2 I (v/r)^2
    v2 = mass * g * (height - loop) / (0.5 * mass + 0.5 * inertia / radius**2)
    return mass * v2 / loop


PARAMS = {"mass": 0.2, "loop": 1.0, "height": 2.7, "g": 10}
VARIANTS = [{"height": 4}, {"mass": 1, "loop": 0.5, "height": 2}, {"g": 9.8}]
ANSWER = 4.8571428571428585
TOL = 1e-9
