"""Theory 3 C.4 figure 3.9: a focusing lens f and a defocusing lens -f a distance L apart (L < f) focus along x at f(f - L)/L behind the second lens, and along y (defocusing first) at f(f + L)/L, so the pair focuses both ways. Adapted: f and L (m) vary; returns f'_x in metres."""


def solve(focal=20.0, gap=2.0):
    return focal * (focal - gap) / gap


def check(focal=20.0, gap=2.0):
    # Ray transfer matrices: lens f, drift L, lens -f; a parallel ray's
    # crossing point behind the second lens.
    def lens(f):
        return ((1.0, 0.0), (-1.0 / f, 1.0))

    def drift(d):
        return ((1.0, d), (0.0, 1.0))

    def mul(a, b):
        return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))

    system = mul(lens(-focal), mul(drift(gap), lens(focal)))
    h, angle = system[0][0], system[1][0]
    return -h / angle


PARAMS = {"focal": 20.0, "gap": 2.0}
VARIANTS = [{"gap": 5.0}, {"focal": 50.0}, {"focal": 8.0, "gap": 3.0}]
ANSWER = 180.0
TOL = 1e-9
