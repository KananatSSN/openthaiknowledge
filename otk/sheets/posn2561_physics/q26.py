"""Written6: mass1kg pulled vertically upward by20N through5m, g9.8. Kinetic energy increase51J; total work includes negative gravity work."""


def solve(mass=1, force=20, distance=5, g=9.8):
    return (force - mass * g) * distance


def check(mass=1, force=20, distance=5, g=9.8):
    from math import sqrt

    acceleration = force / mass - g
    time = sqrt(2 * distance / acceleration)
    final_velocity = acceleration * time
    return mass * final_velocity**2 / 2


PARAMS = {"mass": 1, "force": 20, "distance": 5, "g": 9.8}
VARIANTS = [{"force": 30}, {"distance": 10}, {"mass": 2, "force": 40}]
ANSWER = 51.0
