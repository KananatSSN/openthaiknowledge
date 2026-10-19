"""MC15 figure: plano-convex lens, 1/f = (mu - 1)/R; f is proportional to R, so df/f = dR/R (answer 1). Adapted: the change in f in cm for a small dR."""


def solve(index=1.5, radius=20, change=0.2):
    return change / (index - 1)


def check(index=1.5, radius=20, change=0.2):
    # Central finite difference of the lensmaker focal length.
    focal = lambda r: r / (index - 1)
    h = 1e-6
    return (focal(radius + h) - focal(radius - h)) / (2 * h) * change


PARAMS = {"index": 1.5, "radius": 20, "change": 0.2}
VARIANTS = [{"index": 1.6, "change": 0.3}, {"index": 1.25, "radius": 10}, {"index": 2, "change": 0.5}]
TOL = 1e-8
ANSWER = 0.4
