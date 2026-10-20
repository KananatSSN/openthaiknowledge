"""Lab 1 part 1 figure: five identical diodes sit in two opposed series branches, so the forward and reverse threshold voltages are n V_d and (5 - n) V_d and one diode's threshold is V_d = (V_forward + V_reverse)/5. Adapted with synthetic thresholds read from the I-V graph (volts); returns V_d in volts."""


def solve(forward=1.30, reverse=1.95):
    return (forward + reverse) / 5


def check(forward=1.30, reverse=1.95):
    # Try every split of the five diodes and keep the one whose two branches
    # give the same single-diode threshold.
    best = min(range(1, 5), key=lambda n: abs(forward / n - reverse / (5 - n)))
    return forward / best


PARAMS = {"forward": 1.30, "reverse": 1.95}
VARIANTS = [{"forward": 0.62, "reverse": 2.48}, {"forward": 2.04, "reverse": 1.36}, {"forward": 2.80, "reverse": 0.70}]
ANSWER = 0.65
TOL = 1e-12
