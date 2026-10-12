"""Wave F slice 35 — เคมีเพิ่มเติม 2: equilibrium at work, and acid-base
theories and conjugate pairs.

Three ``additional_outcome`` indicators, each filed whole:

* ``เคมีเพิ่มเติม 2 ม.5/13`` — equilibria in living things, in nature and in
  industry;
* ``เคมีเพิ่มเติม 2 ม.5/14`` — acids and bases by Arrhenius, Brønsted-Lowry
  and Lewis;
* ``เคมีเพิ่มเติม 2 ม.5/15`` — Brønsted-Lowry conjugate acid-base pairs.
"""

from __future__ import annotations

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}


# ══ ม.5/13 — สมดุลเคมีในชีวิตประจำวัน ═══════════════════════════════════════════════


# ══ ม.5/14 — ทฤษฎีกรด-เบส ═════════════════════════════════════════════════════════

# (equation, Brønsted acid, Brønsted base, conjugate acid, conjugate base) for the forward reaction
BL_REACTIONS = (
    ("HCl + H₂O → H₃O⁺ + Cl⁻", "HCl", "H₂O", "H₃O⁺", "Cl⁻"),
    ("HNO₃ + H₂O → H₃O⁺ + NO₃⁻", "HNO₃", "H₂O", "H₃O⁺", "NO₃⁻"),
    ("NH₃ + H₂O ⇌ NH₄⁺ + OH⁻", "H₂O", "NH₃", "NH₄⁺", "OH⁻"),
    ("CH₃COOH + H₂O ⇌ CH₃COO⁻ + H₃O⁺", "CH₃COOH", "H₂O", "H₃O⁺", "CH₃COO⁻"),
    ("HCO₃⁻ + H₂O ⇌ CO₃²⁻ + H₃O⁺", "HCO₃⁻", "H₂O", "H₃O⁺", "CO₃²⁻"),
    ("HCO₃⁻ + H₂O ⇌ H₂CO₃ + OH⁻", "H₂O", "HCO₃⁻", "H₂CO₃", "OH⁻"),
    ("NH₄⁺ + H₂O ⇌ NH₃ + H₃O⁺", "NH₄⁺", "H₂O", "H₃O⁺", "NH₃"),
    ("HF + NH₃ ⇌ F⁻ + NH₄⁺", "HF", "NH₃", "NH₄⁺", "F⁻"),
    ("CH₃COO⁻ + H₂O ⇌ CH₃COOH + OH⁻", "H₂O", "CH₃COO⁻", "CH₃COOH", "OH⁻"),
    ("H₂PO₄⁻ + OH⁻ ⇌ HPO₄²⁻ + H₂O", "H₂PO₄⁻", "OH⁻", "H₂O", "HPO₄²⁻"),
    ("CO₃²⁻ + H₂O ⇌ HCO₃⁻ + OH⁻", "H₂O", "CO₃²⁻", "HCO₃⁻", "OH⁻"),
    ("HSO₄⁻ + H₂O ⇌ SO₄²⁻ + H₃O⁺", "HSO₄⁻", "H₂O", "H₃O⁺", "SO₄²⁻"),
    ("H₂S + NH₃ ⇌ HS⁻ + NH₄⁺", "H₂S", "NH₃", "NH₄⁺", "HS⁻"),
    ("HCN + H₂O ⇌ CN⁻ + H₃O⁺", "HCN", "H₂O", "H₃O⁺", "CN⁻"),
)


# ══ ม.5/15 — คู่กรด-เบส ══════════════════════════════════════════════════════════


