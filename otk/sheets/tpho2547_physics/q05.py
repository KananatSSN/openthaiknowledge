"""Theory 2.1 figure: a uniform rod (m, L) pivoted at its centre with an identical spring k at each end; for small angles kL^2 theta/2 = -(mL^2/12) theta'', so f = (1/2 pi) sqrt(6k/m). Adapted: numbers for m and k; hertz."""

from math import pi, sqrt


def solve(mass=0.5, spring=20, length=0.4):
    return sqrt(6 * spring / mass) / (2 * pi)


def check(mass=0.5, spring=20, length=0.4):
    # Integrate the exact torque (springs stretched by (L/2) sin theta) from a
    # tiny release angle and time the zero crossings.
    inertia = mass * length**2 / 12
    from math import sin, cos

    def accel(t):
        return -2 * spring * (length / 2) * sin(t) * (length / 2) * cos(t) / inertia

    theta, w, dt, time = 1e-4, 0.0, 1e-5, 0.0
    crossings = []
    prev = theta
    while len(crossings) < 3:
        a1 = accel(theta)
        w += a1 * dt
        theta += w * dt
        time += dt
        if prev > 0 >= theta or prev < 0 <= theta:
            crossings.append(time - dt * theta / (theta - prev))
        prev = theta
    return 1 / (crossings[2] - crossings[0])


PARAMS = {"mass": 0.5, "spring": 20, "length": 0.4}
VARIANTS = [{"length": 1.0}, {"mass": 2, "spring": 50}, {"spring": 3}]
ANSWER = 2.4656177762459994
TOL = 1e-4
