"""ประโยชน์ อันตราย และการป้องกันรังสี

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/17

Sets moved here from: science_wave_f18.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f18 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SAFETY = "ประโยชน์ อันตราย และการป้องกันรังสี"


USES = (
    ("ไอโอดีน-131", "ตรวจและรักษาโรคของต่อมไทรอยด์"),
    ("โคบอลต์-60", "ฉายรังสีแกมมารักษามะเร็งและฆ่าเชื้อในเครื่องมือแพทย์"),
    ("คาร์บอน-14", "หาอายุของซากสิ่งมีชีวิตโบราณ"),
    ("อะเมริเซียม-241", "ใช้ในเครื่องตรวจจับควัน"),
    ("เทคนีเชียม-99m", "ถ่ายภาพอวัยวะภายในทางเวชศาสตร์นิวเคลียร์"),
    ("ฟอสฟอรัส-32", "ติดตามการดูดธาตุอาหารของพืช"),
    ("ซีเซียม-137", "วัดความหนาของแผ่นวัสดุในโรงงาน"),
)


PROTECTION = (
    ("ผู้ปฏิบัติงานทางรังสีควรปฏิบัติตามหลักใดเพื่อลดปริมาณรังสีที่ได้รับ", "ใช้เวลาให้น้อย อยู่ให้ห่าง และมีเครื่องกำบัง",
     ("อยู่ใกล้ต้นกำเนิดรังสีให้นานที่สุด", "ถอดเครื่องกำบังเพื่อให้ทำงานสะดวก", "ดื่มน้ำมาก ๆ แทนการกำบัง")),
    ("หน่วยที่ใช้บอกปริมาณรังสีที่มีผลต่อร่างกายคือข้อใด", "ซีเวิร์ต (Sv)", ("เบกเคอเรล (Bq)", "จูล (J)", "เฮิรตซ์ (Hz)")),
    ("สัญลักษณ์ใบพัดสามแฉกสีม่วงแดงบนพื้นเหลืองหมายถึงอะไร", "บริเวณที่มีวัสดุกัมมันตรังสีหรือรังสี",
     ("บริเวณที่มีไฟฟ้าแรงสูง", "บริเวณที่มีสารไวไฟ", "ทางหนีไฟ")),
    ("อันตรายสำคัญจากรังสีต่อร่างกายคือข้อใด", "ทำให้เซลล์และสารพันธุกรรมเสียหาย อาจเกิดมะเร็ง",
     ("ทำให้ร่างกายมีประจุไฟฟ้า", "ทำให้กระดูกเป็นแม่เหล็ก", "ไม่มีอันตรายใด ๆ")),
    ("การฉายรังสีอาหารทำให้อาหารเป็นอย่างไร", "เก็บได้นานขึ้นเพราะจุลินทรีย์ถูกทำลาย โดยอาหารไม่กลายเป็นสารกัมมันตรังสี",
     ("อาหารกลายเป็นสารกัมมันตรังสี", "อาหารมีรสชาติหวานขึ้น", "อาหารสุกทันที")),
)


@question_type(
    "phys.radiation_safety_foundation",
    display_name={"th": "ประโยชน์ของไอโซโทปกัมมันตรังสีในด้านต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SAFETY,
)
class RadiationSafetyFoundation(QuestionType):
    """Each isotope and the job it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(USES, 4)
        iso, use = chosen[0]
        hint = "นึกถึงสมบัติของไอโซโทป เช่น อวัยวะที่ดูดธาตุนั้น ชนิดรังสี และครึ่งชีวิต"
        if rng.random() < 0.5:
            return _labelled(stem=f"{iso}ใช้ประโยชน์ด้านใด", correct=use, wrongs=tuple(u for _, u in chosen[1:]),
                             topic=TOPIC_SAFETY, hint=hint)
        return _labelled(stem=f"ไอโซโทปกัมมันตรังสีใดใช้{use}", correct=iso, wrongs=tuple(i for i, _ in chosen[1:]),
                         topic=TOPIC_SAFETY, hint=hint)


@question_type(
    "phys.radiation_safety_fluency",
    display_name={"th": "ปริมาณรังสีที่ได้รับตามเวลาและระยะห่าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SAFETY,
)
class RadiationSafetyFluency(QuestionType):
    """Dose = rate × time; rate falls as 1/r² from a point source."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rate = rng.randint(1, 40) * 5
        if rng.random() < 0.5:
            minutes = rng.choice((6, 12, 15, 30, 45, 90, 120, 150))
            return numeric(
                stem=f"บริเวณหนึ่งมีอัตราปริมาณรังสี {rate} ไมโครซีเวิร์ตต่อชั่วโมง อยู่ในบริเวณนั้น {minutes} นาที ได้รับรังสีกี่ไมโครซีเวิร์ต",
                answer=Fraction(rate * minutes, 60), wrongs=[rate * minutes, Fraction(rate, minutes), Fraction(rate * 60, minutes)],
                unit="μSv", topic=TOPIC_SAFETY, hint="ปริมาณรังสี = อัตราต่อชั่วโมง × เวลาเป็นชั่วโมง")
        r1 = rng.randint(1, 5)
        k = rng.choice((2, 3, 4, 5, 10))
        r = rate * k * k
        return numeric(
            stem=f"ห่างจากต้นกำเนิดรังสีขนาดเล็ก {r1} m วัดอัตราปริมาณรังสีได้ {r:,} μSv/h ถ้าถอยไปอยู่ห่าง {r1 * k} m อัตราปริมาณรังสีเท่าใด",
            answer=Fraction(r, k * k), wrongs=[Fraction(r, k), r, Fraction(r, 2 * k)], unit="μSv/h", topic=TOPIC_SAFETY,
            hint="รังสีจากต้นกำเนิดขนาดเล็กลดลงตามระยะห่างกำลังสอง: ห่างขึ้น k เท่า เหลือ 1/k²")


@question_type(
    "phys.radiation_safety_application",
    display_name={"th": "การกำบังรังสีและหลักความปลอดภัยทางรังสี"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SAFETY,
)
class RadiationSafetyApplication(QuestionType):
    """Half-value layers of shielding, and the rules of time, distance and shielding."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(PROTECTION)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SAFETY,
                             hint="หลักป้องกันรังสี: เวลาน้อย ระยะห่างมาก และมีเครื่องกำบัง")
        hvl = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, 5, 6))
        material = rng.choice(("ตะกั่ว", "คอนกรีต", "เหล็ก"))
        n = rng.randint(1, 5)
        rate = rng.randint(1, 20) * 2 ** n * 5
        return numeric(
            stem=(f"{material}หนา {show(hvl)} cm ลดความเข้มรังสีแกมมาลงครึ่งหนึ่ง ถ้าใช้{material}หนา {show(hvl * n)} cm "
                  f"กั้นรังสีที่มีอัตรา {rate:,} μSv/h จะเหลืออัตราเท่าใด"),
            answer=Fraction(rate, 2 ** n), wrongs=[Fraction(rate, 2 * n), rate - Fraction(rate, 2 ** n), Fraction(rate, 2 ** (n + 1))],
            unit="μSv/h", topic=TOPIC_SAFETY, hint="ทุกความหนาหนึ่งเท่าของความหนาครึ่งค่า ความเข้มลดลงครึ่งหนึ่ง")
