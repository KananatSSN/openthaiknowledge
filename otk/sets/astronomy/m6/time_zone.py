"""เวลาสุริยคติปานกลางและเขตเวลา

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/16

Sets moved here from: science_wave_f85.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f85 import SUBJECT, UPPER_SIX, _clock

PROVENANCE = Provenance("original")


TOPIC_ZONE = "เวลาสุริยคติปานกลางและเขตเวลา"


ZONE_FACTS = (
    ("เวลาสุริยคติปานกลางต่างจากเวลาสุริยคติปรากฏอย่างไร", "ใช้ดวงอาทิตย์สมมติที่เคลื่อนที่สม่ำเสมอ ทุกวันยาว 24 ชั่วโมงเท่ากัน",
     ("ใช้ดวงอาทิตย์จริง ความยาววันไม่เท่ากัน", "ใช้ดวงจันทร์เป็นหลัก ทุกวันจึงยาวกว่า 24 ชั่วโมงประมาณ 50 นาที", "ใช้ดาวฤกษ์เป็นหลัก ทุกวันจึงสั้นกว่า 24 ชั่วโมงประมาณ 4 นาที", "ไม่มีความแตกต่างกันเลย")),
    ("เขตเวลาหนึ่งเขตกว้างกี่องศาลองจิจูดโดยประมาณ", "15 องศา", ("1 องศา", "4 องศา", "24 องศา", "30 องศา")),
    ("เวลามาตรฐานของประเทศไทยอ้างอิงลองจิจูดใด", "105° ตะวันออก เร็วกว่าเวลาสากล 7 ชั่วโมง",
     ("100° ตะวันออก เร็วกว่าเวลาสากล 7 ชั่วโมง", "0° เท่ากับเวลาสากล", "120° ตะวันออก เร็วกว่าเวลาสากล 8 ชั่วโมง", "105° ตะวันตก ช้ากว่าเวลาสากล 7 ชั่วโมง")),
    ("เมื่อเดินทางข้ามเส้นวันสากลจากทิศตะวันตกไปทิศตะวันออก ต้องปรับวันที่อย่างไร", "ลดวันที่ลง 1 วัน",
     ("เพิ่มวันที่ขึ้น 1 วัน", "ไม่ต้องปรับวันที่", "เพิ่มวันที่ขึ้น 2 วัน", "ปรับเฉพาะเวลา 1 ชั่วโมง")),
    ("ลองจิจูดต่างกัน 1 องศา เวลาสุริยคติปานกลางท้องถิ่นต่างกันเท่าใด", "4 นาที", ("1 นาที", "15 นาที", "1 ชั่วโมง", "24 นาที")),
    ("เหตุใดจึงต้องกำหนดเขตเวลามาตรฐานแทนการใช้เวลาท้องถิ่นของแต่ละเมือง", "ให้คนในพื้นที่เดียวกันใช้เวลาเดียวกัน สะดวกต่อการเดินทางและการสื่อสาร",
     ("เพื่อให้ดวงอาทิตย์ผ่านเมริเดียนตรง 12:00 น. ทุกเมือง", "เพราะโลกหมุนไม่สม่ำเสมอ จึงต้องแบ่งเขตเวลาเพื่อแก้ความคลาดเคลื่อน", "เพื่อให้ทุกเมืองมีกลางวันยาวเท่ากลางคืนตลอดปี และเดินทางได้สะดวก", "เพราะแต่ละเมืองมีดวงอาทิตย์คนละดวง")),
    ("เวลาสากลเชิงพิกัด (UTC) อ้างอิงเส้นลองจิจูดใด", "เส้นลองจิจูด 0° ที่ผ่านกรีนิช ประเทศอังกฤษ",
     ("เส้นลองจิจูด 105° ตะวันออก", "เส้นลองจิจูด 180° ที่ผ่านมหาสมุทรแปซิฟิก", "เส้นศูนย์สูตรที่แบ่งโลกเป็นซีกเหนือและใต้", "เส้นลองจิจูด 90° ตะวันตก")),
)


ZONE_HINT = ("โลกหมุน 360° ใน 24 ชั่วโมง จึง 15° ต่อชั่วโมง และ 1° ต่อ 4 นาที เขตเวลาแบ่งทุก 15° ประเทศไทยใช้ UTC+7 (105° ตะวันออก) "
             "ที่ทางตะวันออกของเส้นอ้างอิงเวลาท้องถิ่นเร็วกว่า ทางตะวันตกช้ากว่า")


CITIES = (("โตเกียว", 9), ("ปักกิ่ง", 8), ("สิงคโปร์", 8), ("นิวเดลี", Fraction(11, 2)), ("ดูไบ", 4), ("ลอนดอน", 0), ("ปารีส", 1),
          ("นิวยอร์ก", -5), ("ซิดนีย์", 10), ("โซล", 9))


@question_type(
    "astro.time_zone_foundation",
    display_name={"th": "เวลาสุริยคติปานกลาง เขตเวลา และเส้นวันสากล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ZONE,
)
class TimeZoneFoundation(QuestionType):
    """Mean vs apparent time, zones of 15°, Thailand's UTC+7, the date line."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(ZONE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ZONE, hint=ZONE_HINT)


