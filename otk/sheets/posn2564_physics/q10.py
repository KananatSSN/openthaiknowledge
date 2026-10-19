"""MC10 figure: C1 carrying +q0/-q0 closes through switch SW and a resistor onto uncharged C2 in one loop. Heat in the resistor = q0^2/(2C1) - q0^2/(2(C1+C2)) = (1/2)(C2/C1)/(C1+C2) q0^2 (answer 3). Units: uF, uC, uJ."""


def solve(c1=2, c2=3, q0=10):
    return q0 * q0 * c2 / (2 * c1 * (c1 + c2))


def check(c1=2, c2=3, q0=10):
    # Integrate I^2 R dt while the charge flows (R = 1, time in units of RC).
    dt = 1e-4
    q1, q2, heat = float(q0), 0.0, 0.0
    for _ in range(400000):
        current = q1 / c1 - q2 / c2
        heat += current * current * dt
        q1 -= current * dt
        q2 += current * dt
        if abs(current) < 1e-12:
            break
    return heat


PARAMS = {"c1": 2, "c2": 3, "q0": 10}
VARIANTS = [{"c1": 1, "c2": 1}, {"c1": 4, "c2": 2, "q0": 12}, {"c2": 6}]
TOL = 1e-2
ANSWER = 15.0
