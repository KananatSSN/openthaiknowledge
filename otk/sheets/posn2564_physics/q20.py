"""MC20 figure: ladder from A: series 56, shunt 112 to the B rail, series 56, shunt 112, series 65, then R to the B rail. Each 56 + (112 || 112) stage is 112, so the last rung needs 65 + R = 112 and R = 47 ohm (answer 3). Adapted: series total/2, shunts total, last series given; R = total - last."""


def solve(total=112, last=65):
    return total - last


def check(total=112, last=65):
    # Evaluate the ladder forward and bisect on R for the required total.
    half = total / 2
    parallel = lambda x, y: x * y / (x + y)

    def ladder(r):
        tail = last + r
        tail = half + parallel(total, tail)
        return half + parallel(total, tail)

    lo, hi = 0.0, 100.0 * total
    for _ in range(200):
        mid = (lo + hi) / 2
        if ladder(mid) < total:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"total": 112, "last": 65}
VARIANTS = [{"total": 100, "last": 30}, {"total": 80, "last": 75}, {"total": 60, "last": 12}]
ANSWER = 47
