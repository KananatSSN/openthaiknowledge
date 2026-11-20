"""MC12: real image by thin lens 1/v + 1/u = 1/f; f grows by small df with u fixed at u0. dv = (u0/(u0 - f))^2 df (answer 2). Returns the factor dv/df."""


def solve(focal=10, object_distance=30):
    return (object_distance / (object_distance - focal)) ** 2


def check(focal=10, object_distance=30):
    # Central finite difference of the image distance from the lens equation.
    image = lambda f: 1 / (1 / f - 1 / object_distance)
    h = 1e-5 * focal
    return (image(focal + h) - image(focal - h)) / (2 * h)


PARAMS = {"focal": 10, "object_distance": 30}
VARIANTS = [{"focal": 20, "object_distance": 30}, {"object_distance": 15}, {"focal": 12, "object_distance": 60}]
TOL = 1e-6
ANSWER = 2.25
