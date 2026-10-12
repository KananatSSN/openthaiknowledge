"""โครงสร้าง สมบัติ และการใช้ประโยชน์ของพอลิเมอร์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/12

Sets moved here from: science_wave_f29.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f29 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_STRUCTURE = "โครงสร้าง สมบัติ และการใช้ประโยชน์ของพอลิเมอร์"


# The textbook's three chain shapes. Vulcanised rubber (a few cross-links) and
# Bakelite (many) are both ร่างแห; they differ in how many links, not in kind.
LINEAR, BRANCHED, NETWORK = "แบบเส้น", "แบบกิ่ง", "แบบร่างแห"


SHAPES = (LINEAR, BRANCHED, NETWORK)


NOT_A_SHAPE = "แบบผลึกไอออนิก"


# chain shape: properties that follow from it
SHAPE_PROPERTIES = {
    LINEAR: "สายพอลิเมอร์เรียงชิดกันได้มาก ความหนาแน่นและจุดหลอมเหลวค่อนข้างสูง เหนียวและแข็ง",
    BRANCHED: "กิ่งทำให้สายเรียงชิดกันไม่ได้ ความหนาแน่นและจุดหลอมเหลวต่ำกว่า ยืดหยุ่นและนิ่มกว่า",
    NETWORK: "สายเชื่อมโยงกันด้วยพันธะโคเวเลนต์ ไม่หลอมเมื่อได้รับความร้อน ถ้าเชื่อมกันแน่นจะแข็งและเปราะ",
}


SHAPE_FILLER = "สายพอลิเมอร์ไม่มีแรงยึดเหนี่ยวกันเลย จึงไหลได้เหมือนของเหลว"


# (resin code, plastic, chain shape, heat behaviour, typical product)
PLASTICS = (
    (1, "พอลิเอทิลีนเทเรฟทาเลต (PET)", LINEAR, "เทอร์มอพลาสติก", "ขวดน้ำดื่มและขวดน้ำอัดลม"),
    (2, "พอลิเอทิลีนความหนาแน่นสูง (HDPE)", LINEAR, "เทอร์มอพลาสติก", "ขวดนมและแกลลอนน้ำยาซักผ้า"),
    (3, "พอลิไวนิลคลอไรด์ (PVC)", LINEAR, "เทอร์มอพลาสติก", "ท่อน้ำและฉนวนหุ้มสายไฟ"),
    (4, "พอลิเอทิลีนความหนาแน่นต่ำ (LDPE)", BRANCHED, "เทอร์มอพลาสติก", "ถุงพลาสติกและฟิล์มห่ออาหาร"),
    (5, "พอลิโพรพิลีน (PP)", LINEAR, "เทอร์มอพลาสติก", "กล่องใส่อาหารเข้าไมโครเวฟและฝาขวด"),
    (6, "พอลิสไตรีน (PS)", LINEAR, "เทอร์มอพลาสติก", "กล่องโฟมและช้อนส้อมพลาสติก"),
)


THERMOSETS = (
    ("เบกาไลต์", "ด้ามกระทะและเต้ารับไฟฟ้า"), ("เมลามีน", "จานชามที่ทนความร้อน"),
    ("อีพอกซี", "กาวสองส่วนและวัสดุเคลือบ"), ("ยางที่ผ่านการวัลคาไนซ์", "ยางรถยนต์"),
)


# (polymer, chain shape)
SHAPE_EXAMPLES = (
    ("พอลิเอทิลีนความหนาแน่นต่ำ (LDPE)", BRANCHED), ("พอลิเอทิลีนความหนาแน่นสูง (HDPE)", LINEAR),
    ("พอลิไวนิลคลอไรด์ (PVC)", LINEAR), ("พอลิเอทิลีนเทเรฟทาเลต (PET)", LINEAR), ("พอลิโพรพิลีน (PP)", LINEAR),
    ("ยางธรรมชาติที่ยังไม่วัลคาไนซ์", LINEAR), ("ยางที่ผ่านการวัลคาไนซ์", NETWORK), ("เบกาไลต์", NETWORK),
    ("เมลามีน", NETWORK), ("อีพอกซีที่แข็งตัวแล้ว", NETWORK),
)


STRUCTURE_REASONS = (
    ("HDPE มีความหนาแน่นมากกว่า LDPE เพราะเหตุใด", "HDPE เป็นพอลิเมอร์แบบเส้น สายจึงเรียงชิดกันได้มากกว่า LDPE ที่มีกิ่ง",
     ("HDPE มีมวลอะตอมมากกว่า", "HDPE มีพันธะคู่ในสายมากกว่า", "LDPE เป็นพอลิเมอร์แบบร่างแห")),
    ("เทอร์มอเซตไม่หลอมเมื่อได้รับความร้อนเพราะเหตุใด",
     "สายพอลิเมอร์เชื่อมโยงกันเป็นร่างแหด้วยพันธะโคเวเลนต์ ความร้อนทำให้สลายตัวก่อนจะหลอม",
     ("สายพอลิเมอร์สั้นมาก", "ไม่มีแรงระหว่างสายเลย", "เป็นพอลิเมอร์แบบกิ่ง")),
    ("เทอร์มอพลาสติกนำกลับมาหลอมขึ้นรูปใหม่ได้เพราะเหตุใด",
     "สายพอลิเมอร์ยึดกันด้วยแรงระหว่างโมเลกุล ซึ่งความร้อนเอาชนะได้โดยไม่สลายพันธะในสาย",
     ("สายพอลิเมอร์เชื่อมกันด้วยพันธะโคเวเลนต์ทั้งหมด", "ความร้อนทำให้เกิดพอลิเมอร์ใหม่",
      "เทอร์มอพลาสติกไม่มีพันธะโคเวเลนต์")),
    ("ยางที่ผ่านการวัลคาไนซ์ยืดแล้วคืนรูปได้เพราะเหตุใด",
     "มีพันธะเชื่อมโยงระหว่างสายที่ดึงสายให้กลับตำแหน่งเดิม",
     ("สายยางไม่มีการเชื่อมโยงกันเลย", "ยางละลายน้ำได้", "ยางเป็นพอลิเมอร์แบบเส้นที่สั้นมาก")),
)


@question_type(
    "chem.polymer_structure_foundation",
    display_name={"th": "โครงสร้างของพอลิเมอร์กับสมบัติ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_STRUCTURE,
)
class PolymerStructureFoundation(QuestionType):
    """Linear packs close, branches keep chains apart, cross-links hold them together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "แบบเส้นเรียงชิดกันได้ แบบกิ่งเรียงชิดไม่ได้ แบบร่างแหมีพันธะเชื่อมระหว่างสาย"
        if rng.random() < 0.5:
            shape = rng.choice(SHAPES)
            right = SHAPE_PROPERTIES[shape]
            return _labelled(stem=f"พอลิเมอร์{shape}มีสมบัติตามข้อใด", correct=right,
                             wrongs=tuple(v for k, v in SHAPE_PROPERTIES.items() if k != shape) + (SHAPE_FILLER,),
                             topic=TOPIC_STRUCTURE,
                             hint=hint)
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(STRUCTURE_REASONS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_STRUCTURE, hint=hint)
        shape = rng.choice(SHAPES)
        pick = rng.choice([e for e in SHAPE_EXAMPLES if e[1] == shape])
        others = [e[0] for e in SHAPE_EXAMPLES if e[1] != shape]
        return _labelled(stem=f"พอลิเมอร์ใดมีโครงสร้าง{shape}", correct=pick[0], wrongs=tuple(others),
                         topic=TOPIC_STRUCTURE, hint=hint)


