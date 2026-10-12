"""โครงสร้างภายในของใบ

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/4

Sets moved here from: science_wave_f55.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f55 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_LEAF = "โครงสร้างภายในของใบ"


LEAF_PARTS = (
    ("เอพิเดอร์มิสด้านบน", "เซลล์เรียงแถวเดียว มีคิวทินเคลือบ และส่วนใหญ่ไม่มีคลอโรพลาสต์"),
    ("แพลิเซดมีโซฟิลล์", "เซลล์รูปทรงกระบอกเรียงชิดกันใต้เอพิเดอร์มิสด้านบน มีคลอโรพลาสต์มากที่สุด"),
    ("สปันจีมีโซฟิลล์", "เซลล์รูปร่างไม่แน่นอน เรียงตัวหลวม ๆ มีช่องว่างระหว่างเซลล์มาก"),
    ("มัดท่อลำเลียงของใบ (เส้นใบ)", "มีไซเลมอยู่ด้านบนและโฟลเอ็มอยู่ด้านล่าง ล้อมรอบด้วยบันเดิลชีท"),
    ("เซลล์คุม", "เซลล์รูปไตในเอพิเดอร์มิสที่มีคลอโรพลาสต์ ควบคุมการปิดเปิดปากใบ"),
    ("เอพิเดอร์มิสด้านล่าง", "มักมีปากใบมากกว่าผิวใบด้านบนในพืชใบเลี้ยงคู่"),
)


LEAF_HINT = ("ภาคตัดขวางใบจากบนลงล่าง: เอพิเดอร์มิสด้านบน แพลิเซดมีโซฟิลล์ สปันจีมีโซฟิลล์ (มีเส้นใบแทรก) "
             "และเอพิเดอร์มิสด้านล่างที่มีปากใบมาก")


LEAF_FACTS = (
    ("ชั้นใดของใบสังเคราะห์ด้วยแสงได้มากที่สุด", "แพลิเซดมีโซฟิลล์",
     ("สปันจีมีโซฟิลล์", "เอพิเดอร์มิสด้านบน", "เอพิเดอร์มิสด้านล่าง", "บันเดิลชีท")),
    ("ช่องว่างระหว่างเซลล์ในสปันจีมีโซฟิลล์มีประโยชน์อย่างไร", "ให้แก๊สแพร่ถึงเซลล์ต่าง ๆ ได้ทั่วถึง",
     ("เก็บน้ำตาลที่สร้างได้", "ทำให้ใบแข็งแรง", "ลำเลียงน้ำไปยังเส้นใบ", "ป้องกันแมลงกัดกิน")),
    ("เซลล์ใดในชั้นเอพิเดอร์มิสของใบมีคลอโรพลาสต์", "เซลล์คุม",
     ("เซลล์เอพิเดอร์มิสทั่วไป", "เซลล์ขน", "เซลล์คอมพาเนียน", "เวสเซลเมมเบอร์")),
    ("คิวทินที่เคลือบผิวใบมีหน้าที่อะไร", "ลดการสูญเสียน้ำทางผิวใบ",
     ("ช่วยดูดแสง", "สร้างอาหาร", "เปิดปิดปากใบ", "ลำเลียงน้ำ")),
    ("ในเส้นใบของใบพืชใบเลี้ยงคู่ ไซเลมอยู่ด้านใด", "ด้านบน (ด้านผิวใบบน)",
     ("ด้านล่าง (ด้านผิวใบล่าง)", "กระจายทั่วเส้นใบไม่เป็นระเบียบ", "อยู่นอกบันเดิลชีท")),
    ("ใบพืชใบเลี้ยงเดี่ยว เช่น หญ้า ต่างจากใบพืชใบเลี้ยงคู่อย่างไร", "มีโซฟิลล์มักไม่แยกเป็นแพลิเซดและสปันจีชัดเจน และมีปากใบทั้งสองด้านใกล้เคียงกัน",
     ("ไม่มีปากใบเลย", "ไม่มีเส้นใบ", "มีแพลิเซดทั้งด้านบนและล่างเสมอ")),
)


@question_type(
    "biology.leaf_structure_foundation",
    display_name={"th": "ส่วนประกอบภายในของใบและลักษณะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LEAF,
)
class LeafStructureFoundation(QuestionType):
    """Each layer of the leaf, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, looks = rng.choice(LEAF_PARTS)
        others = rng.sample([p for p in LEAF_PARTS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีลักษณะอย่างไร", correct=looks, wrongs=tuple(p[1] for p in others), topic=TOPIC_LEAF,
                             hint=LEAF_HINT)
        return _labelled(stem=f"ส่วนใดของใบมีลักษณะ \"{looks}\"", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_LEAF,
                         hint=LEAF_HINT)


@question_type(
    "biology.leaf_structure_fluency",
    display_name={"th": "หน้าที่ของโครงสร้างในใบที่สัมพันธ์กับการสังเคราะห์ด้วยแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LEAF,
)
class LeafStructureFluency(QuestionType):
    """Why the leaf is built the way it is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            order = ["เอพิเดอร์มิสด้านบน", "แพลิเซดมีโซฟิลล์", "สปันจีมีโซฟิลล์", "เอพิเดอร์มิสด้านล่าง"]
            wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrongs) < 3:
                o = order[:]
                rng.shuffle(o)
                if o != order:
                    wrongs[" → ".join(o)] = None
            return _labelled(stem="ข้อใดเรียงชั้นของใบพืชใบเลี้ยงคู่จากผิวใบด้านบนลงไปด้านล่างได้ถูกต้อง", correct=" → ".join(order),
                             wrongs=tuple(wrongs), topic=TOPIC_LEAF, hint=LEAF_HINT)
        stem, right, wrongs = rng.choice(LEAF_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_LEAF, hint=LEAF_HINT)


@question_type(
    "biology.leaf_structure_application",
    display_name={"th": "คำนวณความหนาแน่นของปากใบจากการนับ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LEAF,
)
class LeafStructureApplication(QuestionType):
    """Stomata per mm² = count ÷ field area; scale up to the whole leaf."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        area = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 4), Fraction(1, 2)))
        density = rng.randrange(40, 401, 20)
        count = density * area
        plant = rng.choice(("ผักบุ้ง", "ชบา", "ถั่วเขียว", "ข้าวโพด", "เฟื่องฟ้า"))
        side = rng.choice(("ด้านบน", "ด้านล่าง"))
        hint = "ความหนาแน่นของปากใบ = จำนวนปากใบที่นับได้ ÷ พื้นที่ภาพที่มองเห็น 1 cm² = 100 mm²"
        roll = rng.random()
        if roll < 0.45:
            return numeric(stem=f"ลอกผิวใบ{plant}{side}มาส่องด้วยกล้องจุลทรรศน์ ภาพมีพื้นที่ {show(area)} mm² นับปากใบได้ {show(count)} ปาก "
                                f"ความหนาแน่นของปากใบเป็นกี่ปากต่อ mm²", answer=density,
                           wrongs=[count, count * area, density * 2], unit="ปากต่อ mm²", topic=TOPIC_LEAF, hint=hint)
        if roll < 0.75:
            leaf = rng.randrange(10, 61, 5)
            return numeric(stem=f"ผิวใบ{plant}{side}มีปากใบ {density} ปากต่อ mm² ถ้าผิวใบด้านนี้มีพื้นที่ {leaf} cm² "
                                f"จะมีปากใบทั้งหมดกี่ปาก", answer=density * leaf * 100,
                           wrongs=[density * leaf, density * leaf * 10, density * leaf * 1000], unit="ปาก", topic=TOPIC_LEAF, hint=hint)
        upper = rng.randrange(20, 201, 10)
        ratio = rng.choice((2, Fraction(5, 2), 3, 4, 5))
        lower = upper * ratio
        return numeric(stem=f"ใบ{plant}มีปากใบด้านบน {upper} ปากต่อ mm² และด้านล่าง {show(lower)} ปากต่อ mm² "
                            f"ผิวใบด้านล่างมีปากใบเป็นกี่เท่าของด้านบน", answer=ratio,
                       wrongs=[lower - upper, Fraction(upper, lower) if (Fraction(upper, lower) * 100).denominator == 1 else ratio + 1,
                               ratio * 2], unit="เท่า", topic=TOPIC_LEAF, hint="เทียบจำนวนต่อพื้นที่ที่เท่ากัน: ด้านล่าง ÷ ด้านบน")
