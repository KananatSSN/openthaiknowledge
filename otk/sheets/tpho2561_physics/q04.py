"""Theory 1.2 a)-b) figure 2: summing the reflections between the walls (absorption = emissivity), the inner wall absorbs (E1 a2 + E2 a2 - E2 a1 a2)/(a1 + a2 - a1 a2) and emits E2, so the net flow is e1 e2 sigma (T1^4 - T2^4)/(e1 + e2 - e1 e2). Adapted: the emissivities and the outer temperature (Celsius) vary with the ice at 0 C; returns the net flow in W/m^2."""

SIGMA = 5.670373e-8


def solve(outer=0.08, inner=0.08, warm=25.0, cold=0.0):
    t1, t2 = warm + 273.0, cold + 273.0
    return outer * inner * SIGMA * (t1**4 - t2**4) / (outer + inner - outer * inner)


def check(outer=0.08, inner=0.08, warm=25.0, cold=0.0):
    # Trace the bouncing radiation explicitly: each wall's emission bounces
    # back and forth, the inner wall absorbing a fraction each time it arrives.
    t1, t2 = warm + 273.0, cold + 273.0
    e1, e2 = outer * SIGMA * t1**4, inner * SIGMA * t2**4
    absorbed = 0.0
    beam = e1                       # outer emission heading in
    for _ in range(5000):
        absorbed += inner * beam
        beam *= (1 - inner) * (1 - outer)
    beam = e2 * (1 - outer)         # inner emission reflected back in by the outer wall
    for _ in range(5000):
        absorbed += inner * beam
        beam *= (1 - inner) * (1 - outer)
    return absorbed - e2


PARAMS = {"outer": 0.08, "inner": 0.08, "warm": 25.0, "cold": 0.0}
VARIANTS = [{"outer": 0.05, "inner": 0.1}, {"warm": 35.0}, {"inner": 0.3}]
ANSWER = 5.508716749607697
TOL = 1e-9