@question_type(
    "chem.polymer_structure_fluency",
    display_name={"th": "รหัสพลาสติกและชนิดของพลาสติก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_STRUCTURE,
)
class PolymerStructureFluency(QuestionType):
    """Resin codes 1-6 name the plastic, and the plastic its product."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        code, name, shape, heat, product = rng.choice(PLASTICS)
        others = [p for p in PLASTICS if p[0] != code]
        hint = "1 PET, 2 HDPE, 3 PVC, 4 LDPE, 5 PP, 6 PS และ 7 อื่น ๆ"
        kind = rng.randrange(3)
        if kind == 0:
            return _labelled(stem=f"ผลิตภัณฑ์พลาสติกที่มีสัญลักษณ์รีไซเคิลหมายเลข {code} ทำจากพลาสติกชนิดใด", correct=name,
                             wrongs=tuple(p[1] for p in rng.sample(others, 3)), topic=TOPIC_STRUCTURE, hint=hint)
        if kind == 1:
            return numeric(stem=f"{name} ที่ใช้ทำ{product} มีรหัสรีไซเคิลหมายเลขใด", answer=code,
                           wrongs=[p[0] for p in rng.sample(others, 3)], unit="", topic=TOPIC_STRUCTURE, hint=hint)
        pick = rng.choice([p for p in PLASTICS] + [None])
        if pick is None:
            name, product = rng.choice(THERMOSETS)
            right = f"{name} เพราะเป็นเทอร์มอเซต"
            return _labelled(stem=f"ข้อใดเป็นพอลิเมอร์ที่เหมาะใช้ทำ{product} ซึ่งต้องทนความร้อนโดยไม่อ่อนตัว",
                             correct=right,
                             wrongs=tuple(f"{p[1]} เพราะเป็นเทอร์มอพลาสติก" for p in rng.sample(PLASTICS, 3)),
                             topic=TOPIC_STRUCTURE, hint="งานที่ต้องทนความร้อนสูงโดยไม่อ่อนตัวใช้เทอร์มอเซต")
        return _labelled(stem=f"{pick[4]} มักทำจากพลาสติกชนิดใด", correct=pick[1],
                         wrongs=tuple(p[1] for p in rng.sample([p for p in PLASTICS if p is not pick], 3)),
                         topic=TOPIC_STRUCTURE, hint=hint)


@question_type(
    "chem.polymer_structure_application",
    display_name={"th": "เลือกพอลิเมอร์ให้เหมาะกับงานจากโครงสร้าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_STRUCTURE,
)
class PolymerStructureApplication(QuestionType):
    """The job asks for a property; the property asks for a chain shape."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        jobs = (
            ("ถุงพลาสติกบางที่ยืดหยุ่นได้ดี", "พอลิเอทิลีนความหนาแน่นต่ำ (LDPE)", BRANCHED),
            ("ขวดแกลลอนที่แข็งแรงและทนแรงกด", "พอลิเอทิลีนความหนาแน่นสูง (HDPE)", LINEAR),
            ("ด้ามกระทะที่ต้องทนความร้อนโดยไม่อ่อนตัว", "เบกาไลต์", NETWORK),
            ("ยางรถยนต์ที่ยืดหยุ่นและคืนรูปได้", "ยางที่ผ่านการวัลคาไนซ์", NETWORK),
            ("จานชามที่ทนความร้อนและไม่หลอม", "เมลามีน", NETWORK),
            ("ขวดน้ำดื่มใสที่เหนียวและเบา", "พอลิเอทิลีนเทเรฟทาเลต (PET)", LINEAR),
            ("ฟิล์มห่ออาหารที่ยืดแนบภาชนะได้", "พอลิเอทิลีนความหนาแน่นต่ำ (LDPE)", BRANCHED),
            ("ท่อน้ำที่แข็งและไม่ผุกร่อน", "พอลิไวนิลคลอไรด์ (PVC)", LINEAR),
            ("กล่องใส่อาหารที่เข้าไมโครเวฟได้", "พอลิโพรพิลีน (PP)", LINEAR),
            ("กาวสองส่วนที่แข็งตัวถาวร", "อีพอกซี", NETWORK),
            ("เต้ารับไฟฟ้าที่ไม่อ่อนตัวเมื่อร้อน", "เบกาไลต์", NETWORK),
        )
        job, right, shape = rng.choice(jobs)
        if rng.random() < 0.5:
            others = sorted({j[1] for j in jobs if j[2] != shape})
            return _labelled(stem=f"ต้องการผลิต{job} ควรเลือกพอลิเมอร์ใด", correct=right,
                             wrongs=tuple(others), topic=TOPIC_STRUCTURE,
                             hint="ดูสมบัติที่งานต้องการ แล้วเลือกโครงสร้างแบบเส้น แบบกิ่ง หรือแบบร่างแหให้ตรง")
        return _labelled(stem=f"{right} ที่ใช้ทำ{job} มีโครงสร้างพอลิเมอร์แบบใด", correct=shape,
                         wrongs=tuple(s for s in SHAPES if s != shape) + (NOT_A_SHAPE,), topic=TOPIC_STRUCTURE,
                         hint="ไม่หลอมเมื่อร้อนหรือยืดแล้วคืนรูป = ร่างแห ยืดหยุ่นนิ่ม = แบบกิ่ง แข็งเหนียว = แบบเส้น")
