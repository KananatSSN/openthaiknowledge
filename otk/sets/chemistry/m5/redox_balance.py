"""การดุลสมการรีดอกซ์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/27

Sets moved here from: science_wave_f39.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f39 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_BALANCE = "การดุลสมการรีดอกซ์"


# Balanced in acid: (reactants, products), each a tuple of (coefficient, species).
REDOX_EQUATIONS = (
    (((1, "MnO₄⁻"), (5, "Fe²⁺"), (8, "H⁺")), ((1, "Mn²⁺"), (5, "Fe³⁺"), (4, "H₂O"))),
    (((1, "Cr₂O₇²⁻"), (6, "Fe²⁺"), (14, "H⁺")), ((2, "Cr³⁺"), (6, "Fe³⁺"), (7, "H₂O"))),
    (((2, "MnO₄⁻"), (5, "C₂O₄²⁻"), (16, "H⁺")), ((2, "Mn²⁺"), (10, "CO₂"), (8, "H₂O"))),
    (((2, "MnO₄⁻"), (5, "H₂O₂"), (6, "H⁺")), ((2, "Mn²⁺"), (5, "O₂"), (8, "H₂O"))),
    (((1, "Cr₂O₇²⁻"), (6, "I⁻"), (14, "H⁺")), ((2, "Cr³⁺"), (3, "I₂"), (7, "H₂O"))),
    (((2, "MnO₄⁻"), (10, "I⁻"), (16, "H⁺")), ((2, "Mn²⁺"), (5, "I₂"), (8, "H₂O"))),
    (((3, "Cu"), (8, "H⁺"), (2, "NO₃⁻")), ((3, "Cu²⁺"), (2, "NO"), (4, "H₂O"))),
    (((1, "Cu"), (4, "H⁺"), (2, "NO₃⁻")), ((1, "Cu²⁺"), (2, "NO₂"), (2, "H₂O"))),
    (((2, "MnO₄⁻"), (5, "SO₂"), (2, "H₂O")), ((2, "Mn²⁺"), (5, "SO₄²⁻"), (4, "H⁺"))),
    (((1, "Cr₂O₇²⁻"), (3, "SO₃²⁻"), (8, "H⁺")), ((2, "Cr³⁺"), (3, "SO₄²⁻"), (4, "H₂O"))),
    (((2, "Fe³⁺"), (1, "Sn²⁺")), ((2, "Fe²⁺"), (1, "Sn⁴⁺"))),
    (((1, "MnO₂"), (4, "H⁺"), (2, "Cl⁻")), ((1, "Mn²⁺"), (1, "Cl₂"), (2, "H₂O"))),
    (((1, "IO₃⁻"), (5, "I⁻"), (6, "H⁺")), ((3, "I₂"), (3, "H₂O"))),
    (((2, "I⁻"), (1, "H₂O₂"), (2, "H⁺")), ((1, "I₂"), (2, "H₂O"))),
)


# (half-equation, electrons, H⁺ on its side (+ left / − right), H₂O)
HALVES = (
    ("MnO₄⁻ + 8H⁺ + 5e⁻ → Mn²⁺ + 4H₂O", 5, 8, 4),
    ("Cr₂O₇²⁻ + 14H⁺ + 6e⁻ → 2Cr³⁺ + 7H₂O", 6, 14, 7),
    ("NO₃⁻ + 4H⁺ + 3e⁻ → NO + 2H₂O", 3, 4, 2),
    ("NO₃⁻ + 2H⁺ + e⁻ → NO₂ + H₂O", 1, 2, 1),
    ("H₂O₂ + 2H⁺ + 2e⁻ → 2H₂O", 2, 2, 2),
    ("MnO₂ + 4H⁺ + 2e⁻ → Mn²⁺ + 2H₂O", 2, 4, 2),
    ("SO₄²⁻ + 4H⁺ + 2e⁻ → SO₂ + 2H₂O", 2, 4, 2),
    ("2IO₃⁻ + 12H⁺ + 10e⁻ → I₂ + 6H₂O", 10, 12, 6),
    ("SO₂ + 2H₂O → SO₄²⁻ + 4H⁺ + 2e⁻", 2, 4, 2),
    ("H₂O₂ → O₂ + 2H⁺ + 2e⁻", 2, 2, 0),
    ("C₂O₄²⁻ → 2CO₂ + 2e⁻", 2, 0, 0),
    ("2Cr³⁺ + 7H₂O → Cr₂O₇²⁻ + 14H⁺ + 6e⁻", 6, 14, 7),
)


def side_text(side, blanks: bool = False) -> str:
    return " + ".join(("__" if blanks else ("" if c == 1 else str(c))) + s for c, s in side)


def equation_text(eq, blanks: bool = False) -> str:
    return f"{side_text(eq[0], blanks)} → {side_text(eq[1], blanks)}"


def electrons_moved(eq) -> int:
    """Electrons passed in the equation as written, from the oxidation numbers of the tabled couples."""
    reactants = dict((s, c) for c, s in eq[0])
    products = dict((s, c) for c, s in eq[1])
    if "MnO₄⁻" in reactants:
        return 5 * reactants["MnO₄⁻"]
    if "Cr₂O₇²⁻" in reactants:
        return 6 * reactants["Cr₂O₇²⁻"]
    if "NO₃⁻" in reactants:
        per = 3 if "NO" in products else 1
        return per * reactants["NO₃⁻"]
    if "MnO₂" in reactants:
        return 2
    if "IO₃⁻" in reactants:
        return 5 * reactants["IO₃⁻"]
    if "Fe³⁺" in reactants:
        return reactants["Fe³⁺"]
    return 2 * reactants["H₂O₂"]


@question_type(
    "chem.redox_balance_foundation",
    display_name={"th": "ดุลครึ่งปฏิกิริยาในสารละลายกรด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BALANCE,
)
class RedoxBalanceFoundation(QuestionType):
    """Balance O with H₂O, H with H⁺, then charge with electrons."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        half, electrons, protons, water = rng.choice(HALVES)
        options = [("อิเล็กตรอน", "e⁻", electrons)]
        if protons:
            options.append(("H⁺", "H⁺", protons))
        if water:
            options.append(("H₂O", "H₂O", water))
        label, token, value = rng.choice(options)
        blanked = half.replace(f"{value if value > 1 else ''}{token}", f"□{token}", 1)
        return numeric(stem=f"ครึ่งปฏิกิริยาที่ดุลแล้วในสารละลายกรด: {blanked} "
                            f"ค่า □ หน้า {token} เท่าใด",
                       answer=value, wrongs=[value + 1, value * 2, value - 1 if value > 1 else value + 2], unit="",
                       topic=TOPIC_BALANCE,
                       hint="ดุลอะตอมหลักก่อน ดุล O ด้วย H₂O ดุล H ด้วย H⁺ แล้วดุลประจุด้วยอิเล็กตรอน")


