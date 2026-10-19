"""MC3 figure: m moving at u along +OX splits into alpha m, which moves along +OY at v, and (1 - alpha) m. The second piece moves below OX at theta with tan theta = alpha v / u (answer 2)."""

from math import atan2, tan


def solve(alpha=0.25, speed=8, piece_speed=4):
    return alpha * piece_speed / speed


def check(alpha=0.25, speed=8, piece_speed=4):
    # Momentum components of the second piece, then its angle below OX.
    px = speed - 0.0
    py = 0.0 - alpha * piece_speed
    vx, vy = px / (1 - alpha), py / (1 - alpha)
    return tan(-atan2(vy, vx))


PARAMS = {"alpha": 0.25, "speed": 8, "piece_speed": 4}
VARIANTS = [{"alpha": 0.5}, {"alpha": 0.4, "speed": 5, "piece_speed": 10}, {"piece_speed": 12}]
ANSWER = 0.125
