"""การเกิดเงามืดเงามัว

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.6/7

Sets moved here from: science_wave_d27.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d22 import _facts
from otk.sets._support.science_wave_d26 import SIXTH

PROVENANCE = Provenance("original")


SHADOW_TOPIC = "การเกิดเงามืดเงามัว"


OPAQUE = ("แผ่นไม้", "หนังสือ", "ฝ่ามือ", "กล่องกระดาษแข็ง", "แผ่นเหล็ก", "ก้อนหิน")


TRANSLUCENT = ("กระดาษไข", "กระจกฝ้า", "ถุงพลาสติกขุ่น", "ผ้าม่านบาง")


TRANSPARENT = ("กระจกใส", "แผ่นพลาสติกใส", "น้ำเปล่าในแก้วใส", "แก้วน้ำใส")


SHADOW_FACTS = (
    ("เงามืดและเงามัวต่างกันอย่างไร",
     "เงามืดคือบริเวณที่แสงจากแหล่งกำเนิดส่องไปไม่ถึงเลย ส่วนเงามัวคือบริเวณที่มีแสงบางส่วนส่องถึง",
     ("เงามืดคือบริเวณที่มีแสงส่องถึงทั้งหมด ส่วนเงามัวคือบริเวณที่ไม่มีแสงส่องถึงเลย", "เงามืดและเงามัวเป็นบริเวณเดียวกัน เพียงแต่เรียกชื่อต่างกัน",
      "เงามืดเกิดเฉพาะเวลากลางคืน ส่วนเงามัวเกิดเฉพาะเวลากลางวัน", "เงามัวมืดกว่าเงามืดเสมอ", "เงามืดเกิดจากวัตถุโปร่งใสเท่านั้น")),
    ("เงาเกิดขึ้นได้อย่างไร", "วัตถุทึบแสงกั้นแสงที่เคลื่อนที่เป็นเส้นตรงไว้ ด้านหลังวัตถุจึงไม่มีแสง",
     ("แสงเลี้ยวอ้อมวัตถุไปด้านหลัง", "วัตถุผลิตเงาออกมาเอง", "วัตถุโปร่งใสทุกชนิดทำให้เกิดเงามืด", "เงาเกิดจากเสียงที่สะท้อน", "เงาเกิดเฉพาะในที่มืดสนิท")),
    ("ถ้าเลื่อนวัตถุเข้าใกล้หลอดไฟมากขึ้น โดยฉากอยู่ที่เดิม เงาบนฉากจะเป็นอย่างไร", "เงามีขนาดใหญ่ขึ้น",
     ("เงามีขนาดเล็กลง", "เงามีขนาดเท่าเดิม", "เงาหายไป", "เงากลายเป็นสีขาว", "เงาไปอยู่ด้านหน้าหลอดไฟ")),
)


SHADOW_HINT = "วัตถุทึบแสงกั้นแสงทั้งหมดเกิดเงามืด วัตถุโปร่งแสงให้แสงผ่านบางส่วน เงาจึงจาง วัตถุโปร่งใสให้แสงผ่านเกือบทั้งหมด เงามืดจึงแทบไม่เกิด"


SHADOW_SCENARIOS = (
    ("ระหว่างเกิดสุริยุปราคาเต็มดวง ผู้สังเกตในบางพื้นที่เห็นดวงอาทิตย์มืดสนิท ส่วนพื้นที่ใกล้เคียงเห็นเพียงบางส่วนของดวงอาทิตย์ถูกบัง เหตุใดจึงเป็นเช่นนี้",
     "พื้นที่ที่เห็นมืดสนิทอยู่ในเงามืดของดวงจันทร์ ส่วนพื้นที่ใกล้เคียงอยู่ในเงามัวซึ่งได้รับแสงบางส่วนจากดวงอาทิตย์",
     ("ทุกพื้นที่ควรเห็นดวงอาทิตย์มืดสนิทเท่ากันหมด", "พื้นที่ที่เห็นบางส่วนอยู่ในเงามืดเช่นเดียวกับพื้นที่มืดสนิท", "ความแตกต่างเกิดจากสภาพอากาศเพียงอย่างเดียว ไม่เกี่ยวกับเงา")),
    ("ช่างภาพบนเวทีมักใช้ไฟหลายดวงจากหลายทิศทางแทนไฟดวงเดียว เพื่อลดความเข้มของเงาบนตัวนักแสดง เหตุใดวิธีนี้จึงได้ผล",
     "แสงจากหลายทิศทางทำให้บริเวณเงามืดเดิมได้รับแสงจากดวงอื่นแทน เงาจึงกลายเป็นเงามัวที่จางลง",
     ("ไฟหลายดวงทำให้เกิดเงามืดที่เข้มข้นขึ้นกว่าเดิม", "จำนวนดวงไฟไม่มีผลต่อความเข้มของเงาเลย", "ไฟหลายดวงทำให้วัตถุทึบแสงกลายเป็นโปร่งใส")),
    ("โคมไฟตั้งโต๊ะที่มีโป๊ะไฟขนาดใหญ่ให้เงาที่นุ่มนวลขอบไม่ชัดเจน ต่างจากหลอดไฟเปลือยขนาดเล็กที่ให้เงาคมชัด เหตุใดจึงต่างกัน",
     "โป๊ะไฟขนาดใหญ่ทำให้แหล่งกำเนิดแสงมีขนาดใหญ่ขึ้น เกิดเงามัวบริเวณขอบมากขึ้น เงาจึงนุ่มนวลกว่า",
     ("โป๊ะไฟทำให้แหล่งกำเนิดแสงกลายเป็นแหล่งกำเนิดแบบจุดมากขึ้น", "ขนาดของแหล่งกำเนิดแสงไม่เกี่ยวข้องกับความคมชัดของเงา", "เงาที่นุ่มนวลเกิดจากสีของโป๊ะไฟเพียงอย่างเดียว")),
)


ECLIPSE = {
    "เงามืด": ("สุริยุปราคาเต็มดวง ดวงอาทิตย์ถูกบังทั้งดวง", "ท้องฟ้ามืดลงเหมือนพลบค่ำชั่วครู่"),
    "เงามัว": ("สุริยุปราคาบางส่วน ดวงอาทิตย์ถูกบังเพียงบางส่วน", "ยังมีแสงแดดแต่อ่อนลง"),
    "นอกเงา": ("ไม่เห็นสุริยุปราคา ดวงอาทิตย์เต็มดวงตามปกติ", "แสงแดดปกติ"),
}


TOWNS = ("เชียงใหม่", "ขอนแก่น", "นครราชสีมา", "ชลบุรี", "สงขลา", "ภูเก็ต", "อุบลราชธานี", "พิษณุโลก")


@question_type(
    "phys.shadow_foundation",
    display_name={"th": "บอกความแตกต่างระหว่างเงามืดและเงามัว"},
    level=SIXTH, subject=SUBJECT, topic=SHADOW_TOPIC,
)
class ShadowFoundation(QuestionType):
    """Umbra and penumbra, and which materials cast a dark shadow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _labelled(stem="วัตถุใดกั้นแสงแล้วทำให้เกิดเงามืดชัดเจนที่สุด", correct=rng.choice(OPAQUE),
                             wrongs=(rng.choice(TRANSLUCENT), *rng.sample(TRANSPARENT, 2)), hint=SHADOW_HINT, topic=SHADOW_TOPIC)
        return _facts(rng, SHADOW_FACTS, hint=SHADOW_HINT, topic=SHADOW_TOPIC)


