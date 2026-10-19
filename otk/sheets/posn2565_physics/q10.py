"""MC10 figure: object at distance u in front of a diverging lens of focal -|f|; a concave mirror stands D behind the lens; the light returns onto the object. The ray must meet the mirror normally, i.e. head for its centre of curvature, which therefore sits at the lens's virtual image: R = D + u|f|/(u + |f|) (answer 3). cm."""


def solve(object_distance=30, focal=60, gap=20):
    return gap + object_distance * focal / (object_distance + focal)


def check(object_distance=30, focal=60, gap=20):
    # Paraxial ray trace with slopes taken per unit distance travelled. A
    # diverging lens adds y/|f|; a concave mirror of radius R turns the
    # travel slope s into s - 2y/R. Bisect R until the ray comes back to the
    # axis at the object.
    def miss(radius):
        y, s = 0.0, 0.01
        y += s * object_distance
        s += y / focal
        y += s * gap
        s = s - 2 * y / radius
        y += s * gap
        s += y / focal
        y += s * object_distance
        return y

    lo, hi = gap * 0.5, 1e5
    assert miss(lo) * miss(hi) < 0
    for _ in range(300):
        mid = (lo + hi) / 2
        if miss(lo) * miss(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2

PARAMS = {"object_distance": 30, "focal": 60, "gap": 20}
VARIANTS = [{"object_distance": 10, "focal": 10}, {"object_distance": 20, "focal": 30, "gap": 12}, {"gap": 50}]
TOL = 1e-6
ANSWER = 40.0
