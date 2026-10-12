"""สนามแม่เหล็กและฟลักซ์แม่เหล็ก

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/1

Sets moved here from: science_wave_f12.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f12 import (
    DIRECTIONS,
    NAME_OF,
    SUBJECT,
    UPPER_SIX,
    _exact,
    cross,
)

PROVENANCE = Provenance("original")


TOPIC_FLUX = "สนามแม่เหล็กและฟลักซ์แม่เหล็ก"


SIDES = {"ด้านขวา": (1, 0, 0), "ด้านซ้าย": (-1, 0, 0), "ด้านบน": (0, 1, 0), "ด้านล่าง": (0, -1, 0)}


FLUX_FACTS = (
    ("เส้นสนามแม่เหล็กภายนอกแท่งแม่เหล็กมีทิศใด", "ออกจากขั้วเหนือเข้าสู่ขั้วใต้",
     ("ออกจากขั้วใต้เข้าสู่ขั้วเหนือ", "วนรอบกลางแท่งแม่เหล็ก", "ขนานกับแท่งแม่เหล็กเสมอ")),
    ("บริเวณที่เส้นสนามแม่เหล็กอยู่ชิดกันมากหมายความว่าอย่างไร", "สนามแม่เหล็กมีขนาดมาก",
     ("สนามแม่เหล็กมีขนาดน้อย", "ไม่มีสนามแม่เหล็ก", "สนามแม่เหล็กเปลี่ยนทิศ")),
    ("สนามแม่เหล็กรอบเส้นลวดตรงที่มีกระแสไฟฟ้ามีลักษณะใด", "เป็นวงกลมรอบเส้นลวด ทิศตามกฎมือขวา",
     ("เป็นเส้นตรงขนานกับเส้นลวด", "พุ่งออกจากเส้นลวดในแนวรัศมี", "มีเฉพาะที่ปลายลวด")),
    ("สนามแม่เหล็กของโซเลนอยด์ที่มีกระแสไฟฟ้ามีลักษณะคล้ายสิ่งใด", "แท่งแม่เหล็ก โดยภายในขดลวดสนามเกือบสม่ำเสมอ",
     ("สนามรอบเส้นลวดตรงเส้นเดียว", "สนามไฟฟ้าของจุดประจุ", "ไม่มีสนามภายในขดลวด")),
    ("ข้อใดทำให้สนามแม่เหล็กภายในโซเลนอยด์มีขนาดมากขึ้น", "เพิ่มจำนวนรอบต่อความยาวหรือเพิ่มกระแสไฟฟ้า",
     ("ลดกระแสไฟฟ้า", "ใช้ลวดที่ยาวขึ้นแต่จำนวนรอบเท่าเดิม", "เปลี่ยนทิศกระแสไฟฟ้า")),
    ("หน่วยของฟลักซ์แม่เหล็กคือข้อใด", "เวเบอร์ (Wb) ซึ่งเท่ากับเทสลา × ตารางเมตร",
     ("เทสลา (T)", "เวเบอร์ต่อตารางเมตร", "แอมแปร์ต่อเมตร")),
)


@question_type(
    "phys.magnetic_flux_foundation",
    display_name={"th": "เส้นสนามแม่เหล็กและสนามแม่เหล็กจากกระแสไฟฟ้า"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FLUX,
)
class MagneticFluxFoundation(QuestionType):
    """Field lines, the field round a wire and inside a coil."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(FLUX_FACTS)
        if rng.random() < 0.4:
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_FLUX,
                             hint="เส้นสนามออกจากขั้วเหนือเข้าขั้วใต้ ยิ่งชิดกันสนามยิ่งมาก")
        b = Fraction(rng.randint(1, 20), rng.choice((10, 100)))
        area = Fraction(rng.randint(1, 40), rng.choice((10, 100)))
        flux = b * area
        if not _exact(flux):
            area = Fraction(rng.randint(1, 20) * 5, 100)
            b = Fraction(rng.randint(1, 20) * 2, 10)
            flux = b * area
        return numeric(
            stem=f"สนามแม่เหล็กสม่ำเสมอ {show(b)} T ตั้งฉากกับพื้นผิวพื้นที่ {show(area)} m² ฟลักซ์แม่เหล็กผ่านพื้นผิวเท่าใด",
            answer=flux, wrongs=[b / area, flux * 2, b + area], unit="Wb", topic=TOPIC_FLUX, hint="Φ = BA เมื่อ B ตั้งฉากกับพื้นผิว")


