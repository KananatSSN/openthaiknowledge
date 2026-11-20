"""Source p8, MC20: C ionic, D ionizing molecular, A metal (choice ค).

The printed question says only 'covalent', although B, D and E all have
covalent molecular properties. Its choices make C,D,A uniquely selectable.
The adaptation explicitly identifies the covalent substance whose aqueous
solution conducts, so the generated answer remains unique.
"""

_PROPERTIES = (
    (1455, 2837, True, True, "insoluble"),
    (-56, -28, False, False, "no"),
    (685, 1324, False, True, "yes"),
    (-51, -35, False, False, "yes"),
    (-89, 118, False, False, "no"),
)


def solve(labels=("A", "B", "C", "D", "E")):
    metal = ionic = ionizing_molecular = None
    for label, (_, _, solid, liquid, water) in zip(labels, _PROPERTIES):
        if solid and liquid:
            metal = label
        elif not solid and liquid and water == "yes":
            ionic = label
        elif not solid and not liquid and water == "yes":
            ionizing_molecular = label
    return ionic, ionizing_molecular, metal


def check(labels=("A", "B", "C", "D", "E")):
    # Independently classify the fixed source rows by their physical models:
    # index 0 conducts in solid and melt, 2 only in melt/solution, 3 only
    # after dissolution and ionization.
    return labels[2], labels[3], labels[0]


PARAMS = {"labels": ("A", "B", "C", "D", "E")}
VARIANTS = [
    {"labels": ("C", "A", "E", "B", "D")},
    {"labels": ("E", "D", "B", "A", "C")},
    {"labels": ("B", "E", "A", "C", "D")},
]
ANSWER = ("C", "D", "A")
