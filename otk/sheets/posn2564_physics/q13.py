"""MC13 figure: sunlight parallel to the axis through a converging lens f, no losses, onto a screen (3/4) f behind the lens. Beam radius shrinks to 1/4, intensity rises 16 times (answer 4). Adapted: screen at p f with 0 < p < 1; intensity ratio (1/(1 - p))^2."""


def solve(fraction=0.75):
    return (1 / (1 - fraction)) ** 2


def check(fraction=0.75):
    # Trace a marginal paraxial ray: height 1, slope change -y/f at the lens,
    # then compare the illuminated disc areas (same power through each).
    focal = 1.0
    height = 1.0
    slope = -height / focal
    at_screen = height + slope * fraction * focal
    return (height / at_screen) ** 2


PARAMS = {"fraction": 0.75}
VARIANTS = [{"fraction": 2 / 3}, {"fraction": 0.25}, {"fraction": 0.8}]
ANSWER = 16.0
