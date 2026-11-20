"""Theory 3.2: with P = P0 at the rim R, Bernoulli gives P - P0 = (rho K^2/2)(1/R^2 - 1/r^2), K = a^2 v0/(2t). Adapted: numbers; returns the gauge pressure P - P0 at r in pascals."""


def solve(density=1.2, tube=0.01, speed=20, gap=0.002, rim=0.1, radius=0.05):
    k = tube**2 * speed / (2 * gap)
    return density * k * k / 2 * (1 / rim**2 - 1 / radius**2)


def check(density=1.2, tube=0.01, speed=20, gap=0.002, rim=0.1, radius=0.05):
    # Integrate the radial Euler equation dP/dr = -rho v dv/dr from the rim
    # inward with the continuity speed.
    k = tube**2 * speed / (2 * gap)
    n = 100000
    pressure = 0.0
    for i in range(n):
        r = rim - (rim - radius) * (i + 0.5) / n
        dr = -(rim - radius) / n
        v, dv = k / r, -k / r**2
        pressure += -density * v * dv * dr
    return pressure


PARAMS = {"density": 1.2, "tube": 0.01, "speed": 20, "gap": 0.002, "rim": 0.1, "radius": 0.05}
VARIANTS = [{"radius": 0.02}, {"speed": 10, "gap": 0.001}, {"rim": 0.3, "radius": 0.1}]
ANSWER = -44.99999999999999
TOL = 1e-6
