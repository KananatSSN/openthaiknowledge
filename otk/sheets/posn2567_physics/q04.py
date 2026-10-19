"""Short4 figure: wheel (radius R, mass M, moment of inertia I about its centre) rolls without slipping down a slope of angle theta. Friction f = M g sin(theta) I / (I + M R^2). Inputs: I as a multiple k of M R^2, sin theta; newtons, g = 10."""


def solve(mass=4, inertia_factor=0.5, sine=0.6, g=10):
    return mass * g * sine * inertia_factor / (inertia_factor + 1)


def check(mass=4, inertia_factor=0.5, sine=0.6, g=10, radius=0.3):
    # Solve Newton + Euler + rolling as a 2x2 system in (a, f) by Cramer.
    inertia = inertia_factor * mass * radius**2
    # M a + f = M g sin ; I a / R^2 - f = 0
    a11, a12, b1 = mass, 1.0, mass * g * sine
    a21, a22, b2 = inertia / radius**2, -1.0, 0.0
    det = a11 * a22 - a12 * a21
    return (a11 * b2 - b1 * a21) / det


PARAMS = {"mass": 4, "inertia_factor": 0.5, "sine": 0.6, "g": 10}
VARIANTS = [{"inertia_factor": 1}, {"inertia_factor": 0.4, "sine": 0.8}, {"mass": 13, "sine": 5 / 13}]
ANSWER = 8.0
