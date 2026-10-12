"""คลื่นแม่เหล็กไฟฟ้า แสงโพลาไรส์ และการนำไปใช้

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/7

Sets moved here from: science_wave_f14.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f14 import SUBJECT, UPPER_SIX, _exact

PROVENANCE = Provenance("original")


TOPIC_POLAR = "คลื่นแม่เหล็กไฟฟ้า แสงโพลาไรส์ และการนำไปใช้"


EM_FACTS = (
    ("คลื่นแม่เหล็กไฟฟ้าเกิดขึ้นได้อย่างไร", "ประจุไฟฟ้าที่เคลื่อนที่ด้วยความเร่งทำให้สนามไฟฟ้าและสนามแม่เหล็กเปลี่ยนแปลงแผ่ออกไป",
     ("ประจุไฟฟ้าที่อยู่นิ่ง", "แม่เหล็กถาวรที่อยู่นิ่ง", "การสั่นของโมเลกุลอากาศเท่านั้น")),
    ("ในคลื่นแม่เหล็กไฟฟ้า สนามไฟฟ้าและสนามแม่เหล็กมีทิศสัมพันธ์กันอย่างไร", "ตั้งฉากกันและตั้งฉากกับทิศการเคลื่อนที่ของคลื่น",
     ("ขนานกันและขนานกับทิศการเคลื่อนที่", "สนามไฟฟ้าขนานกับทิศการเคลื่อนที่", "ทำมุม 45° กัน")),
    ("แสงโพลาไรส์เชิงเส้นคือแสงแบบใด", "แสงที่สนามไฟฟ้าสั่นในระนาบเดียว",
     ("แสงที่สนามไฟฟ้าสั่นทุกระนาบ", "แสงที่มีหลายความยาวคลื่น", "แสงที่ไม่มีสนามแม่เหล็ก")),
    ("แสงจากดวงอาทิตย์และหลอดไฟทั่วไปเป็นแสงแบบใด", "แสงไม่โพลาไรส์",
     ("แสงโพลาไรส์เชิงเส้น", "แสงเลเซอร์", "แสงสีเดียว")),
    ("แว่นกันแดดแบบโพลารอยด์ช่วยลดแสงจ้าจากผิวน้ำได้ เพราะเหตุใด", "แสงสะท้อนจากผิวน้ำเป็นแสงโพลาไรส์บางส่วน แผ่นโพลารอยด์กั้นไว้ได้",
     ("แผ่นโพลารอยด์สะท้อนแสงทุกทิศ", "แสงสะท้อนจากผิวน้ำไม่มีสนามไฟฟ้า", "แผ่นโพลารอยด์เปลี่ยนสีของแสง")),
    ("คลื่นเสียงถูกทำให้โพลาไรส์ไม่ได้ เพราะเหตุใด", "เสียงเป็นคลื่นตามยาว",
     ("เสียงเป็นคลื่นตามขวาง", "เสียงเร็วเกินไป", "เสียงไม่มีความยาวคลื่น")),
)


MALUS = ((0, Fraction(1)), (60, Fraction(1, 4)), (37, Fraction(16, 25)), (53, Fraction(9, 25)), (90, Fraction(0)))


BANDS = (
    ("เตาไมโครเวฟ", "คลื่นไมโครเวฟ ทำให้โมเลกุลน้ำในอาหารสั่นจนร้อน"),
    ("เรดาร์ตรวจจับเครื่องบิน", "คลื่นไมโครเวฟ สะท้อนจากวัตถุแล้วจับเวลาที่คลื่นกลับมา"),
    ("รีโมตคอนโทรลโทรทัศน์", "รังสีอินฟราเรด ส่งสัญญาณเป็นจังหวะไปยังตัวรับ"),
    ("กล้องถ่ายภาพความร้อน", "รังสีอินฟราเรด ที่วัตถุอุ่นแผ่ออกมามากกว่าวัตถุเย็น"),
    ("หลอดฆ่าเชื้อโรค", "รังสีอัลตราไวโอเลต ทำลายสารพันธุกรรมของจุลินทรีย์"),
    ("การถ่ายภาพกระดูก", "รังสีเอกซ์ ทะลุเนื้อเยื่ออ่อนได้แต่ถูกกระดูกดูดกลืนมาก"),
    ("การฉายรังสีรักษามะเร็ง", "รังสีแกมมา พลังงานสูงทำลายเซลล์มะเร็ง"),
    ("วิทยุกระจายเสียง", "คลื่นวิทยุ ความยาวคลื่นยาว เลี้ยวเบนและสะท้อนจากชั้นบรรยากาศได้ดี"),
)


@question_type(
    "phys.polarisation_em_foundation",
    display_name={"th": "การเกิดคลื่นแม่เหล็กไฟฟ้าและแสงโพลาไรส์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_POLAR,
)
class PolarisationEmFoundation(QuestionType):
    """How EM waves arise, and what polarised light is; λ = c/f."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(EM_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_POLAR,
                             hint="คลื่นแม่เหล็กไฟฟ้าเป็นคลื่นตามขวาง จึงโพลาไรส์ได้")
        unit, scale = rng.choice((("MHz", 10 ** 6), ("GHz", 10 ** 9), ("kHz", 10 ** 3)))
        f = rng.choice([x for x in (1, 2, 3, 5, 6, 10, 15, 20, 30, 50, 60, 75, 100, 150, 300, 600, 750)
                        if _exact(Fraction(3 * 10 ** 8, x * scale))])
        return numeric(
            stem=f"คลื่นแม่เหล็กไฟฟ้าความถี่ {f} {unit} มีความยาวคลื่นเท่าใดในอากาศ (c = 3 × 10⁸ m/s)",
            answer=Fraction(3 * 10 ** 8, f * scale), wrongs=[Fraction(3 * 10 ** 8, f * scale) * 10,
                                                              Fraction(3 * 10 ** 8, f * scale) * 100,
                                                              Fraction(3 * 10 ** 8, f * scale) * 1000],
            unit="m", topic=TOPIC_POLAR, hint="λ = c/f")


