"""หลักฐานการเคลื่อนที่ของแผ่นธรณี

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/2

Sets moved here from: science_wave_f74.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f74 import GEOLOGY, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_DRIFT = "หลักฐานการเคลื่อนที่ของแผ่นธรณี"


EVIDENCE = (
    ("รอยต่อของทวีป", "ขอบทวีปอเมริกาใต้และแอฟริกาต่อกันได้พอดีเหมือนชิ้นส่วนภาพต่อ"),
    ("ซากดึกดำบรรพ์", "พบซากมีโซซอรัสและกลอสซอพเทอริสในทวีปที่ปัจจุบันอยู่ห่างกันด้วยมหาสมุทร"),
    ("หินและแนวเทือกเขา", "ชนิดหินและแนวเทือกเขาที่มีอายุเดียวกันต่อเนื่องกันเมื่อนำทวีปมาต่อกัน"),
    ("ภูมิอากาศบรรพกาล", "พบร่องรอยธารน้ำแข็งในอินเดียและแอฟริกา และพบถ่านหินในแอนตาร์กติกา"),
    ("ภาวะแม่เหล็กโลกบรรพกาล", "แถบหินที่มีทิศแม่เหล็กสลับกันเรียงสมมาตรทั้งสองข้างของสันเขากลางมหาสมุทร"),
    ("อายุหินพื้นมหาสมุทร", "หินพื้นมหาสมุทรมีอายุมากขึ้นเมื่ออยู่ห่างจากสันเขากลางมหาสมุทร"),
)


DRIFT_HINT = ("หลักฐานทวีปเลื่อน: รอยต่อทวีป ซากดึกดำบรรพ์ หินและเทือกเขา ภูมิอากาศบรรพกาล หลักฐานพื้นทะเลแผ่: แถบแม่เหล็กสมมาตร "
              "และอายุหินที่มากขึ้นเมื่อห่างจากสันเขากลางมหาสมุทร")


DRIFT_FACTS = (
    ("การพบถ่านหินในทวีปแอนตาร์กติกาบอกอะไร", "ทวีปแอนตาร์กติกาเคยอยู่ในเขตที่อบอุ่นและมีป่าไม้มาก่อน",
     ("แอนตาร์กติกาเคยมีภูเขาไฟมาก", "ถ่านหินเกิดได้ในน้ำแข็งที่ขั้วโลกโดยไม่ต้องมีพืช", "แอนตาร์กติกาเคยอยู่ใต้ทะเลลึก", "ถ่านหินถูกลมพัดมาจากทวีปอื่น")),
    ("มีโซซอรัสเป็นสัตว์เลื้อยคลานน้ำจืด การพบซากในบราซิลและแอฟริกาใต้บอกอะไร", "สองทวีปนี้เคยเชื่อมต่อกัน เพราะมีโซซอรัสว่ายข้ามมหาสมุทรไม่ได้",
     ("มีโซซอรัสว่ายข้ามมหาสมุทรได้", "มีโซซอรัสว่ายข้ามมหาสมุทรได้ จึงพบซากในทั้งสองทวีป", "สองทวีปอยู่ห่างกันเท่าเดิมตลอดมา แต่มีสะพานแผ่นดินเชื่อมชั่วคราว", "ซากถูกกระแสน้ำในมหาสมุทรพัดพาข้ามจากทวีปหนึ่งไปอีกทวีปหนึ่ง")),
    ("แถบแม่เหล็กที่สมมาตรสองข้างสันเขากลางมหาสมุทรสนับสนุนแนวคิดใด", "พื้นทะเลแผ่ขยายจากสันเขากลางมหาสมุทรออกไปสองข้าง",
     ("พื้นทะเลหดตัวเข้าหาสันเขากลางมหาสมุทรจากทั้งสองข้าง", "สนามแม่เหล็กโลกไม่เคยกลับทิศ", "เปลือกโลกมหาสมุทรเก่ากว่าเปลือกโลกทวีปเสมอ", "สันเขาเกิดจากการชนของทวีป")),
    ("หินพื้นมหาสมุทรที่อายุน้อยที่สุดพบบริเวณใด", "ใกล้สันเขากลางมหาสมุทร",
     ("ใกล้ชายฝั่งทวีป", "ในร่องลึกก้นสมุทรเท่านั้น", "กลางทวีปขนาดใหญ่", "บนยอดเขาสูงบนบก", "กระจายเท่ากันทุกที่")),
    ("เหตุใดแนวคิดทวีปเลื่อนของเวเกเนอร์จึงไม่ได้รับการยอมรับในตอนแรก", "ยังอธิบายไม่ได้ว่าแรงใดทำให้ทวีปเคลื่อนที่",
     ("ไม่มีหลักฐานซากดึกดำบรรพ์ที่พบในหลายทวีปเลย", "ขอบทวีปไม่มีส่วนใดต่อกันได้พอดีเลย", "เขาไม่มีหลักฐานว่าทวีปต่อกันได้", "ยังไม่มีใครพบซากดึกดำบรรพ์ในสองทวีป", "เขาใช้แต่หลักฐานจากดวงจันทร์")),
    ("ใครเสนอทฤษฎีทวีปเลื่อนเป็นคนแรก", "อัลเฟรด เวเกเนอร์", ("ชาลส์ ดาร์วิน", "อัลเฟรด แวลเลซ", "แฮร์รี แฮมมอนด์ เฮสส์", "เกรเกอร์ เมนเดล")),
    ("แพนเจียคืออะไร", "มหาทวีปที่ทวีปทั้งหมดเคยรวมกันอยู่เมื่อประมาณ 200 ล้านปีก่อน",
     ("มหาสมุทรโบราณที่ใหญ่ที่สุด", "ชื่อของแผ่นธรณีแปซิฟิก", "มหาสมุทรโบราณที่ล้อมรอบทวีปทั้งหมดเมื่อประมาณ 200 ล้านปีก่อน", "ชื่อของแผ่นธรณีแปซิฟิกที่ใหญ่ที่สุดในปัจจุบันของโลก")),
)


@question_type(
    "geo.drift_evidence_foundation",
    display_name={"th": "หลักฐานที่สนับสนุนการเคลื่อนที่ของแผ่นธรณี"},
    level=UPPER_FOUR, subject=GEOLOGY, topic=TOPIC_DRIFT,
)
class DriftEvidenceFoundation(QuestionType):
    """Name the kind of evidence from what was found, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind, found = rng.choice(EVIDENCE)
        others = rng.sample([e for e in EVIDENCE if e[0] != kind], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{found}\" เป็นหลักฐานประเภทใด", correct=f"หลักฐานจาก{kind}", wrongs=tuple(f"หลักฐานจาก{e[0]}" for e in others),
                             topic=TOPIC_DRIFT, hint=DRIFT_HINT)
        return _labelled(stem=f"ข้อใดเป็นหลักฐานจาก{kind}", correct=found, wrongs=tuple(e[1] for e in others), topic=TOPIC_DRIFT, hint=DRIFT_HINT)


