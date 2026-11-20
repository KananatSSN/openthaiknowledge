"""Constant-volume gas pressure follows absolute temperature."""


def solve(p1=2.0, t1=27, t2=327):
    return round(p1 * (t2 + 273) / (t1 + 273), 2)


def check(p1=2.0, t1=27, t2=327):
    # Ideal gas with nR/V calibrated by the initial state.
    factor = p1 / (t1 + 273)
    return round(factor * (t2 + 273), 2)


PARAMS = {"p1": 2.0, "t1": 27, "t2": 327}
VARIANTS = [
    {"p1": 1.5, "t1": 27, "t2": 327},
    {"p1": 3.0, "t1": 27, "t2": 327},
    {"p1": 2.0, "t1": 27, "t2": 477},
]
ANSWER = solve(**PARAMS)
