"""ผลกระทบจากการใช้และการกำจัดผลิตภัณฑ์พอลิเมอร์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/15

Sets moved here from: science_wave_f29.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find
from otk.sets._support.science_wave_f29 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_WASTE = "ผลกระทบจากการใช้และการกำจัดผลิตภัณฑ์พอลิเมอร์"


IMPACTS = (
    ("เผาถุงพลาสติกและขยะพลาสติกในที่โล่ง", "เกิดแก๊ส CO เขม่า และสารพิษเช่นไดออกซิน ทำลายสุขภาพและคุณภาพอากาศ"),
    ("เผาผลิตภัณฑ์ PVC", "เกิดแก๊ส HCl ที่เป็นกรด และไดออกซิน"),
    ("ฝังกลบขยะพลาสติกจำนวนมาก", "พลาสติกย่อยสลายได้ช้ามาก ใช้พื้นที่ฝังกลบมากและตกค้างในดินนาน"),
    ("ทิ้งขยะพลาสติกลงแหล่งน้ำ", "สัตว์ทะเลกินหรือติดพันพลาสติก และพลาสติกแตกเป็นไมโครพลาสติกเข้าสู่ห่วงโซ่อาหาร"),
    ("ใช้ภาชนะโฟมใส่อาหารร้อนจัดหรือมันมาก", "อาจมีสารจากพลาสติก เช่น สไตรีน ปนเปื้อนสู่อาหาร"),
    ("ทิ้งถุงพลาสติกอุดตันท่อระบายน้ำ", "น้ำระบายไม่ทันจนเกิดน้ำท่วมขังและเป็นแหล่งเพาะพันธุ์ยุง"),
    ("ปล่อยเศษอวนและเชือกพลาสติกทิ้งในทะเล", "สัตว์ทะเลติดพันจนบาดเจ็บหรือตาย"),
)


SOLUTIONS = (
    ("ลดการใช้ถุงพลาสติกโดยพกถุงผ้า", "ลดปริมาณขยะตั้งแต่ต้นทาง (Reduce)"),
    ("ล้างขวด PET แล้วนำกลับมาใส่น้ำใช้ในบ้าน", "ใช้ซ้ำ (Reuse)"),
    ("คัดแยกพลาสติกตามรหัสรีไซเคิลส่งโรงงาน", "นำกลับมาผลิตใหม่ (Recycle)"),
    ("เลือกใช้ภาชนะจากพลาสติกชีวภาพ PLA", "ใช้วัสดุที่ย่อยสลายได้ทางชีวภาพ"),
    ("ปฏิเสธหลอดพลาสติกเมื่อไม่จำเป็น", "ปฏิเสธการใช้ (Refuse)"),
    ("ซ่อมเก้าอี้พลาสติกที่ขาหักแทนการซื้อใหม่", "ซ่อมแซม (Repair)"),
    ("นำยางรถยนต์เก่ามาทำกระถางต้นไม้", "ใช้ซ้ำ (Reuse)"),
    ("หลอมขวด HDPE เป็นเม็ดพลาสติกเพื่อผลิตถังขยะ", "นำกลับมาผลิตใหม่ (Recycle)"),
)


@question_type(
    "chem.polymer_waste_foundation",
    display_name={"th": "ผลกระทบจากการใช้และกำจัดผลิตภัณฑ์พอลิเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_WASTE,
)
class PolymerWasteFoundation(QuestionType):
    """What each way of using or disposing of polymers does to people and places."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        action, harm = rng.choice(IMPACTS)
        others = [i for i in IMPACTS if i[1] != harm]
        hint = "การเผาให้แก๊สพิษ การฝังกลบใช้เวลาย่อยสลายนาน ขยะในน้ำกลายเป็นไมโครพลาสติก"
        if rng.random() < 0.5:
            return _labelled(stem=f"{action} ก่อให้เกิดผลกระทบใดมากที่สุด", correct=harm,
                             wrongs=tuple(i[1] for i in rng.sample(others, 3)), topic=TOPIC_WASTE, hint=hint)
        return _labelled(stem=f"ผลกระทบ \"{harm}\" เกิดจากการกระทำใด", correct=action,
                         wrongs=tuple(i[0] for i in rng.sample(others, 3)), topic=TOPIC_WASTE, hint=hint)


