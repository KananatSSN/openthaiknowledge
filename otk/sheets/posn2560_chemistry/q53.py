"""Source p13, MC53: 4% NH3 in equilibrium mix gives y(H2)=0.72 (ค)."""


def solve(ammonia_fraction=0.04):
    # 2NH3 -> N2 + 3H2. Mole fraction H2 is 3/4 of the non-NH3 fraction.
    assert 0 < ammonia_fraction < 1
    return round(0.75 * (1 - ammonia_fraction), 2)


def check(ammonia_fraction=0.04):
    # Start with one mole NH3 and solve its reacted fraction alpha from
    # remaining NH3/(all gas) = (1-alpha)/(1+alpha).
    alpha = (1 - ammonia_fraction) / (1 + ammonia_fraction)
    hydrogen_mol = 1.5 * alpha
    total_mol = 1 + alpha
    return round(hydrogen_mol / total_mol, 2)


PARAMS = {"ammonia_fraction": 0.04}
VARIANTS = [
    {"ammonia_fraction": 0.20},
    {"ammonia_fraction": 0.12},
    {"ammonia_fraction": 0.36},
]
ANSWER = 0.72
