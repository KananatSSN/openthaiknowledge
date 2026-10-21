"""MC29: methanol, nitrous acid and acetic acid all hydrogen-bond."""

GROUPS = (("H2S", "H2O", "CO2"), ("PH3", "AsH3", "NH3"),
          ("CS2", "SO2", "COCl2"), ("CH3OH", "HNO2", "CH3COOH"))
FORCE = {"H2S": "dipole", "H2O": "Hbond", "CO2": "dispersion",
         "PH3": "dipole", "AsH3": "dipole", "NH3": "Hbond",
         "CS2": "dispersion", "SO2": "dipole", "COCl2": "dipole",
         "CH3OH": "Hbond", "HNO2": "Hbond", "CH3COOH": "Hbond"}


def solve(order=(0, 1, 2, 3)):
    valid = [i for i, group in enumerate(GROUPS)
             if len({FORCE[molecule] for molecule in group}) == 1]
    assert valid == [3]
    return order.index(valid[0])


def check(order=(0, 1, 2, 3)):
    # Each member of the final group has an O-H donor and O acceptor.
    hbond = {"CH3OH", "HNO2", "CH3COOH", "H2O", "NH3"}
    assert all(mol in hbond for mol in GROUPS[3])
    assert all(any(mol not in hbond for mol in group) for group in GROUPS[:3])
    return order.index(3)


PARAMS = {"order": (0, 1, 2, 3)}
VARIANTS = [{"order": (3, 0, 1, 2)}, {"order": (1, 3, 2, 0)},
            {"order": (2, 1, 0, 3)}]
ANSWER = solve(**PARAMS)
