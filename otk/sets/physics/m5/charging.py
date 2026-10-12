"""การทำให้วัตถุมีประจุไฟฟ้า

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/1

Sets moved here from: science_wave_f10.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f10 import SUBJECT, UPPER_FIVE, _charge

PROVENANCE = Provenance("original")


TOPIC_CHARGE = "การทำให้วัตถุมีประจุไฟฟ้า"


SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _sci(mantissa, exponent: int) -> str:
    return f"{show(mantissa)} × 10{str(exponent).translate(SUPERSCRIPT)}"


CHARGE_FACTS = (
    ("ถูแท่งพลาสติกกับผ้าขนสัตว์ แล้วแท่งพลาสติกมีประจุลบ เพราะเหตุใด", "อิเล็กตรอนถ่ายโอนจากผ้าขนสัตว์ไปยังแท่งพลาสติก",
     ("โปรตอนถ่ายโอนจากแท่งพลาสติกไปยังผ้าขนสัตว์", "การถูสร้างประจุลบขึ้นใหม่", "อิเล็กตรอนถ่ายโอนจากแท่งพลาสติกไปยังผ้าขนสัตว์")),
    ("หลังถูวัตถุสองชิ้นเข้าด้วยกัน ประจุบนวัตถุทั้งสองเป็นอย่างไร", "ขนาดเท่ากันแต่ชนิดตรงข้ามกัน",
     ("ขนาดเท่ากันและชนิดเดียวกัน", "มีประจุเฉพาะวัตถุที่แข็งกว่า", "ประจุรวมของทั้งสองเพิ่มขึ้น")),
    ("นำแท่งประจุลบเข้าใกล้ลูกพิทที่เป็นกลาง (ไม่แตะ) ด้านที่อยู่ใกล้แท่งมีประจุชนิดใด", "ประจุบวก",
     ("ประจุลบ", "ไม่มีประจุ", "ทั้งประจุบวกและลบเท่ากัน")),
    ("การทำให้ตัวนำมีประจุโดยการเหนี่ยวนำ ต้องทำตามลำดับใด",
     "นำวัตถุมีประจุเข้าใกล้ ต่อสายดิน ตัดสายดิน แล้วจึงนำวัตถุมีประจุออก",
     ("ต่อสายดินก่อน แล้วแตะวัตถุมีประจุ", "นำวัตถุมีประจุออกก่อน แล้วจึงตัดสายดิน", "ถูตัวนำกับวัตถุมีประจุ")),
    ("ตัวนำที่ได้ประจุโดยการเหนี่ยวนำมีประจุชนิดใดเทียบกับวัตถุที่นำมาเหนี่ยวนำ", "ชนิดตรงข้ามกัน",
     ("ชนิดเดียวกัน", "ไม่มีประจุ", "ขึ้นกับขนาดของตัวนำ")),
    ("อิเล็กโทรสโคปแผ่นโลหะบางใช้ทำอะไร", "ตรวจว่าวัตถุมีประจุหรือไม่ โดยแผ่นโลหะกางออกเมื่อมีประจุ",
     ("วัดกระแสไฟฟ้าในวงจร", "สร้างประจุไฟฟ้าให้วัตถุ", "วัดความต่างศักย์ของแบตเตอรี่")),
)


# (rod as described, the charge it carries)
RODS = (("แท่งแก้วที่ถูกับผ้าไหม", "บวก"), ("แท่งพลาสติกที่ถูกับผ้าขนสัตว์", "ลบ"), ("ลูกโป่งที่ถูกับผม", "ลบ"),
        ("แท่งอีโบไนต์ที่ถูกับขนแมว", "ลบ"), ("แท่งประจุบวก", "บวก"), ("แท่งประจุลบ", "ลบ"))


CONDUCTORS = ("ทรงกลมโลหะ", "กระป๋องโลหะบนขาตั้งพลาสติก", "ลูกพิทเคลือบโลหะ", "แผ่นโลหะบนขาตั้งฉนวน")


@question_type(
    "phys.charging_foundation",
    display_name={"th": "การทำให้วัตถุมีประจุโดยการขัดสีและการเหนี่ยวนำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CHARGE,
)
class ChargingFoundation(QuestionType):
    """Electrons move, protons stay: rubbing and induction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(CHARGE_FACTS)
        if rng.random() < 0.5:
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_CHARGE,
                             hint="ประจุที่เคลื่อนที่ได้คืออิเล็กตรอน วัตถุที่ได้อิเล็กตรอนมีประจุลบ วัตถุที่เสียอิเล็กตรอนมีประจุบวก")
        rod = rng.choice(("แท่งแก้ว", "แท่งพลาสติก", "ลูกโป่ง", "หวีพลาสติก"))
        n = rng.randint(1, 9)
        exponent = rng.randint(8, 12)
        gained = rng.random() < 0.5
        right = "ประจุลบ" if gained else "ประจุบวก"
        return _labelled(
            stem=(f"ถู{rod}กับผ้า แล้ว{rod}{'ได้รับ' if gained else 'เสีย'}อิเล็กตรอนไป "
                  f"{_sci(n, exponent)} ตัว {rod}มีประจุชนิดใด และขนาดเท่าใด (e = 1.6 × 10⁻¹⁹ C)"),
            correct=f"{right} {_sci(Fraction(16 * n, 10), exponent - 19)} C",
            wrongs=(f"{'ประจุบวก' if gained else 'ประจุลบ'} {_sci(Fraction(16 * n, 10), exponent - 19)} C",
                    f"{right} {_sci(n, exponent)} C", f"{right} {_sci(Fraction(16 * n, 10), exponent + 19)} C"),
            topic=TOPIC_CHARGE, hint="ประจุ = จำนวนอิเล็กตรอน × 1.6 × 10⁻¹⁹ C ได้อิเล็กตรอนเป็นลบ เสียอิเล็กตรอนเป็นบวก")


