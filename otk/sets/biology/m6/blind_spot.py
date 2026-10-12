"""จุดบอด โฟเวีย และความไวของผิวหนัง

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/8

Sets moved here from: science_wave_f67.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f67 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SPOT = "จุดบอด โฟเวีย และความไวของผิวหนัง"


SPOT_FACTS = (
    ("จุดบอดคือบริเวณใดของเรตินา", "บริเวณที่เส้นประสาทตาออกจากลูกตา ไม่มีเซลล์รับแสง",
     ("บริเวณที่มีเซลล์รูปกรวยหนาแน่นที่สุด", "บริเวณกลางเลนส์ตาที่แสงผ่านเข้ามาไม่ได้", "บริเวณที่มีเซลล์รูปแท่งหนาแน่นที่สุด ใกล้ขอบเรตินา", "บริเวณที่มีเซลล์รูปแท่งมากที่สุด")),
    ("โฟเวียมีลักษณะอย่างไร", "มีเซลล์รูปกรวยหนาแน่น เห็นภาพชัดและแยกสีได้ดีที่สุด",
     ("ไม่มีเซลล์รับแสงเลย", "มีเซลล์รูปแท่งหนาแน่น เห็นภาพในที่มืดได้ดีที่สุด", "ไม่มีเซลล์รับแสงเลย เพราะเส้นประสาทตาออกที่จุดนี้", "เป็นจุดที่เส้นประสาทตาออก")),
    ("เหตุใดในชีวิตประจำวันเราจึงไม่รู้สึกว่ามีจุดบอด", "ตาสองข้างมองเห็นชดเชยกันและสมองเติมภาพส่วนที่ขาด",
     ("จุดบอดมีเฉพาะตอนกลางคืน", "เลนส์ตาหักเหแสงไม่ให้ภาพตกบนจุดบอดเลย", "คนปกติไม่มีจุดบอด เพราะเซลล์รับแสงกระจายทั่วเรตินา", "จุดบอดอยู่ที่กระจกตา")),
    ("ในการทดลองหาจุดบอด ต้องปิดตาข้างหนึ่งเพราะเหตุใด", "เพื่อไม่ให้ตาอีกข้างมองเห็นชดเชยภาพที่ตกบนจุดบอด",
     ("เพื่อให้ม่านตาของตาข้างที่เปิดขยายรับแสงได้มากขึ้น", "เพื่อให้ภาพตกบนโฟเวียของตาข้างเดียวได้ชัดขึ้น", "เพื่อให้เห็นสีชัดขึ้น", "เพื่อเพิ่มจำนวนเซลล์รูปกรวย")),
    ("เมื่อต้องการมองวัตถุให้ชัดที่สุด ตาจะปรับให้ภาพตกที่ใด", "โฟเวีย",
     ("จุดบอด", "ม่านตา", "เลนส์ตา", "ขอบเรตินา")),
    ("ในที่แสงสลัว การมองเลยวัตถุไปด้านข้างเล็กน้อยช่วยให้เห็นวัตถุชัดขึ้นเพราะเหตุใด", "ภาพตกบริเวณรอบโฟเวียที่มีเซลล์รูปแท่งมาก",
     ("ภาพตกที่จุดบอดซึ่งไม่มีเซลล์รับแสง", "ภาพตกที่โฟเวียซึ่งมีเซลล์รูปแท่งมาก", "เลนส์ตาหยุดทำงาน", "ม่านตาหรี่ลงจนแสงเข้าตาน้อยเกินไป")),
    ("ความไวในการรับสัมผัสของผิวหนังแต่ละบริเวณต่างกันเพราะเหตุใด", "จำนวนหน่วยรับสัมผัสต่อพื้นที่ต่างกัน",
     ("ความหนาของกระดูกต่างกัน", "ความหนาของผิวหนังที่ต่างกันในแต่ละบริเวณ", "จำนวนต่อมเหงื่อเท่ากันทุกบริเวณ", "ปริมาณเลือดที่ไปเลี้ยงแต่ละบริเวณต่างกัน")),
)


SPOT_HINT = ("จุดบอดคือบริเวณที่เส้นประสาทตาออก ไม่มีเซลล์รับแสง โฟเวียมีเซลล์รูปกรวยหนาแน่น ระยะสองจุดที่แยกได้ยิ่งสั้น "
             "ผิวหนังบริเวณนั้นยิ่งไว เพราะมีหน่วยรับสัมผัสหนาแน่น")


AREAS = (("ปลายนิ้วมือ", 2, 5), ("ริมฝีปาก", 3, 6), ("ฝ่ามือ", 8, 15), ("หน้าผาก", 12, 20), ("หลังมือ", 20, 30),
         ("แขนท่อนล่าง", 30, 40), ("หลัง", 40, 70))


@question_type(
    "biology.blind_spot_foundation",
    display_name={"th": "จุดบอด โฟเวีย และหน่วยรับสัมผัส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPOT,
)
class BlindSpotFoundation(QuestionType):
    """What the blind spot and fovea are, and why the skin varies."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(SPOT_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SPOT, hint=SPOT_HINT)


