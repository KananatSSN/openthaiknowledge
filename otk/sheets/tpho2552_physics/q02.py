"""Theory 1.2 figure: a point source P, 21 cm from a thin convex lens (f = 12 cm), moves up perpendicular to the axis at 5.4 cm/s; the image (28 cm away, magnification -4/3) moves at 7.2 cm/s downward. Adapted: numbers vary; returns the image's velocity, upward positive, cm/s."""


def solve(focal=12, distance=21, speed=5.4):
    return -speed * focal / (distance - focal)


def check(focal=12, distance=21, speed=5.4):
    # Image height of the source at two nearby times, through the chief ray.
    image = 1 / (1 / focal - 1 / distance)

    def height(t):
        return -(speed * t) * image / distance

    dt = 1e-3
    return (height(dt) - height(0)) / dt


PARAMS = {"focal": 12, "distance": 21, "speed": 5.4}
VARIANTS = [{"distance": 16}, {"focal": 10, "distance": 30, "speed": 2}, {"speed": 9}]
ANSWER = -7.200000000000001
TOL = 1e-9
