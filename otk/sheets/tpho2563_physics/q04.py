"""Theory 1.2 a): a thin beam meeting a glass sphere (index n, radius R) at a - x from its centre is deviated (n - 1)/n times the incidence angle at each face, delta = 2((n - 1)/n)(a - x)/R for a, x << R. Adapted: the index, the beam offset a, the bead offset x and R (micrometres) vary; returns milliradians."""


def solve(index=1.5, beam=5.0, shift=2.0, radius=50.0):
    return 2 * (index - 1) / index * (beam - shift) / radius * 1e3


def check(index=1.5, beam=5.0, shift=2.0, radius=50.0):
    from otk.sheets.tpho2563_physics._shared import sphere_deviation

    return sphere_deviation(beam - shift, radius, index) * 1e3


PARAMS = {"index": 1.5, "beam": 5.0, "shift": 2.0, "radius": 50.0}
VARIANTS = [{"index": 1.6}, {"shift": 0.5}, {"radius": 100.0}]
ANSWER = 40.0
TOL = 1e-2
