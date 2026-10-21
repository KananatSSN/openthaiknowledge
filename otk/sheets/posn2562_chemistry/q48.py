"""Combustion gives C and H masses; O follows by subtraction."""


def solve(sample_mg=4.00, co2_mg=5.86, h2o_mg=2.40, order=(0, 1, 2, 3)):
    c = co2_mg * 12 / 44
    h = h2o_mg * 2 / 18
    o = sample_mg - c - h
    claims = (abs(c / h - 8) < 0.3, abs(o / sample_mg * 100 - 53.3) < 0.3, abs(c - 1.6) < 0.05)
    groups = ({1, 2}, {1, 3}, {2, 3}, {1, 2, 3})
    return order.index(groups.index({i + 1 for i, v in enumerate(claims) if v}))


def check(sample_mg=4.00, co2_mg=5.86, h2o_mg=2.40, order=(0, 1, 2, 3)):
    carbon_percent = 100 * (co2_mg / 44 * 12) / sample_mg
    hydrogen_percent = 100 * (h2o_mg / 18 * 2) / sample_mg
    oxygen_percent = 100 - carbon_percent - hydrogen_percent
    mass_c = carbon_percent / 100 * sample_mg
    truths = (
        abs(carbon_percent / hydrogen_percent - 8) < 0.3,
        abs(oxygen_percent - 53.3) < 0.3,
        abs(mass_c - 1.6) < 0.05,
    )
    assert truths == (False, True, True)
    return order.index(2)


PARAMS = {"sample_mg": 4.0, "co2_mg": 5.86, "h2o_mg": 2.4, "order": (0, 1, 2, 3)}
VARIANTS = [
    {"sample_mg": 4.0, "co2_mg": 5.86, "h2o_mg": 2.4, "order": (1, 0, 2, 3)},
    {"sample_mg": 4.0, "co2_mg": 5.86, "h2o_mg": 2.4, "order": (2, 3, 0, 1)},
    {"sample_mg": 4.0, "co2_mg": 5.86, "h2o_mg": 2.4, "order": (3, 1, 2, 0)},
]
ANSWER = solve(**PARAMS)
