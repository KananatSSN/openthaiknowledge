"""2% w/v Hg in one litre requires 20 g Hg, or 32.4 g Hg(NO3)2."""


def solve(volume_l=1, hg_percent_wv=2, hg_atomic=200):
    hg_g = hg_percent_wv * volume_l * 10
    return round(hg_g * (hg_atomic + 2 * 62) / hg_atomic, 2)


def check(volume_l=1, hg_percent_wv=2, hg_atomic=200):
    salt_mol = (hg_percent_wv / 100) * (volume_l * 1000) / hg_atomic
    return round(salt_mol * (hg_atomic + 2 * (14 + 3 * 16)), 2)


PARAMS = {"volume_l": 1, "hg_percent_wv": 2, "hg_atomic": 200}
VARIANTS = [
    {"volume_l": 0.5, "hg_percent_wv": 2, "hg_atomic": 200},
    {"volume_l": 1, "hg_percent_wv": 1, "hg_atomic": 200},
    {"volume_l": 1, "hg_percent_wv": 3, "hg_atomic": 200},
]

ANSWER = solve(**PARAMS)