@question_type(
    "biology.blind_spot_fluency",
    display_name={"th": "อ่านผลการทดลองความไวในการรับสัมผัสของผิวหนัง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPOT,
)
class BlindSpotFluency(QuestionType):
    """Smallest two-point distance means the most sensitive skin."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        picked = sorted(rng.sample(range(len(AREAS)), 4))
        values = []
        last = 0
        for i in picked:
            name, lo, hi = AREAS[i]
            v = max(rng.randint(lo, hi), last + 1)
            values.append((name, v))
            last = v
        table = " ".join(f"{n} {v} mm" for n, v in sorted(values, key=lambda x: rng.random()))
        most = rng.random() < 0.5
        right = values[0][0] if most else values[-1][0]
        return _labelled(stem=f"ระยะห่างน้อยที่สุดที่รู้สึกได้ว่าเป็นสองจุด: {table} ผิวหนังบริเวณใดมีความไวในการรับสัมผัส"
                              f"{'มากที่สุด' if most else 'น้อยที่สุด'}", correct=right,
                         wrongs=tuple(n for n, _ in values if n != right), topic=TOPIC_SPOT, hint=SPOT_HINT)


@question_type(
    "biology.blind_spot_application",
    display_name={"th": "คำนวณตำแหน่งจุดบอดบนเรตินาจากการทดลอง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPOT,
)
class BlindSpotApplication(QuestionType):
    """Similar triangles: retina spacing = page spacing × 1.7 cm ÷ eye-to-page distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eye = Fraction(17, 10)
        while True:
            page = rng.choice((20, 25, 30, 34, 40, 50))
            gap = rng.choice((5, 6, 7, 8, 9, 10, 12))
            retina = Fraction(gap) * eye / page * 10  # mm
            if (retina * 100).denominator == 1:
                break
        if rng.random() < 0.6:
            return numeric(stem=f"ในการหาจุดบอด ภาพจุดหายไปเมื่อตาอยู่ห่างกระดาษ {page} cm ขณะที่เครื่องหมายบวกกับจุดห่างกัน {gap} cm "
                                f"ถ้าเลนส์ตาอยู่ห่างเรตินา 1.7 cm จุดบอดอยู่ห่างจากโฟเวียบนเรตินากี่มิลลิเมตร", answer=retina,
                           wrongs=[retina / 10, Fraction(gap * page, 17) if (Fraction(gap * page, 17) * 100).denominator == 1 else retina * 2,
                                   retina * 10], unit="mm", topic=TOPIC_SPOT,
                           hint="สามเหลี่ยมคล้าย: ระยะบนเรตินา ÷ 1.7 cm = ระยะบนกระดาษ ÷ ระยะตาถึงกระดาษ แล้วแปลงเป็น mm")
        return numeric(stem=f"จุดบอดอยู่ห่างโฟเวีย {show(retina)} mm บนเรตินา ซึ่งอยู่ห่างเลนส์ตา 1.7 cm ถ้าวางกระดาษห่างตา {page} cm "
                            f"ควรวาดเครื่องหมายบวกกับจุดห่างกันกี่เซนติเมตร จึงจะหาจุดบอดได้พอดี", answer=gap,
                       wrongs=[gap * 2, gap + 1, page - gap], unit="cm", topic=TOPIC_SPOT,
                       hint="ระยะบนกระดาษ = ระยะบนเรตินา × ระยะตาถึงกระดาษ ÷ 1.7 cm (ใช้หน่วยเดียวกัน)")
