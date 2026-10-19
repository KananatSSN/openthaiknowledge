"""Short30 figure: conical pendulum, string l at a fixed angle theta to the vertical. Its period 2 pi sqrt(l cos theta / g) is sqrt(cos theta) times the small-swing simple pendulum's 2 pi sqrt(l/g). Angle given by its cosine."""

from math import pi, sqrt


def solve(cosine=0.64):
    return sqrt(cosine)


def check(cosine=0.64, length=2.0, g=10):
    # Conical period from the force balance (radius l sin, tan = w^2 r / g),
    # simple-pendulum period from a small-amplitude time-stepped swing: twice
    # the time between two successive crossings of the vertical.
    sine = sqrt(1 - cosine * cosine)
    omega = sqrt(g * (sine / cosine) / (length * sine))
    cone = 2 * pi / omega
    angle, rate, t, dt = 1e-3, 0.0, 0.0, 1e-5
    crossings = []
    while len(crossings) < 2:
        rate -= g / length * angle * dt
        new = angle + rate * dt
        if (angle > 0) != (new > 0):
            crossings.append(t + dt * abs(angle) / abs(new - angle))
        angle = new
        t += dt
    return cone / (2 * (crossings[1] - crossings[0]))

PARAMS = {"cosine": 0.64}
VARIANTS = [{"cosine": 0.36}, {"cosine": 0.5}, {"cosine": 144 / 169}]
TOL = 1e-4
ANSWER = 0.8