@question_type(
    "phys.shadow_fluency",
    display_name={"th": "อธิบายการเกิดเงามืดเงามัวจากหลักฐานเชิงประจักษ์"},
    level=SIXTH, subject=SUBJECT, topic=SHADOW_TOPIC,
)
class ShadowFluency(QuestionType):
    """Source size decides the penumbra; distance decides the shadow's size."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _labelled(
                stem=("นักเรียนใช้ไฟฉายขนาดเล็ก (แหล่งกำเนิดแสงเป็นจุด) ส่องผ่านวัตถุทึบแสงไปที่ฉาก พบว่ามีเพียงเงามืดเข้มบริเวณเดียว ไม่มีเงามัว "
                      "เมื่อเปลี่ยนเป็นหลอดไฟขนาดใหญ่ (แหล่งกำเนิดแสงเป็นบริเวณกว้าง) พบว่ามีทั้งเงามืดตรงกลางและเงามัวล้อมรอบ "
                      "จากผลการทดลองนี้ ข้อใดอธิบายการเกิดเงามืดเงามัวได้ถูกต้อง"),
                correct=("แหล่งกำเนิดแสงเป็นจุดทำให้เกิดเงามืดเพียงอย่างเดียว ส่วนแหล่งกำเนิดแสงขนาดใหญ่ทำให้เกิดทั้งเงามืดและเงามัว "
                         "เพราะบางบริเวณได้รับแสงจากบางส่วนของแหล่งกำเนิดเท่านั้น"),
                wrongs=("แหล่งกำเนิดแสงเป็นจุดทำให้เกิดทั้งเงามืดและเงามัว ส่วนแหล่งกำเนิดแสงขนาดใหญ่ทำให้เกิดเงามืดเพียงอย่างเดียว",
                        "ขนาดของแหล่งกำเนิดแสงไม่มีผลต่อการเกิดเงามืดเงามัวเลย",
                        "เงามัวเกิดจากวัตถุทึบแสงที่มีสีอ่อนเท่านั้น ไม่เกี่ยวกับขนาดแหล่งกำเนิดแสง"),
                hint="แหล่งกำเนิดแสงที่มีขนาดใหญ่ส่งแสงจากหลายมุม บางบริเวณหลังวัตถุจึงได้รับแสงบางส่วนเท่านั้น",
                topic=SHADOW_TOPIC,
            )
        thing = rng.choice(OPAQUE)
        base = rng.choice((10, 15, 20, 25, 30))
        distances = sorted(rng.sample(range(10, 61, 5), 3))
        sizes = [Fraction(base * 60, d) for d in distances]
        if any((s * 10).denominator != 1 for s in sizes):
            distances, sizes = [10, 20, 30], [Fraction(base * 6), Fraction(base * 3), Fraction(base * 2)]
        table = " ".join(f"ห่างหลอด {d} cm → เงากว้าง {show(s)} cm" for d, s in zip(distances, sizes))
        return _labelled(stem=f"นักเรียนวาง{thing}ระหว่างหลอดไฟกับฉาก แล้วเลื่อน{thing}ไปหลายระยะ ได้ผลดังนี้: {table} ข้อสรุปใดถูกต้อง",
                         correct=f"ยิ่งวาง{thing}ใกล้หลอดไฟ เงาบนฉากยิ่งใหญ่ขึ้น",
                         wrongs=(f"ยิ่งวาง{thing}ใกล้หลอดไฟ เงาบนฉากยิ่งเล็กลง", "ระยะห่างไม่มีผลต่อขนาดของเงา",
                                 f"เงาเกิดเฉพาะเมื่อวาง{thing}ห่างหลอดไฟมากที่สุด"),
                         hint="วัตถุที่อยู่ใกล้แหล่งกำเนิดแสงกั้นแสงเป็นมุมกว้าง เงาบนฉากจึงใหญ่", topic=SHADOW_TOPIC)


@question_type(
    "phys.shadow_application",
    display_name={"th": "ใช้ความรู้เรื่องเงามืดเงามัวอธิบายปรากฏการณ์จริง"},
    level=SIXTH, subject=SUBJECT, topic=SHADOW_TOPIC,
)
class ShadowApplication(QuestionType):
    """Authored scenes, and what a town sees from inside or outside the Moon's shadow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(
                rng, SHADOW_SCENARIOS,
                hint="แหล่งกำเนิดแสงที่มีขนาดใหญ่ขึ้นทำให้เงามัวกว้างขึ้นและขอบเงานุ่มนวลขึ้น",
            ), SHADOW_TOPIC)
        region = rng.choice(tuple(ECLIPSE))
        town = rng.choice(TOWNS)
        where = {"เงามืด": "อยู่ในเงามืดของดวงจันทร์", "เงามัว": "อยู่ในเงามัวของดวงจันทร์", "นอกเงา": "อยู่นอกเงาของดวงจันทร์"}[region]
        if rng.random() < 0.5:
            return _labelled(stem=f"ขณะเกิดสุริยุปราคา จังหวัด{town}{where} ผู้สังเกตที่นั่นจะเห็นอย่างไร", correct=ECLIPSE[region][0],
                             wrongs=tuple(v[0] for k, v in ECLIPSE.items() if k != region) + ("ดวงจันทร์เต็มดวงสว่างกลางวัน",),
                             hint="ในเงามืดไม่มีแสงจากดวงอาทิตย์ส่องถึงเลย ในเงามัวได้รับแสงบางส่วน", topic=SHADOW_TOPIC)
        return _labelled(stem=f"ขณะเกิดสุริยุปราคา ผู้สังเกตที่จังหวัด{town}เห็น{ECLIPSE[region][0]} จังหวัด{town}อยู่บริเวณใด",
                         correct=where, wrongs=tuple(w for w in ("อยู่ในเงามืดของดวงจันทร์", "อยู่ในเงามัวของดวงจันทร์", "อยู่นอกเงาของดวงจันทร์") if w != where)
                         + ("อยู่ในเงาของโลก",), hint="ในเงามืดไม่มีแสงจากดวงอาทิตย์ส่องถึงเลย ในเงามัวได้รับแสงบางส่วน", topic=SHADOW_TOPIC)
