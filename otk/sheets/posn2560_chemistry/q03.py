"""Source p4, MC3: 97 nm excites hydrogen from n=1 to n=4.

Figure reading: the labelled 97 nm Lyman transition joins n=1 and n=4.
For an ensemble, all downward transitions among levels 1..n can occur.
The adaptation states n explicitly, so a rounded wavelength is never used
to decide whether an ideal monochromatic photon is resonant.
"""

from fractions import Fraction


def solve(upper=4):
    if not isinstance(upper, int) or upper < 2:
        raise ValueError("upper must be an integer at least 2")
    return upper * (upper - 1) // 2


def check(upper=4):
    # Construct exact Bohr energy differences, rather than count pairs.
    energies = [Fraction(-1, n * n) for n in range(1, upper + 1)]
    frequencies = {high - low for low in energies for high in energies if high > low}
    return len(frequencies)


PARAMS = {"upper": 4}
VARIANTS = [{"upper": 2}, {"upper": 3}, {"upper": 6}, {"upper": 8}]
ANSWER = 6
