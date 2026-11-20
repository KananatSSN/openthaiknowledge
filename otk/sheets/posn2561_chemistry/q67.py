"""Source p15, written 7: carbonyl fluoride Lewis structure and polarity."""


CHALCOGENS = {"O", "S"}
HALOGENS = {"F", "Cl"}


def solve(x="O", y="F"):
    assert x in CHALCOGENS and y in HALOGENS
    formula = f"C{x}{y}2"
    skeleton = f"{y}–C(={x})–{y}"
    return formula, skeleton, "dipole-dipole"


def check(x="O", y="F"):
    assert x in CHALCOGENS and y in HALOGENS
    # C uses four bond orders; group-16 X uses two, each halogen uses one.
    bond_orders = {"C": 2 + 1 + 1, x: 2, y: 1}
    assert bond_orders["C"] == 4 and bond_orders[x] == 2 and bond_orders[y] == 1
    molecular_formula = "C" + x + y + "2"
    lewis_bonds = y + "–C(=" + x + ")–" + y
    # Trigonal-planar CXY2 has nonidentical X and Y ends, so dipoles do not cancel.
    return molecular_formula, lewis_bonds, "dipole-dipole"


PARAMS = {"x": "O", "y": "F"}
VARIANTS = [{"x": "O", "y": "Cl"}, {"x": "S", "y": "F"},
            {"x": "S", "y": "Cl"}]
ANSWER = ("COF2", "F–C(=O)–F", "dipole-dipole")
