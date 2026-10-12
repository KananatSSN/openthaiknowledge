"""การหมุนเวียนของน้ำในมหาสมุทร

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/6

Sets moved here from: science_wave_f79.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f79 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_CURRENT = "การหมุนเวียนของน้ำในมหาสมุทร"


CURRENT_FACTS = (
    ("กระแสน้ำผิวหน้าในมหาสมุทรเกิดจากปัจจัยใดเป็นหลัก", "ลมประจำที่พัดผ่านผิวน้ำ",
     ("ความแตกต่างของความหนาแน่นที่ก้นมหาสมุทร", "แผ่นดินไหวใต้ทะเล", "ภูเขาไฟใต้ทะเล", "สิ่งมีชีวิตในทะเลว่ายน้ำ")),
    ("กระแสน้ำลึกในมหาสมุทรเกิดจากปัจจัยใดเป็นหลัก", "ความแตกต่างของความหนาแน่นจากอุณหภูมิและความเค็ม",
     ("ลมประจำที่พัดผ่านผิวน้ำ", "คลื่นที่ซัดเข้าฝั่ง", "ลมประจำที่พัดผ่านผิวน้ำอย่างต่อเนื่องตลอดทั้งปี", "น้ำขึ้นน้ำลงรายวันที่เกิดจากแรงดึงของดวงจันทร์")),
    ("น้ำผุด (upwelling) คืออะไร", "น้ำเย็นจากด้านล่างเคลื่อนขึ้นมาแทนที่น้ำผิวหน้าที่ถูกลมพัดออกไป",
     ("น้ำผิวหน้าถูกลมพัดเข้าหาฝั่งแล้วจมลง", "น้ำจืดจากแม่น้ำไหลลงทะเล", "น้ำจืดจากแม่น้ำไหลลงทะเลแล้วดันน้ำเค็มขึ้นมา", "น้ำผิวหน้าถูกลมพัดเข้าหาฝั่งแล้วจมตัวลงด้านล่าง")),
    ("น้ำจม (downwelling) คืออะไร", "น้ำผิวหน้าถูกลมพัดเข้าหาฝั่งแล้วจมตัวลงด้านล่าง",
     ("น้ำเย็นจากด้านล่างเคลื่อนขึ้นมาแทนที่", "น้ำแข็งละลายเป็นน้ำจืดแล้วจมลงก้นทะเล", "น้ำทะเลระเหยจนเค็มขึ้น", "น้ำเย็นจากด้านล่างเคลื่อนขึ้นมาแทนที่ผิวน้ำ")),
    ("การหมุนเวียนของน้ำแบบเทอร์โมฮาไลน์เริ่มต้นจากบริเวณใด", "น้ำทะเลใกล้ขั้วโลกที่เย็นและเค็มจัดจมตัวลง",
     ("น้ำอุ่นที่เส้นศูนย์สูตรจมตัวลง", "น้ำจืดจากแม่น้ำจมลงก้นทะเล", "น้ำอุ่นที่เส้นศูนย์สูตรจมตัวลงเพราะเค็มจัด", "น้ำในทะเลสาบไหลลงมหาสมุทร")),
    ("ปัจจัยใดทำให้กระแสน้ำผิวหน้าในมหาสมุทรหมุนเป็นวงวน", "แรงคอริออลิสและแนวขอบทวีปที่กั้นการไหล",
     ("แรงโน้มถ่วงของดวงอาทิตย์เพียงอย่างเดียว", "ความลึกของมหาสมุทรที่เท่ากันทุกแห่ง", "แผ่นดินไหวใต้ทะเล", "ปะการังที่ขวางทางน้ำ")),
    ("กระแสน้ำผิวหน้าที่ไหลจากเขตร้อนไปทางขั้วโลกเป็นกระแสน้ำชนิดใด", "กระแสน้ำอุ่น",
     ("กระแสน้ำเย็น", "กระแสน้ำลึก", "น้ำผุด", "น้ำจม")),
    ("เหตุใดน้ำผิวหน้าจึงไม่ไหลไปตามทิศลมตรง ๆ แต่เบนออกไป", "แรงคอริออลิสจากการหมุนรอบตัวเองของโลก",
     ("แรงโน้มถ่วงของดวงจันทร์", "ความเค็มของน้ำผิวหน้า", "แรงโน้มถ่วงของดวงจันทร์ที่ดึงน้ำ", "คลื่นที่ซัดเข้าฝั่ง")),
    ("การหมุนเวียนของน้ำทั่วโลกแบบสายพานลำเลียงมหาสมุทรมีบทบาทอย่างไร", "ลำเลียงความร้อนและสารต่าง ๆ ระหว่างมหาสมุทรทั่วโลก",
     ("ทำให้น้ำทะเลทุกแห่งมีอุณหภูมิเท่ากัน", "ทำให้น้ำทะเลทุกแห่งมีอุณหภูมิและความเค็มเท่ากัน", "ทำให้เกิดน้ำขึ้นน้ำลงวันละสองครั้งทั่วโลก", "ทำให้น้ำขึ้นน้ำลงวันละสองครั้ง")),
)


CURRENT_HINT = ("กระแสน้ำผิวหน้าเกิดจากลมประจำ เบนด้วยแรงคอริออลิสและถูกทวีปกั้น จึงหมุนเป็นวงวน ตามเข็มนาฬิกาในซีกโลกเหนือ "
                "ทวนเข็มนาฬิกาในซีกโลกใต้ กระแสน้ำลึกเกิดจากน้ำเย็นและเค็มที่หนาแน่นจมตัวลง")


CURRENTS = (
    ("กระแสน้ำกัลฟ์สตรีม", "อุ่น"), ("กระแสน้ำคุโรชิโอ", "อุ่น"), ("กระแสน้ำบราซิล", "อุ่น"), ("กระแสน้ำออสเตรเลียตะวันออก", "อุ่น"),
    ("กระแสน้ำแอตแลนติกเหนือ", "อุ่น"), ("กระแสน้ำอะกุลฮัส", "อุ่น"),
    ("กระแสน้ำแคลิฟอร์เนีย", "เย็น"), ("กระแสน้ำฮัมโบลต์ (เปรู)", "เย็น"), ("กระแสน้ำเบงเกวลา", "เย็น"), ("กระแสน้ำคานารี", "เย็น"),
    ("กระแสน้ำลาบราดอร์", "เย็น"), ("กระแสน้ำโอยาชิโอ", "เย็น"), ("กระแสน้ำออสเตรเลียตะวันตก", "เย็น"),
)


DIRS = ("ทิศเหนือ", "ทิศตะวันออก", "ทิศใต้", "ทิศตะวันตก")


@question_type(
    "geo.ocean_current_foundation",
    display_name={"th": "ปัจจัยที่ทำให้เกิดการหมุนเวียนของน้ำในมหาสมุทร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CURRENT,
)
class OceanCurrentFoundation(QuestionType):
    """Wind, density, Coriolis, upwelling and downwelling."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(CURRENT_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_CURRENT, hint=CURRENT_HINT)


