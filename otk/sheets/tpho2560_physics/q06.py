"""Theory 1.3.2: without diffraction two points are resolved when their images fall on neighbouring cone cells 1.0 um apart, 24 mm behind the pupil: 1.0 um/24 mm = 42 microradians. Adapted: the cone spacing (um) and eye depth (mm) vary; returns the angle in microradians."""


def solve(cone=1.0, depth=24.0):
    return cone * 1e-6 / (depth * 1e-3) * 1e6


def check(cone=1.0, depth=24.0):
    # Exact pinhole geometry: the angle subtended by one spacing at the pupil.
    from math import atan

    return atan(cone * 1e-6 / (depth * 1e-3)) * 1e6


PARAMS = {"cone": 1.0, "depth": 24.0}
VARIANTS = [{"cone": 2.5}, {"depth": 20.0}, {"cone": 1.5, "depth": 22.0}]
ANSWER = 41.666666666666664
TOL = 1e-6
