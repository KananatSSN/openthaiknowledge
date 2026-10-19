"""MC15 figure: masses A and B on the ends of a spring of natural length l oscillate symmetrically about O; each is l/2 + x from O, so the spring is stretched by 2x and pulls B with k(2x) = 2kx (answer 4). Returns newtons for k in N/m and x in cm."""


def solve(k=50, x=4):
    return k * 2 * x / 100


def check(k=50, x=4):
    # Positions of the two blocks, spring length minus natural length, Hooke.
    natural = 0.3
    a, b = -(natural / 2 + x / 100), natural / 2 + x / 100
    return k * ((b - a) - natural)


PARAMS = {"k": 50, "x": 4}
VARIANTS = [{"k": 200, "x": 1}, {"x": 10}, {"k": 75, "x": 6}]
ANSWER = 4.0
