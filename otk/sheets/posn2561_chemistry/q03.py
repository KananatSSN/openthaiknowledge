"""Source p3, MC3: among four listed lines, only E(C) > E(B) is true.

The heading says five lines but labels only A, B, C, D. The adaptation
explicitly says four. For the recorded variants, wavelengths remain ordered
A > B > C > D so the comparison remains unique.
"""


def solve(a_nm=656, b_nm=486, c_nm=434, d_nm=410):
    # Photon energy and frequency both scale as the inverse wavelength.
    statements = (a_nm < b_nm, c_nm < b_nm, a_nm < c_nm, d_nm > max(a_nm, b_nm, c_nm))
    true = [index for index, claim in enumerate(statements) if claim]
    assert len(true) == 1
    return true[0]


def check(a_nm=656, b_nm=486, c_nm=434, d_nm=410):
    h = 6.62607015e-34
    speed = 299792458
    wavelengths = [value * 1e-9 for value in (a_nm, b_nm, c_nm, d_nm)]
    frequencies = [speed / value for value in wavelengths]
    energies = [h * value for value in frequencies]
    statements = (frequencies[0] > frequencies[1], energies[2] > energies[1],
                  energies[0] > energies[2], energies[3] < min(energies[:3]))
    true = [index for index, claim in enumerate(statements) if claim]
    assert len(true) == 1
    return true[0]


PARAMS = {"a_nm": 656, "b_nm": 486, "c_nm": 434, "d_nm": 410}
VARIANTS = [
    {"a_nm": 700, "b_nm": 520, "c_nm": 470, "d_nm": 420},
    {"a_nm": 620, "b_nm": 500, "c_nm": 450, "d_nm": 390},
    {"a_nm": 780, "b_nm": 600, "c_nm": 550, "d_nm": 460},
]
ANSWER = 1
