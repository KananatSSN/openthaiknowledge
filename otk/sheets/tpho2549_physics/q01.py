"""Theory 1.1 figure: a convex and a concave thin lens of the same focal length f, L apart (L < f), light entering the convex lens first; parallel light focuses f(f - L)/L beyond the concave lens, so (f(f - L)/L) + L from the convex lens. Adapted: numbers for f and L; cm."""


def solve(focal=20, gap=5):
    return focal * (focal - gap) / gap + gap


def check(focal=20, gap=5):
    # Trace a paraxial ray with ray-transfer matrices and find where it
    # crosses the axis.
    h, angle = 1.0, 0.0
    angle -= h / focal          # convex lens
    h += gap * angle            # travel L
    angle += h / focal          # concave lens (power -1/f)
    beyond = -h / angle
    return gap + beyond


PARAMS = {"focal": 20, "gap": 5}
VARIANTS = [{"gap": 10}, {"focal": 30, "gap": 1}, {"focal": 12, "gap": 9}]
ANSWER = 65.0
TOL = 1e-12
