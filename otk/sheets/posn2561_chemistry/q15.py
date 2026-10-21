"""Source p5, MC15: beta-minus emission increases Z by one."""


RADIATIONS = ("α", "β⁻", "γ", "β⁺")


def solve(z=6, a=14):
    assert 1 < z < a - 1
    daughter_z = z + 1
    changes = (-2, 1, 0, -1)
    valid = [i for i, change in enumerate(changes) if z + change == daughter_z]
    assert len(valid) == 1
    return valid[0]


def check(z=6, a=14):
    # Conserve charge in each nuclear equation; daughter mass number stays A
    # for beta and gamma, while alpha also loses four nucleons.
    daughters = ((z - 2, a - 4), (z + 1, a), (z, a), (z - 1, a))
    target = (z + 1, a)
    return daughters.index(target)


PARAMS = {"z": 6, "a": 14}
VARIANTS = [
    {"z": 11, "a": 22},
    {"z": 27, "a": 60},
    {"z": 53, "a": 131},
]
ANSWER = 1
