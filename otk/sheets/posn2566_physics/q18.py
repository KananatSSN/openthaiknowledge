"""MC18 figure: binary stars M and m a fixed R apart circle their centre of mass; m's orbit radius is M R/(M + m) (answer 2). Units: solar masses and AU."""


def solve(big=3, small=1, separation=8):
    return big * separation / (big + small)


def check(big=3, small=1, separation=8):
    # Bisect on m's radius so the two centripetal forces match (same omega).
    lo, hi = 0.0, float(separation)
    for _ in range(200):
        r = (lo + hi) / 2
        # m r omega^2 = M (R - r) omega^2
        if small * r < big * (separation - r):
            lo = r
        else:
            hi = r
    return (lo + hi) / 2


PARAMS = {"big": 3, "small": 1, "separation": 8}
VARIANTS = [{"big": 1, "small": 1}, {"big": 9, "small": 3, "separation": 4}, {"small": 2}]
ANSWER = 6.0
