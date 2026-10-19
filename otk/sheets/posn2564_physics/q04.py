"""MC4 figure: m moving at u hits M at rest on level ground; afterwards m has v and M has V, both rightward. With e = (V - v)/u < 1, m stops exactly when m/M = e (answer 3)."""


def solve(e=0.5):
    return e


def check(e=0.5):
    # For a trial mass ratio r = m/M, solve momentum plus restitution for m's
    # final velocity, then bisect on r until that velocity is zero.
    def final_v(r, u=1.0):
        # r u = r v + V and V - v = e u  =>  v = u (r - e) / (r + 1)
        big_v = (r * u + e * u * r) / (r + 1)
        return big_v - e * u

    lo, hi = 1e-9, 10.0
    for _ in range(200):
        mid = (lo + hi) / 2
        if final_v(mid) < 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


PARAMS = {"e": 0.5}
VARIANTS = [{"e": 0.25}, {"e": 0.8}, {"e": 2 / 3}]
ANSWER = 0.5
