"""การลดลงของสัตว์ป่าและการอนุรักษ์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/13

Sets moved here from: science_wave_f74.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f74 import BIOLOGY, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_WILD = "การลดลงของสัตว์ป่าและการอนุรักษ์"


THREATS = ("การสูญเสียแหล่งที่อยู่จากการบุกรุกป่า", "การล่าเพื่อการค้าอวัยวะและซาก", "การนำสัตว์ต่างถิ่นเข้ามาแย่งอาหารและที่อยู่",
           "มลพิษในแหล่งน้ำ", "การเปลี่ยนแปลงสภาพภูมิอากาศ")


IN_SITU = ("ประกาศเขตรักษาพันธุ์สัตว์ป่า", "จัดตั้งอุทยานแห่งชาติ", "ทำทางเชื่อมผืนป่าให้สัตว์ป่าเคลื่อนย้ายได้", "ลาดตระเวนป้องกันการล่า",
           "ฟื้นฟูแหล่งหญ้าทะเลที่เป็นอาหารของพะยูน")


EX_SITU = ("เพาะเลี้ยงสัตว์ใกล้สูญพันธุ์ในสวนสัตว์", "เก็บน้ำเชื้อและตัวอ่อนแช่แข็งในธนาคารพันธุกรรม", "อนุบาลลูกเต่าทะเลในบ่อก่อนปล่อยคืนธรรมชาติ",
           "เพาะพันธุ์ละองละมั่งในสถานีเพาะเลี้ยงก่อนปล่อยคืนป่า")


RESERVED = ("สมเสร็จ", "พะยูน", "กูปรี", "แรด", "นกแต้วแล้วท้องดำ", "ละองหรือละมั่ง")


WILD_HINT = ("สัตว์ป่าลดลงจากการเสียแหล่งที่อยู่ การล่า สัตว์ต่างถิ่น มลพิษ และภูมิอากาศเปลี่ยน การอนุรักษ์ในถิ่นที่อยู่เช่นเขตรักษาพันธุ์ "
             "การอนุรักษ์นอกถิ่นที่อยู่เช่นสวนสัตว์และธนาคารพันธุกรรม")


@question_type(
    "biology.wildlife_conservation_foundation",
    display_name={"th": "สาเหตุการลดลงของสัตว์ป่า"},
    level=UPPER_SIX, subject=BIOLOGY, topic=TOPIC_WILD,
)
class WildlifeConservationFoundation(QuestionType):
    """Threats against conservation actions; and reserved species."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _labelled(stem="สัตว์ใดเป็นสัตว์ป่าสงวนของไทย", correct=rng.choice(RESERVED),
                             wrongs=tuple(("ไก่บ้าน", "สุนัขบ้าน", "ปลานิล", "หนูบ้าน", "นกพิราบ")), topic=TOPIC_WILD, hint=WILD_HINT)
        threat = rng.random() < 0.5
        right, wrong = (THREATS, IN_SITU + EX_SITU) if threat else (IN_SITU + EX_SITU, THREATS)
        return _labelled(stem=f"ข้อใด{'เป็นสาเหตุที่ทำให้สัตว์ป่าลดลง' if threat else 'เป็นแนวทางอนุรักษ์สัตว์ป่า'}", correct=rng.choice(right),
                         wrongs=tuple(wrong), topic=TOPIC_WILD, hint=WILD_HINT)


@question_type(
    "biology.wildlife_conservation_fluency",
    display_name={"th": "การอนุรักษ์ในถิ่นที่อยู่และนอกถิ่นที่อยู่"},
    level=UPPER_SIX, subject=BIOLOGY, topic=TOPIC_WILD,
)
class WildlifeConservationFluency(QuestionType):
    """In situ or ex situ."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        in_situ = rng.random() < 0.5
        same, other = (IN_SITU, EX_SITU) if in_situ else (EX_SITU, IN_SITU)
        kind = "การอนุรักษ์ในถิ่นที่อยู่" if in_situ else "การอนุรักษ์นอกถิ่นที่อยู่"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็น{kind}", correct=rng.choice(same), wrongs=tuple(other) if len(other) >= 3
                             else (*other, rng.choice(THREATS)), topic=TOPIC_WILD, hint=WILD_HINT)
        return _labelled(stem=f"\"{rng.choice(same)}\" เป็นการอนุรักษ์แบบใด", correct=kind,
                         wrongs=("การอนุรักษ์นอกถิ่นที่อยู่" if in_situ else "การอนุรักษ์ในถิ่นที่อยู่", "การล่าอย่างยั่งยืน", "ไบโอแมกนิฟิเคชัน"),
                         topic=TOPIC_WILD, hint=WILD_HINT)


@question_type(
    "biology.wildlife_conservation_application",
    display_name={"th": "วิเคราะห์การเปลี่ยนแปลงประชากรสัตว์ป่า"},
    level=UPPER_SIX, subject=BIOLOGY, topic=TOPIC_WILD,
)
class WildlifeConservationApplication(QuestionType):
    """Share recovered or lost, from survey counts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal = rng.choice(("ช้างป่า", "พะยูน", "เสือโคร่ง", "นกเงือก", "กวางผา"))
        before = rng.randrange(20, 401, 20)
        change = rng.choice((10, 15, 20, 25, 40, 50, 60, 75))
        up = rng.random() < 0.5
        after = Fraction(before * (100 + change if up else 100 - change), 100)
        if rng.random() < 0.6:
            return numeric(stem=f"สำรวจพบ{animal} {before} ตัว หลัง{'ประกาศเขตคุ้มครองได้' if up else 'ป่าถูกบุกรุกเป็นเวลา'} 10 ปี พบ {show(after)} ตัว "
                                f"ประชากร{'เพิ่มขึ้น' if up else 'ลดลง'}ร้อยละเท่าใด", answer=change,
                           wrongs=[100 - change if change != 50 else 25, abs(after - before), Fraction(after * 100, before)], unit="%",
                           topic=TOPIC_WILD, hint="ร้อยละที่เปลี่ยน = ผลต่าง × 100 ÷ จำนวนเดิม")
        return numeric(stem=f"{animal}มี {before} ตัว ถ้าประชากร{'เพิ่มขึ้น' if up else 'ลดลง'}ร้อยละ {change} จะเหลือ{'หรือมี' if up else ''}กี่ตัว",
                       answer=after, wrongs=[Fraction(before * change, 100), before, before + change if up else before - change], unit="ตัว",
                       topic=TOPIC_WILD, hint="จำนวนใหม่ = จำนวนเดิม × (100 ± ร้อยละ) ÷ 100")
