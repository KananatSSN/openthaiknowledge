"""Theory 3.1 (a)-(e) figures 1-2: water arrives at u = sqrt(2 g h0); in Delta t the stopped column grows by vA Delta t from water that held (v + u) A Delta t, so the momentum lost is rho (v + u) u A Delta t and the pressure jump across the front S is rho v u + rho u^2, about rho v u for v >> u. Adapted: h0 and the sound speed v vary; returns rho v u in MPa (rho = 1000, g = 9.8)."""

from math import sqrt


def solve(head=2.0, sound=1480.0, g=9.8):
    return 1000 * sound * sqrt(2 * g * head) / 1e6


def check(head=2.0, sound=1480.0, g=9.8):
    # Speed from a parcel falling the head in small time steps, then the
    # impulse per area per time on the arriving water (v >> u).
    n = 100000
    v, y = 0.0, 0.0
    dt = sqrt(2 * head / g) / n
    for _ in range(n):
        y += v * dt + 0.5 * g * dt * dt
        v += g * dt
    impulse_rate = 1000 * sound * v      # rho v A u / A
    return impulse_rate / 1e6


PARAMS = {"head": 2.0, "sound": 1480.0, "g": 9.8}
VARIANTS = [{"head": 5.0}, {"sound": 1400.0}, {"head": 0.8}]
ANSWER = 9.26626569875913
TOL = 1e-9
