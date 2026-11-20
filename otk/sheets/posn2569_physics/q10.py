"""MC10 figure: the charged ring of item 9 spun about OX gives an axial B(x) proportional to (1 + x^2/R^2)^(-3/2): even, peaked at x = 0 (answer 5). Adapted quantity: B(x)/B(0)."""

from math import cos, pi, sin


def solve(radius=3, distance=4):
    return (radius**2 / (radius**2 + distance**2)) ** 1.5


def check(radius=3, distance=4, n=4000):
    # Biot-Savart axial sums at x and at 0.
    def axial(x):
        total = 0.0
        for k in range(n):
            p = 2 * pi * k / n
            dl = (-sin(p), cos(p))
            r = (-radius * cos(p), -radius * sin(p))
            total += (dl[0] * r[1] - dl[1] * r[0]) / (radius**2 + x * x) ** 1.5
        return total

    return axial(distance) / axial(0.0)


PARAMS = {"radius": 3, "distance": 4}
VARIANTS = [{"radius": 4, "distance": 3}, {"radius": 5, "distance": 12}, {"radius": 1, "distance": 0}]
ANSWER = 0.216
