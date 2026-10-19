"""Part2 item 1 figure: a symmetric biconvex lens (focal F) split along its middle plane gives two plano-convex lenses of focal 2F. Adapted: radii R1 : R2 = p : q; the half with radius R1 has focal F(1 + R1/R2)."""


def solve(focal=10, first=1, second=1):
    return focal * (1 + first / second)


def check(focal=10, first=1, second=1, index=1.5):
    # Lensmaker: find the radius scale that makes the whole lens focal F,
    # then the plano-convex half.
    # 1/F = (n - 1)(1/(s first) + 1/(s second)) -> s
    scale = (index - 1) * focal * (1 / first + 1 / second)
    return 1 / ((index - 1) / (scale * first))


PARAMS = {"focal": 10, "first": 1, "second": 1}
VARIANTS = [{"first": 1, "second": 2}, {"focal": 20, "first": 3, "second": 1}, {"first": 2, "second": 3}]
ANSWER = 20.0
