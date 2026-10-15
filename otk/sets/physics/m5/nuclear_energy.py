"""พลังงานนิวเคลียร์ ฟิชชัน ฟิวชัน และความสัมพันธ์ระหว่างมวลกับพลังงาน

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/1

Sets moved here from: science_wave_e13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math, text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import SUBJECT, UPPER_FIVE, _labelled, show

PROVENANCE = Provenance("original")


TOPIC_NUCLEAR = "พลังงานนิวเคลียร์ ฟิชชัน ฟิวชัน และความสัมพันธ์ระหว่างมวลกับพลังงาน"


FISSION, FUSION, BOTH, NEITHER = ("ฟิชชัน", "ฟิวชัน", "ทั้งฟิชชันและฟิวชัน",
                                  "ไม่ใช่ปฏิกิริยานิวเคลียร์")


NUCLEAR_KINDS = (FISSION, FUSION, BOTH, NEITHER)


NUCLEAR_DESCRIPTIONS = (
    ("นิวเคลียสหนักแตกออกเป็นนิวเคลียสที่เบากว่าสองนิวเคลียส", FISSION),
    ("ยูเรเนียม-235 ถูกนิวตรอนชนแล้วแตกตัว พร้อมปล่อยนิวตรอนออกมาอีก 2-3 ตัว", FISSION),
    ("เกิดปฏิกิริยาลูกโซ่ได้ ถ้ามีนิวตรอนที่ปล่อยออกมาไปชนนิวเคลียสอื่นต่อ", FISSION),
    ("เป็นแหล่งพลังงานของโรงไฟฟ้านิวเคลียร์ที่ใช้งานอยู่ในปัจจุบัน", FISSION),
    ("นิวเคลียสเบาสองนิวเคลียสรวมกันเป็นนิวเคลียสที่หนักขึ้น", FUSION),
    ("ไฮโดรเจนรวมกันเป็นฮีเลียมในแกนของดวงอาทิตย์", FUSION),
    ("ต้องใช้อุณหภูมิสูงหลายล้านองศาเซลเซียสจึงจะเกิดได้", FUSION),
    ("เป็นแหล่งพลังงานของดาวฤกษ์", FUSION),
    ("มวลรวมหลังเกิดปฏิกิริยาน้อยกว่ามวลรวมก่อนเกิดปฏิกิริยา", BOTH),
    ("ปลดปล่อยพลังงานออกมาตามความสัมพันธ์ E = mc²", BOTH),
    ("ให้พลังงานต่อมวลเชื้อเพลิงมากกว่าการเผาไหม้หลายล้านเท่า", BOTH),
    ("การเผาไหม้ถ่านหินในโรงไฟฟ้า", NEITHER),
    ("แบตเตอรี่จ่ายพลังงานไฟฟ้าจากปฏิกิริยาเคมี", NEITHER),
    ("การระเบิดของดินปืนในพลุ", NEITHER),
)


# (statement, what it is about) — true statements are the Fluency answers.
NUCLEAR_TRUE = (
    ("ในฟิชชัน นิวเคลียสหนักแตกตัว และมวลที่หายไปเปลี่ยนเป็นพลังงาน", FISSION),
    ("ฟิชชันของยูเรเนียมในโรงไฟฟ้าต้องควบคุมจำนวนนิวตรอนเพื่อไม่ให้ปฏิกิริยาลูกโซ่รุนแรงเกินไป", FISSION),
    ("ในฟิวชัน นิวเคลียสเบารวมกัน และมวลที่หายไปเปลี่ยนเป็นพลังงาน", FUSION),
    ("ฟิวชันเกิดยากบนโลก เพราะต้องใช้อุณหภูมิและความดันสูงมากให้นิวเคลียสเข้าใกล้กันได้", FUSION),
    ("พลังงานที่ปลดปล่อยเท่ากับมวลที่หายไปคูณด้วยกำลังสองของอัตราเร็วแสง", "มวลกับพลังงาน"),
    ("มวลเพียงเล็กน้อยที่หายไปให้พลังงานมหาศาล เพราะอัตราเร็วแสงยกกำลังสองมีค่ามาก", "มวลกับพลังงาน"),
)


NUCLEAR_FALSE = (
    "ในฟิชชัน มวลของผลิตภัณฑ์มากกว่ามวลของสารตั้งต้น",
    "ฟิวชันคือการที่นิวเคลียสหนักแตกออกเป็นนิวเคลียสเล็ก ๆ",
    "พลังงานนิวเคลียร์มาจากการเผาไหม้ยูเรเนียมกับแก๊สออกซิเจน",
    "มวลกับพลังงานเปลี่ยนรูปกันไม่ได้ พลังงานจึงมาจากอิเล็กตรอนเท่านั้น",
    "ดวงอาทิตย์ได้พลังงานจากฟิชชันของยูเรเนียม",
    "ฟิวชันเกิดได้ง่ายที่อุณหภูมิห้อง",
    "พลังงานที่ปลดปล่อยเท่ากับมวลที่หายไปคูณด้วยอัตราเร็วแสง (ไม่ยกกำลังสอง)",
)


def sci(mantissa: Fraction, exponent: int) -> str:
    """a × 10ⁿ as TeX, with 1 ≤ a < 10."""
    while mantissa >= 10:
        mantissa, exponent = mantissa / 10, exponent + 1
    while mantissa < 1:
        mantissa, exponent = mantissa * 10, exponent - 1
    return rf"{show(mantissa)} \times 10^{{{exponent}}}"


@question_type(
    "phys.nuclear_energy_foundation",
    display_name={"th": "จำแนกฟิชชันและฟิวชัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUCLEAR,
)
class NuclearEnergyFoundation(QuestionType):
    """Sort a description: fission, fusion, both, or not nuclear at all."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        description, kind = rng.choice(NUCLEAR_DESCRIPTIONS)
        if kind in (FISSION, FUSION) and rng.random() < 0.5:
            # Reverse: pick the description of a named reaction. Descriptions
            # true of both are left out so exactly one choice fits.
            others = [d for d, k in NUCLEAR_DESCRIPTIONS if k not in (kind, BOTH)]
            return _labelled(
                stem=f"ข้อใดเป็นลักษณะของ{kind}เท่านั้น",
                correct=description, wrongs=tuple(others),
                topic=TOPIC_NUCLEAR,
                hint="ฟิชชันคือนิวเคลียสหนักแตกตัว ฟิวชันคือนิวเคลียสเบารวมกัน")
        return _labelled(
            stem=f"\"{description}\" เป็นลักษณะของปฏิกิริยาใด",
            correct=kind, wrongs=tuple(k for k in NUCLEAR_KINDS if k != kind),
            topic=TOPIC_NUCLEAR,
            hint="ฟิชชันคือนิวเคลียสหนักแตกตัว ฟิวชันคือนิวเคลียสเบารวมกัน ทั้งสองแบบมีมวลหายไปและเปลี่ยนเป็นพลังงาน")


