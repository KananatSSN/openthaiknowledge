"""Part2 item 5 figure: a uniform disc of radius R has a circular hole of radius kR cut so it touches the rim and its centre is (1 - k)R from O; k = 1/2. The rest's centre of mass is k^2 R/(1 + k) = R/6 from O, away from the hole."""

def solve(radius=12, ratio=0.5):
    return ratio * ratio * radius / (1 + ratio)


def check(radius=12, ratio=0.5, n=600):
    # Grid integration over the disc minus the hole.
    h = 2 * radius / n
    total = moment = 0.0
    hole_c, hole_r = (1 - ratio) * radius, ratio * radius
    for i in range(n):
        x = -radius + (i + 0.5) * h
        for j in range(n):
            y = -radius + (j + 0.5) * h
            if x * x + y * y <= radius * radius and (x - hole_c) ** 2 + y * y > hole_r**2:
                total += 1
                moment += x
    return -moment / total


PARAMS = {"radius": 12, "ratio": 0.5}
VARIANTS = [{"ratio": 1 / 3}, {"ratio": 0.25, "radius": 20}, {"ratio": 2 / 3}]
TOL = 1e-2
ANSWER = 2.0
