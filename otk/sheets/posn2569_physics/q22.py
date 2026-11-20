"""Part2 item 12 figure: C1 holding Q is switched onto uncharged C2; energy left is C1/(C1 + C2) of before, as a percentage."""


def solve(first=3, second=1):
    return 100 * first / (first + second)


def check(first=3, second=1, charge=6.0):
    before = charge**2 / (2 * first)
    after = charge**2 / (2 * (first + second))
    return 100 * after / before


PARAMS = {"first": 3, "second": 1}
VARIANTS = [{"second": 3}, {"first": 1, "second": 4}, {"first": 7, "second": 3}]
ANSWER = 75.0
