"""Theory 3.2 f): the overlap is widest, (D - a)/2, at L_max/2, so the screen shows at most N = (D - a)a/(2 lambda f) fringes. Adapted: lambda (nm), f (cm), the lens height D and cut a (mm) vary."""


def solve(wavelength=600.0, focal=20.0, height=40.0, cut=1.0):
    return (height - cut) * 1e-3 * cut * 1e-3 / (2 * wavelength * 1e-9 * focal * 1e-2)


def check(wavelength=600.0, focal=20.0, height=40.0, cut=1.0):
    from otk.sheets.tpho2564_physics import q23
    from otk.sheets.tpho2564_physics._shared import golden_min

    tilt, width = cut / (2 * focal * 10), (height - cut) / 2  # mm per mm, mm

    def overlap(dist):
        return min(width - tilt * dist, tilt * dist) - max(-tilt * dist, -width + tilt * dist)

    best = golden_min(lambda dist: -overlap(dist), 0.0, width / tilt)
    return overlap(best) / q23.solve(wavelength=wavelength, focal=focal, cut=cut)


PARAMS = {"wavelength": 600.0, "focal": 20.0, "height": 40.0, "cut": 1.0}
VARIANTS = [{"wavelength": 450.0}, {"cut": 2.0}, {"height": 25.0}]
ANSWER = 162.49999999999997
TOL = 1e-6
