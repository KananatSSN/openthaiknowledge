"""Part1,8: source curve2 has lower apex and shorter range than vacuum, without changed launch tangent. Adaptation specifies linear drag -mkv and compares apex and range at equal landing height. Return ratios (H_drag/H_vac,R_drag/R_vac)."""

from math import exp, log1p

TOL = 2e-7


def solve(vx=10, vy=10, decay=0.2, g=9.8):
    k = decay
    top = log1p(k * vy / g) / k
    height = (vy + g / k) * (1 - exp(-k * top)) / k - g * top / k
    lo, hi = top, 2 * vy / g
    for _ in range(100):
        t = (lo + hi) / 2
        y = (vy + g / k) * (1 - exp(-k * t)) / k - g * t / k
        if y > 0:
            lo = t
        else:
            hi = t
    distance = vx * (1 - exp(-k * (lo + hi) / 2)) / k
    return (height / (vy * vy / (2 * g)), distance / (2 * vx * vy / g))


def check(vx=10, vy=10, decay=0.2, g=9.8):
    # Independent RK4 integration of positions and velocities, no closed forms.
    state = [0.0, 0.0, float(vx), float(vy)]

    def derivative(s):
        return [s[2], s[3], -decay * s[2], -g - decay * s[3]]

    dt = 0.0001
    peak = 0.0
    for _ in range(200000):
        old = state[:]
        a = derivative(state)
        b = derivative([s + dt * k / 2 for s, k in zip(state, a)])
        c = derivative([s + dt * k / 2 for s, k in zip(state, b)])
        d = derivative([s + dt * k for s, k in zip(state, c)])
        state = [s + dt * (w + 2 * x + 2 * y + z) / 6 for s, w, x, y, z in zip(state, a, b, c, d)]
        peak = max(peak, state[1])
        if state[1] < 0:
            fraction = old[1] / (old[1] - state[1])
            distance = old[0] + fraction * (state[0] - old[0])
            return (peak / (vy * vy / (2 * g)), distance / (2 * vx * vy / g))
    raise RuntimeError("did not land")


PARAMS = {"vx": 10, "vy": 10, "decay": 0.2, "g": 9.8}
VARIANTS = [{"vx": 20}, {"vy": 15}, {"decay": 0.5}]
ANSWER = (0.8818626589196441, 0.7807060462439622)
