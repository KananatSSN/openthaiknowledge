"""ปัจจัยที่มีผลต่อภาวะสมดุลและหลักของเลอชาเตอลิเอ

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/12

Sets moved here from: science_wave_f34.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f34 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SHIFT = "ปัจจัยที่มีผลต่อภาวะสมดุลและหลักของเลอชาเตอลิเอ"


# (equation, gas moles left, gas moles right, forward ΔH sign, a reactant, a product)
SHIFT_SYSTEMS = (
    ("N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", 4, 2, -1, "N₂", "NH₃"),
    ("2SO₂(g) + O₂(g) ⇌ 2SO₃(g)", 3, 2, -1, "O₂", "SO₃"),
    ("N₂O₄(g) ⇌ 2NO₂(g)", 1, 2, 1, "N₂O₄", "NO₂"),
    ("PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)", 1, 2, 1, "PCl₅", "Cl₂"),
    ("H₂(g) + I₂(g) ⇌ 2HI(g)", 2, 2, -1, "H₂", "HI"),
    ("CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g)", 2, 2, -1, "CO", "H₂"),
    ("N₂(g) + O₂(g) ⇌ 2NO(g)", 2, 2, 1, "O₂", "NO"),
    ("2NO(g) + O₂(g) ⇌ 2NO₂(g)", 3, 2, -1, "NO", "NO₂"),
    ("CaCO₃(s) ⇌ CaO(s) + CO₂(g)", 0, 1, 1, "CaCO₃", "CO₂"),
)


# A solid's amount does not enter K, so adding or removing it (while some is left) shifts nothing.
SOLIDS = frozenset({"CaCO₃"})


RIGHT, LEFT, NONE = "เลื่อนไปทางขวา (ไปข้างหน้า)", "เลื่อนไปทางซ้าย (ย้อนกลับ)", "ไม่เลื่อน"


def shift(system, change: str) -> str:
    _, left, right, dh, reactant, _ = system
    if change in ("add_reactant", "remove_reactant") and reactant in SOLIDS:
        return NONE
    if change in ("add_reactant", "remove_product"):
        return RIGHT
    if change in ("add_product", "remove_reactant"):
        return LEFT
    if change in ("pressure_up", "pressure_down"):
        if left == right:
            return NONE
        fewer_right = right < left
        return (RIGHT if fewer_right else LEFT) if change == "pressure_up" else (LEFT if fewer_right else RIGHT)
    if change in ("heat", "cool"):
        endo_right = dh > 0
        return (RIGHT if endo_right else LEFT) if change == "heat" else (LEFT if endo_right else RIGHT)
    return NONE


def change_text(system, change: str) -> str:
    _, _, _, _, reactant, product = system
    return {"add_reactant": f"เติม {reactant}", "remove_product": f"ดึง {product} ออก",
            "add_product": f"เติม {product}", "remove_reactant": f"ดึง {reactant} ออก",
            "pressure_up": "เพิ่มความดันโดยลดปริมาตรภาชนะ", "pressure_down": "ลดความดันโดยเพิ่มปริมาตรภาชนะ",
            "heat": "เพิ่มอุณหภูมิ", "cool": "ลดอุณหภูมิ", "catalyst": "เติมตัวเร่งปฏิกิริยา",
            "inert": "เติมแก๊สอาร์กอนโดยปริมาตรคงที่"}[change]


CHANGES = ("add_reactant", "remove_product", "add_product", "remove_reactant", "pressure_up", "pressure_down", "heat",
           "cool", "catalyst", "inert")


def _dh(system) -> str:
    return "ΔH < 0 (คายความร้อน)" if system[3] < 0 else "ΔH > 0 (ดูดความร้อน)"


@question_type(
    "chem.le_chatelier_foundation",
    display_name={"th": "ทิศทางการเลื่อนของภาวะสมดุลเมื่อถูกรบกวน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SHIFT,
)
class LeChatelierFoundation(QuestionType):
    """The system shifts to undo the disturbance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        system = rng.choice(SHIFT_SYSTEMS)
        change = rng.choice(CHANGES)
        right = shift(system, change)
        return _labelled(stem=f"ระบบ {system[0]} {_dh(system)} อยู่ในภาวะสมดุล ถ้า{change_text(system, change)} "
                              "ภาวะสมดุลจะเลื่อนไปทางใด",
                         correct=right, wrongs=tuple(x for x in (RIGHT, LEFT, NONE, "ปฏิกิริยาหยุดเกิดทั้งสองทิศทาง") if x != right),
                         topic=TOPIC_SHIFT,
                         hint="ระบบเลื่อนไปทางที่ลดผลของการรบกวน: ใช้สารที่เติม ชดเชยสารที่ดึงออก ไปทางโมลแก๊สน้อยเมื่อความดันเพิ่ม "
                              "ไปทางดูดความร้อนเมื่อให้ความร้อน ตัวเร่งไม่ทำให้เลื่อน")


