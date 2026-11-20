"""Theory 1.3.3-1.3.4: at 30 cm the diffraction limit 336 microradians spans 101 um and the cone limit 42 microradians spans 13 um; pixels closer than 101 um cannot be resolved. Adapted: the viewing distance (cm), lambda (nm) and pupil (mm) vary; returns the largest unresolved pixel spacing in um (the diffraction limit)."""


def solve(distance=30.0, wavelength=550.0, pupil=2.0):
    return distance * 1e-2 * 1.22 * wavelength * 1e-9 / (pupil * 1e-3) * 1e6


def check(distance=30.0, wavelength=550.0, pupil=2.0, cone=1.0, depth=24.0):
    # The binding limit is the larger of the two angles; project it with tan.
    from math import tan

    diffraction = 1.22 * wavelength * 1e-9 / (pupil * 1e-3)
    cells = cone * 1e-6 / (depth * 1e-3)
    return distance * 1e-2 * tan(max(diffraction, cells)) * 1e6


PARAMS = {"distance": 30.0, "wavelength": 550.0, "pupil": 2.0}
VARIANTS = [{"distance": 50.0}, {"pupil": 3.0}, {"distance": 25.0, "wavelength": 450.0}]
ANSWER = 100.64999999999999
TOL = 1e-6