@question_type(
    "phys.magnetic_flux_fluency",
    display_name={"th": "คำนวณฟลักซ์แม่เหล็กเมื่อสนามทำมุมกับพื้นผิว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FLUX,
)
class MagneticFluxFluency(QuestionType):
    """Φ = BA cos θ with θ from the normal, and B back from a measured flux."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        angle, cos = rng.choice(((0, Fraction(1)), (37, Fraction(4, 5)), (53, Fraction(3, 5)), (60, Fraction(1, 2)),
                                 (90, Fraction(0))))
        b, area = rng.choice([(Fraction(x * 5, 10), Fraction(y * 5, 100)) for x in range(1, 11) for y in range(1, 21)
                              if _exact(Fraction(x * 5, 10) * Fraction(y * 5, 100) * cos)])
        flux = b * area * cos
        stated = "(cos 37° = 0.8, cos 53° = 0.6, cos 60° = 0.5)"
        if angle == 90:
            return _labelled(
                stem=f"สนามแม่เหล็ก {show(b)} T มีทิศขนานกับระนาบของขดลวดพื้นที่ {show(area)} m² ฟลักซ์ผ่านขดลวดเท่าใด",
                correct="0 Wb", wrongs=(f"{show(b * area)} Wb", f"{show(b * area * 2)} Wb", f"{show(b * area / 2)} Wb"),
                topic=TOPIC_FLUX, hint="สนามขนานกับระนาบ (ตั้งฉากกับเส้นแนวฉาก) ไม่มีเส้นสนามผ่านขดลวด")
        if rng.random() < 0.6 or angle != 0:
            return numeric(
                stem=(f"สนามแม่เหล็ก {show(b)} T ทำมุม {angle}° กับเส้นแนวฉากของขดลวดพื้นที่ {show(area)} m² "
                      f"ฟลักซ์แม่เหล็กผ่านขดลวดเท่าใด {stated}"),
                answer=flux, wrongs=[b * area, b * area * (1 - cos) if cos != 1 else b * area * 2, b * area * cos * 2],
                unit="Wb", topic=TOPIC_FLUX, hint="Φ = BA cos θ โดย θ วัดจากเส้นแนวฉากของพื้นผิว")
        return numeric(
            stem=(f"ฟลักซ์แม่เหล็ก {show(flux)} Wb ผ่านขดลวดพื้นที่ {show(area)} m² ที่วางตั้งฉากกับสนาม "
                  "สนามแม่เหล็กมีขนาดเท่าใด"),
            answer=flux / area, wrongs=[flux * area, area / flux if flux else 1, flux], unit="T", topic=TOPIC_FLUX,
            hint="B = Φ/A")


@question_type(
    "phys.magnetic_flux_application",
    display_name={"th": "ทิศของสนามแม่เหล็กรอบเส้นลวดตรงและโซเลนอยด์ตามกฎมือขวา"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_FLUX,
)
class MagneticFluxApplication(QuestionType):
    """The right-hand grip rule, worked as B ∝ I × r̂."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "กำมือขวาให้นิ้วโป้งชี้ทิศกระแส นิ้วที่เหลือวนตามทิศสนามแม่เหล็ก"
        if rng.random() < 0.75:
            if rng.random() < 0.5:
                current = rng.choice(("พุ่งออกจากกระดาษ", "พุ่งเข้าไปในกระดาษ"))
                side = rng.choice(list(SIDES))
            else:
                current = rng.choice(("ไปทางขวา", "ไปทางซ้าย", "ขึ้นด้านบนของหน้ากระดาษ", "ลงด้านล่างของหน้ากระดาษ"))
                axis = DIRECTIONS[current]
                side = rng.choice([s for s, v in SIDES.items() if sum(a * b for a, b in zip(v, axis)) == 0])
            field = NAME_OF[cross(DIRECTIONS[current], SIDES[side])]
            wrongs = [n for n in DIRECTIONS if n != field]
            return _labelled(
                stem=f"เส้นลวดตรงยาว{'ตั้งฉากกับกระดาษ' if 'กระดาษ' in current and 'หน้า' not in current else 'วางบนหน้ากระดาษ'} มีกระแสไฟฟ้าทิศ{current} "
                     f"สนามแม่เหล็กที่จุด{side}ของเส้นลวดมีทิศใด",
                correct=f"ทิศ{field}", wrongs=tuple(f"ทิศ{w}" for w in rng.sample(wrongs, 3)),
                topic=TOPIC_FLUX, hint=hint)
        # A solenoid lying left-right; seen from its right end, current anticlockwise means that end is N.
        anticlockwise = rng.random() < 0.5
        end = rng.choice(("ขวา", "ซ้าย"))
        north = anticlockwise
        return _labelled(
            stem=(f"มองโซเลนอยด์จากปลายด้าน{end} เห็นกระแสไฟฟ้าในขดลวดวน{'ทวนเข็มนาฬิกา' if anticlockwise else 'ตามเข็มนาฬิกา'} "
                  f"ปลายด้าน{end}เป็นขั้วใด"),
            correct="ขั้วเหนือ" if north else "ขั้วใต้",
            wrongs=("ขั้วใต้" if north else "ขั้วเหนือ", "ไม่เป็นขั้วแม่เหล็ก", "เป็นขั้วเหนือและขั้วใต้สลับกัน"),
            topic=TOPIC_FLUX, hint="มองที่ปลายขดลวด ถ้ากระแสวนทวนเข็มนาฬิกา ปลายนั้นเป็นขั้วเหนือ ตามเข็มเป็นขั้วใต้")
