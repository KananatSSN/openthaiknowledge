"""MC6 figure: M at speed u on a smooth floor collects small masses m one at a time, sticking; after the N-th, v = M u / (M + N m) (answer 4)."""


def solve(big=6, small=1, count=3, speed=9):
    return big * speed / (big + count * small)


def check(big=6, small=1, count=3, speed=9):
    # Collide one at a time.
    mass, v = big, speed
    for _ in range(count):
        v = mass * v / (mass + small)
        mass += small
    return v


PARAMS = {"big": 6, "small": 1, "count": 3, "speed": 9}
VARIANTS = [{"count": 6}, {"big": 10, "small": 2, "count": 5, "speed": 6}, {"count": 1}]
ANSWER = 6.0
