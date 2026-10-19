"""Short26 figure: a rod of cross-section A fits between rigid walls at t0; heated by dt it would grow alpha l0 dt; the walls hold it at l0, so the compressive force is F = Y A alpha dt. Returns newtons for Y in GPa, A in cm^2, alpha in 1e-6 per K."""


def solve(modulus=200, area=2, alpha=12, rise=50):
    return modulus * 1e9 * area * 1e-4 * alpha * 1e-6 * rise


def check(modulus=200, area=2, alpha=12, rise=50, length=1.5):
    # Free expansion, then the force that squeezes it back: F = Y A (dl / l).
    free = length * alpha * 1e-6 * rise
    strain = free / (length + free)
    # Small-strain answer uses the original length; correct to first order.
    return modulus * 1e9 * area * 1e-4 * strain * (1 + alpha * 1e-6 * rise)


PARAMS = {"modulus": 200, "area": 2, "alpha": 12, "rise": 50}
VARIANTS = [{"modulus": 70, "alpha": 23}, {"area": 5, "rise": 20}, {"modulus": 110, "alpha": 17, "rise": 100}]
ANSWER = 24000.0
