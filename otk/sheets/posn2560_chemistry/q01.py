"""Source p3, MC1: X reaches the screen behind the cathode; Y reaches the
screen behind the anode. X is a positive canal-ray ion, Y an electron.

The source's true choice ง compares their masses even when the gases differ.
The adaptation names a singly charged isotope ion and quantifies that mass
comparison using the stated approximation m_nucleon / m_e = 1836.
"""


def solve(nucleons=1, nucleon_to_electron=1836):
    if nucleons < 1 or nucleon_to_electron < 1:
        raise ValueError("positive particle masses required")
    return nucleons * nucleon_to_electron


def check(nucleons=1, nucleon_to_electron=1836):
    # At the same field and charge magnitude, acceleration is inversely
    # proportional to mass. Construct both accelerations independently.
    electron_acceleration = 1
    ion_acceleration = 1 / (nucleons * nucleon_to_electron)
    return round(electron_acceleration / ion_acceleration)


PARAMS = {"nucleons": 1, "nucleon_to_electron": 1836}
VARIANTS = [
    {"nucleons": 2, "nucleon_to_electron": 1836},
    {"nucleons": 4, "nucleon_to_electron": 1836},
    {"nucleons": 20, "nucleon_to_electron": 1836},
]
ANSWER = 1836