@question_type(
    "phys.polarisation_em_fluency",
    display_name={"th": "ความเข้มแสงที่ผ่านแผ่นโพลารอยด์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_POLAR,
)
class PolarisationEmFluency(QuestionType):
    """The first polaroid halves unpolarised light; the second passes I cos² θ."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        i0 = rng.randint(1, 20) * 50
        angle, cos2 = rng.choice(MALUS)
        stated = "(cos 60° = 0.5, cos 37° = 0.8, cos 53° = 0.6)"
        if rng.random() < 0.35:
            return numeric(stem=f"แสงไม่โพลาไรส์ความเข้ม {i0} W/m² ผ่านแผ่นโพลารอยด์แผ่นเดียว ความเข้มแสงที่ผ่านออกมาเท่าใด",
                           answer=Fraction(i0, 2), wrongs=[i0, Fraction(i0, 4), i0 * 2],
                           unit="W/m²", topic=TOPIC_POLAR, hint="แผ่นโพลารอยด์แผ่นแรกให้แสงผ่านครึ่งหนึ่งของแสงไม่โพลาไรส์")
        out = Fraction(i0, 2) * cos2
        if angle == 90:
            return _labelled(
                stem=f"แสงไม่โพลาไรส์ความเข้ม {i0} W/m² ผ่านแผ่นโพลารอยด์สองแผ่นที่แกนทำมุม 90° กัน ความเข้มแสงที่ออกมาเท่าใด",
                correct="0 W/m²", wrongs=(f"{show(Fraction(i0, 2))} W/m²", f"{show(Fraction(i0, 4))} W/m²", f"{i0} W/m²"),
                topic=TOPIC_POLAR, hint="แผ่นที่สองตั้งฉากกับแผ่นแรก cos 90° = 0 แสงผ่านไม่ได้เลย")
        return numeric(
            stem=(f"แสงไม่โพลาไรส์ความเข้ม {i0} W/m² ผ่านแผ่นโพลารอยด์สองแผ่นที่แกนทำมุม {angle}° กัน "
                  f"ความเข้มแสงที่ออกมาเท่าใด {stated}"),
            answer=out, wrongs=[i0 * cos2, Fraction(i0, 2), out * 2 if angle else Fraction(i0, 4)], unit="W/m²",
            topic=TOPIC_POLAR, hint="แผ่นแรกเหลือ I₀/2 แผ่นที่สองเหลือ (I₀/2) cos² θ ตามกฎของมาลุส")


@question_type(
    "phys.polarisation_em_application",
    display_name={"th": "การนำคลื่นแม่เหล็กไฟฟ้าช่วงต่าง ๆ และแสงโพลาไรส์ไปใช้"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_POLAR,
)
class PolarisationEmApplication(QuestionType):
    """Which band each device uses, and how."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(BANDS, 4)
        device, how = chosen[0]
        hint = "คลื่นวิทยุ → ไมโครเวฟ → อินฟราเรด → แสง → อัลตราไวโอเลต → เอกซ์ → แกมมา ความถี่และพลังงานเพิ่มขึ้นตามลำดับ"
        if rng.random() < 0.5:
            return _labelled(stem=f"{device}ใช้คลื่นแม่เหล็กไฟฟ้าช่วงใดและทำงานอย่างไร", correct=how,
                             wrongs=tuple(h for _, h in chosen[1:]), topic=TOPIC_POLAR, hint=hint)
        return _labelled(stem=f"อุปกรณ์ใดใช้{how}", correct=device,
                         wrongs=tuple(d for d, _ in chosen[1:]), topic=TOPIC_POLAR, hint=hint)
