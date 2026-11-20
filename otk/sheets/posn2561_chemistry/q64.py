"""Source p14, written 4: Cr/Mn/Fe from consecutive transition metals."""


CLUES = {
    "heme": "X เป็นโลหะตรงกลางของฮีมในเม็ดเลือดแดง",
    "atomic_number": "X มีเลขอะตอม 26",
    "symbol": "X มีสัญลักษณ์ Fe",
    "hemoglobin": "X เป็นโลหะที่จับ O₂ ในฮีโมโกลบิน",
}
FIRST_ROW = ("Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn")


def solve(clue="heme"):
    assert clue in CLUES
    x = "Fe"
    index = FIRST_ROW.index(x)
    m, middle = FIRST_ROW[index - 2:index]
    assert (m, middle) == ("Cr", "Mn")
    # Highest oxidation state of Cr is +6, so three O²⁻ are needed.
    return "CrO3", "[Ar]3d5 4s2", x


def check(clue="heme"):
    assert clue in CLUES
    atomic_numbers = {"Cr": 24, "Mn": 25, "Fe": 26}
    assert [atomic_numbers[name] for name in ("Cr", "Mn", "Fe")] == [24, 25, 26]
    oxide_oxygen = 6 // 2
    manganese_d = atomic_numbers["Mn"] - 18 - 2
    return f"CrO{oxide_oxygen}", f"[Ar]3d{manganese_d} 4s2", "Fe"


PARAMS = {"clue": "heme"}
VARIANTS = [{"clue": "atomic_number"}, {"clue": "symbol"},
            {"clue": "hemoglobin"}]
ANSWER = ("CrO3", "[Ar]3d5 4s2", "Fe")
