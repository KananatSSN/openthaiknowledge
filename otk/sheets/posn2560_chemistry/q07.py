"""Source p5, MC7: Cr+ and Mn2+ both have five unpaired 3d electrons.

The source's other pairs are As/Mn2+, Cu2+/Cr3+, and As3+/Cu.
This model covers the listed free atoms/ions and a few related ions;
the neutral Cr and Cu exceptions are explicit. It assumes Hund filling
of separate orbitals, not ligand-field splitting in coordination complexes.
"""

_NEUTRAL = {
    "Cr": (5, 1, 0), "Mn": (5, 2, 0), "Fe": (6, 2, 0),
    "Co": (7, 2, 0), "Cu": (10, 1, 0), "As": (10, 2, 3),
}


def _occupations(symbol, charge):
    d, s, p = _NEUTRAL[symbol]
    if not isinstance(charge, int) or charge < 0 or charge > d + s + p:
        raise ValueError("unsupported charge")
    take = charge
    removed = min(take, p)
    p -= removed
    take -= removed
    removed = min(take, s)
    s -= removed
    take -= removed
    d -= take
    return d, s, p


def _unpaired(symbol, charge):
    d, s, p = _occupations(symbol, charge)
    return min(d, 10 - d) + min(s, 2 - s) + min(p, 6 - p)


def solve(first_symbol="Cr", first_charge=1, second_symbol="Mn", second_charge=2):
    return _unpaired(first_symbol, first_charge) == _unpaired(second_symbol, second_charge)


def check(first_symbol="Cr", first_charge=1, second_symbol="Mn", second_charge=2):
    def fill(symbol, charge):
        d, s, p = _NEUTRAL[symbol]
        electrons = ["3d"] * d + ["4s"] * s + ["4p"] * p
        for _ in range(charge):
            electrons.remove(max(electrons, key=lambda orbital: (int(orbital[0]),
                                                                  "spd".index(orbital[1]))))
        total = 0
        for orbital, boxes in (("3d", 5), ("4s", 1), ("4p", 3)):
            count = electrons.count(orbital)
            spins = [0] * boxes
            for i in range(count):
                spins[i % boxes] += 1
            total += spins.count(1)
        return total

    return fill(first_symbol, first_charge) == fill(second_symbol, second_charge)


PARAMS = {"first_symbol": "Cr", "first_charge": 1,
          "second_symbol": "Mn", "second_charge": 2}
VARIANTS = [
    {"first_symbol": "As", "first_charge": 0, "second_symbol": "Mn", "second_charge": 2},
    {"first_symbol": "As", "first_charge": 0, "second_symbol": "Cr", "second_charge": 3},
    {"first_symbol": "Cu", "first_charge": 2, "second_symbol": "Cu", "second_charge": 0},
    {"first_symbol": "As", "first_charge": 3, "second_symbol": "Cu", "second_charge": 0},
]
ANSWER = True
