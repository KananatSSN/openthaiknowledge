"""แผนผัง แผนที่ และลูกโลก

ภูมิศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ส 5.1 ป.2/2
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.sets._support.geography import COMMUNITY_MAPS, LETTERS, P2, SUBJECT, choices, map_question, stage

PROVENANCE = Provenance("original")


TOPIC = "แผนผัง แผนที่ และลูกโลก"


@question_type(
    "geog.globe_and_map_p2",
    display_name={"th": "บอกสิ่งที่แผนผัง แผนที่ และลูกโลกแสดง"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class GlobeAndMap(ConceptBankType):
    ITEMS = [
        Concept("ลูกโลกจำลองสิ่งใด", "รูปร่างและพื้นผิวของโลก",
                ("ดวงอาทิตย์และดาวเคราะห์", "ห้องเรียนและโรงเรียน", "ท้องฟ้าในเวลากลางคืน")),
        Concept("เส้นที่ลากรอบกลางลูกโลก แบ่งโลกเป็นซีกโลกเหนือและซีกโลกใต้ เรียกว่าอะไร",
                "เส้นศูนย์สูตร", ("เส้นเมริเดียนแรก", "ขั้วโลกเหนือ", "เส้นแบ่งเขตประเทศ")),
        Concept("จุดบนสุดของลูกโลกคือที่ใด", "ขั้วโลกเหนือ",
                ("ขั้วโลกใต้", "เส้นศูนย์สูตร", "ประเทศไทย")),
        Concept("สิ่งใดแสดงพื้นที่ทั้งหมดของโลกได้ในแผ่นเดียว และพับเก็บได้", "แผนที่โลก",
                ("ลูกโลก", "แผนผังห้องเรียน", "รูปถ่ายโรงเรียน")),
        Concept("สิ่งใดแสดงรูปร่างกลมของโลกได้ใกล้เคียงของจริงที่สุด", "ลูกโลก",
                ("แผนที่โลก", "แผนผังโรงเรียน", "รูปถ่ายบ้าน")),
        Concept("บนลูกโลกมีพื้นที่สีน้ำเงินมากกว่าสีอื่น แสดงว่าอย่างไร", "พื้นผิวโลกส่วนใหญ่เป็นน้ำ",
                ("พื้นผิวโลกส่วนใหญ่เป็นภูเขา", "พื้นผิวโลกส่วนใหญ่เป็นป่าไม้",
                 "พื้นผิวโลกส่วนใหญ่เป็นทะเลทราย")),
        Concept("แผนผังต่างจากรูปถ่ายอย่างไร", "แผนผังใช้สัญลักษณ์แทนสิ่งของจริง",
                ("แผนผังแสดงสีเหมือนของจริงทุกอย่าง", "แผนผังต้องถ่ายด้วยกล้องเท่านั้น",
                 "แผนผังแสดงได้เฉพาะสิ่งที่อยู่ไกลมาก")),
        Concept("ถ้าต้องการบอกเพื่อนใหม่ว่าห้องสมุดอยู่ตรงไหนในโรงเรียน ควรใช้สิ่งใด", "แผนผังโรงเรียน",
                ("ลูกโลก", "แผนที่โลก", "ปฏิทิน")),
    ]


# The colours of a physical map or globe and the land or water each shows.
COLOURS = (
    ("สีน้ำเงิน", "พื้นน้ำ เช่น ทะเลและมหาสมุทร"),
    ("สีเขียว", "ที่ราบ"),
    ("สีน้ำตาล", "ภูเขาและที่สูง"),
    ("สีขาว", "บริเวณที่มีหิมะหรือน้ำแข็งปกคลุม"),
)


@question_type(
    "geog.map_colour_p2",
    display_name={"th": "อ่านความหมายของสีบนแผนที่และลูกโลก"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class MapColour(QuestionType):
    def build(self, rng: Random, **params):
        colour, shows = rng.choice(COLOURS)
        hint = "สีบนลูกโลกบอกลักษณะของพื้นผิว: น้ำเงินคือน้ำ เขียวคือที่ราบ น้ำตาลคือที่สูง ขาวคือหิมะ"
        if rng.random() < 0.5:
            return choices(stem=f"บนแผนที่และลูกโลก {colour}แสดงลักษณะใดของพื้นผิวโลก",
                           correct=shows, wrongs=[s for c, s in COLOURS if c != colour],
                           hint=hint, topic=TOPIC)
        return choices(stem=f"บนแผนที่และลูกโลก {shows}แสดงด้วยสีใด",
                       correct=colour, wrongs=[c for c, s in COLOURS if c != colour],
                       hint=hint, topic=TOPIC)


def _nearest(spec, here: int):
    """The place nearest ``here`` when it is clearly nearest: every other
    place at least one square further away, so it can be seen by eye."""
    hx, hy = spec.places[here]
    dist = sorted((((x - hx) ** 2 + (y - hy) ** 2) ** 0.5, i)
                  for i, (x, y) in enumerate(spec.places) if i != here)
    return dist[0][1] if dist[1][0] - dist[0][0] >= 1 else None


NEAREST = tuple((spec, here, near) for spec in COMMUNITY_MAPS for here in range(len(spec.places))
                if (near := _nearest(spec, here)) is not None)


@question_type(
    "geog.map_nearest_p2",
    display_name={"th": "ใช้แผนที่บอกว่าสถานที่ใดอยู่ใกล้ที่สุด"},
    level=P2, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class MapNearest(QuestionType):
    def build(self, rng: Random, **params):
        spec, here, near = rng.choice(NEAREST)
        others = [LETTERS[i] for i in range(len(spec.places)) if i not in (here, near)]
        return map_question(
            spec, stem=f"จากแผนที่ สถานที่ใดอยู่ใกล้ {LETTERS[here]} มากที่สุด",
            correct=LETTERS[near], wrongs=rng.sample(others, 3),
            hint="นับช่องจากสถานที่นั้นไปยังสถานที่อื่นทีละแห่ง สถานที่ที่ห่างน้อยที่สุดคือใกล้ที่สุด",
            topic=TOPIC)