@question_type(
    "phys.nuclear_energy_fluency",
    display_name={"th": "อธิบายพลังงานจากฟิชชัน ฟิวชัน และความสัมพันธ์ระหว่างมวลกับพลังงาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUCLEAR,
)
class NuclearEnergyFluency(QuestionType):
    """The indicator across its three objects: one true account among three wrong ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        statement, _ = rng.choice(NUCLEAR_TRUE)
        return _labelled(
            stem="ข้อใดอธิบายพลังงานนิวเคลียร์ได้ถูกต้อง",
            correct=statement, wrongs=tuple(NUCLEAR_FALSE),
            topic=TOPIC_NUCLEAR,
            hint="ทั้งฟิชชันและฟิวชันมีมวลหายไปเล็กน้อย มวลนั้นเปลี่ยนเป็นพลังงานตาม E = mc²")


@question_type(
    "phys.nuclear_energy_application",
    display_name={"th": "คำนวณพลังงานจากมวลที่หายไปด้วย E = mc²"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NUCLEAR,
)
class NuclearEnergyApplication(QuestionType):
    """E = mc² with numbers, both ways, with c = 3 × 10⁸ m/s."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a = Fraction(rng.randint(1, 9))
        k = rng.randint(2, 6)
        # m = a × 10⁻ᵏ kg, E = 9a × 10^(16-k) J
        energy = (9 * a, 16 - k)
        mass = (a, -k)
        hint = [text("E = mc² เมื่อ c = 3 × 10⁸ m/s ดังนั้น c² = 9 × 10¹⁶ m²/s²")]
        if rng.random() < 0.5:
            correct = sci(*energy)
            wrongs = [sci(3 * a, 8 - k),            # forgot to square c
                      sci(9 * a, 16 + k),           # sign slip on the exponent
                      sci(9 * a, 15 - k)]           # one power of ten off
            process = rng.choice(("ฟิชชันของยูเรเนียม", "ฟิวชันของไฮโดรเจน"))
            return GeneratedQuestion(
                stem=[text(f"ใน{process}ชุดหนึ่ง มวลหายไป "), math(sci(*mass)),
                      text(" กิโลกรัม พลังงานที่ปลดปล่อยออกมาเท่ากับกี่จูล (c = 3 × 10⁸ m/s)")],
                correct=[math(correct)],
                distractors=fixed(*[[math(w)] for w in wrongs if w != correct]),
                topic=TOPIC_NUCLEAR, hint=hint)
        correct = sci(*mass)
        wrongs = [sci(3 * a, -k + 8), sci(a, k), sci(a, -k - 1)]
        return GeneratedQuestion(
            stem=[text("ปฏิกิริยานิวเคลียร์หนึ่งปลดปล่อยพลังงาน "), math(sci(*energy)),
                  text(" จูล มวลที่หายไปในปฏิกิริยานี้เท่ากับกี่กิโลกรัม (c = 3 × 10⁸ m/s)")],
            correct=[math(correct)],
            distractors=fixed(*[[math(w)] for w in wrongs if w != correct]),
            topic=TOPIC_NUCLEAR, hint=[text("m = E/c² เมื่อ c² = 9 × 10¹⁶ m²/s²")])


# More true accounts, at least one for each of the three objects.
NUCLEAR_TRUE = (*NUCLEAR_TRUE,
    ("ดวงอาทิตย์ได้พลังงานจากฟิวชันของนิวเคลียสไฮโดรเจนเป็นฮีเลียมที่แก่นของดาว", FUSION),
    ("ในฟิชชัน นิวตรอนที่เกิดขึ้นใหม่ไปชนนิวเคลียสอื่นต่อได้ จึงเกิดปฏิกิริยาลูกโซ่", FISSION),
    ("แท่งควบคุมในเครื่องปฏิกรณ์ดูดกลืนนิวตรอนไว้ เพื่อลดอัตราการเกิดฟิชชัน", FISSION),
    ("มวลรวมหลังฟิวชันน้อยกว่ามวลรวมของนิวเคลียสก่อนรวมกันเล็กน้อย", FUSION),
    ("พลังงานจากมวลที่หายไปคำนวณได้จาก E = mc² ไม่ว่าจะเป็นฟิชชันหรือฟิวชัน", "มวลกับพลังงาน"),
)