@question_type(
    "chem.le_chatelier_fluency",
    display_name={"th": "ผลของการรบกวนต่อปริมาณสารและค่าคงที่สมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SHIFT,
)
class LeChatelierFluency(QuestionType):
    """Only temperature changes K; the shift decides whether a product's amount rises."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        system = rng.choice(SHIFT_SYSTEMS)
        change = rng.choice(CHANGES)
        hint = "ค่า K เปลี่ยนเมื่อเปลี่ยนอุณหภูมิเท่านั้น: ดูดความร้อน K เพิ่มเมื่อร้อนขึ้น คายความร้อน K ลดเมื่อร้อนขึ้น"
        if rng.random() < 0.5:
            if change in ("heat", "cool"):
                grows = (system[3] > 0) == (change == "heat")
                right = "ค่า K เพิ่มขึ้น" if grows else "ค่า K ลดลง"
            else:
                right = "ค่า K ไม่เปลี่ยน"
            return _labelled(stem=f"ระบบ {system[0]} {_dh(system)} ถ้า{change_text(system, change)} ค่าคงที่สมดุลเปลี่ยนอย่างไร",
                             correct=right, wrongs=tuple(x for x in ("ค่า K เพิ่มขึ้น", "ค่า K ลดลง", "ค่า K ไม่เปลี่ยน",
                                                                     "ค่า K กลายเป็นศูนย์") if x != right),
                             topic=TOPIC_SHIFT, hint=hint)
        change = rng.choice([c for c in CHANGES if c not in ("add_product", "remove_product")])
        moved = shift(system, change)
        product = system[5]
        right = {RIGHT: f"ปริมาณ {product} เพิ่มขึ้น", LEFT: f"ปริมาณ {product} ลดลง", NONE: f"ปริมาณ {product} ไม่เปลี่ยน"}[moved]
        return _labelled(stem=f"ระบบ {system[0]} {_dh(system)} ถ้า{change_text(system, change)} เมื่อเข้าสู่สมดุลใหม่ "
                              f"ปริมาณ {product} เปลี่ยนอย่างไร",
                         correct=right, wrongs=tuple(x for x in (f"ปริมาณ {product} เพิ่มขึ้น", f"ปริมาณ {product} ลดลง",
                                                                 f"ปริมาณ {product} ไม่เปลี่ยน", f"{product} หมดไป") if x != right),
                         topic=TOPIC_SHIFT, hint="หาทิศทางการเลื่อนก่อน เลื่อนไปทางขวาผลิตภัณฑ์เพิ่ม ทางซ้ายผลิตภัณฑ์ลด")


@question_type(
    "chem.le_chatelier_application",
    display_name={"th": "เลือกภาวะที่ให้ผลิตภัณฑ์มากที่สุด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SHIFT,
)
class LeChatelierApplication(QuestionType):
    """Pressure toward fewer gas moles and temperature toward the product side."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            system = rng.choice(SHIFT_SYSTEMS)
            good = [c for c in CHANGES if shift(system, c) == RIGHT]
            bad = [c for c in CHANGES if shift(system, c) != RIGHT]
            pick = rng.choice(good)
            return _labelled(stem=f"ระบบ {system[0]} {_dh(system)} อยู่ในภาวะสมดุล ต้องการให้ได้ {system[5]} มากขึ้น ควรทำอย่างไร",
                             correct=change_text(system, pick),
                             wrongs=tuple(change_text(system, c) for c in rng.sample(bad, 3)), topic=TOPIC_SHIFT,
                             hint="เลือกการรบกวนที่ทำให้สมดุลเลื่อนไปทางขวา (ทางผลิตภัณฑ์)")
        system = rng.choice([s for s in SHIFT_SYSTEMS if s[1] != s[2]])
        _, left, right, dh, _, product = system
        pressure = "ความดันสูง" if right < left else "ความดันต่ำ"
        temp = "อุณหภูมิสูง" if dh > 0 else "อุณหภูมิต่ำ"
        right_answer = f"{pressure} และ{temp}"
        options = [f"{p} และ{t}" for p in ("ความดันสูง", "ความดันต่ำ") for t in ("อุณหภูมิสูง", "อุณหภูมิต่ำ")]
        return _labelled(stem=f"ระบบ {system[0]} {_dh(system)} ต้องการให้ได้ {product} ที่ภาวะสมดุลมากที่สุด ควรใช้ภาวะใด",
                         correct=right_answer, wrongs=tuple(o for o in options if o != right_answer), topic=TOPIC_SHIFT,
                         hint="ความดันสูงเลื่อนไปทางโมลแก๊สน้อย ความดันต่ำไปทางโมลแก๊สมาก อุณหภูมิสูงเลื่อนไปทางดูดความร้อน")
