"""การเกิดระบบสุริยะและดาวเคราะห์ที่เอื้อต่อชีวิต

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/10

Sets moved here from: science_wave_f84.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f84 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_ZONE = "การเกิดระบบสุริยะและดาวเคราะห์ที่เอื้อต่อชีวิต"


FORMATION = ("เนบิวลาสุริยะยุบตัวด้วยแรงโน้มถ่วง", "เนบิวลาหมุนเร็วขึ้นและแบนเป็นจานรอบดาวฤกษ์ก่อนเกิด",
             "ฝุ่นและแก๊สในจานรวมกันเป็นดาวเคราะห์ก่อนเกิด", "ดาวเคราะห์ก่อนเกิดชนและรวมกันเป็นดาวเคราะห์")


ZONES = {
    "เขตดาวเคราะห์ชั้นใน (ดาวเคราะห์หิน)": ("ดาวพุธ", "ดาวศุกร์", "โลก", "ดาวอังคาร"),
    "แถบดาวเคราะห์น้อย": ("ดาวซีรีส", "ดาวเวสตา", "ดาวพาลัส"),
    "เขตดาวเคราะห์ชั้นนอก (ดาวเคราะห์แก๊ส)": ("ดาวพฤหัสบดี", "ดาวเสาร์", "ดาวยูเรนัส", "ดาวเนปจูน"),
    "แถบไคเปอร์": ("ดาวพลูโต", "ดาวอีริส", "ดาวเมคมค"),
}


ZONE_FACTS = (
    ("เหตุใดดาวเคราะห์ชั้นในจึงเป็นดาวเคราะห์หิน ส่วนดาวเคราะห์ชั้นนอกเป็นดาวเคราะห์แก๊ส", "ใกล้ดวงอาทิตย์ร้อนมาก สารระเหยง่ายกลายเป็นแก๊สถูกผลักออกไป เหลือหินและโลหะ",
     ("ดาวเคราะห์ชั้นในเกิดก่อนดวงอาทิตย์", "ดาวเคราะห์ชั้นนอกได้รับความร้อนมากกว่า", "ดาวเคราะห์ชั้นในจับแก๊สได้มากกว่า", "ดาวเคราะห์ทุกดวงเกิดเป็นหินแล้วค่อยกลายเป็นแก๊ส")),
    ("เขตเอื้อต่อชีวิต (habitable zone) หมายถึงบริเวณใด", "ระยะจากดาวฤกษ์ที่ดาวเคราะห์มีอุณหภูมิเหมาะให้น้ำเป็นของเหลวได้",
     ("บริเวณที่ไม่มีแรงโน้มถ่วง", "บริเวณที่ใกล้ดาวฤกษ์ที่สุด", "บริเวณที่มีดาวเคราะห์แก๊สเท่านั้น", "บริเวณที่ไม่ได้รับแสงเลย")),
    ("สมบัติใดของโลกช่วยป้องกันอนุภาคพลังงานสูงจากลมสุริยะ", "สนามแม่เหล็กโลก",
     ("ความเค็มของน้ำทะเล", "ภูเขาสูง", "แกนเอียงของโลก", "ดวงจันทร์")),
    ("ข้อใดเป็นสมบัติของดาวเคราะห์ที่เอื้อต่อการดำรงชีวิต", "อยู่ในเขตเอื้อต่อชีวิต มีน้ำเป็นของเหลว มีบรรยากาศและสนามแม่เหล็กห่อหุ้ม",
     ("อยู่ใกล้ดาวฤกษ์จนร้อนจัด", "ไม่มีบรรยากาศ", "มีพื้นผิวเป็นแก๊สทั้งหมด", "หมุนรอบตัวเองนานหลายพันปี")),
    ("อายุของระบบสุริยะประมาณเท่าใด", "ประมาณ 4,600 ล้านปี",
     ("ประมาณ 13,800 ล้านปี", "ประมาณ 460 ล้านปี", "ประมาณ 1 ล้านปี", "ประมาณ 46,000 ล้านปี")),
)


ZONE_HINT = ("เนบิวลาสุริยะยุบตัว หมุนเร็วขึ้นแบนเป็นจาน ใจกลางเป็นดวงอาทิตย์ ฝุ่นแก๊สรวมเป็นดาวเคราะห์ ใกล้ดวงอาทิตย์เป็นดาวเคราะห์หิน "
             "ไกลออกไปเป็นดาวเคราะห์แก๊ส ถัดไปแถบไคเปอร์และเมฆออร์ต เขตเอื้อต่อชีวิตคือระยะที่น้ำเป็นของเหลวได้")


@question_type(
    "astro.habitable_zone_foundation",
    display_name={"th": "การเกิดระบบสุริยะและเขตเอื้อต่อชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ZONE,
)
class HabitableZoneFoundation(QuestionType):
    """Rock inside, gas outside; the habitable zone; what life needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            perms = [p for p in permutations(FORMATION) if p != FORMATION]
            return _labelled(stem="ข้อใดเรียงลำดับการเกิดระบบสุริยะได้ถูกต้อง", correct=" → ".join(FORMATION),
                             wrongs=tuple(" → ".join(p) for p in rng.sample(perms, 3)), topic=TOPIC_ZONE, hint=ZONE_HINT)
        stem, right, wrongs = rng.choice(ZONE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ZONE, hint=ZONE_HINT)


