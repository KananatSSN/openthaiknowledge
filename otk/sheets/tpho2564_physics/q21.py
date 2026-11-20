"""Theory 3.2 c): each half of the bilens has its optical centre a/2 off the axis, so its image lies on the line from the source through that centre and the two images are d = a(|v|/u - 1) = au/(f - u) apart. Adapted: u, f (cm) and the cut a (mm) vary; returns mm."""


def solve(source=15.0, focal=20.0, cut=1.0):
    return cut * source / (focal - source)


def check(source=15.0, focal=20.0, cut=1.0):
    from otk.sheets.tpho2564_physics import q20

    v = q20.check(source=source, focal=focal)
    # the line from (x = -u, y = 0) through (0, c) reaches y = c(1 - |v|/u) at x = -|v|
    upper = cut / 2 * (1 - v / source)
    return 2 * abs(upper)


PARAMS = {"source": 15.0, "focal": 20.0, "cut": 1.0}
VARIANTS = [{"source": 10.0}, {"cut": 2.0}, {"focal": 30.0}]
ANSWER = 3.0
TOL = 1e-9
