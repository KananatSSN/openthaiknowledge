"""MC18 figure: projectiles leave A and B, distance D apart on level ground, at the same instant and speed u, at equal elevation theta0 toward each other in one vertical plane. They meet at t = D / (2 u cos theta0) (answer 2). Angles given by cos theta0."""

from math import sqrt


def solve(distance=40, speed=10, cosine=0.8):
    return distance / (2 * speed * cosine)


def check(distance=40, speed=10, cosine=0.8, g=10):
    # Bisect on time for zero horizontal gap and confirm the heights match.
    sine = sqrt(1 - cosine * cosine)
    pos = lambda x0, sign, t: (x0 + sign * speed * cosine * t, speed * sine * t - g * t * t / 2)
    lo, hi = 0.0, 1000.0
    for _ in range(200):
        t = (lo + hi) / 2
        if pos(0, 1, t)[0] < pos(distance, -1, t)[0]:
            lo = t
        else:
            hi = t
    t = (lo + hi) / 2
    assert abs(pos(0, 1, t)[1] - pos(distance, -1, t)[1]) < 1e-9
    return t


PARAMS = {"distance": 40, "speed": 10, "cosine": 0.8}
VARIANTS = [{"cosine": 0.6}, {"distance": 26, "speed": 13, "cosine": 5 / 13}, {"speed": 25}]
ANSWER = 2.5
