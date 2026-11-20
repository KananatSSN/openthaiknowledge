"""Short14 figure: an object along the axis from A (2.0f) to B (1.5f) in front of a converging lens; its real image runs from 2f to 3f, so A'B'/AB = 2. Adapted: ends at a f and b f; ratio 1/((a - 1)(b - 1))."""


def solve(far=2.0, near=1.5):
    return 1 / ((far - 1) * (near - 1))


def check(far=2.0, near=1.5):
    # Image each end with the lens equation (f = 1) and take the length ratio.
    image = lambda u: 1 / (1 - 1 / u)
    return abs(image(near) - image(far)) / (far - near)


PARAMS = {"far": 2.0, "near": 1.5}
VARIANTS = [{"far": 3, "near": 2}, {"far": 5, "near": 3}, {"far": 2.5, "near": 1.25}]
ANSWER = 2.0
