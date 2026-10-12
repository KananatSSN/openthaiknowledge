"""เส้นทางการขึ้นตกของดวงอาทิตย์และดาวฤกษ์

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/14

Sets moved here from: science_wave_f85.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f85 import SUBJECT, TOWNS, UPPER_SIX, _clock

PROVENANCE = Provenance("original")


TOPIC_PATH = "เส้นทางการขึ้นตกของดวงอาทิตย์และดาวฤกษ์"


PATH_FACTS = (
    ("ผู้สังเกตที่เส้นศูนย์สูตรเห็นดาวขึ้นและตกอย่างไร", "ดาวขึ้นและตกตั้งฉากกับขอบฟ้า ทุกดวงอยู่เหนือขอบฟ้าครึ่งวัน",
     ("ดาวเคลื่อนเป็นวงขนานกับขอบฟ้า ไม่ขึ้นไม่ตก ทุกดวงอยู่เหนือขอบฟ้าตลอดวัน", "ดาวขึ้นทางทิศตะวันตก", "ดาวขึ้นและตกเอียงทำมุมกับขอบฟ้า ทุกดวงอยู่เหนือขอบฟ้าไม่เท่ากัน", "เห็นเฉพาะดาวในซีกฟ้าเหนือ")),
    ("ผู้สังเกตที่ขั้วโลกเหนือเห็นดาวเคลื่อนที่อย่างไร", "ดาวเคลื่อนเป็นวงขนานกับขอบฟ้า ไม่ขึ้นไม่ตก",
     ("ดาวขึ้นและตกตั้งฉากกับขอบฟ้า", "ดาวขึ้นทางทิศใต้และตกทางทิศเหนือทุกดวง", "ดาวทุกดวงเคลื่อนผ่านจุดเหนือศีรษะ แล้วตกทางทิศตะวันตก", "เห็นดาวทั้งท้องฟ้าทั้งซีกเหนือและใต้")),
    ("วันที่ดวงอาทิตย์ขึ้นตรงทิศตะวันออกพอดีคือวันใด", "วันวิษุวัต ราววันที่ 21 มีนาคม และ 23 กันยายน",
     ("วันครีษมายัน ราววันที่ 21 มิถุนายน", "วันเหมายัน ราววันที่ 22 ธันวาคม", "วันครีษมายันและวันเหมายัน ราวเดือนมิถุนายนและธันวาคม", "วันเพ็ญของทุกเดือน ราววันขึ้น 15 ค่ำ")),
    ("ในช่วงเดือนมิถุนายน ผู้สังเกตในประเทศไทยเห็นดวงอาทิตย์ขึ้นทางใด", "ค่อนไปทางทิศตะวันออกเฉียงเหนือ",
     ("ค่อนไปทางทิศตะวันออกเฉียงใต้", "ตรงทิศตะวันออกพอดี", "ทางทิศตะวันตกเฉียงเหนือ", "ทางทิศเหนือ ตรงกับตำแหน่งของดาวเหนือ")),
    ("ในช่วงเดือนธันวาคม ผู้สังเกตในประเทศไทยเห็นดวงอาทิตย์ขึ้นทางใด", "ค่อนไปทางทิศตะวันออกเฉียงใต้",
     ("ค่อนไปทางทิศตะวันออกเฉียงเหนือ", "ตรงทิศตะวันออกพอดี", "ทางทิศตะวันตกเฉียงเหนือ", "ค่อนไปทางทิศตะวันตกเฉียงใต้")),
    ("เหตุใดดาวฤกษ์ขึ้นเร็วขึ้นวันละประมาณ 4 นาที", "โลกโคจรรอบดวงอาทิตย์ วันดาราคติจึงสั้นกว่าวันสุริยคติประมาณ 4 นาที",
     ("ดาวเคลื่อนเข้าใกล้โลกทุกวัน", "โลกหมุนรอบตัวเองช้าลงวันละประมาณ 4 นาที ดาวจึงขึ้นเร็วขึ้นทุกวัน", "ดวงจันทร์ดึงดาวให้ขึ้นเร็ว", "ดาวฤกษ์เคลื่อนที่รอบโลกเร็วกว่าดวงอาทิตย์วันละประมาณ 4 นาที")),
    ("เหตุใดผู้สังเกตในประเทศไทยจึงไม่เห็นดาวเหนือเป็นดาวค้างฟ้าสูงเหนือศีรษะ แต่เห็นอยู่ต่ำใกล้ขอบฟ้าทิศเหนือ", "ประเทศไทยอยู่ละติจูดต่ำ มุมเงยของขั้วฟ้าเหนือจึงน้อย",
     ("ดาวเหนืออยู่ไกลจากโลกมาก แสงจึงอ่อนจนมองเห็นได้ต่ำ", "ประเทศไทยอยู่ใกล้ขั้วโลกเหนือ มุมเงยของขั้วฟ้าเหนือจึงน้อย", "ดาวเหนือเคลื่อนที่ไปทางใต้ทุกปี", "บรรยากาศประเทศไทยหนากว่าที่อื่น")),
    ("ดาวที่อยู่บนเส้นศูนย์สูตรฟ้าขึ้นและตกที่ทิศใด", "ขึ้นทิศตะวันออกพอดีและตกทิศตะวันตกพอดี",
     ("ขึ้นทิศตะวันออกเฉียงเหนือและตกทิศตะวันตกเฉียงเหนือ", "ขึ้นทิศตะวันออกเฉียงเหนือเสมอ", "ขึ้นทิศตะวันออกเฉียงใต้และตกทิศตะวันตกเฉียงใต้", "ขึ้นทิศตะวันตกและตกทิศตะวันออก")),
)


PATH_HINT = ("ดาวขึ้นทางตะวันออกตกทางตะวันตก เส้นทางเอียงทำมุม 90° − ละติจูดกับขอบฟ้า ที่ศูนย์สูตรตั้งฉาก ที่ขั้วโลกขนานขอบฟ้า "
             "ดาวค้างฟ้าในซีกเหนือมีเดคลิเนชันมากกว่า 90° − ละติจูด ดาวที่เดคลิเนชันต่ำกว่า −(90° − ละติจูด) ไม่ขึ้นเลย "
             "ดาวขึ้นเร็วขึ้นวันละ 4 นาที (เดือนละ 2 ชั่วโมง)")


@question_type(
    "astro.star_path_foundation",
    display_name={"th": "เส้นทางการขึ้นตกของดาวที่ละติจูดต่าง ๆ และของดวงอาทิตย์ตามฤดู"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PATH,
)
class StarPathFoundation(QuestionType):
    """Equator and pole paths; sunrise points through the year; four minutes a day."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(PATH_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_PATH, hint=PATH_HINT)


