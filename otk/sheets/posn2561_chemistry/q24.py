"""Source p7, MC24: identify three water-soluble covalent substances."""


GROUPS = (
    ("กลูโคส", "เบนซีน", "คาร์บอนไดออกไซด์แข็ง"),
    ("เอทานอล", "ไฮโดรเจนฟลูออไรด์", "กรดแอซีติก"),
    ("ไฮโดรเจนคลอไรด์", "คาร์บอนเตตระคลอไรด์", "ซิลิคอนไดออกไซด์"),
    ("คาร์บอนไดซัลไฟด์", "ออกซิเจนไดฟลูออไรด์", "แอมโมเนียมคลอไรด์"),
)


def solve(options=(0, 1, 2, 3)):
    assert sorted(options) == [0, 1, 2, 3]
    water_soluble = {"กลูโคส", "เอทานอล", "ไฮโดรเจนฟลูออไรด์",
                     "กรดแอซีติก", "ไฮโดรเจนคลอไรด์", "แอมโมเนียมคลอไรด์"}
    covalent = set().union(*map(set, GROUPS)) - {"แอมโมเนียมคลอไรด์"}
    matches = [i for i, option in enumerate(options)
               if all(substance in water_soluble & covalent
                      for substance in GROUPS[option])]
    assert len(matches) == 1
    return matches[0]


def check(options=(0, 1, 2, 3)):
    # Each wrong row has a separate decisive counterexample: benzene,
    # CCl4 and CS2 are poorly water soluble; ammonium chloride is ionic.
    counterexample = {0: "เบนซีน", 2: "คาร์บอนเตตระคลอไรด์",
                      3: "คาร์บอนไดซัลไฟด์"}
    for row, substance in counterexample.items():
        assert substance in GROUPS[row]
    return options.index(next(row for row in range(4)
                              if row not in counterexample))


PARAMS = {"options": (0, 1, 2, 3)}
VARIANTS = [
    {"options": (1, 0, 2, 3)},
    {"options": (2, 3, 1, 0)},
    {"options": (3, 2, 0, 1)},
]
ANSWER = 1
