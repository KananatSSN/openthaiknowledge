"""สูตรอย่างง่ายและสูตรโมเลกุล

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/8

Sets moved here from: science_wave_f42.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import ATOMIC
from otk.sets._support.science_wave_f42 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_FORMULA = "สูตรอย่างง่ายและสูตรโมเลกุล"


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


# Carbon compounds write C then H; others put the less electronegative element first (P₂O₅, N₂O₄, B₂H₆).
INORGANIC_ORDER = ("B", "Na", "Mg", "Al", "Si", "P", "N", "S", "H", "Cl", "O")


def formula_of(counts: dict) -> str:
    if "C" in counts:
        order = ["C", "H"] + sorted(k for k in counts if k not in ("C", "H"))
    else:
        order = [k for k in INORGANIC_ORDER if k in counts]
    return "".join(k + (str(counts[k]).translate(SUB) if counts[k] > 1 else "") for k in order if counts.get(k))


# (empirical formula, molecular formulas that share it)
EMPIRICAL = (
    ({"C": 1, "H": 2, "O": 1}, ({"C": 6, "H": 12, "O": 6}, {"C": 2, "H": 4, "O": 2}, {"C": 3, "H": 6, "O": 3})),
    ({"C": 1, "H": 1}, ({"C": 6, "H": 6}, {"C": 2, "H": 2})),
    ({"C": 1, "H": 2}, ({"C": 2, "H": 4}, {"C": 3, "H": 6}, {"C": 4, "H": 8})),
    ({"C": 1, "H": 3}, ({"C": 2, "H": 6},)),
    ({"N": 1, "O": 2}, ({"N": 2, "O": 4},)),
    ({"P": 2, "O": 5}, ({"P": 4, "O": 10},)),
    ({"H": 1, "O": 1}, ({"H": 2, "O": 2},)),
    ({"C": 2, "H": 4, "O": 1}, ({"C": 4, "H": 8, "O": 2},)),
    ({"C": 2, "H": 5}, ({"C": 4, "H": 10},)),
    ({"C": 1, "H": 2, "Cl": 1}, ({"C": 2, "H": 4, "Cl": 2},)),
    ({"C": 3, "H": 4}, ({"C": 9, "H": 12},)),
    ({"B": 1, "H": 3}, ({"B": 2, "H": 6},)),
)


EXTRA_MASS = {"P": 31, "B": Fraction(108, 10)}


def mass_counts(counts: dict) -> Fraction:
    return sum((ATOMIC.get(e, EXTRA_MASS.get(e)) * n for e, n in counts.items()), Fraction(0))


def reduce(counts: dict) -> dict:
    g = 0
    for n in counts.values():
        g = gcd(g, n)
    return {e: n // g for e, n in counts.items()}


@question_type(
    "chem.empirical_formula_foundation",
    display_name={"th": "สูตรอย่างง่ายจากสูตรโมเลกุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class EmpiricalFormulaFoundation(QuestionType):
    """Divide every subscript by their greatest common factor."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        empirical, molecules = rng.choice(EMPIRICAL)
        molecule = rng.choice(molecules)
        if rng.random() < 0.5 and "C" in empirical and set(empirical) <= {"C", "H", "O"}:
            # Scaling practice on carbon compounds: CₙH₂ₙ and friends at other chain lengths.
            # A real molecule of C, H and O has an even number of H atoms, and at most 2C + 2 of them.
            multiple = rng.choice([k for k in range(2, 7) if empirical.get("H", 0) * k % 2 == 0
                                   and empirical.get("H", 0) * k <= 2 * empirical["C"] * k + 2])
            molecule = {e: n * multiple for e, n in empirical.items()}
        right = formula_of(empirical)
        # dict.fromkeys de-duplicates in a fixed order; a set's order changes per process.
        wrongs = [w for w in dict.fromkeys([
            formula_of(molecule), formula_of({e: n * 2 for e, n in empirical.items()}),
            formula_of({e: (n + 1 if i == 0 else n) for i, (e, n) in enumerate(empirical.items())})]) if w != right]
        while len(wrongs) < 3:
            wrongs.append(formula_of({e: n * 3 for e, n in empirical.items()}))
        return _labelled(stem=f"สารที่มีสูตรโมเลกุล {formula_of(molecule)} มีสูตรอย่างง่ายตามข้อใด", correct=right,
                         wrongs=tuple(dict.fromkeys(wrongs))[:3], topic=TOPIC_FORMULA,
                         hint="สูตรอย่างง่ายคืออัตราส่วนอย่างต่ำของจำนวนอะตอม หารตัวห้อยทุกตัวด้วย ห.ร.ม.")