@question_type(
    "chem.polymer_waste_fluency",
    display_name={"th": "คำนวณปริมาณขยะพลาสติกและการรีไซเคิล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_WASTE,
)
class PolymerWasteFluency(QuestionType):
    """Mass of bottles recycled, and HCl from burning PVC."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            def draw():
                bottles = rng.randrange(100, 2001, 100)
                grams = rng.choice((10, 12, 15, 20, 25, 30))
                percent = rng.choice((50, 60, 70, 75, 80, 90))
                fibre = Fraction(bottles * grams * percent, 100 * 1000)
                return (bottles, grams, percent, fibre) if (fibre * 100).denominator == 1 else None

            bottles, grams, percent, fibre = _find(rng, draw)
            return numeric(stem=f"นำขวด PET ใบละ {grams} กรัม จำนวน {bottles:,} ใบ ไปรีไซเคิลเป็นเส้นใย ถ้าได้เส้นใย {percent}% "
                                "ของมวลขวด จะได้เส้นใยกี่กิโลกรัม",
                           answer=fibre, wrongs=[fibre * 1000, Fraction(bottles * grams, 1000), fibre / 10 if fibre > 1 else fibre + 1],
                           unit="กิโลกรัม", topic=TOPIC_WASTE, hint="มวลขวดรวม × ร้อยละที่ได้ ÷ 100 แล้วแปลงกรัมเป็นกิโลกรัม")
        if kind == 1:
            people = rng.randrange(1000, 20001, 1000)
            bags = rng.randint(2, 8)
            days = rng.choice((7, 30, 365))
            total = people * bags * days
            return numeric(stem=f"ชุมชนหนึ่งมี {people:,} คน ใช้ถุงพลาสติกคนละ {bags} ใบต่อวัน ถ้าทุกคนเปลี่ยนมาใช้ถุงผ้า "
                                f"ใน {days} วันจะลดถุงพลาสติกได้กี่ใบ",
                           answer=total, wrongs=[people * bags, people * days, total * 2], unit="ใบ", topic=TOPIC_WASTE,
                           hint="จำนวนคน × ถุงต่อคนต่อวัน × จำนวนวัน")
        # Each PVC repeat unit –CH₂–CHCl– (62.5) gives one HCl (36.5) when burned.
        # Only amounts whose mass shows exactly: 0.25 × 62.5 = 15.625 would print rounded.
        units = rng.choice([Fraction(n, 4) for n in range(1, 41) if (Fraction(n, 4) * Fraction(125, 2) * 100).denominator == 1])
        mass = units * Fraction(125, 2)
        return numeric(stem=f"เผา PVC {show(mass)} กรัม (หน่วยซ้ำ –CH₂–CHCl– มวล 62.5) คลอรีนทั้งหมดกลายเป็นแก๊ส HCl "
                            "จะเกิด HCl กี่โมล",
                       answer=units, wrongs=[units * 2, units + 1, units * Fraction(1, 2)],
                       unit="โมล", topic=TOPIC_WASTE,
                       hint="โมลหน่วยซ้ำ = มวล ÷ 62.5 และหน่วยซ้ำหนึ่งหน่วยมี Cl หนึ่งอะตอม จึงให้ HCl หนึ่งโมเลกุล")


@question_type(
    "chem.polymer_waste_application",
    display_name={"th": "แนวทางลดและแก้ปัญหาขยะพอลิเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_WASTE,
)
class PolymerWasteApplication(QuestionType):
    """Name the approach behind an action, and pick the best fix for a case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            action, approach = rng.choice(SOLUTIONS)
            others = sorted({s[1] for s in SOLUTIONS if s[1] != approach})
            return _labelled(stem=f"\"{action}\" เป็นแนวทางใด", correct=approach, wrongs=tuple(others),
                             topic=TOPIC_WASTE, hint="Refuse ปฏิเสธ Reduce ลด Reuse ใช้ซ้ำ Recycle ผลิตใหม่")
        cases = (
            ("ขยะขวด PET จำนวนมากจากงานกีฬา", "คัดแยกขวดตามรหัส 1 แล้วส่งรีไซเคิล",
             ("เผาขวดในที่โล่งเพื่อลดปริมาตร", "ฝังกลบรวมกับขยะเปียกในสวน", "ทิ้งลงแหล่งน้ำใกล้เคียงให้ย่อยสลายเอง")),
            ("ร้านอาหารใช้กล่องโฟมใส่อาหารร้อนวันละหลายร้อยกล่อง", "เปลี่ยนเป็นภาชนะที่ย่อยสลายได้หรือใช้ซ้ำได้",
             ("ใช้กล่องโฟมสองชั้นแทนเพื่อไม่ให้แตก", "เผากล่องโฟมหลังใช้ทุกครั้งเพื่อไม่ให้เป็นขยะ", "ทิ้งรวมกับขยะอื่นโดยไม่แยกลงถังใกล้แม่น้ำ")),
            ("ท่อ PVC เก่าจากการรื้อบ้าน", "ส่งโรงงานรีไซเคิลที่รับ PVC แทนการเผา",
             ("เผาในที่โล่งเพราะให้ความร้อนสูง", "ทิ้งลงคลองให้น้ำพัดไป", "เผารวมกับขยะใบไม้ในสวน")),
            ("ไมโครพลาสติกจากถุงพลาสติกในแม่น้ำ", "ลดการใช้ถุงพลาสติกและจัดเก็บขยะก่อนลงแหล่งน้ำ",
             ("เปลี่ยนเป็นถุงพลาสติกที่บางลง", "เผาถุงที่ริมแม่น้ำให้หมดไป", "ฝังถุงที่ตลิ่งแม่น้ำ")),
        )
        case, right, wrongs = rng.choice(cases)
        bad = sorted({w for _, _, ws in cases for w in ws})
        wrongs = (rng.choice(wrongs), *rng.sample([w for w in bad if w not in wrongs], 2))
        return _labelled(stem=f"สถานการณ์: {case} แนวทางใดเหมาะสมที่สุด", correct=right, wrongs=wrongs, topic=TOPIC_WASTE,
                         hint="เลือกวิธีที่ลดขยะหรือนำกลับมาใช้ และไม่สร้างมลพิษใหม่ เช่น การเผาหรือทิ้งลงน้ำ")
