"""Source p16, written 10: empirical and molecular formula from composition."""

from fractions import Fraction


MASSES = {"C": Fraction("12.01"), "H": Fraction("1.008"), "Br": Fraction("79.90")}
SCHOOL_MASSES = {"C": 12, "H": 1, "Br": 80}


def _formula(c, h, br):
    return f"C{c}H{h}Br{br if br > 1 else ''}"


def solve(carbon_pct="30.55", hydrogen_pct="1.71", bromine_pct="67.74",
          sample_g="4.72", volume_ml=200, molarity="0.100"):
    # Normalize amount of each element to bromine's amount, then reduce.
    moles = [Fraction(carbon_pct) / MASSES["C"],
             Fraction(hydrogen_pct) / MASSES["H"],
             Fraction(bromine_pct) / MASSES["Br"]]
    relative = [round(float(value / moles[2])) for value in moles]
    c, h, br = relative
    assert br == 1 and c > 0 and h > 0
    empirical_mass = c * SCHOOL_MASSES["C"] + h + br * SCHOOL_MASSES["Br"]
    molecular_mass = Fraction(sample_g) * 1000 / (Fraction(molarity) * volume_ml)
    multiple = round(float(molecular_mass / empirical_mass))
    assert abs(molecular_mass - multiple * empirical_mass) < Fraction(1, 20)
    return _formula(c, h, br), _formula(c * multiple, h * multiple, br * multiple)


def check(carbon_pct="30.55", hydrogen_pct="1.71", bromine_pct="67.74",
          sample_g="4.72", volume_ml=200, molarity="0.100"):
    targets = [Fraction(carbon_pct), Fraction(hydrogen_pct), Fraction(bromine_pct)]
    matches = []
    for c in range(1, 13):
        for h in range(1, 13):
            for br in range(1, 5):
                parts = [c * MASSES["C"], h * MASSES["H"], br * MASSES["Br"]]
                total = sum(parts)
                if all(abs(100 * part / total - target) < Fraction(3, 100)
                       for part, target in zip(parts, targets)):
                    matches.append((c + h + br, c, h, br))
    _, c, h, br = min(matches)
    # Search for the smallest integer multiple compatible with measured molarity.
    observed_mass = Fraction(sample_g) / (Fraction(molarity) * volume_ml / 1000)
    base_mass = c * 12 + h + br * 80
    multiple = next(k for k in range(1, 10)
                    if abs(observed_mass - k * base_mass) < Fraction(1, 20))
    return _formula(c, h, br), _formula(c * multiple, h * multiple, br * multiple)


PARAMS = {"carbon_pct": "30.55", "hydrogen_pct": "1.71",
          "bromine_pct": "67.74", "sample_g": "4.72",
          "volume_ml": 200, "molarity": "0.100"}
VARIANTS = [
    {**PARAMS, "sample_g": "11.80"},
    {**PARAMS, "sample_g": "7.08"},
    {**PARAMS, "sample_g": "9.44"},
]
ANSWER = ("C3H2Br", "C6H4Br2")
