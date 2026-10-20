"""Theory 2.2(b): once rolling, omega = 5 V0/(7R). Adapted: numbers for V0 and R; rad/s."""


def solve(speed=7, radius=0.05, friction=0.2, g=10):
    return 5 * speed / (7 * radius)


def check(speed=7, radius=0.05, friction=0.2, g=10):
    # Angular momentum about the contact line is conserved:
    # M V0 R = M v R + (2/5) M R^2 omega with v = omega R.
    return speed * radius / (radius**2 + 0.4 * radius**2)


PARAMS = {"speed": 7, "radius": 0.05, "friction": 0.2, "g": 10}
VARIANTS = [{"speed": 2}, {"radius": 0.1}, {"speed": 3.5, "radius": 0.028}]
ANSWER = 99.99999999999999
TOL = 1e-9
