"""ภูเขาไฟระเบิด

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/5

Sets moved here from: science_wave_f75.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f75 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_VOLCANO = "ภูเขาไฟระเบิด"


VOLCANOES = (
    ("ภูเขาไฟรูปโล่", "แมกมาบะซอลต์ ซิลิกาต่ำ หนืดน้อย ไหลได้ไกล ปะทุไม่รุนแรง", "ภูเขาไฟเมานาโลอา ฮาวาย"),
    ("ภูเขาไฟรูปโล่", "ลาวาไหลแผ่ออกเป็นบริเวณกว้าง ลาดเขาชันน้อย", "ภูเขาไฟคีเลาเวอา ฮาวาย"),
    ("ภูเขาไฟสลับชั้น", "แมกมาซิลิกาสูง หนืดมาก มีแก๊สมาก ปะทุรุนแรงสลับกับลาวาไหล", "ภูเขาไฟฟูจิ ญี่ปุ่น"),
    ("ภูเขาไฟสลับชั้น", "ชั้นลาวาและชั้นเถ้าถ่านสลับกันเป็นกรวยสูงชัน", "ภูเขาไฟปินาตูโบ ฟิลิปปินส์"),
    ("ภูเขาไฟสลับชั้น", "ปะทุระเบิดรุนแรง พ่นเถ้าถ่านสูงหลายกิโลเมตร", "ภูเขาไฟเซนต์เฮเลนส์ สหรัฐอเมริกา"),
    ("ภูเขาไฟกรวยกรวด", "เศษหินภูเขาไฟพุ่งออกมากองรอบปล่อง ขนาดเล็ก ลาดชัน", "ภูเขาไฟปาริคูติน เม็กซิโก"),
)


ERUPT_FACTS = (
    ("ปัจจัยใดทำให้ภูเขาไฟปะทุรุนแรง", "แมกมามีซิลิกาสูง หนืดมาก และมีแก๊สละลายอยู่มาก",
     ("แมกมามีซิลิกาต่ำและหนืดน้อย แก๊สจึงสะสมได้มาก", "แมกมามีอุณหภูมิต่ำและไม่มีแก๊สละลายอยู่เลย", "ภูเขาไฟอยู่กลางมหาสมุทรเสมอ น้ำจึงทำให้ระเบิดแรง", "ลาวาไหลออกช้า ๆ")),
    ("สัญญาณใดบอกว่าภูเขาไฟอาจจะปะทุในไม่ช้า", "แผ่นดินไหวถี่ขึ้น พื้นดินโป่งพอง และปล่อยแก๊สมากขึ้น",
     ("อุณหภูมิอากาศลดลงทั่วบริเวณและมีหิมะตกบนยอดเขาบ่อย", "น้ำทะเลใสขึ้น", "นกอพยพตามฤดูกาลผ่านภูเขาไฟ", "ฝนตกหนักติดต่อกันหลายวันบนยอดเขา")),
    ("หากอยู่ใกล้ภูเขาไฟที่กำลังปะทุ ควรปฏิบัติอย่างไร", "อพยพตามคำแนะนำ สวมหน้ากากกันเถ้า และเลี่ยงหุบเขาที่ลาวาอาจไหลผ่าน",
     ("เข้าไปดูใกล้ปล่องภูเขาไฟเพื่อประเมินความรุนแรงเอง", "หลบในหุบเขาใต้ภูเขาไฟ", "อยู่กลางแจ้งโดยไม่ป้องกันเถ้า เพราะเถ้าภูเขาไฟไม่เป็นอันตรายต่อปอด", "ขับรถผ่านเส้นทางลาวาให้เร็วที่สุดเพื่อออกจากพื้นที่")),
    ("เถ้าภูเขาไฟเป็นอันตรายต่อการบินเพราะเหตุใด", "เถ้าเป็นเศษหินแก้วแหลมคมที่หลอมในเครื่องยนต์ไอพ่นจนเครื่องดับได้",
     ("เถ้าทำให้เครื่องบินเบาลง", "เถ้าดูดความร้อนจนอากาศเย็นลง เครื่องยนต์จึงดับเพราะความเย็น", "เถ้าเป็นแก๊สที่มองไม่เห็นและไม่มีผลต่อเครื่องบินเลย", "เถ้าทำให้ฝนตกบนเครื่องบินเท่านั้นจนมองไม่เห็นทาง")),
    ("แก๊สชนิดใดพ่นออกมาจากภูเขาไฟมากที่สุด", "ไอน้ำ", ("ออกซิเจน", "ฮีเลียม", "ไนโตรเจนเท่านั้น", "คลอรีน")),
    ("ประเทศไทยเคยมีภูเขาไฟหรือไม่", "เคยมี แต่เป็นภูเขาไฟที่ดับแล้ว เช่น ที่บุรีรัมย์",
     ("ไม่เคยมีเลย เพราะประเทศไทยไม่ได้อยู่บนแผ่นธรณีใด", "มีภูเขาไฟที่ยังปะทุทุกปี", "มีเฉพาะใต้ทะเลอ่าวไทยที่ยังปะทุทุกปี", "มีภูเขาไฟที่ยังปะทุอยู่เฉพาะในภาคใต้")),
)


VOLCANO_HINT = ("แมกมาซิลิกาสูงหนืดมากและมีแก๊สมาก ปะทุรุนแรงเกิดภูเขาไฟสลับชั้น แมกมาบะซอลต์หนืดน้อยไหลไกลเกิดภูเขาไฟรูปโล่ "
                "เฝ้าระวังจากแผ่นดินไหว การโป่งของพื้นดิน และแก๊ส")


@question_type(
    "geo.eruption_style_foundation",
    display_name={"th": "รูปร่างภูเขาไฟและลักษณะแมกมา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_VOLCANO,
)
class EruptionStyleFoundation(QuestionType):
    """Shield, composite or cinder cone, from magma or example."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, magma, example = rng.choice(VOLCANOES)
        kinds = sorted({v[0] for v in VOLCANOES} - {name}) + ["ภูเขาไฟใต้ธารน้ำแข็ง"]
        others = [v for v in VOLCANOES if v[0] != name]
        roll = rng.random()
        if roll < 0.4:
            return _labelled(stem=f"ภูเขาไฟที่มีลักษณะ \"{magma}\" เป็นแบบใด", correct=name, wrongs=tuple(kinds), topic=TOPIC_VOLCANO,
                             hint=VOLCANO_HINT)
        if roll < 0.7:
            return _labelled(stem=f"{example}เป็นภูเขาไฟแบบใด", correct=name, wrongs=tuple(kinds), topic=TOPIC_VOLCANO, hint=VOLCANO_HINT)
        pool = [v[1] for v in others] + ["ไม่มีแมกมา เกิดจากการยกตัวของเปลือกโลกเท่านั้น"]
        return _labelled(stem=f"ข้อใดเป็นลักษณะของ{name}", correct=magma, wrongs=tuple(pool), topic=TOPIC_VOLCANO, hint=VOLCANO_HINT)


