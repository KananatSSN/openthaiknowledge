"""Source MC11: an alkali metal, unlike Be/Zn/NH3, gives H2 with cold water."""


def solve(alkali="K", second="Be", third="Zn", fourth="NH3"):
    assert alkali in ("Li", "Na", "K")
    assert {second, third} == {"Be", "Zn"} and fourth == "NH3"
    reacts_at_room_temp = (True, False, False, False)
    return reacts_at_room_temp.index(True)


def check(alkali="K", second="Be", third="Zn", fourth="NH3"):
    assert {second, third} == {"Be", "Zn"} and fourth == "NH3"
    # 2M + 2H2O -> 2MOH + H2 for each allowed alkali metal.
    gas_moles = {"Li": 0.5, "Na": 0.5, "K": 0.5,
                 "Be": 0, "Zn": 0, "NH3": 0}
    values = [gas_moles[x] for x in (alkali, second, third, fourth)]
    return values.index(max(values)) if values.count(max(values)) == 1 else None


PARAMS = {"alkali": "K", "second": "Be", "third": "Zn", "fourth": "NH3"}
VARIANTS = [
    {"alkali": "Li", "second": "Be", "third": "Zn", "fourth": "NH3"},
    {"alkali": "Na", "second": "Be", "third": "Zn", "fourth": "NH3"},
    {"alkali": "K", "second": "Zn", "third": "Be", "fourth": "NH3"},
]
ANSWER = solve(**PARAMS)
