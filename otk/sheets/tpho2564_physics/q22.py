"""Theory 3.2 d): with the source at f each half sends a parallel beam tilted a/(2f) towards the axis; the beams, each (D - a)/2 wide, stop overlapping beyond L_max = f(D - a)/a. Adapted: f (cm), the lens height D and the cut a (mm) vary; returns cm."""


def solve(focal=20.0, height=40.0, cut=1.0):
    return focal * (height - cut) / cut


def check(focal=20.0, height=40.0, cut=1.0):
    from otk.sheets.tpho2564_physics._shared import bisect

    # overlap of the upper beam [-tL, w - tL] and the lower one [-w + tL, tL]
    tilt, width = cut / (2 * focal * 10), (height - cut) / 2

    def overlap(dist):
        return min(width - tilt * dist, tilt * dist) - max(-tilt * dist, -width + tilt * dist)

    return bisect(overlap, 1e-6, 1e9) / 10  # mm to cm


PARAMS = {"focal": 20.0, "height": 40.0, "cut": 1.0}
VARIANTS = [{"cut": 2.0}, {"focal": 30.0}, {"height": 25.0}]
ANSWER = 780.0
TOL = 1e-6
