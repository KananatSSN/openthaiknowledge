"""Part2 item 9 figure: a projectile from O just grazes the tops of equal poles A (L1 from O) and B (L2 beyond A). Equal heights sit symmetrically about the apex, so the range is L1 + L2 + L1 and it lands L1 + L2 beyond A."""

def solve(first=6, second=10):
    return first + second


def check(first=6, second=10, pole=3.0, g=10.0):
    # Fit the parabola y = a x - b x^2 through (L1, h) and (L1 + L2, h), then
    # find the landing point.
    x1, x2 = first, first + second
    # a x1 - b x1^2 = h, a x2 - b x2^2 = h
    b = pole * (1 / x1 - 1 / x2) / (x2 - x1)
    a = pole / x1 + b * x1
    landing = a / b
    return landing - first


PARAMS = {"first": 6, "second": 10}
VARIANTS = [{"first": 2, "second": 5}, {"first": 10, "second": 1}, {"second": 30}]
ANSWER = 16
