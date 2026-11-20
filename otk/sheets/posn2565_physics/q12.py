"""MC12 figure: A top and C bottom of a vertical circle of radius R; a smooth straight chute BC makes theta with the vertical. Sliding from rest at B to C takes 2 sqrt(R/g) for every theta (answer 4: one tau). Returns the time in s, g = 10."""

from math import sqrt


def solve(radius=10, cosine=0.8, g=10):
    return 2 * sqrt(radius / g)


def check(radius=10, cosine=0.8, g=10):
    # Step the slide in time: chord length 2R cos(theta), acceleration g cos(theta).
    length = 2 * radius * cosine
    accel = g * cosine
    dt, s, v, t = 1e-5, 0.0, 0.0, 0.0
    while s < length:
        v += accel * dt
        s += v * dt
        t += dt
    return t - (s - length) / v


PARAMS = {"radius": 10, "cosine": 0.8, "g": 10}
VARIANTS = [{"cosine": 0.6}, {"radius": 40, "cosine": 12 / 13}, {"radius": 2.5, "cosine": 0.5}]
TOL = 1e-4
ANSWER = 2.0
