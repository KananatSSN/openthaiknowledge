"""Short8 figure: a battery drives R1 and R2 in series; C1 sits across R1 and C2 across R2. In the steady state Q1/Q2 = C1 R1 / (C2 R2), which is 1 when R1 C1 = R2 C2."""


def solve(r1=2, c1=3, r2=3, c2=2):
    return c1 * r1 / (c2 * r2)


def check(r1=2, c1=3, r2=3, c2=2, emf=1.0):
    # Simulate from the switch-on instant. The battery fixes v1 + v2 = emf;
    # at t = 0+ the capacitors divide it as series capacitors; afterwards the
    # middle node's current balance gives (C1 + C2) dv1/dt = v2/R2 - v1/R1.
    v1 = emf * c2 / (c1 + c2)
    dt = 1e-3 * min(r1 * c1, r2 * c2)
    for _ in range(200000):
        v2 = emf - v1
        v1 += (v2 / r2 - v1 / r1) / (c1 + c2) * dt
    return c1 * v1 / (c2 * (emf - v1))


PARAMS = {"r1": 2, "c1": 3, "r2": 3, "c2": 2}
VARIANTS = [{"r1": 1, "c1": 1, "r2": 1, "c2": 3}, {"r2": 6}, {"r1": 4, "c1": 5}]
TOL = 1e-6
ANSWER = 1.0
