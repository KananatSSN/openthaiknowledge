"""MC10 figure: convex thinlens, upright virtual image17cm fromlens on objectside. Magnitude M=1+17/f, source answer3. General image-distance magnitude d>0, focalf>0."""

from fractions import Fraction


def solve(distance=17, focal=10):
    return 1 + Fraction(distance, focal)


def check(distance=17, focal=10):
    # Shoot a ray parallel to axis at height1 through the lens, trace backward
    # until it intersects the virtual image plane x=-distance.
    slope = -1 / focal
    steps = 1000
    height = 1.0
    dx = -distance / steps
    for _ in range(steps):
        height += slope * dx
    # The central undeviated ray must meet this same point for a real object.
    object_distance = distance / height
    assert 0 < object_distance < focal
    assert abs(height - object_distance * height / focal - 1) < 1e-9
    return height


PARAMS = {"distance": 17, "focal": 10}
VARIANTS = [{"distance": 25}, {"focal": 20}, {"distance": 12, "focal": 8}]
ANSWER = Fraction(27, 10)
