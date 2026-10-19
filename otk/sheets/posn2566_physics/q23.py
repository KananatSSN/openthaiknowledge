"""Short23 figure: a nucleus at rest emits an alpha (mass m) with kinetic energy E; the daughter (mass M) recoils with KE (m/M) E. MeV."""


def solve(alpha=4, daughter=222, energy=5.5):
    return alpha * energy / daughter


def check(alpha=4, daughter=222, energy=5.5):
    # Equal and opposite momenta: p^2 = 2 m E, then KE = p^2 / (2 M).
    p2 = 2 * alpha * energy
    return p2 / (2 * daughter)


PARAMS = {"alpha": 4, "daughter": 222, "energy": 5.5}
VARIANTS = [{"daughter": 234, "energy": 4.2}, {"daughter": 206}, {"energy": 6}]
ANSWER = 0.0990990990990991