@question_type(
    "phys.charging_fluency",
    display_name={"th": "ประจุบนทรงกลมตัวนำเมื่อแตะกันและจำนวนอิเล็กตรอนที่ถ่ายโอน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CHARGE,
)
class ChargingFluency(QuestionType):
    """Identical spheres share their total charge; charge counts electrons."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            q1, q2 = rng.sample([x for x in range(-12, 13) if x], 2)
            if (q1 + q2) % 2:
                q2 += 1 if q2 != -1 else 2
            share = Fraction(q1 + q2, 2)
            return numeric(
                stem=(f"ทรงกลมโลหะขนาดเท่ากันสองลูกมีประจุ {_charge(q1)} และ {_charge(q2)} นำมาแตะกันแล้วแยกออก "
                      "แต่ละลูกมีประจุกี่ไมโครคูลอมบ์ (ตอบค่าลบถ้าเป็นประจุลบ)"),
                answer=share, wrongs=[q1 + q2, Fraction(abs(q1) + abs(q2), 2), -share if share else 1],
                unit="μC", topic=TOPIC_CHARGE, allow_negative=True,
                hint="ทรงกลมตัวนำขนาดเท่ากันแบ่งประจุรวมเท่ากัน: (q₁ + q₂) ÷ 2 โดยคิดเครื่องหมายด้วย")
        exponent = rng.randint(-12, -8)
        # The charge is a whole multiple of 1.6, so the electron count is a whole number times a power of ten.
        q_mantissa = Fraction(16 * rng.randint(1, 9), 10)
        count = q_mantissa / Fraction(16, 10)
        return _labelled(
            stem=f"วัตถุมีประจุ {_sci(q_mantissa, exponent)} C ต้องเสียอิเล็กตรอนไปกี่ตัว (e = 1.6 × 10⁻¹⁹ C)",
            correct=f"{_sci(count, exponent + 19)} ตัว",
            wrongs=(f"{_sci(count, exponent - 19)} ตัว", f"{_sci(q_mantissa * Fraction(16, 10), exponent + 19)} ตัว",
                    f"{_sci(count, exponent + 18)} ตัว"),
            topic=TOPIC_CHARGE, hint="จำนวนอิเล็กตรอน = ประจุ ÷ 1.6 × 10⁻¹⁹ C")


@question_type(
    "phys.charging_application",
    display_name={"th": "อธิบายการเกิดประจุจากการเหนี่ยวนำด้วยอิเล็กโทรสโคปและทรงกลมตัวนำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CHARGE,
)
class ChargingApplication(QuestionType):
    """Follow the electrons through each step of an induction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, rod = rng.choice(RODS)
        opposite = "ลบ" if rod == "บวก" else "บวก"
        body = rng.choice(CONDUCTORS)
        shape = rng.randrange(5)
        if shape == 4:
            return _labelled(
                stem=(f"ทรงกลมโลหะ A และ B วางแตะกันบนขาตั้งฉนวน นำ{name}เข้าใกล้ A แล้วแยก A กับ B ออกจากกัน "
                      "ก่อนนำวัตถุที่มีประจุออก ทรงกลมทั้งสองมีประจุอย่างไร"),
                correct=f"A มีประจุ{opposite} และ B มีประจุ{rod} ขนาดเท่ากัน",
                wrongs=(f"A มีประจุ{rod} และ B มีประจุ{opposite} ขนาดเท่ากัน", "ทั้งสองเป็นกลาง",
                        f"ทั้งสองมีประจุ{opposite}"),
                topic=TOPIC_CHARGE,
                hint="อิเล็กตรอนเคลื่อนไปอีกด้านของตัวนำคู่ แยกออกขณะแท่งยังอยู่ ประจุจึงค้างอยู่ด้านละชนิด")
        if shape == 0:
            return _labelled(
                stem=(f"นำ{name}เข้าใกล้จานโลหะของอิเล็กโทรสโคปที่เป็นกลาง (ไม่แตะ) "
                      "แผ่นโลหะบางด้านล่างมีประจุชนิดใดและเป็นอย่างไร"),
                correct=f"ประจุ{rod} แผ่นโลหะกางออก",
                wrongs=(f"ประจุ{opposite} แผ่นโลหะกางออก", "ไม่มีประจุ แผ่นโลหะหุบ", f"ประจุ{rod} แผ่นโลหะหุบ"),
                topic=TOPIC_CHARGE, hint="ประจุชนิดตรงข้ามถูกดึงขึ้นไปที่จาน ประจุชนิดเดียวกับแท่งถูกผลักลงไปที่แผ่นโลหะ")
        if shape == 1:
            return _labelled(
                stem=(f"นำ{name}เข้าใกล้{body}ที่เป็นกลาง แตะ{body}ด้วยนิ้ว (ต่อลงดิน) เอานิ้วออก "
                      f"แล้วจึงนำวัตถุที่มีประจุออก {body}มีประจุชนิดใด"),
                correct=f"ประจุ{opposite}", wrongs=(f"ประจุ{rod}", "เป็นกลาง", "มีทั้งสองชนิดเท่ากัน"),
                topic=TOPIC_CHARGE, hint="การเหนี่ยวนำให้ประจุชนิดตรงข้ามกับวัตถุที่นำมาเหนี่ยวนำ")
        if shape == 2:
            return _labelled(
                stem=(f"นำ{name}เข้าใกล้{body}ที่เป็นกลาง แตะ{body}ด้วยนิ้ว (ต่อลงดิน) "
                      "อิเล็กตรอนเคลื่อนที่อย่างไร"),
                correct=(f"อิเล็กตรอนจากพื้นดินเคลื่อนเข้าสู่{body}" if rod == "บวก"
                         else f"อิเล็กตรอนจาก{body}เคลื่อนลงสู่พื้นดิน"),
                wrongs=((f"อิเล็กตรอนจาก{body}เคลื่อนลงสู่พื้นดิน" if rod == "บวก"
                         else f"อิเล็กตรอนจากพื้นดินเคลื่อนเข้าสู่{body}"),
                        f"โปรตอนจาก{body}เคลื่อนลงสู่พื้นดิน", "ไม่มีประจุเคลื่อนที่"),
                topic=TOPIC_CHARGE, hint="มีเฉพาะอิเล็กตรอนที่เคลื่อนที่ได้ ประจุบวกดึงอิเล็กตรอนเข้า ประจุลบผลักอิเล็กตรอนออก")
        return _labelled(
            stem=(f"แตะ{name}กับจานโลหะของอิเล็กโทรสโคปที่เป็นกลาง แล้วนำออก อิเล็กโทรสโคปมีประจุชนิดใด"),
            correct=f"ประจุ{rod} แผ่นโลหะยังกางอยู่",
            wrongs=(f"ประจุ{opposite} แผ่นโลหะยังกางอยู่", "เป็นกลาง แผ่นโลหะหุบ", f"ประจุ{opposite} แผ่นโลหะหุบ"),
            topic=TOPIC_CHARGE, hint="การแตะทำให้ประจุถ่ายเทมาอยู่บนอิเล็กโทรสโคป ได้ประจุชนิดเดียวกับแท่ง")
