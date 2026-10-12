"""ระยะทางของดาวฤกษ์ด้วยแพรัลแลกซ์

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/8

Sets moved here from: science_wave_f83.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f83 import NAMES, SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_PARALLAX = "ระยะทางของดาวฤกษ์ด้วยแพรัลแลกซ์"


PARALLAX_FACTS = (
    ("แพรัลแลกซ์ของดาวฤกษ์คืออะไร", "ตำแหน่งปรากฏของดาวใกล้เปลี่ยนไปเทียบกับดาวไกล เมื่อโลกอยู่คนละตำแหน่ง",
     ("การที่ดาวเปลี่ยนสีตามฤดูกาลเมื่อโลกอยู่คนละตำแหน่งในวงโคจร", "การที่ดาวกะพริบเพราะบรรยากาศของโลกหักเหแสงไม่สม่ำเสมอ", "การที่ดาวเคลื่อนที่จริงไปตามแรงโน้มถ่วงของดาวดวงอื่นที่อยู่ใกล้กว่า", "การที่ดาวหมุนรอบตัวเอง")),
    ("ในการวัดแพรัลแลกซ์ นักดาราศาสตร์ถ่ายภาพดาวห่างกันกี่เดือน", "ประมาณ 6 เดือน เมื่อโลกอยู่คนละฝั่งของวงโคจร",
     ("ประมาณ 1 วัน เมื่อโลกหมุนรอบตัวเองครบรอบ", "ห่างกัน 1 ชั่วโมง", "ประมาณ 12 ปี เมื่อดาวพฤหัสบดีโคจรครบรอบ", "ประมาณ 1 นาที เพื่อไม่ให้ดาวเคลื่อนที่")),
    ("1 พาร์เซกคือระยะทางเท่าใด", "ระยะที่ดาวมีมุมแพรัลแลกซ์ 1 ฟิลิปดา ประมาณ 3.26 ปีแสง",
     ("ระยะจากโลกถึงดวงอาทิตย์ ประมาณ 150 ล้านกิโลเมตร", "ระยะที่แสงเดินทางใน 1 ปี", "ระยะที่ดาวมีมุมแพรัลแลกซ์ 1 องศา ประมาณ 1 ปีแสงพอดี", "ระยะจากโลกถึงดวงจันทร์ ประมาณ 384,000 กิโลเมตร")),
    ("เหตุใดวิธีแพรัลแลกซ์จึงใช้วัดระยะได้เฉพาะดาวที่อยู่ค่อนข้างใกล้", "ดาวไกลมากมีมุมแพรัลแลกซ์เล็กเกินกว่าจะวัดได้แม่นยำ",
     ("ดาวไกลไม่มีแสง", "ดาวไกลเคลื่อนที่เร็วเกินไปจนวัดตำแหน่งในภาพถ่ายไม่ทัน", "ดาวไกลอยู่นอกเอกภพที่แสงเดินทางมาไม่ถึง", "ดาวไกลไม่เปลี่ยนสี จึงเทียบตำแหน่งกันไม่ได้")),
    ("มุมแพรัลแลกซ์กับระยะทางของดาวสัมพันธ์กันอย่างไร", "ระยะทางแปรผกผันกับมุมแพรัลแลกซ์",
     ("ระยะทางแปรผันตรงกับมุมแพรัลแลกซ์", "ไม่สัมพันธ์กัน", "ระยะทางเท่ากับมุมยกกำลังสอง", "มุมแพรัลแลกซ์เท่ากันทุกดาว")),
    ("ดาวฤกษ์ที่อยู่ใกล้ระบบสุริยะที่สุดคือดาวใด และอยู่ห่างประมาณเท่าใด", "ดาวพร็อกซิมาเซนทอรี ห่าง 1.3 พาร์เซก",
     ("ดาวซีรีอัส ห่างประมาณ 1 ปีแสง", "ดาวเหนือ ห่างประมาณ 0.1 พาร์เซก", "ดาวเวกา ห่างประมาณ 1 หน่วยดาราศาสตร์", "ดาวบีเทลจุส ห่างประมาณ 1 พาร์เซก")),
    ("เหตุใดกล้องโทรทรรศน์อวกาศ เช่น ไกอา จึงวัดแพรัลแลกซ์ได้ไกลกว่ากล้องบนพื้นโลก", "ไม่มีบรรยากาศรบกวน จึงวัดมุมเล็กมากได้แม่นยำกว่า",
     ("อยู่ใกล้ดาวฤกษ์มากกว่าหลายปีแสง", "ใช้เวลาถ่ายภาพห่างกัน 1 วัน จึงไม่ต้องรอ 6 เดือน", "ดาวในอวกาศสว่างกว่าเสมอ จึงวัดตำแหน่งได้ง่าย", "ไม่ต้องใช้วงโคจรของโลกในการวัดมุมเลย")),
)


PARALLAX_HINT = "d (พาร์เซก) = 1 ÷ p (ฟิลิปดา) มุมแพรัลแลกซ์ยิ่งเล็ก ดาวยิ่งไกล 1 พาร์เซก ≈ 3.26 ปีแสง"


# Two decimal places at most, so the angle in the stem is shown exactly.
PARALLAX_ANGLES = (Fraction(1, 2), Fraction(1, 4), Fraction(1, 5), Fraction(1, 10), Fraction(1, 20), Fraction(1, 25),
                   Fraction(1, 50), Fraction(1, 100), Fraction(2, 5), Fraction(4, 5), Fraction(2, 25), Fraction(4, 25))


@question_type(
    "astro.parallax_foundation",
    display_name={"th": "หลักการแพรัลแลกซ์และหน่วยพาร์เซก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PARALLAX,
)
class ParallaxFoundation(QuestionType):
    """What parallax is, six months apart, the parsec, the limit."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(PARALLAX_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_PARALLAX, hint=PARALLAX_HINT)


