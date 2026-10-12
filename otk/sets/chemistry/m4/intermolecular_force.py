"""แรงยึดเหนี่ยวระหว่างโมเลกุลและสมบัติของสารโคเวเลนต์

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/18

Sets moved here from: science_wave_f23.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import combinations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, show
from otk.sets._support.science_wave_f23 import SUBJECT, UPPER_FOUR, _order_choices

PROVENANCE = Provenance("original")


TOPIC_FORCE = "แรงยึดเหนี่ยวระหว่างโมเลกุลและสมบัติของสารโคเวเลนต์"


FORCES = {"L": "แรงแผ่กระจายลอนดอน", "D": "แรงดึงดูดระหว่างขั้ว", "H": "พันธะไฮโดรเจน"}


FORCE_RANK = {"L": 0, "D": 1, "H": 2}


# (formula, Thai name, molar mass, boiling point °C, strongest force between molecules)
SUBSTANCES = (
    ("H₂", "ไฮโดรเจน", 2, -253, "L"), ("N₂", "ไนโตรเจน", 28, -196, "L"), ("O₂", "ออกซิเจน", 32, -183, "L"),
    ("F₂", "ฟลูออรีน", 38, -188, "L"), ("Cl₂", "คลอรีน", 71, -34, "L"), ("Br₂", "โบรมีน", 160, 59, "L"),
    ("I₂", "ไอโอดีน", 254, 184, "L"), ("CH₄", "มีเทน", 16, -162, "L"), ("C₂H₆", "อีเทน", 30, -89, "L"),
    ("C₃H₈", "โพรเพน", 44, -42, "L"), ("C₄H₁₀", "บิวเทน", 58, -1, "L"), ("C₅H₁₂", "เพนเทน", 72, 36, "L"),
    ("CCl₄", "คาร์บอนเตตระคลอไรด์", 154, 77, "L"), ("HCl", "ไฮโดรเจนคลอไรด์", Fraction(73, 2), -85, "D"),
    ("HBr", "ไฮโดรเจนโบรไมด์", 81, -67, "D"), ("HI", "ไฮโดรเจนไอโอไดด์", 128, -35, "D"),
    ("H₂S", "ไฮโดรเจนซัลไฟด์", 34, -60, "D"), ("CH₃Cl", "คลอโรมีเทน", Fraction(101, 2), -24, "D"),
    ("CH₂O", "เมทานาล", 30, -19, "D"), ("CH₃OCH₃", "ไดเมทิลอีเทอร์", 46, -24, "D"),
    ("CH₃COCH₃", "โพรพาโนน", 58, 56, "D"), ("SO₂", "ซัลเฟอร์ไดออกไซด์", 64, -10, "D"),
    ("NH₃", "แอมโมเนีย", 17, -33, "H"), ("H₂O", "น้ำ", 18, 100, "H"), ("HF", "ไฮโดรเจนฟลูออไรด์", 20, 20, "H"),
    ("CH₃OH", "เมทานอล", 32, 65, "H"), ("C₂H₅OH", "เอทานอล", 46, 78, "H"),
    ("CH₃NH₂", "เมทิลเอมีน", 31, -6, "H"), ("C₃H₇OH", "โพรพานอล", 60, 97, "H"),
)


WATER_SOLUBLE = ("NH₃", "CH₃OH", "C₂H₅OH", "CH₃COCH₃", "HF", "CH₃NH₂", "C₃H₇OH", "HCl")


WATER_INSOLUBLE = ("H₂", "N₂", "O₂", "CH₄", "C₂H₆", "C₃H₈", "C₄H₁₀", "C₅H₁₂", "CCl₄", "I₂")


HEXANE_SOLUBLE = ("I₂", "CCl₄", "C₅H₁₂", "Br₂")


HEXANE_INSOLUBLE = ("NaCl", "CuSO₄", "KNO₃", "H₂O")


def higher_boiling(a, b):
    """The one the textbook rule picks, or None where the rule does not decide.

    Same force: the heavier molecule, if at least 10 heavier. Different force:
    the stronger force, unless it is on a molecule more than 5 lighter. A pick
    is kept only where the measured boiling points agree.
    """
    if a[4] == b[4]:
        if a[4] == "H" or abs(a[2] - b[2]) < 10:
            return None
        pick = a if a[2] > b[2] else b
    else:
        pick = a if FORCE_RANK[a[4]] > FORCE_RANK[b[4]] else b
        other = b if pick is a else a
        if pick[2] < other[2] - 5:
            return None
    other = b if pick is a else a
    return pick if pick[3] > other[3] else None


PAIRS = tuple((a, b) for a, b in combinations(SUBSTANCES, 2) if higher_boiling(a, b) is not None)


TRIPLES = tuple(t for t in combinations(SUBSTANCES, 3)
                if len({x[4] for x in t}) == 1 and all(higher_boiling(a, b) for a, b in combinations(t, 2)))


def _mass(x) -> str:
    return f"{x[0]} (มวลโมเลกุล {show(x[2])})"


@question_type(
    "chem.intermolecular_force_foundation",
    display_name={"th": "ชนิดของแรงยึดเหนี่ยวระหว่างโมเลกุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORCE,
)
class IntermolecularForceFoundation(QuestionType):
    """London forces act everywhere; polar molecules add dipole forces; H on N, O or F adds hydrogen bonds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("ทุกโมเลกุลมีแรงแผ่กระจายลอนดอน โมเลกุลมีขั้วมีแรงดึงดูดระหว่างขั้วเพิ่ม "
                "ถ้ามี H ต่อกับ N O หรือ F โดยตรงจะเกิดพันธะไฮโดรเจน")
        if rng.random() < 0.5:
            x = rng.choice(SUBSTANCES)
            right = FORCES[x[4]]
            return _labelled(stem=f"แรงยึดเหนี่ยวระหว่างโมเลกุลที่แข็งแรงที่สุดใน {x[0]} ({x[1]}) คือแรงใด",
                             correct=right,
                             wrongs=tuple(f for f in FORCES.values() if f != right) + ("พันธะโคเวเลนต์",),
                             topic=TOPIC_FORCE, hint=hint)
        kind = rng.choice(sorted(FORCES))
        pick = rng.choice([x for x in SUBSTANCES if x[4] == kind])
        others = [x for x in SUBSTANCES if x[4] != kind]
        ask = {"L": "มีเพียงแรงแผ่กระจายลอนดอนระหว่างโมเลกุล",
               "D": "มีแรงดึงดูดระหว่างขั้วเป็นแรงหลัก แต่ไม่มีพันธะไฮโดรเจน",
               "H": "เกิดพันธะไฮโดรเจนระหว่างโมเลกุล"}[kind]
        return _labelled(stem=f"สารใด{ask}", correct=f"{pick[0]} ({pick[1]})",
                         wrongs=tuple(f"{x[0]} ({x[1]})" for x in rng.sample(others, 3)), topic=TOPIC_FORCE, hint=hint)


