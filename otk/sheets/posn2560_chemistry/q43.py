"""Source p11, MC43 has two true choices: C 0.36 kg and CO2 672 L.

The repaired adaptation asks for the pair of true statements.
"""

_DEFAULT_CLAIMS = (("carbon_kg", 0.36), ("hematite_mol", 20.0),
                   ("oxygen_mol", 10.0), ("co2_l", 672.0))


def _amounts(iron_kg):
    iron_mol = iron_kg * 1000 / 56
    return {
        "carbon_kg": 1.5 * iron_mol * 12 / 1000,
        "hematite_mol": iron_mol / 2,
        "oxygen_mol": 0.75 * iron_mol,
        "co2_l": 1.5 * iron_mol * 22.4,
    }


def solve(iron_kg=1.12, claims=_DEFAULT_CLAIMS):
    expected = _amounts(iron_kg)
    true = tuple(i for i, (kind, value) in enumerate(claims)
                 if abs(expected[kind] - value) < 1e-7)
    assert len(true) == 2
    return true


def check(iron_kg=1.12, claims=_DEFAULT_CLAIMS):
    # One extent of Fe2O3 reduction produces 2 mol Fe and needs 3 mol CO;
    # producing 3 mol CO requires 3 mol C and 1.5 mol O2.
    reduction_extent = iron_kg * 1000 / (2 * 56)
    produced_co2_mol = 3 * reduction_extent
    facts = (
        3 * reduction_extent * 12 / 1000,
        reduction_extent,
        1.5 * reduction_extent,
        produced_co2_mol * 22.4,
    )
    return tuple(i for i, (_, value) in enumerate(claims)
                 if abs(facts[i] - value) < 1e-7)


PARAMS = {"iron_kg": 1.12, "claims": _DEFAULT_CLAIMS}
VARIANTS = [
    {"iron_kg": 0.56, "claims": (("carbon_kg", 0.18), ("hematite_mol", 5.0),
                                  ("oxygen_mol", 5.0), ("co2_l", 672.0))},
    {"iron_kg": 2.24, "claims": (("carbon_kg", 0.72), ("hematite_mol", 40.0),
                                  ("oxygen_mol", 30.0), ("co2_l", 672.0))},
    {"iron_kg": 3.36, "claims": (("carbon_kg", 0.36), ("hematite_mol", 30.0),
                                  ("oxygen_mol", 45.0), ("co2_l", 672.0))},
]
ANSWER = (0, 3)
