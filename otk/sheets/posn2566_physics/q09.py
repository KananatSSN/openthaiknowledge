"""MC9: psi = sin(x - t) + sin(x + t) = 2 sin x cos t; at t = pi it is -2 sin x (answer 3). Adapted: the value of psi at given x and t, both multiples of pi/6."""

from math import cos, pi, sin


def solve(x_sixths=3, t_sixths=6):
    return 2 * sin(x_sixths * pi / 6) * cos(t_sixths * pi / 6)


def check(x_sixths=3, t_sixths=6):
    # Add the two travelling waves directly.
    x, t = x_sixths * pi / 6, t_sixths * pi / 6
    return sin(x - t) + sin(x + t)


PARAMS = {"x_sixths": 3, "t_sixths": 6}
VARIANTS = [{"x_sixths": 1, "t_sixths": 2}, {"x_sixths": 4, "t_sixths": 1}, {"x_sixths": 2, "t_sixths": 3}]
ANSWER = -2.0