@question_type(
    "chem.empirical_formula_fluency",
    display_name={"th": "หาสูตรอย่างง่ายจากมวลของธาตุ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class EmpiricalFormulaFluency(QuestionType):
    """Grams → moles of each element → the smallest whole-number ratio."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            empirical, _ = rng.choice(EMPIRICAL)
            k = Fraction(rng.randrange(1, 21), rng.choice((2, 4, 10)))
            grams = {e: ATOMIC.get(e, EXTRA_MASS.get(e)) * n * k for e, n in empirical.items()}
            return (empirical, grams) if all(exact(g) for g in grams.values()) else None

        empirical, grams = _find(rng, draw)
        right = formula_of(empirical)
        listed = ", ".join(f"{e} {show(g)} กรัม" for e, g in grams.items())
        given = ", ".join(f"{e} = {show(ATOMIC.get(e, EXTRA_MASS.get(e)))}" for e in grams)
        mass_ratio_formula = {}
        for e, g in grams.items():
            mass_ratio_formula[e] = max(1, round(float(g)))
        swapped = dict(zip(empirical, reversed(list(empirical.values()))))
        candidates = [formula_of(reduce(mass_ratio_formula)), formula_of(swapped),
                      formula_of({e: n * 2 for e, n in empirical.items()}), formula_of({e: n + 1 for e, n in empirical.items()}),
                      formula_of({e: (n + 1 if i == 0 else n) for i, (e, n) in enumerate(empirical.items())}),
                      formula_of({e: (n + 1 if i == 1 else n) for i, (e, n) in enumerate(empirical.items())})]
        wrongs = [c for c in dict.fromkeys(candidates) if c != right]
        return _labelled(stem=f"สารประกอบหนึ่งประกอบด้วย {listed} (มวลอะตอม {given}) มีสูตรอย่างง่ายตามข้อใด", correct=right,
                         wrongs=tuple(dict.fromkeys(wrongs))[:3], topic=TOPIC_FORMULA,
                         hint="เปลี่ยนมวลของแต่ละธาตุเป็นโมล หารด้วยค่าน้อยที่สุด แล้วปรับให้เป็นเลขจำนวนเต็ม")


@question_type(
    "chem.empirical_formula_application",
    display_name={"th": "หาสูตรโมเลกุลจากสูตรอย่างง่ายและมวลโมเลกุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORMULA,
)
class EmpiricalFormulaApplication(QuestionType):
    """n = molar mass ÷ empirical formula mass; multiply every subscript by n."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        empirical, molecules = rng.choice(EMPIRICAL)
        molecule = rng.choice(molecules)
        n = next(iter(molecule.values())) // next(iter(empirical.values()))
        m = mass_counts(molecule)
        given = ", ".join(f"{e} = {show(ATOMIC.get(e, EXTRA_MASS.get(e)))}" for e in empirical)
        if rng.random() < 0.5:
            right = formula_of(molecule)
            wrongs = {formula_of(empirical), formula_of({e: c * (n + 1) for e, c in empirical.items()})}
            if n > 2:
                wrongs.add(formula_of({e: c * (n - 1) for e, c in empirical.items()}))
            wrongs.add(formula_of({e: c * n + (1 if i == 0 else 0) for i, (e, c) in enumerate(empirical.items())}))
            wrongs.discard(right)
            return _labelled(stem=f"สารมีสูตรอย่างง่าย {formula_of(empirical)} และมวลโมเลกุล {show(m)} มีสูตรโมเลกุลตามข้อใด "
                                  f"(มวลอะตอม {given})",
                             correct=right, wrongs=tuple(sorted(wrongs))[:3], topic=TOPIC_FORMULA,
                             hint="หา n = มวลโมเลกุล ÷ มวลของสูตรอย่างง่าย แล้วคูณตัวห้อยทุกตัวด้วย n")
        return numeric(stem=f"สารมีสูตรอย่างง่าย {formula_of(empirical)} และมวลโมเลกุล {show(m)} สูตรโมเลกุลเป็นกี่เท่าของสูตรอย่างง่าย "
                            f"(มวลอะตอม {given})",
                       answer=n, wrongs=[n + 1, n * 2, n - 1 if n > 1 else 3], unit="เท่า", topic=TOPIC_FORMULA,
                       hint="n = มวลโมเลกุล ÷ มวลของสูตรอย่างง่าย")
