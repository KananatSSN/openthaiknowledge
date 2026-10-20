"""Lab 1 part 2 figure 3: the current is the 2.00 kOhm resistor's voltage over 2000 Ohm; above the threshold the diode set and R obey V = V_on + I R, so R is the slope of V against I (least squares). Adapted with synthetic readings (V across the 2 kOhm resistor, V across diodes and R); returns R in ohms."""


def solve(readings=((1.0, 1.85), (1.5, 2.15), (2.0, 2.45), (2.5, 2.75), (3.0, 3.05))):
    current = [a / 2000 for a, _ in readings]
    volts = [b for _, b in readings]
    n = len(readings)
    mx, my = sum(current) / n, sum(volts) / n
    return sum((x - mx) * (y - my) for x, y in zip(current, volts)) / sum((x - mx) ** 2 for x in current)


def check(readings=((1.0, 1.85), (1.5, 2.15), (2.0, 2.45), (2.5, 2.75), (3.0, 3.05))):
    # Normal equations solved by Cramer's rule.
    xs = [a / 2000 for a, _ in readings]
    ys = [b for _, b in readings]
    n, sx, sy = len(xs), sum(xs), sum(ys)
    sxx, sxy = sum(x * x for x in xs), sum(x * y for x, y in zip(xs, ys))
    return (n * sxy - sx * sy) / (n * sxx - sx * sx)


PARAMS = {"readings": ((1.0, 1.85), (1.5, 2.15), (2.0, 2.45), (2.5, 2.75), (3.0, 3.05))}
VARIANTS = [
    {"readings": ((0.8, 2.02), (1.2, 2.22), (1.6, 2.42), (2.0, 2.62))},
    {"readings": ((1.0, 1.0), (2.0, 2.1), (3.0, 3.1), (4.0, 4.2))},
    {"readings": ((2.0, 3.30), (2.4, 3.54), (2.8, 3.78))},
]
ANSWER = 1200.0
TOL = 1e-9
