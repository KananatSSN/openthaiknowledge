"""Theory 2.3: inside the ball the force on -q is kqQx/R^3 toward O, so its work from O to B is -kqQ/(2R). Adapted: kqQ (J m) and R (m) given; joules."""


def solve(product=4.0, radius=0.5):
    return -product / (2 * radius)


def check(product=4.0, radius=0.5):
    # Midpoint sum of F dx with F = -kqQ x/R^3 along OB.
    n = 100000
    return sum(-product * (radius * (i + 0.5) / n) / radius**3 * radius / n for i in range(n))


PARAMS = {"product": 4.0, "radius": 0.5}
VARIANTS = [{"radius": 2.0}, {"product": 9.0}, {"product": 0.3, "radius": 0.1}]
ANSWER = -4.0
TOL = 1e-9