@question_type(
    "astro.star_path_fluency",
    display_name={"th": "จำแนกดาวค้างฟ้า ดาวขึ้นตก และดาวที่ไม่ขึ้นเหนือขอบฟ้า"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PATH,
)
class StarPathFluency(QuestionType):
    """Circumpolar, rising and setting, or never rising, from δ and φ."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        lat = rng.choice((0, 6, 14, 19, 30, 40, 50, 60, 70))
        limit = 90 - lat
        dec = rng.choice([d for d in range(-89, 90) if abs(d) != limit])
        right = ("เป็นดาวค้างฟ้า อยู่เหนือขอบฟ้าตลอดเวลา" if dec > limit else "ไม่ขึ้นเหนือขอบฟ้าเลย มองไม่เห็นตลอดทั้งปี" if dec < -limit
                 else "ขึ้นและตกทุกวัน เห็นได้เพียงบางช่วงของคืน")
        return _labelled(stem=f"ผู้สังเกตที่ละติจูด {lat}° เหนือ เห็นดาวที่มีเดคลิเนชัน {dec:+d}° เป็นอย่างไร",
                         correct=right, wrongs=tuple(o for o in ("เป็นดาวค้างฟ้า อยู่เหนือขอบฟ้าตลอดเวลา", "ไม่ขึ้นเหนือขอบฟ้าเลย มองไม่เห็นตลอดทั้งปี",
                                                                 "ขึ้นและตกทุกวัน เห็นได้เพียงบางช่วงของคืน", "ขึ้นทางทิศตะวันตกและตกทางทิศตะวันออก") if o != right),
                         topic=TOPIC_PATH, hint=PATH_HINT)


@question_type(
    "astro.star_path_application",
    display_name={"th": "คำนวณมุมเส้นทางดาว ขอบเขตดาวค้างฟ้า และเวลาขึ้นที่เปลี่ยนไป"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PATH,
)
class StarPathApplication(QuestionType):
    """Path angle 90 − φ; circumpolar limit; four minutes earlier each day."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        town, lat = rng.choice(TOWNS)
        if roll < 0.3:
            return numeric(stem=f"ที่{town} (ละติจูดประมาณ {lat}° เหนือ) เส้นทางขึ้นของดาวทำมุมกับขอบฟ้ากี่องศา", answer=90 - lat,
                           wrongs=[lat, 90, 90 - lat + 10], unit="องศา", topic=TOPIC_PATH, hint="มุมของเส้นทางกับขอบฟ้า = 90° − ละติจูด")
        if roll < 0.55:
            return numeric(stem=f"ที่{town} (ละติจูดประมาณ {lat}° เหนือ) ดาวในซีกฟ้าเหนือต้องมีเดคลิเนชันมากกว่ากี่องศาจึงเป็นดาวค้างฟ้า",
                           answer=90 - lat, wrongs=[lat, 90, 90 - lat + 5], unit="องศา", topic=TOPIC_PATH, hint="ขอบเขตดาวค้างฟ้า = 90° − ละติจูด")
        days = rng.randint(2, 60)
        start = rng.randrange(18 * 60, 23 * 60 + 1, 5)
        if rng.random() < 0.5:
            return numeric(stem=f"ดาวดวงหนึ่งขึ้นเร็วขึ้นวันละประมาณ 4 นาที ผ่านไป {days} วัน ดาวจะขึ้นเร็วกว่าเดิมกี่นาที", answer=4 * days,
                           wrongs=[days, 2 * days, 4 * days + 60], unit="นาที", topic=TOPIC_PATH, hint="เวลาที่เร็วขึ้น = 4 นาที × จำนวนวัน")
        days = rng.choice((15, 30, 45, 60, 90))
        right = _clock(start - 4 * days)
        return _labelled(stem=f"วันนี้ดาวดวงหนึ่งขึ้นเวลา {_clock(start)} ถ้าขึ้นเร็วขึ้นวันละ 4 นาที อีก {days} วันจะขึ้นเวลาใด", correct=right,
                         wrongs=(_clock(start + 4 * days), _clock(start - 2 * days), _clock(start - 4 * days - 60)), topic=TOPIC_PATH,
                         hint="เวลาใหม่ = เวลาเดิม − 4 นาที × จำนวนวัน")
