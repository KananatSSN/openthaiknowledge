"""ผลิตภัณฑ์จากปิโตรเลียมและถ่านหิน

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/11

Sets moved here from: science_wave_f77.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f77 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_PRODUCT = "ผลิตภัณฑ์จากปิโตรเลียมและถ่านหิน"


FRACTIONS = (
    ("แก๊สปิโตรเลียมเหลว (LPG)", "ใช้เป็นแก๊สหุงต้มและเชื้อเพลิงรถยนต์"),
    ("แก๊สโซลีน (น้ำมันเบนซิน)", "ใช้เป็นเชื้อเพลิงเครื่องยนต์เบนซิน"),
    ("น้ำมันก๊าด", "ใช้เป็นเชื้อเพลิงเครื่องบินไอพ่นและตะเกียง"),
    ("น้ำมันดีเซล", "ใช้เป็นเชื้อเพลิงเครื่องยนต์ดีเซล"),
    ("น้ำมันเตา", "ใช้เป็นเชื้อเพลิงเตาเผาในโรงงานและเรือขนาดใหญ่"),
    ("น้ำมันหล่อลื่น", "ใช้หล่อลื่นเครื่องจักรลดการสึกหรอ"),
    ("ยางมะตอย", "ใช้ราดถนนและกันซึม"),
)


PRODUCT_HINT = ("กลั่นลำดับส่วนแยกน้ำมันดิบตามจุดเดือด: LPG จุดเดือดต่ำสุด → แก๊สโซลีน → น้ำมันก๊าด → ดีเซล → น้ำมันเตา → "
                "น้ำมันหล่อลื่น → ยางมะตอยจุดเดือดสูงสุด โมเลกุลยิ่งใหญ่จุดเดือดยิ่งสูง")


@question_type(
    "geo.fossil_product_foundation",
    display_name={"th": "ผลิตภัณฑ์จากการกลั่นน้ำมันดิบและการใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PRODUCT,
)
class FossilProductFoundation(QuestionType):
    """Each fraction and its use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, use = rng.choice(FRACTIONS)
        others = rng.sample([f for f in FRACTIONS if f[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}ใช้ประโยชน์อย่างไร", correct=use, wrongs=tuple(f[1] for f in others), topic=TOPIC_PRODUCT, hint=PRODUCT_HINT)
        return _labelled(stem=f"ผลิตภัณฑ์ใด{use}", correct=name, wrongs=tuple(f[0] for f in others), topic=TOPIC_PRODUCT, hint=PRODUCT_HINT)


@question_type(
    "geo.fossil_product_fluency",
    display_name={"th": "จุดเดือดของผลิตภัณฑ์ปิโตรเลียมและการใช้อย่างเหมาะสม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PRODUCT,
)
class FossilProductFluency(QuestionType):
    """Which fraction boils higher, and wise use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            picks = sorted(rng.sample(range(len(FRACTIONS)), 4))
            high = rng.random() < 0.5
            right = FRACTIONS[picks[-1]][0] if high else FRACTIONS[picks[0]][0]
            return _labelled(stem=f"ผลิตภัณฑ์ใดต่อไปนี้มีจุดเดือด{'สูงที่สุด' if high else 'ต่ำที่สุด'}", correct=right,
                             wrongs=tuple(FRACTIONS[i][0] for i in picks if FRACTIONS[i][0] != right), topic=TOPIC_PRODUCT, hint=PRODUCT_HINT)
        facts = (("การใช้ผลิตภัณฑ์ปิโตรเลียมอย่างเหมาะสมคือข้อใด", "ใช้รถสาธารณะหรือรถร่วมกันและดูแลเครื่องยนต์ให้เผาไหม้สมบูรณ์",
                  ("ติดเครื่องยนต์ทิ้งไว้นาน ๆ ให้เครื่องอุ่นก่อนออกรถทุกครั้ง", "ใช้เชื้อเพลิงผิดประเภทกับเครื่องยนต์", "เติมน้ำมันเกินความจุถัง", "ขับรถด้วยความเร็วสูงตลอดเวลาเพื่อให้ถึงที่หมายเร็วและประหยัดน้ำมัน")),
                 ("ก๊าซธรรมชาติส่วนใหญ่ในประเทศไทยใช้ทำอะไรมากที่สุด", "ใช้เป็นเชื้อเพลิงผลิตไฟฟ้า", ("ทำยางมะตอยราดถนน", "กลั่นเป็นน้ำมันหล่อลื่น", "ผลิตปุ๋ยเท่านั้น", "ทำเทียนไขและพาราฟิน")),
                 ("ถ่านหินลิกไนต์ในไทยใช้ประโยชน์หลักด้านใด", "เป็นเชื้อเพลิงผลิตไฟฟ้าและในอุตสาหกรรมปูนซีเมนต์",
                  ("ใช้ทำเครื่องประดับ", "ใช้เป็นแก๊สหุงต้มในครัวเรือนแทนแก๊สปิโตรเลียมเหลว", "ใช้ราดถนน", "ใช้กลั่นเป็นน้ำมันเครื่องบินและน้ำมันเบนซิน")),
                 ("การเผาเชื้อเพลิงซากดึกดำบรรพ์มากเกินไปส่งผลอย่างไร", "เพิ่มแก๊สเรือนกระจกและมลพิษทางอากาศ",
                  ("ทำให้ชั้นโอโซนหนาขึ้นและกรองรังสีได้ดีขึ้น", "ลดแก๊สเรือนกระจกเพราะคาร์บอนถูกเผาหมด", "เพิ่มปริมาณน้ำใต้ดิน", "ไม่มีผลต่อสิ่งแวดล้อม")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_PRODUCT, hint=PRODUCT_HINT)


@question_type(
    "geo.fossil_product_application",
    display_name={"th": "คำนวณการใช้เชื้อเพลิงอย่างประหยัด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PRODUCT,
)
class FossilProductApplication(QuestionType):
    """Fuel used and money spent over a distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rate = rng.choice((10, 12, 15, 16, 20, 25))  # km per litre
        litres = rng.randint(5, 60)
        distance = rate * litres
        price = Fraction(rng.randrange(300, 451, 5), 10)
        if rng.random() < 0.5:
            return numeric(stem=f"รถคันหนึ่งใช้น้ำมันได้ {rate} km ต่อลิตร เดินทาง {distance:,} km ต้องใช้น้ำมันกี่ลิตร", answer=litres,
                           wrongs=[distance * rate, Fraction(rate, 1) + litres, litres * 2], unit="ลิตร", topic=TOPIC_PRODUCT,
                           hint="ปริมาณน้ำมัน = ระยะทาง ÷ ระยะทางต่อลิตร")
        return numeric(stem=f"รถใช้น้ำมันได้ {rate} km ต่อลิตร เดินทาง {distance:,} km น้ำมันราคาลิตรละ {show(price)} บาท ค่าน้ำมันเป็นกี่บาท",
                       answer=price * litres, wrongs=[price * distance, price * rate, price * litres * 2], unit="บาท", topic=TOPIC_PRODUCT,
                       hint="ค่าน้ำมัน = (ระยะทาง ÷ ระยะทางต่อลิตร) × ราคาต่อลิตร")
