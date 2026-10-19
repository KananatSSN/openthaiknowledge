"""Part2 item 11 figure: source emf E with internal r drives R; the load power P makes R a root of R^2 - (E^2/P - 2r) R + r^2 = 0, real only if P <= E^2/(4r). Watts."""


def solve(emf=12, internal=2):
    return emf * emf / (4 * internal)


def check(emf=12, internal=2):
    # Scan the load and take the largest power.
    best = 0.0
    for k in range(1, 200001):
        load = internal * k / 10000
        best = max(best, emf**2 * load / (internal + load) ** 2)
    return best


PARAMS = {"emf": 12, "internal": 2}
VARIANTS = [{"emf": 6, "internal": 0.5}, {"internal": 3}, {"emf": 20, "internal": 5}]
TOL = 1e-8
ANSWER = 18.0