@question_type(
    "geo.ocean_current_fluency",
    display_name={"th": "กระแสน้ำอุ่น กระแสน้ำเย็น และทิศการหมุนของวงวน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CURRENT,
)
class OceanCurrentFluency(QuestionType):
    """Warm or cold by name and by coast; gyre sense by hemisphere."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            kind = rng.choice(("อุ่น", "เย็น"))
            right = rng.choice([n for n, k in CURRENTS if k == kind])
            wrongs = rng.sample([n for n, k in CURRENTS if k != kind], 3)
            return _labelled(stem=f"ข้อใดเป็นกระแสน้ำ{kind}", correct=right, wrongs=tuple(wrongs), topic=TOPIC_CURRENT,
                             hint=CURRENT_HINT + " กระแสน้ำที่ไหลจากเขตร้อนไปทางขั้วโลกเป็นกระแสน้ำอุ่น ที่ไหลจากขั้วโลกมาทางเส้นศูนย์สูตรเป็นกระแสน้ำเย็น")
        if roll < 0.7:
            north = rng.random() < 0.5
            ocean = rng.choice(("มหาสมุทรแปซิฟิก", "มหาสมุทรแอตแลนติก") + (("มหาสมุทรอินเดีย",) if not north else ()))
            right = "ตามเข็มนาฬิกา" if north else "ทวนเข็มนาฬิกา"
            return _labelled(stem=f"วงวนกระแสน้ำผิวหน้าใน{ocean}{'เหนือ' if north else 'ใต้'}หมุนไปทางใด", correct=right,
                             wrongs=("ทวนเข็มนาฬิกา" if north else "ตามเข็มนาฬิกา", "ไม่หมุน ไหลตรงจากเหนือลงใต้", "เปลี่ยนทิศทุกวันตามน้ำขึ้นน้ำลง"),
                             topic=TOPIC_CURRENT, hint=CURRENT_HINT)
        west_coast = rng.random() < 0.5
        continent = rng.choice(("ทวีปอเมริกาเหนือ", "ทวีปอเมริกาใต้", "ทวีปแอฟริกา", "ทวีปออสเตรเลีย"))
        right = "กระแสน้ำเย็นไหลจากขั้วโลกมาทางเส้นศูนย์สูตร" if west_coast else "กระแสน้ำอุ่นไหลจากเขตร้อนไปทางขั้วโลก"
        other = "กระแสน้ำอุ่นไหลจากเขตร้อนไปทางขั้วโลก" if west_coast else "กระแสน้ำเย็นไหลจากขั้วโลกมาทางเส้นศูนย์สูตร"
        return _labelled(stem=f"ชายฝั่งด้าน{'ตะวันตก' if west_coast else 'ตะวันออก'}ของ{continent}ในเขตละติจูดกลางค่อนมาทางเขตร้อน มักมีกระแสน้ำแบบใดไหลเลียบฝั่ง",
                         correct=right, wrongs=(other, "กระแสน้ำเย็นไหลจากเขตร้อนไปทางขั้วโลก", "กระแสน้ำอุ่นไหลจากขั้วโลกมาทางเส้นศูนย์สูตร"),
                         topic=TOPIC_CURRENT, hint=CURRENT_HINT + " ด้านตะวันตกของมหาสมุทร (ฝั่งตะวันออกของทวีป) มีกระแสน้ำอุ่น "
                                                                   "ด้านตะวันออกของมหาสมุทร (ฝั่งตะวันตกของทวีป) มีกระแสน้ำเย็น")


@question_type(
    "geo.ocean_current_application",
    display_name={"th": "ทำนายน้ำผุดน้ำจมและคำนวณการเคลื่อนที่ตามกระแสน้ำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CURRENT,
)
class OceanCurrentApplication(QuestionType):
    """Ekman transport 90° from the wind decides upwelling; drift distance and time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            north = rng.random() < 0.5
            land = rng.randrange(4)
            heading = rng.choice(((land + 1) % 4, (land + 3) % 4))
            transport = (heading + 1) % 4 if north else (heading + 3) % 4
            up = transport == (land + 2) % 4
            right = ("เกิดน้ำผุด เพราะน้ำผิวหน้าถูกพัดออกจากฝั่ง" if up else "เกิดน้ำจม เพราะน้ำผิวหน้าถูกพัดเข้าหาฝั่ง")
            return _labelled(stem=f"ชายฝั่งแห่งหนึ่งในซีกโลก{'เหนือ' if north else 'ใต้'}มีแผ่นดินอยู่ทาง{DIRS[land]}ของทะเล ลมพัดขนานฝั่งไปทาง{DIRS[heading]} "
                                  f"น้ำผิวหน้าโดยรวมเคลื่อนเบนไป 90° จากทิศลม (ขวาในซีกโลกเหนือ ซ้ายในซีกโลกใต้) บริเวณชายฝั่งนี้จะเกิดอะไร",
                             correct=right,
                             wrongs=("เกิดน้ำจม เพราะน้ำผิวหน้าถูกพัดเข้าหาฝั่ง" if up else "เกิดน้ำผุด เพราะน้ำผิวหน้าถูกพัดออกจากฝั่ง",
                                     "เกิดน้ำผุด เพราะน้ำผิวหน้าถูกพัดเข้าหาฝั่ง", "เกิดน้ำจม เพราะน้ำผิวหน้าถูกพัดออกจากฝั่ง"),
                             topic=TOPIC_CURRENT, hint="หาทิศที่น้ำผิวหน้าเคลื่อน ถ้าออกจากฝั่ง น้ำเย็นด้านล่างผุดขึ้นมาแทน ถ้าเข้าหาฝั่ง น้ำจะจมตัวลง")
        speed = rng.choice((12, 15, 20, 24, 25, 30, 36, 40, 45, 50, 60, 75, 80))
        days = rng.randint(3, 40)
        what = rng.choice(("ขวดพลาสติก", "ทุ่นวัดกระแสน้ำ", "ซากเรือ", "แพสาหร่าย"))
        if rng.random() < 0.5:
            return numeric(stem=f"{what}ลอยไปตามกระแสน้ำด้วยอัตราเร็วเฉลี่ย {speed} km ต่อวัน ในเวลา {days} วัน จะเคลื่อนที่ได้กี่ km",
                           answer=speed * days, wrongs=[speed + days, speed * (days + 1), Fraction(speed * days, 24) if (Fraction(speed * days, 24) * 100).denominator == 1 else speed * days * 2],
                           unit="km", topic=TOPIC_CURRENT, hint="ระยะทาง = อัตราเร็ว × เวลา")
        return numeric(stem=f"{what}ลอยไปตามกระแสน้ำด้วยอัตราเร็วเฉลี่ย {speed} km ต่อวัน ต้องใช้เวลากี่วันจึงเคลื่อนที่ได้ {show(speed * days)} km",
                       answer=days, wrongs=[days * 2, days + 5, speed], unit="วัน", topic=TOPIC_CURRENT, hint="เวลา = ระยะทาง ÷ อัตราเร็ว")
