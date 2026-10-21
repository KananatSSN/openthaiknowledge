"""Figure table: C-H413, C-C348, C=C614, O-H463, O-O144, C-O360, C≡O1070; C=O unknown."""

FIGURE = {"C-H": 413, "C-C": 348, "C=C": 614, "O-H": 463, "O-O": 144, "C-O": 360, "C≡O": 1070}


def solve(delta_h=-78, c_c=348, c_triple_o=1070):
    # Common CH, CO and OH bonds cancel between methanol+CO and acetic acid.
    return c_triple_o - c_c - delta_h


def check(delta_h=-78, c_c=348, c_triple_o=1070):
    reactants = 3 * 413 + 360 + 463 + c_triple_o
    products_without_unknown = 3 * 413 + c_c + 360 + 463
    return reactants - products_without_unknown - delta_h


PARAMS = {"delta_h": -78, "c_c": 348, "c_triple_o": 1070}
VARIANTS = [
    {"delta_h": -58, "c_c": 348, "c_triple_o": 1070},
    {"delta_h": -78, "c_c": 328, "c_triple_o": 1070},
    {"delta_h": -100, "c_c": 348, "c_triple_o": 1070},
]

ANSWER = solve(**PARAMS)
