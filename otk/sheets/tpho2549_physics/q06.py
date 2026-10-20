"""Theory 2(b): to push all the water out the air must be at Pa + rho g h, so the air's amount rises by the factor (Pa + rho g h)/Pa; the extra is rho g h/Pa times the original (1.39 for h = 14.13 m). Adapted: the depth from 2(a) with L and k given."""


def solve(length=8.0, fraction=0.5, pa=1.013e5, rho_g=1.0e4):
    depth = fraction * length + fraction * pa / ((1 - fraction) * rho_g)
    return rho_g * depth / pa


def check(length=8.0, fraction=0.5, pa=1.013e5, rho_g=1.0e4):
    # Ideal-gas moles at fixed T and volume LA: n ~ P V.
    depth = fraction * length + fraction * pa / ((1 - fraction) * rho_g)
    before = pa * length          # moles x RT / A at the surface
    after = (pa + rho_g * depth) * length
    return (after - before) / before


PARAMS = {"length": 8.0, "fraction": 0.5, "pa": 1.013e5, "rho_g": 1.0e4}
VARIANTS = [{"fraction": 0.25}, {"length": 5, "fraction": 0.6}, {"length": 10, "fraction": 0.2}]
ANSWER = 1.3948667324777888
TOL = 1e-12
