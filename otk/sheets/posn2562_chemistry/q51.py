"""Subtract HCl chloride from AgCl precipitate; divide residual Cl by two."""


def solve(hcl_m=0.10, aliquot_l=0.025, agcl_g=0.574):
    chloride = agcl_g / 143.5
    ca_m = (chloride - hcl_m * aliquot_l) / (2 * aliquot_l)
    return round(ca_m * 111, 2)


def check(hcl_m=0.10, aliquot_l=0.025, agcl_g=0.574):
    for ca_g_l in (3.33, 6.66, 9.99, 13.32, 4.44, 5.55):
        predicted = (hcl_m + 2 * ca_g_l / 111) * aliquot_l * 143.5
        if abs(predicted - agcl_g) < 0.002:
            return round(ca_g_l, 2)
    raise ValueError("no concentration matches")


PARAMS = {"hcl_m": 0.10, "aliquot_l": 0.025, "agcl_g": 0.574}
VARIANTS = [
    {"hcl_m": 0.10, "aliquot_l": 0.05, "agcl_g": 1.148},
    {"hcl_m": 0.20, "aliquot_l": 0.025, "agcl_g": 0.93275},
    {"hcl_m": 0.10, "aliquot_l": 0.025, "agcl_g": 0.64575},
]

ANSWER = solve(**PARAMS)