@question_type(
    "chem.redox_balance_fluency",
    display_name={"th": "ดุลสมการรีดอกซ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BALANCE,
)
class RedoxBalanceFluency(QuestionType):
    """Electrons lost equal electrons gained; then atoms and charge balance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(REDOX_EQUATIONS)
        coef, species = rng.choice([*eq[0], *eq[1]])
        return numeric(stem=f"ดุลสมการรีดอกซ์ในสารละลายกรด {equation_text(eq, blanks=True)} ด้วยเลขจำนวนเต็มน้อยที่สุด "
                            f"สัมประสิทธิ์ของ {species} เท่าใด",
                       answer=coef, wrongs=[coef + 1, coef * 2, coef + 2 if coef > 1 else 3], unit="", topic=TOPIC_BALANCE,
                       hint="เขียนครึ่งปฏิกิริยาทั้งสอง ดุลแต่ละครึ่ง แล้วคูณให้อิเล็กตรอนเท่ากันก่อนรวม")


@question_type(
    "chem.redox_balance_application",
    display_name={"th": "จำนวนอิเล็กตรอนและผลรวมสัมประสิทธิ์ในสมการรีดอกซ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BALANCE,
)
class RedoxBalanceApplication(QuestionType):
    """Electrons moved, or the balanced equation among near misses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq = rng.choice(REDOX_EQUATIONS)
        kind = rng.randrange(3)
        if kind == 0:
            moved = electrons_moved(eq)
            return numeric(stem=f"สมการ {equation_text(eq)} ตามที่เขียน มีการถ่ายโอนอิเล็กตรอนทั้งหมดกี่ตัว (ต่อหนึ่งหน่วยสมการ)",
                           answer=moved, wrongs=[moved + 1, moved * 2, moved // 2 if moved > 2 else moved + 2], unit="",
                           topic=TOPIC_BALANCE, hint="คูณจำนวนอิเล็กตรอนในครึ่งปฏิกิริยารีดักชันด้วยจำนวนเท่าที่ใช้ในสมการ")
        if kind == 1:
            total = sum(c for c, _ in eq[0]) + sum(c for c, _ in eq[1])
            return numeric(stem=f"ดุลสมการ {equation_text(eq, blanks=True)} ด้วยเลขจำนวนเต็มน้อยที่สุด ผลรวมสัมประสิทธิ์ทั้งหมดเท่าใด",
                           answer=total, wrongs=[total + 1, total - 1, total + 2], unit="", topic=TOPIC_BALANCE,
                           hint="ดุลให้ครบทั้งอะตอมและประจุก่อน แล้วรวมสัมประสิทธิ์ทุกตัว")
        wrongs = []
        for _ in range(60):
            if len(wrongs) == 3:
                break
            side_index = rng.randrange(2)
            side = list(eq[side_index])
            i = rng.randrange(len(side))
            c, s = side[i]
            side[i] = (c + rng.choice((1, 1, 2)) if c == 1 else c + rng.choice((-1, 1, 2)), s)
            bad = (tuple(side), eq[1]) if side_index == 0 else (eq[0], tuple(side))
            text = equation_text(bad)
            if text not in wrongs:
                wrongs.append(text)
        return _labelled(stem="สมการรีดอกซ์ในสารละลายกรดข้อใดดุลแล้วทั้งจำนวนอะตอมและประจุ", correct=equation_text(eq),
                         wrongs=tuple(wrongs[:3]), topic=TOPIC_BALANCE,
                         hint="ตรวจจำนวนอะตอมของทุกธาตุ และผลรวมประจุทั้งสองข้างต้องเท่ากัน")
