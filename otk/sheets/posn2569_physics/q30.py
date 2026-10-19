"""Part2 item 20 figure: a parallel beam passes a diverging lens (focal -a) then a converging lens (focal +b) a distance x behind it, focusing d behind the second. The first lens's virtual image is a in front of it; that must be the second lens's object at u = b d/(d - b), so x = u - a. Source: a = f, b = 2f, d = 4f gives x = 3f. cm."""


def solve(diverging=10, converging=20, focus=40):
    return converging * focus / (focus - converging) - diverging


def check(diverging=10, converging=20, focus=40):
    # Paraxial ray trace with the separation bisected until the ray crosses
    # the axis at `focus` behind the second lens.
    def crossing(gap):
        y, s = 1.0, 0.0
        s += y / diverging
        y += s * gap
        s -= y / converging
        return -y / s

    lo, hi = 1e-6, 1e4
    for _ in range(300):
        mid = (lo + hi) / 2
        if crossing(mid) > focus:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"diverging": 10, "converging": 20, "focus": 40}
VARIANTS = [{"diverging": 5, "converging": 10, "focus": 30}, {"focus": 60}, {"diverging": 4, "converging": 12, "focus": 20}]
TOL = 1e-9
ANSWER = 30.0
