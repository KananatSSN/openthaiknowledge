"""Part2 item 2 figure: a converging lens of focal f forms a real image of a real object only if their separation x is at least 4f. Returns the least separation."""


def solve(focal=10):
    return 4 * focal


def check(focal=10):
    # Scan object distances u > f; separation u + v with v = u f/(u - f).
    best = float("inf")
    for k in range(1, 400000):
        u = focal * (1 + k / 100000)
        best = min(best, u + u * focal / (u - focal))
    return best


PARAMS = {"focal": 10}
VARIANTS = [{"focal": 15}, {"focal": 4}, {"focal": 25}]
TOL = 1e-7
ANSWER = 40
