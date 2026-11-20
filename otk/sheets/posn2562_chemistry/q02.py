"""Source MC2: compare photons specified by frequency, energy, or wavelength."""

H = 6.62607015e-34
C = 299792458


def solve(frequency=4e12, energy=3.3e-23, long_nm=400, short_nm=300):
    energies = (H * frequency, energy, H * C / (long_nm * 1e-9),
                H * C / (short_nm * 1e-9))
    return max(range(4), key=lambda i: energies[i])


def check(frequency=4e12, energy=3.3e-23, long_nm=400, short_nm=300):
    # Put each choice on the frequency scale instead of the energy scale.
    equivalent = (frequency, energy / H, C * 1e9 / long_nm,
                  C * 1e9 / short_nm)
    winner = [i for i, value in enumerate(equivalent)
              if all(value > other for j, other in enumerate(equivalent) if i != j)]
    assert len(winner) == 1
    return winner[0]


PARAMS = {"frequency": 4e12, "energy": 3.3e-23, "long_nm": 400, "short_nm": 300}
VARIANTS = [
    {"frequency": 5e12, "energy": 4e-20, "long_nm": 500, "short_nm": 250},
    {"frequency": 8e11, "energy": 6e-22, "long_nm": 700, "short_nm": 350},
    {"frequency": 2e13, "energy": 2e-21, "long_nm": 550, "short_nm": 450},
]
ANSWER = solve(**PARAMS)
