"""Theory 2.3.1 figure 2.3: a conducting wheel of radius r0 with spokes turns at omega in B; the brush on the rim and the one on the axle see (1/2) omega B r0^2 (the spokes are in parallel), so i = omega B r0^2/(2R). Adapted: numbers; amperes."""


def solve(omega=20, field=0.5, radius=0.2, resistor=2):
    return omega * field * radius**2 / (2 * resistor)


def check(omega=20, field=0.5, radius=0.2, resistor=2, spokes=8):
    # Each spoke is a source of emf integral of omega r B dr with no internal
    # resistance; any number of them in parallel give the same voltage.
    n = 2000
    emf = sum(omega * (radius * (k + 0.5) / n) * field * radius / n for k in range(n))
    parallel = emf  # identical ideal sources in parallel
    return parallel / resistor


PARAMS = {"omega": 20, "field": 0.5, "radius": 0.2, "resistor": 2}
VARIANTS = [{"omega": 50}, {"field": 1.0, "radius": 0.1}, {"resistor": 0.5}]
ANSWER = 0.10000000000000002
TOL = 1e-6
