"""MC4 figure: open tank crosssection A, water head h above bottom jet crosssection a. Finite tank surface speed (a/A)v matters; v=sqrt(2gh/(1-(a/A)^2)), source answer4. Instantaneous inviscid quasisteady Bernoulli; jet and surface atmospheric."""

from math import sqrt


def solve(height=5, g=10, area_ratio=0.2):
    return sqrt(2 * g * height / (1 - area_ratio**2))


def check(height=5, g=10, area_ratio=0.2):
    # Solve Bernoulli residual while satisfying continuity for each trial.
    lo, hi = 0.0, 1000.0
    for _ in range(100):
        outlet = (lo + hi) / 2
        surface = area_ratio * outlet
        if outlet * outlet / 2 < g * height + surface * surface / 2:
            lo = outlet
        else:
            hi = outlet
    return (lo + hi) / 2


PARAMS = {"height": 5, "g": 10, "area_ratio": 0.2}
VARIANTS = [{"height": 10}, {"area_ratio": 0.5}, {"area_ratio": 0.1}]
ANSWER = 10.206207261596576
