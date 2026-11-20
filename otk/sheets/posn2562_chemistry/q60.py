"""Water colligative ratio ΔTf/ΔTb = Kf/Kb gives about -6.2 C."""


def solve(boiling_c=101.7, kb=0.512, kf=1.86):
    return round(-(boiling_c - 100) * kf / kb, 1)


def check(boiling_c=101.7, kb=0.512, kf=1.86):
    molality = (boiling_c - 100) / kb
    freezing_c = 0 - kf * molality
    return round(freezing_c, 1)


PARAMS = {"boiling_c": 101.7, "kb": 0.512, "kf": 1.86}
VARIANTS = [
    {"boiling_c": 101.0, "kb": 0.512, "kf": 1.86},
    {"boiling_c": 102.0, "kb": 0.512, "kf": 1.86},
    {"boiling_c": 100.5, "kb": 0.512, "kf": 1.86},
]

ANSWER = solve(**PARAMS)