@question_type(
    "astro.parallax_fluency",
    display_name={"th": "เปรียบเทียบระยะทางของดาวจากมุมแพรัลแลกซ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PARALLAX,
)
class ParallaxFluency(QuestionType):
    """Bigger parallax, nearer star."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        angles = rng.sample(range(1, 100), 4)
        near = rng.random() < 0.5
        pick = angles.index(max(angles) if near else min(angles))
        table = " ".join(f"{n} มุมแพรัลแลกซ์ {show(Fraction(a, 100))} ฟิลิปดา" for n, a in zip(NAMES, angles))
        return _labelled(stem=f"{table} ดาวใดอยู่{'ใกล้' if near else 'ไกล'}โลกที่สุด", correct=NAMES[pick],
                         wrongs=tuple(n for n in NAMES if n != NAMES[pick]), topic=TOPIC_PARALLAX, hint=PARALLAX_HINT)


@question_type(
    "astro.parallax_application",
    display_name={"th": "คำนวณระยะทางของดาวจากมุมแพรัลแลกซ์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PARALLAX,
)
class ParallaxApplication(QuestionType):
    """d = 1 / p, p = 1 / d, and parsecs to light-years."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p = rng.choice(PARALLAX_ANGLES)
        d = 1 / p
        roll = rng.random()
        if roll < 0.35:
            return numeric(stem=f"ดาวฤกษ์ดวงหนึ่งมีมุมแพรัลแลกซ์ {show(p)} ฟิลิปดา อยู่ห่างจากโลกกี่พาร์เซก", answer=d,
                           wrongs=[p * 100 if p * 100 != d else d * 2, d * 2, d + 1], unit="พาร์เซก", topic=TOPIC_PARALLAX, hint=PARALLAX_HINT)
        if roll < 0.6:
            return numeric(stem=f"ดาวฤกษ์ดวงหนึ่งอยู่ห่างจากโลก {show(d)} พาร์เซก มุมแพรัลแลกซ์เป็นกี่ฟิลิปดา", answer=p,
                           wrongs=[p * 2, p * 10, p + 1], unit="ฟิลิปดา", topic=TOPIC_PARALLAX, hint="p = 1 ÷ d")
        if roll < 0.8:
            shift = 2 * p
            return numeric(stem=f"ถ่ายภาพดาวฤกษ์ห่างกัน 6 เดือน พบตำแหน่งปรากฏเลื่อนไปรวม {show(shift)} ฟิลิปดา "
                                f"(มุมแพรัลแลกซ์เป็นครึ่งหนึ่งของมุมที่เลื่อน) ดาวอยู่ห่างกี่พาร์เซก", answer=d,
                           wrongs=[1 / shift, d * 2, shift], unit="พาร์เซก", topic=TOPIC_PARALLAX, hint="p = มุมที่เลื่อน ÷ 2 แล้ว d = 1 ÷ p")
        whole = [a for a in PARALLAX_ANGLES if (1 / a).denominator == 1]
        p = rng.choice(whole)
        d = 1 / p
        return numeric(stem=f"ดาวฤกษ์ดวงหนึ่งมีมุมแพรัลแลกซ์ {show(p)} ฟิลิปดา (1 พาร์เซก = 3.26 ปีแสง) อยู่ห่างจากโลกกี่ปีแสง",
                       answer=d * Fraction(326, 100), wrongs=[d, d * 3, Fraction(d, Fraction(326, 100)) if (Fraction(d, Fraction(326, 100)) * 100).denominator == 1 else d * 6],
                       unit="ปีแสง", topic=TOPIC_PARALLAX, hint="d (ปีแสง) = (1 ÷ p) × 3.26")