@question_type(
    "astro.time_zone_fluency",
    display_name={"th": "เปรียบเทียบเวลาของแต่ละเขตเวลา"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ZONE,
)
class TimeZoneFluency(QuestionType):
    """Thai time to another city's time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        city, offset = rng.choice(CITIES)
        thai = rng.randrange(6 * 60, 22 * 60 + 1, 30)
        shift = int((Fraction(offset) - 7) * 60)
        right = _clock(thai + shift)
        label = f"UTC{'+' if offset >= 0 else '−'}{abs(Fraction(offset)).numerator if Fraction(offset).denominator == 1 else '5:30'}"
        candidates = [thai - shift, thai + shift + 60, thai + int(Fraction(offset) * 60), thai + shift - 60, thai + 7 * 60, thai - 7 * 60]
        wrongs = []
        for c in candidates:
            if _clock(c) != right and _clock(c) not in wrongs:
                wrongs.append(_clock(c))
        return _labelled(stem=f"เวลาในประเทศไทย (UTC+7) เป็น {_clock(thai)} เวลาที่{city} ({label}) เป็นเท่าใด", correct=right,
                         wrongs=tuple(wrongs[:3]),
                         topic=TOPIC_ZONE, hint="ผลต่างเวลา = (เขตเวลาของเมืองนั้น − 7) ชั่วโมง")


@question_type(
    "astro.time_zone_application",
    display_name={"th": "คำนวณเวลาท้องถิ่นจากลองจิจูด"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ZONE,
)
class TimeZoneApplication(QuestionType):
    """Four minutes per degree from 105° E; zone from longitude."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            lon = rng.randint(97, 104)
            place = rng.choice(("อำเภอหนึ่ง", "สถานีวิจัยแห่งหนึ่ง", "หมู่บ้านแห่งหนึ่ง", "โรงเรียนแห่งหนึ่ง"))
            return numeric(stem=f"{place}ในประเทศไทยอยู่ที่ลองจิจูด {lon}° ตะวันออก เวลาสุริยคติปานกลางท้องถิ่นช้ากว่าเวลามาตรฐานประเทศไทย (105° ตะวันออก) กี่นาที",
                           answer=(105 - lon) * 4, wrongs=[105 - lon, (105 - lon) * 15, (105 - lon) * 4 + 60], unit="นาที", topic=TOPIC_ZONE,
                           hint="ผลต่าง = (105 − ลองจิจูด) × 4 นาที")
        if roll < 0.7:
            a, b = rng.sample(range(0, 181, 5), 2)
            return numeric(stem=f"สถานที่ ก อยู่ลองจิจูด {a}° ตะวันออก สถานที่ ข อยู่ลองจิจูด {b}° ตะวันออก เวลาสุริยคติปานกลางท้องถิ่นต่างกันกี่นาที",
                           answer=abs(a - b) * 4, wrongs=[abs(a - b), abs(a - b) * 15, abs(a - b) * 4 + 60], unit="นาที", topic=TOPIC_ZONE,
                           hint="ผลต่างเวลา = ผลต่างลองจิจูด × 4 นาที")
        zone = rng.randint(1, 12)
        return numeric(stem=f"เส้นลองจิจูดอ้างอิงของเขตเวลาหนึ่งอยู่ที่ {zone * 15}° ตะวันออก เวลามาตรฐานของเขตนี้เร็วกว่าเวลาสากลกี่ชั่วโมง",
                       answer=zone, wrongs=[zone * 15, zone + 7 if zone != 7 else 14, zone * 4], unit="ชั่วโมง", topic=TOPIC_ZONE,
                       hint="จำนวนชั่วโมง = ลองจิจูด ÷ 15")
