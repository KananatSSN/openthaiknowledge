"""Short27 figure: parallel-plate capacitor of capacitance C, plate gap d, held at emf E. The plates attract with F = C E^2/(2d). Returns newtons for C in pF, E in volts and d in mm."""


def solve(capacitance=100, emf=1000, gap=1):
    return capacitance * 1e-12 * emf**2 / (2 * gap / 1000)


def check(capacitance=100, emf=1000, gap=1):
    # Charge on one plate times the field of the other plate alone (half the
    # gap field): F = Q * (E/d)/2.
    q = capacitance * 1e-12 * emf
    return q * (emf / (gap / 1000)) / 2


PARAMS = {"capacitance": 100, "emf": 1000, "gap": 1}
VARIANTS = [{"emf": 500}, {"capacitance": 20, "gap": 2}, {"emf": 3000, "gap": 0.5}]
ANSWER = 0.05
