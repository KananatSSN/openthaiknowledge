"""Short22 figure: point stars M and m a fixed R apart circle their centre of mass at constant omega; total orbital KE = G M m / (2R). Returns KE / G for masses in kg and R in m."""


def solve(big=6, small=3, separation=2):
    return big * small / (2 * separation)


def check(big=6, small=3, separation=2):
    # omega^2 = G (M + m)/R^3 (G = 1), radii from the centre of mass, then sum.
    omega2 = (big + small) / separation**3
    r_big = small * separation / (big + small)
    r_small = big * separation / (big + small)
    return 0.5 * big * omega2 * r_big**2 + 0.5 * small * omega2 * r_small**2


PARAMS = {"big": 6, "small": 3, "separation": 2}
VARIANTS = [{"big": 10, "small": 1}, {"separation": 5}, {"big": 4, "small": 4, "separation": 1}]
ANSWER = 4.5
