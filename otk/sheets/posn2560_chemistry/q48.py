"""Source p12, MC48: the mass ranking is a > b > c (ก)."""

_AVOGADRO = 6.02e23


def _masses(a_molecules, b_l, c_molecules, x_sample_g=22.0):
    return {
        "a": a_molecules / _AVOGADRO * 2,
        "b": b_l / 22.4 * 17,
        "c": c_molecules / _AVOGADRO * (x_sample_g / 0.25),
    }


def solve(a_molecules=30.1e23, b_l=3.36, c_molecules=1.5e22,
          x_sample_g=22.0):
    masses = _masses(a_molecules, b_l, c_molecules, x_sample_g)
    return tuple(sorted(masses, key=lambda label: -masses[label]))


def check(a_molecules=30.1e23, b_l=3.36, c_molecules=1.5e22,
          x_sample_g=22.0):
    # Independently convert each sample to mass via molecule counts: NH3's
    # gas volume corresponds to b_l/22.4 * N_A molecules at STP.
    mass_per_molecule = {
        "a": 2 / _AVOGADRO,
        "b": 17 / _AVOGADRO,
        "c": 4 * x_sample_g / _AVOGADRO,
    }
    counts = {"a": a_molecules, "b": b_l / 22.4 * _AVOGADRO,
              "c": c_molecules}
    masses = {label: counts[label] * mass_per_molecule[label] for label in counts}
    return tuple(sorted(masses, key=lambda label: -masses[label]))


PARAMS = {"a_molecules": 30.1e23, "b_l": 3.36, "c_molecules": 1.5e22,
          "x_sample_g": 22.0}
VARIANTS = [
    {"a_molecules": 3.01e23, "b_l": 3.36, "c_molecules": 1.5e22,
     "x_sample_g": 22.0},
    {"a_molecules": 6.02e23, "b_l": 4.48, "c_molecules": 3.01e22,
     "x_sample_g": 22.0},
    {"a_molecules": 12.04e23, "b_l": 2.24, "c_molecules": 1.5e22,
     "x_sample_g": 22.0},
]
ANSWER = ("a", "b", "c")
