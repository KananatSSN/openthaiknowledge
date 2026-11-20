"""MC17 figure: lens A, a converging meniscus with R1 then R2 (both centres to the right), has 1/f_A = (mu - 1)(1/R1 - 1/R2). Lens B carries the same two surfaces in the other order, R2 then R1, curving the same way: thick at the edge, 1/f_B = (1 - mu)(1/R1 - 1/R2) (answer 3). cm."""


def solve(index=1.5, first=10, second=20):
    return 1 / ((1 - index) * (1 / first - 1 / second))


def check(index=1.5, first=10, second=20):
    # Paraxial ray trace through two refracting spheres (thin lens): a ray at
    # height y parallel to the axis; each surface of radius r (centre to the
    # right, positive) changes n*slope by -(n2 - n1) y / r.
    y = 1e-3
    slope = 0.0
    # Surface 1 of lens B: radius `second`, air -> glass
    slope = (1.0 * slope - (index - 1.0) * y / second) / index
    # Surface 2: radius `first`, glass -> air
    slope = index * slope - (1.0 - index) * y / first
    return -y / slope


PARAMS = {"index": 1.5, "first": 10, "second": 20}
VARIANTS = [{"index": 1.6, "first": 15, "second": 30}, {"first": 5}, {"index": 1.25, "second": 40}]
TOL = 1e-9
ANSWER = -40.0
