"""Source MC3: a lower adjacent electronic transition needs a shorter photon.

The source implicitly uses hydrogen-like levels, E_n proportional to -1/n².
"""


def solve(lower=3, wavelength_nm=600):
    assert lower >= 2 and wavelength_nm > 0
    gap_low = 1 / (lower - 1)**2 - 1 / lower**2
    gap_high = 1 / lower**2 - 1 / (lower + 1)**2
    required_nm = wavelength_nm * gap_high / gap_low
    return 0 if required_nm < wavelength_nm else 1 if required_nm > wavelength_nm else 2


def check(lower=3, wavelength_nm=600):
    levels = {n: -1 / n**2 for n in range(lower - 1, lower + 2)}
    low_frequency = levels[lower] - levels[lower - 1]
    high_frequency = levels[lower + 1] - levels[lower]
    implied_nm = wavelength_nm * high_frequency / low_frequency
    return 0 if implied_nm < wavelength_nm else 1 if implied_nm > wavelength_nm else 2


PARAMS = {"lower": 3, "wavelength_nm": 600}
VARIANTS = [
    {"lower": 4, "wavelength_nm": 550},
    {"lower": 5, "wavelength_nm": 650},
    {"lower": 6, "wavelength_nm": 720},
]
ANSWER = solve(**PARAMS)
