"""MC5 figure: picture 1 mass hanging at rest on the spring; picture 2 the mass is lifted a above that equilibrium, held and released; picture 3 the lowest point, x below the picture-1 level. SHM about equilibrium gives x = a (answer 4). Adapted quantity: the spring's greatest extension from its natural length, mg/k + a, in cm; requires a <= mg/k is not needed for an ideal spring but the generator keeps the spring stretched."""


def solve(mass=0.5, k=50, lift=4, g=10):
    static_cm = 100 * mass * g / k
    return static_cm + lift


def check(mass=0.5, k=50, lift=4, g=10):
    # Energy from the release point: mg drop = (k/2)(e_low^2 - e_release^2), with
    # extensions in metres. Bisect on the lowest extension.
    release = mass * g / k - lift / 100
    lo, hi = release + 1e-9, release + 10.0

    def residual(e):
        drop = e - release
        return mass * g * drop - k / 2 * (e * e - release * release)

    for _ in range(200):
        mid = (lo + hi) / 2
        if residual(mid) > 0:
            lo = mid
        else:
            hi = mid
    return 100 * (lo + hi) / 2


PARAMS = {"mass": 0.5, "k": 50, "lift": 4, "g": 10}
VARIANTS = [{"mass": 1, "k": 100, "lift": 5}, {"lift": 2}, {"k": 25, "lift": 10}]
ANSWER = 14.0