@question_type(
    "chem.intermolecular_force_fluency",
    display_name={"th": "เปรียบเทียบจุดเดือดของสารโคเวเลนต์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORCE,
)
class IntermolecularForceFluency(QuestionType):
    """Stronger force first; the same force, then the heavier molecule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("แรงยึดเหนี่ยวระหว่างโมเลกุลแข็งแรง จุดเดือดสูง: พันธะไฮโดรเจน > แรงดึงดูดระหว่างขั้ว > แรงลอนดอน "
                "ถ้าเป็นแรงชนิดเดียวกัน โมเลกุลที่มีมวลมากกว่ามีจุดเดือดสูงกว่า")
        if rng.random() < 0.6:
            a, b = rng.choice(PAIRS)
            if rng.random() < 0.5:
                a, b = b, a
            right = higher_boiling(a, b)
            other = b if right is a else a
            return _labelled(stem=f"{_mass(a)} กับ {_mass(b)} สารใดมีจุดเดือดสูงกว่า", correct=right[0],
                             wrongs=(other[0], "มีจุดเดือดเท่ากัน", "บอกไม่ได้จากข้อมูลนี้"), topic=TOPIC_FORCE,
                             hint=hint)
        trio = sorted(rng.choice(TRIPLES), key=lambda x: -x[3])
        shown = rng.sample(trio, 3)
        right, wrongs = _order_choices(rng, tuple(x[0] for x in trio))
        return _labelled(stem=f"เรียงจุดเดือดของ {', '.join(_mass(x) for x in shown)} จากสูงไปต่ำ", correct=right,
                         wrongs=wrongs, topic=TOPIC_FORCE, hint=hint)


@question_type(
    "chem.intermolecular_force_application",
    display_name={"th": "อธิบายจุดเดือดและการละลายน้ำด้วยแรงระหว่างโมเลกุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_FORCE,
)
class IntermolecularForceApplication(QuestionType):
    """Explain a measured difference, or pick what dissolves by like-dissolves-like."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            a, b = rng.choice(PAIRS)
            x = higher_boiling(a, b)
            y = b if x is a else a
            if x[4] == y[4]:
                right = f"{x[0]} มีมวลโมเลกุลมากกว่า จึงมี{FORCES[x[4]]}แข็งแรงกว่า"
                wrongs = (f"{x[0]} มีพันธะไฮโดรเจนระหว่างโมเลกุล แต่ {y[0]} ไม่มี",
                          f"พันธะโคเวเลนต์ภายในโมเลกุล {x[0]} แข็งแรงกว่า",
                          f"{y[0]} มีมวลโมเลกุลมากกว่า จึงระเหยง่ายกว่า")
            elif abs(x[2] - y[2]) <= 5:
                right = f"{x[0]} มี{FORCES[x[4]]} ซึ่งแข็งแรงกว่า{FORCES[y[4]]}ที่เป็นแรงหลักของ {y[0]}"
                wrongs = (f"{x[0]} มีมวลโมเลกุลมากกว่ามาก", f"พันธะโคเวเลนต์ภายในโมเลกุล {x[0]} แข็งแรงกว่า",
                          f"{y[0]} ไม่มีแรงยึดเหนี่ยวระหว่างโมเลกุลเลย")
            else:
                return self.build(rng)
            return _labelled(stem=(f"{x[0]} ({x[1]}, มวลโมเลกุล {show(x[2])}) มีจุดเดือด {x[3]} °C สูงกว่า "
                                   f"{y[0]} ({y[1]}, มวลโมเลกุล {show(y[2])}) ที่มีจุดเดือด {y[3]} °C เหตุผลหลักคือข้อใด"),
                             correct=right, wrongs=wrongs, topic=TOPIC_FORCE,
                             hint="การเดือดคือการแยกโมเลกุลออกจากกัน ต้องเอาชนะแรงยึดเหนี่ยวระหว่างโมเลกุล "
                                  "ไม่ใช่สลายพันธะภายในโมเลกุล")
        if rng.random() < 0.6:
            return _labelled(stem="สารใดละลายน้ำได้ดีที่สุด", correct=rng.choice(WATER_SOLUBLE),
                             wrongs=tuple(WATER_INSOLUBLE), topic=TOPIC_FORCE,
                             hint="สารที่มีขั้วหรือเกิดพันธะไฮโดรเจนกับน้ำได้จะละลายน้ำได้ดี (มีขั้วละลายในมีขั้ว)")
        return _labelled(stem="สารใดละลายในเฮกเซน (ตัวทำละลายไม่มีขั้ว) ได้ดีที่สุด", correct=rng.choice(HEXANE_SOLUBLE),
                         wrongs=tuple(HEXANE_INSOLUBLE), topic=TOPIC_FORCE,
                         hint="สารไม่มีขั้วละลายได้ดีในตัวทำละลายไม่มีขั้ว สารไอออนิกและสารมีขั้วมากไม่ละลายในเฮกเซน")
