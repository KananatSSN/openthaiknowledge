"""Theory 3(b): light of wavelength lambda from an electron oscillating at omega = 2 pi c/lambda in Thomson's hydrogen means R = (e^2/(4 pi eps0 m omega^2))^(1/3). For 656 nm this is 0.313 nm with the paper's constants; the marking scheme prints ~0.28 nm. Adapted: lambda in nm; R in nm."""

from math import pi

E, M, EPS0, C = 1.6e-19, 9.1e-31, 8.85e-12, 3.0e8


def solve(wavelength=656):
    omega = 2 * pi * C / (wavelength * 1e-9)
    return (E * E / (4 * pi * EPS0 * M * omega**2)) ** (1 / 3) * 1e9


def check(wavelength=656):
    # Bisect on R until the oscillation frequency, from the Gauss's-law force
    # constant, emits the given wavelength.
    from math import sqrt

    def emitted(radius_nm):
        r = radius_nm * 1e-9
        omega = sqrt(E * E / (4 * pi * EPS0 * M * r**3))
        return 2 * pi * C / omega * 1e9

    lo, hi = 1e-4, 100.0
    for _ in range(200):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if emitted(mid) < wavelength else (lo, mid)
    return lo


PARAMS = {"wavelength": 656}
VARIANTS = [{"wavelength": 486}, {"wavelength": 434}, {"wavelength": 1000}]
ANSWER = 0.3129082091066258
TOL = 1e-9