@question_type(
    "geo.eruption_style_fluency",
    display_name={"th": "ความรุนแรงของการปะทุ การเฝ้าระวัง และการปฏิบัติตน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_VOLCANO,
)
class EruptionStyleFluency(QuestionType):
    """What makes eruptions violent, warning signs, and safety."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(ERUPT_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_VOLCANO, hint=VOLCANO_HINT)


@question_type(
    "geo.eruption_style_application",
    display_name={"th": "วิเคราะห์ข้อมูลการเฝ้าระวังภูเขาไฟ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_VOLCANO,
)
class EruptionStyleApplication(QuestionType):
    """Ground uplift rates, and comparing magmas by silica."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            rate = rng.choice((2, 3, 4, 5, 8, 10, 12, 15))
            days = rng.choice((5, 10, 15, 20, 30))
            total = rate * days
            if rng.random() < 0.5:
                return numeric(stem=f"เครื่องวัดพบว่าพื้นดินบนภูเขาไฟโป่งขึ้น {total} mm ใน {days} วัน อัตราการโป่งตัวเฉลี่ยกี่มิลลิเมตรต่อวัน",
                               answer=rate, wrongs=[total * days, total, rate * 2], unit="mm/วัน", topic=TOPIC_VOLCANO,
                               hint="อัตรา = การเปลี่ยนแปลงทั้งหมด ÷ เวลา การโป่งตัวเร็วขึ้นบอกว่าแมกมากำลังสะสมตัว")
            return numeric(stem=f"พื้นดินบนภูเขาไฟโป่งขึ้นด้วยอัตรา {rate} mm ต่อวัน ใน {days} วันจะโป่งขึ้นกี่เซนติเมตร", answer=Fraction(total, 10),
                           wrongs=[total, rate * days * 100 // 100 * 10, rate], unit="cm", topic=TOPIC_VOLCANO,
                           hint="ระยะรวม = อัตรา × เวลา แล้วแปลงมิลลิเมตรเป็นเซนติเมตร (÷ 10)")
        silica = sorted(rng.sample(range(45, 76, 5), 3))
        names = ["แมกมา ก", "แมกมา ข", "แมกมา ค"]
        pairs = list(zip(names, silica))
        rng.shuffle(pairs)
        most = rng.random() < 0.5
        right = max(pairs, key=lambda x: x[1])[0] if most else min(pairs, key=lambda x: x[1])[0]
        listing = " ".join(f"{n} มีซิลิการ้อยละ {s}" for n, s in pairs)
        return _labelled(stem=f"{listing} แมกมาใดน่าจะทำให้ภูเขาไฟปะทุ{'รุนแรงที่สุด' if most else 'แบบลาวาไหลเรียบที่สุด'}", correct=right,
                         wrongs=(*(n for n in names if n != right), "ปะทุเหมือนกันทั้งหมด"), topic=TOPIC_VOLCANO, hint=VOLCANO_HINT)
