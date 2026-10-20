"""Lab part 1: a sheet pulled out between two sheets under a load W0 rubs on two faces, so mu = <T>/(2 W0); four large nuts (153.6 g, W0 = 1.507 N) and pulls of 1.681, 1.586, 1.606, 1.606 and 1.586 N give mu = 0.53. Adapted: the number of 38.4 g nuts and the five pulls (N) vary."""

PULLS = (1.681, 1.586, 1.606, 1.606, 1.586)


def solve(nuts=4, pulls=PULLS):
    load = nuts * 38.4e-3 * 9.81
    return sum(pulls) / len(pulls) / (2 * load)


def check(nuts=4, pulls=PULLS):
    # the mean of the five single-pull coefficients
    load = nuts * 38.4e-3 * 9.81
    return sum(t / (2 * load) for t in pulls) / len(pulls)


PARAMS = {"nuts": 4, "pulls": PULLS}
VARIANTS = [{"nuts": 3}, {"pulls": (1.20, 1.25, 1.18, 1.22, 1.21)}, {"nuts": 6, "pulls": (2.6, 2.5, 2.55, 2.62, 2.48)}]
ANSWER = 0.5352345608222903
TOL = 1e-9