@question_type(
    "geo.drift_evidence_fluency",
    display_name={"th": "แปลความหมายหลักฐานทวีปเลื่อนและพื้นทะเลแผ่"},
    level=UPPER_FOUR, subject=GEOLOGY, topic=TOPIC_DRIFT,
)
class DriftEvidenceFluency(QuestionType):
    """What each piece of evidence lets you conclude."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(DRIFT_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_DRIFT, hint=DRIFT_HINT)


@question_type(
    "geo.drift_evidence_application",
    display_name={"th": "คำนวณอัตราการแผ่ขยายของพื้นทะเล"},
    level=UPPER_FOUR, subject=GEOLOGY, topic=TOPIC_DRIFT,
)
class DriftEvidenceApplication(QuestionType):
    """Rate = distance ÷ age; 1 km per million years is 0.1 cm per year."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        while True:
            km = rng.randrange(50, 3001, 50)
            ma = rng.choice((1, 2, 4, 5, 10, 20, 25, 40, 50, 100))
            rate = Fraction(km, ma) / 10  # cm per year
            if (rate * 100).denominator == 1 and 1 <= rate <= 20:
                break
        roll = rng.random()
        if roll < 0.5:
            return numeric(stem=f"หินพื้นมหาสมุทรที่ห่างจากสันเขากลางมหาสมุทร {km:,} km มีอายุ {ma} ล้านปี พื้นทะเลแผ่ขยายด้วยอัตราเฉลี่ยกี่เซนติเมตรต่อปี",
                           answer=rate, wrongs=[Fraction(km, ma), rate * 10 if rate * 10 != Fraction(km, ma) else rate * 2, Fraction(ma * 10, km) if
                                                (Fraction(ma * 10, km) * 100).denominator == 1 else rate + 1], unit="cm/ปี", topic=TOPIC_DRIFT,
                           hint="1 km = 100,000 cm และ 1 ล้านปี = 1,000,000 ปี อัตรา (cm/ปี) = ระยะทาง (km) ÷ อายุ (ล้านปี) ÷ 10")
        years = rng.choice((10, 50, 100, 1000))
        if (rate * years / 100 * 100).denominator != 1:
            years = 100
        moved = rate * years
        return numeric(stem=f"พื้นทะเลแผ่ขยายด้วยอัตรา {show(rate)} cm ต่อปี ใน {years:,} ปีจะเคลื่อนที่ได้กี่เมตร", answer=moved / 100,
                       wrongs=[moved, moved / 10, rate * years * 10], unit="m", topic=TOPIC_DRIFT,
                       hint="ระยะทาง = อัตรา × เวลา แล้วแปลงเซนติเมตรเป็นเมตร (÷ 100)")