@question_type(
    "astro.habitable_zone_fluency",
    display_name={"th": "แบ่งเขตบริวารของดวงอาทิตย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ZONE,
)
class HabitableZoneFluency(QuestionType):
    """Which zone an object is in, and which object is in a zone."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        zone = rng.choice(tuple(ZONES))
        body = rng.choice(ZONES[zone])
        if rng.random() < 0.5:
            return _labelled(stem=f"{body}อยู่ในเขตใดของระบบสุริยะ", correct=zone, wrongs=tuple(z for z in ZONES if z != zone),
                             topic=TOPIC_ZONE, hint=ZONE_HINT)
        pool = [b for z, bs in ZONES.items() if z != zone for b in bs]
        return _labelled(stem=f"ข้อใดอยู่ใน{zone}", correct=body, wrongs=tuple(pool), topic=TOPIC_ZONE, hint=ZONE_HINT)


@question_type(
    "astro.habitable_zone_application",
    display_name={"th": "คำนวณระยะเขตเอื้อต่อชีวิตและพลังงานที่ดาวเคราะห์ได้รับ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ZONE,
)
class HabitableZoneApplication(QuestionType):
    """Habitable distance √L AU; energy received L / d² relative to Earth."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            root = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), 2, 3, 4, 5, 10, Fraction(3, 10)))
            lum = Fraction(root) ** 2
            return numeric(stem=f"ดาวฤกษ์ดวงหนึ่งส่องสว่าง {show(lum)} เท่าของดวงอาทิตย์ (ระยะเขตเอื้อต่อชีวิต ≈ √L หน่วยดาราศาสตร์) "
                                f"เขตเอื้อต่อชีวิตอยู่ห่างจากดาวฤกษ์ประมาณกี่หน่วยดาราศาสตร์", answer=root,
                           wrongs=[lum if lum != root else root * 2, root * 2, root + 1], unit="AU", topic=TOPIC_ZONE,
                           hint="ระยะ = √L เพราะพลังงานที่ได้รับลดลงตามระยะทางยกกำลังสอง")
        if roll < 0.75:
            lum = rng.choice((1, 4, 9, 16, 25, Fraction(1, 4), Fraction(1, 100)))
            d = rng.choice((Fraction(1, 2), 1, 2, 3, 4, 5, 10, Fraction(1, 10)))
            flux = Fraction(lum) / Fraction(d) ** 2
            if (flux * 100).denominator != 1:
                d = 1
                flux = Fraction(lum)
            return numeric(stem=f"ดาวเคราะห์ดวงหนึ่งอยู่ห่างดาวฤกษ์ {show(d)} AU ดาวฤกษ์ส่องสว่าง {show(lum)} เท่าของดวงอาทิตย์ "
                                f"ดาวเคราะห์ได้รับพลังงานต่อพื้นที่กี่เท่าของที่โลกได้รับ (พลังงาน ∝ L ÷ d²)", answer=flux,
                           wrongs=[Fraction(lum) / Fraction(d) if (Fraction(lum) / Fraction(d) * 100).denominator == 1 else flux * 2, flux * 2 + 1, Fraction(lum) * Fraction(d) ** 2],
                           unit="เท่า", topic=TOPIC_ZONE, hint="พลังงานที่ได้รับ = L ÷ d² เมื่อเทียบกับโลก (L = 1, d = 1 AU)")
        root = rng.choice((1, 2, 3, 4, 5))
        lum = root * root
        inner, outer = Fraction(root * 95, 100), Fraction(root * 137, 100)
        d = Fraction(rng.randint(1, 80), 10)
        right = "อยู่ในเขตเอื้อต่อชีวิต" if inner <= d <= outer else "ใกล้ดาวฤกษ์เกินไป น้ำจะระเหยหมด" if d < inner else "ไกลดาวฤกษ์เกินไป น้ำจะแข็งตัว"
        return _labelled(stem=f"ดาวฤกษ์ส่องสว่าง {lum} เท่าของดวงอาทิตย์ มีเขตเอื้อต่อชีวิตตั้งแต่ {show(inner)} ถึง {show(outer)} AU "
                              f"ดาวเคราะห์ที่อยู่ห่าง {show(d)} AU เป็นอย่างไร", correct=right,
                         wrongs=tuple(o for o in ("อยู่ในเขตเอื้อต่อชีวิต", "ใกล้ดาวฤกษ์เกินไป น้ำจะระเหยหมด", "ไกลดาวฤกษ์เกินไป น้ำจะแข็งตัว",
                                                  "ไม่ได้รับพลังงานจากดาวฤกษ์เลย") if o != right),
                         topic=TOPIC_ZONE, hint="เทียบระยะของดาวเคราะห์กับขอบในและขอบนอกของเขตเอื้อต่อชีวิต")
