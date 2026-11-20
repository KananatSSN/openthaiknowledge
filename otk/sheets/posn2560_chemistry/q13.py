"""Source p6, MC13: Cl2O7 and P4O10 acidify water (choice ข)."""

_PRODUCTS = {
    "P4O10": "H3PO4", "Cl2O7": "HClO4", "SO3": "H2SO4",
    "N2O5": "HNO3", "Na2O": "NaOH", "K2O": "KOH",
    "Cr2O3": None, "Al2O3": None,
}


def solve(oxides=("P4O10", "Cr2O3", "Cl2O7", "Na2O")):
    return tuple(sorted(oxide for oxide in oxides if _PRODUCTS[oxide]
                        and _PRODUCTS[oxide].startswith("H")))


def check(oxides=("P4O10", "Cr2O3", "Cl2O7", "Na2O")):
    # Independent acid-anhydride classification: these nonmetal oxides
    # form oxyacids; alkali oxides form hydroxides, and the amphoteric
    # trivalent oxides do not react appreciably with water.
    acidic_anhydrides = {"P4O10", "Cl2O7", "SO3", "N2O5"}
    return tuple(sorted(set(oxides) & acidic_anhydrides))


PARAMS = {"oxides": ("P4O10", "Cr2O3", "Cl2O7", "Na2O")}
VARIANTS = [
    {"oxides": ("SO3", "Al2O3", "N2O5", "K2O")},
    {"oxides": ("P4O10", "Na2O", "SO3", "Cr2O3")},
    {"oxides": ("Cl2O7", "K2O", "N2O5", "Al2O3")},
]
ANSWER = ("Cl2O7", "P4O10")
