"""องค์ประกอบของเลือด

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/12

Sets moved here from: science_wave_f62.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f62 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_BLOOD = "องค์ประกอบของเลือด"


COMPONENTS = (
    ("เซลล์เม็ดเลือดแดง", "รูปร่างกลมแบนเว้าตรงกลาง ไม่มีนิวเคลียส มีฮีโมโกลบินลำเลียง O₂"),
    ("เซลล์เม็ดเลือดขาว", "มีนิวเคลียส ทำหน้าที่ต่อต้านและทำลายสิ่งแปลกปลอม"),
    ("เพลตเลต", "เป็นชิ้นส่วนของเซลล์ขนาดเล็ก ช่วยในการแข็งตัวของเลือด"),
    ("พลาสมา", "เป็นของเหลวสีเหลืองอ่อนประมาณร้อยละ 55 ของเลือด มีน้ำเป็นส่วนใหญ่"),
)


WBC = (
    ("นิวโทรฟิล", "พบมากที่สุดในเม็ดเลือดขาว กินสิ่งแปลกปลอมด้วยฟาโกไซโทซิส"),
    ("ลิมโฟไซต์", "สร้างแอนติบอดีและทำลายเซลล์ที่ติดเชื้อ ทำงานแบบจำเพาะ"),
    ("โมโนไซต์", "เปลี่ยนเป็นแมโครฟาจที่กินสิ่งแปลกปลอมขนาดใหญ่"),
    ("อีโอซิโนฟิล", "เพิ่มจำนวนเมื่อเกิดภูมิแพ้หรือมีพยาธิ"),
    ("เบโซฟิล", "หลั่งฮีสตามีนที่เกี่ยวข้องกับการอักเสบและภูมิแพ้"),
)


BLOOD_HINT = ("เม็ดเลือดแดงไม่มีนิวเคลียส มีฮีโมโกลบิน เม็ดเลือดขาวมีนิวเคลียส ต่อต้านเชื้อโรค เพลตเลตช่วยให้เลือดแข็งตัว "
              "พลาสมาเป็นของเหลวประมาณร้อยละ 55 ของเลือด")


@question_type(
    "biology.blood_component_foundation",
    display_name={"th": "ลักษณะและหน้าที่ขององค์ประกอบของเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BLOOD,
)
class BloodComponentFoundation(QuestionType):
    """Red cells, white cells, platelets and plasma."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, feature = rng.choice(COMPONENTS)
        others = [c for c in COMPONENTS if c[0] != name]
        roll = rng.random()
        if roll < 0.4:
            pool = [c[1] for c in others] + ["เป็นเซลล์ขนาดใหญ่ที่มีนิวเคลียสหลายอันและสร้างฮอร์โมน", "เป็นของเหลวใสที่ไม่มีโปรตีนละลายอยู่เลย"]
            return _labelled(stem=f"{name}มีลักษณะและหน้าที่อย่างไร", correct=feature, wrongs=tuple(pool), topic=TOPIC_BLOOD,
                             hint=BLOOD_HINT)
        if roll < 0.8:
            pool = [c[0] for c in others] + ["น้ำเหลือง", "ฮีโมโกลบิน"]
            return _labelled(stem=f"องค์ประกอบใดของเลือด{feature}", correct=name, wrongs=tuple(pool), topic=TOPIC_BLOOD,
                             hint=BLOOD_HINT)
        facts = (("เซลล์เม็ดเลือดแดงของผู้ใหญ่สร้างที่ใด", "ไขกระดูกแดง", ("ตับ", "ม้าม", "ไต", "หัวใจ")),
                 ("เซลล์เม็ดเลือดแดงมีอายุประมาณเท่าใด", "ประมาณ 120 วัน", ("ประมาณ 1 วัน", "ประมาณ 7 วัน", "ตลอดชีวิต", "ประมาณ 10 ปี")),
                 ("เซลล์เม็ดเลือดแดงที่หมดอายุถูกทำลายที่ใด", "ตับและม้าม", ("ปอด", "ไขกระดูกแดง", "กระเพาะอาหาร", "หัวใจ")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_BLOOD, hint=BLOOD_HINT)


@question_type(
    "biology.blood_component_fluency",
    display_name={"th": "ชนิดของเซลล์เม็ดเลือดขาวและหน้าที่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BLOOD,
)
class BloodComponentFluency(QuestionType):
    """The five white cells, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role = rng.choice(WBC)
        others = rng.sample([w for w in WBC if w[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"เซลล์เม็ดเลือดขาวชนิดใด{role}", correct=name, wrongs=tuple(w[0] for w in others), topic=TOPIC_BLOOD,
                             hint="นิวโทรฟิลกินเชื้อโรค ลิมโฟไซต์ทำงานแบบจำเพาะ โมโนไซต์เป็นแมโครฟาจ อีโอซิโนฟิลเกี่ยวกับพยาธิและภูมิแพ้ เบโซฟิลหลั่งฮีสตามีน")
        return _labelled(stem=f"{name}มีบทบาทอย่างไร", correct=role, wrongs=tuple(w[1] for w in others), topic=TOPIC_BLOOD,
                         hint="นิวโทรฟิลกินเชื้อโรค ลิมโฟไซต์ทำงานแบบจำเพาะ โมโนไซต์เป็นแมโครฟาจ อีโอซิโนฟิลเกี่ยวกับพยาธิและภูมิแพ้ เบโซฟิลหลั่งฮีสตามีน")


@question_type(
    "biology.blood_component_application",
    display_name={"th": "คำนวณปริมาตรเลือด พลาสมา และจำนวนเซลล์เม็ดเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BLOOD,
)
class BloodComponentApplication(QuestionType):
    """Blood is about 8% of body mass; plasma is what the red cells leave."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            mass = rng.randrange(40, 91, 5)
            share = rng.choice((7, 8))
            return numeric(stem=f"คนหนักประมาณ {mass} kg ถ้าเลือดคิดเป็นร้อยละ {share} ของน้ำหนักตัว และเลือด 1 kg มีปริมาตรประมาณ 1 ลิตร "
                                f"คนนี้มีเลือดประมาณกี่ลิตร", answer=Fraction(mass * share, 100),
                           wrongs=[mass * share, Fraction(mass * (100 - share), 100), share], unit="ลิตร", topic=TOPIC_BLOOD,
                           hint="ปริมาตรเลือด ≈ น้ำหนักตัว × ร้อยละ ÷ 100")
        if roll < 0.7:
            blood = Fraction(rng.randrange(40, 61), 10)
            hct = rng.choice((40, 42, 44, 45, 46, 48))
            plasma = blood * (100 - hct) / 100
            if (plasma * 100).denominator != 1:
                blood = Fraction(5)
                plasma = blood * (100 - hct) / 100
            return numeric(stem=f"เลือด {show(blood)} ลิตร มีเซลล์เม็ดเลือดอัดแน่นร้อยละ {hct} (ฮีมาโทคริต) เป็นพลาสมากี่ลิตร", answer=plasma,
                           wrongs=[blood * hct / 100, blood, Fraction(100 - hct, 10)], unit="ลิตร", topic=TOPIC_BLOOD,
                           hint="พลาสมา = ปริมาตรเลือด × (100 − ฮีมาโทคริต) ÷ 100")
        per_mm3 = Fraction(rng.randrange(40, 61), 10)  # million per mm³
        ml = rng.randint(1, 10)
        total = per_mm3 * 1000 * ml
        return numeric(stem=f"เลือด 1 mm³ มีเซลล์เม็ดเลือดแดงประมาณ {show(per_mm3)} ล้านเซลล์ เลือด {ml} mL มีเซลล์เม็ดเลือดแดงประมาณกี่ล้านเซลล์",
                       answer=total, wrongs=[per_mm3 * ml, total * 1000, per_mm3 * 100 * ml], unit="ล้านเซลล์", topic=TOPIC_BLOOD,
                       hint="1 mL = 1,000 mm³ จำนวนเซลล์ = จำนวนต่อ mm³ × 1,000 × จำนวน mL")
