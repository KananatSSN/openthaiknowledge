"""แผนภาพแสดงแรงเสียดทานและแรงอื่น ๆ

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/8

Sets moved here from: science_wave_d20.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.force_diagrams import FRICTION_SPECS, diagram_question
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


FRICTION_FORCES_TOPIC = "แผนภาพแสดงแรงเสียดทานและแรงอื่น ๆ"


FRICTION_FORCES_HINT = "มีแรงในแนวราบ (แรงดึงหรือผลัก แรงเสียดทาน) และแนวดิ่ง (น้ำหนัก แรงที่พื้นดัน) แรงเสียดทานชี้ตรงข้ามการเคลื่อนที่"


FRICTION_FORCES_SCENARIOS = (
    ("แผนภาพของกล่องที่ถูกลากมีแรงดึง 10 ช่องไปทางขวา และแรงเสียดทาน 6 ช่องไปทางซ้าย กล่องจะเคลื่อนที่อย่างไร",
     "เคลื่อนที่ไปทางขวาเร็วขึ้น เพราะแรงลัพธ์ 4 ช่องไปทางขวา",
     ("เคลื่อนที่ไปทางซ้าย", "อยู่นิ่ง", "เคลื่อนที่ด้วยความเร็วคงที่ เพราะแรงลัพธ์เป็นศูนย์")),
    ("เพื่อนวาดแผนภาพกล่องที่ไถลลงทางลาดโดยให้ลูกศรแรงเสียดทานชี้ลงตามทางลาด ข้อใดแก้ไขได้ถูกต้อง",
     "แรงเสียดทานควรชี้ขึ้นตามทางลาด เพราะต้านการเคลื่อนที่ที่ลงตามทางลาด",
     ("ถูกต้องแล้ว", "แรงเสียดทานควรชี้ตั้งฉากกับทางลาด", "ไม่ต้องวาดแรงเสียดทานบนทางลาด")),
    ("ลากกล่องด้วยความเร็วคงที่ แผนภาพควรมีลูกศรแรงดึงและแรงเสียดทานเป็นอย่างไร",
     "ยาวเท่ากันและชี้ในทิศตรงข้ามกัน", ("แรงดึงยาวกว่าแรงเสียดทานเสมอ", "ชี้ไปทางเดียวกัน", "ไม่ต้องมีแรงเสียดทาน")),
)


@question_type(
    "phys.friction_forces_diagram_foundation",
    display_name={"th": "บอกแรงทั้งหมดที่กระทำต่อกล่องที่ถูกลากบนพื้น"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_FORCES_TOPIC,
)
class FrictionForcesDiagramFoundation(QuestionType):
    """Which forces a box's diagram shows, and how big the floor's push is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        thing = rng.choice(("กล่อง", "ลังไม้", "ตู้", "กระเป๋าเดินทาง", "โต๊ะ"))
        if roll < 0.4:
            side = rng.choice(("ขวา", "ซ้าย"))
            back = "ซ้าย" if side == "ขวา" else "ขวา"
            verb = rng.choice(("ถูกลาก", "ถูกผลัก"))
            force = "แรงดึง" if verb == "ถูกลาก" else "แรงผลัก"
            return _labelled(
                stem=f"{thing}{verb}ให้ไถลไปทาง{side}บนพื้นราบ แผนภาพควรแสดงแรงใดบ้าง",
                correct=f"{force}ไปทาง{side} แรงเสียดทานไปทาง{back} น้ำหนักชี้ลง และแรงที่พื้นดันชี้ขึ้น",
                wrongs=(f"{force}ไปทาง{side} แรงเสียดทานไปทาง{side} น้ำหนักชี้ลง และแรงที่พื้นดันชี้ขึ้น",
                        f"{force}ไปทาง{side}และแรงเสียดทานไปทาง{back}เท่านั้น",
                        f"{force}ไปทาง{side} แรงเสียดทานไปทาง{back} น้ำหนักชี้ขึ้น และแรงที่พื้นดันชี้ลง",
                        # Two things wrong at once.
                        f"{force}ไปทาง{side} แรงเสียดทานไปทาง{side} น้ำหนักชี้ขึ้น และแรงที่พื้นดันชี้ลง",
                        f"{force}ไปทาง{back} แรงเสียดทานไปทาง{side} น้ำหนักชี้ลง และแรงที่พื้นดันชี้ขึ้น"),
                hint=FRICTION_FORCES_HINT, topic=FRICTION_FORCES_TOPIC,
            )
        if roll < 0.55:
            return _labelled(
                stem=f"{thing}วางนิ่งบนพื้นราบ ไม่มีใครผลักหรือดึง แผนภาพควรแสดงแรงใดบ้าง",
                correct="น้ำหนักชี้ลงและแรงที่พื้นดันชี้ขึ้นเท่านั้น",
                wrongs=("น้ำหนักชี้ลง แรงที่พื้นดันชี้ขึ้น และแรงเสียดทานไปทางซ้าย", "น้ำหนักชี้ลงเพียงแรงเดียว",
                        "ไม่มีแรงใดกระทำเพราะวัตถุอยู่นิ่ง",
                        "น้ำหนักชี้ขึ้น แรงที่พื้นดันชี้ลง และแรงเสียดทานไปทางซ้าย",
                        "น้ำหนักชี้ขึ้นและแรงที่พื้นดันชี้ลงเท่านั้น"),
                hint=FRICTION_FORCES_HINT, topic=FRICTION_FORCES_TOPIC,
            )
        if roll < 0.85:
            weight = rng.randrange(20, 401, 10)
            return _labelled(
                stem=f"{thing}หนัก {weight} นิวตัน ถูกลากไปตามพื้นราบ แรงที่พื้นดัน{thing}มีขนาดและทิศทางอย่างไร",
                correct=f"{weight} นิวตัน ชี้ขึ้น",
                wrongs=(f"{weight} นิวตัน ชี้ลง", f"{weight * 2} นิวตัน ชี้ขึ้น", "0 นิวตัน เพราะ" + thing + "เคลื่อนที่",
                        f"{weight * 2} นิวตัน ชี้ลง", f"{weight // 2} นิวตัน ชี้ลง"),
                hint="วัตถุไม่จมลงในพื้นและไม่ลอยขึ้น แรงที่พื้นดันจึงเท่ากับน้ำหนักและมีทิศตรงข้าม",
                topic=FRICTION_FORCES_TOPIC,
            )
        return _labelled(
            stem="กล่องถูกลากไปทางขวาบนพื้น แผนภาพควรแสดงแรงใดบ้าง",
            correct="แรงดึงไปทางขวา แรงเสียดทานไปทางซ้าย น้ำหนักชี้ลง และแรงที่พื้นดันกล่องชี้ขึ้น",
            wrongs=("แรงดึงไปทางขวาเพียงแรงเดียว",
                    "แรงดึงไปทางขวา แรงเสียดทานไปทางขวา และน้ำหนักชี้ขึ้น",
                    "แรงเสียดทานไปทางซ้ายและแรงที่พื้นดันกล่องชี้ลง"),
            hint="มีแรงในแนวราบ (แรงดึง แรงเสียดทาน) และแนวดิ่ง (น้ำหนัก แรงที่พื้นดัน)",
            topic=FRICTION_FORCES_TOPIC,
        )


@question_type(
    "phys.friction_forces_diagram_fluency",
    display_name={"th": "อ่านแรงลัพธ์และการเคลื่อนที่จากแผนภาพแรงเสียดทาน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_FORCES_TOPIC,
)
class FrictionForcesDiagramFluency(QuestionType):
    """The student is shown all four forces drawn and reads the motion off them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(FRICTION_SPECS)
        push = spec.of("P").newtons
        friction = spec.of("f").newtons
        weight = spec.of("W").newtons
        net = spec.horizontal
        balanced = net == 0
        correct = ("แรงลัพธ์ในแนวราบเป็นศูนย์ กล่องจึงอยู่นิ่งหรือเคลื่อนที่ด้วยความเร็วคงที่" if balanced else
                   f"แรงลัพธ์ในแนวราบ {net} นิวตัน ไปทางขวา กล่องจึงเคลื่อนที่ไปทางขวาเร็วขึ้น")
        wrongs = [
            # Adding the opposing pair instead of subtracting, ignoring friction,
            # and dragging the vertical pair into a horizontal answer.
            f"แรงลัพธ์ในแนวราบ {push + friction} นิวตัน ไปทางขวา เพราะแรงเสียดทานรวมกับแรงผลัก กล่องจึงเร็วขึ้น",
            f"แรงลัพธ์ในแนวราบ {push} นิวตัน ไปทางขวา เพราะแรงเสียดทานไม่มีผล กล่องจึงเร็วขึ้น",
            f"แรงลัพธ์ {weight} นิวตัน ชี้ลง กล่องจึงจมลงในพื้นแทนการเคลื่อนที่",
            ("แรงลัพธ์ในแนวราบ 2 นิวตัน ไปทางซ้าย กล่องจึงเคลื่อนที่ไปทางซ้ายเร็วขึ้น" if balanced else
             "แรงลัพธ์ในแนวราบเป็นศูนย์ กล่องจึงอยู่นิ่งหรือเคลื่อนที่ด้วยความเร็วคงที่"),
        ]
        return diagram_question(
            spec,
            stem="จากแผนภาพ ข้อใดอธิบายแรงลัพธ์และการเคลื่อนที่ของกล่องได้ถูกต้อง",
            correct=correct,
            wrongs=tuple(dict.fromkeys(w for w in wrongs if w != correct))[:3],
            hint="แรงในแนวดิ่งหักล้างกันอยู่แล้ว ให้เทียบแรงผลักกับแรงเสียดทานในแนวราบ",
            topic=FRICTION_FORCES_TOPIC,
        )


@question_type(
    "phys.friction_forces_diagram_application",
    display_name={"th": "อ่านและแก้ไขแผนภาพแรงเสียดทานและแรงอื่น"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_FORCES_TOPIC,
)
class FrictionForcesDiagramApplication(QuestionType):
    """Authored cases, steady dragging, and an unbalanced pull with numbers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        thing = rng.choice(("กล่อง", "ลังไม้", "ตู้", "เลื่อน", "ถังน้ำ"))
        if roll < 0.35:
            pull = rng.randrange(5, 121, 5)
            side = rng.choice(("ขวา", "ซ้าย"))
            back = "ซ้าย" if side == "ขวา" else "ขวา"
            return _labelled(
                stem=f"ลาก{thing}ไปทาง{side}ด้วยแรง {pull} นิวตัน {thing}เคลื่อนที่ด้วยความเร็วคงที่ ในแผนภาพ แรงเสียดทานควรเป็นเท่าใด",
                correct=f"{pull} นิวตัน ไปทาง{back}",
                wrongs=(f"{pull} นิวตัน ไปทาง{side}", f"{pull * 2} นิวตัน ไปทาง{back}", f"0 นิวตัน เพราะ{thing}เคลื่อนที่อยู่แล้ว",
                        f"{pull * 2} นิวตัน ไปทาง{side}"),  # wrong size and wrong direction
                hint="ความเร็วคงที่หมายถึงแรงลัพธ์เป็นศูนย์ แรงเสียดทานจึงเท่ากับแรงลากและมีทิศตรงข้าม",
                topic=FRICTION_FORCES_TOPIC,
            )
        if roll < 0.7:
            pull = rng.randrange(10, 121, 5)
            friction = rng.randrange(5, pull, 5)
            return _labelled(
                stem=(f"แผนภาพของ{thing}ที่ถูกลากไปทางขวามีแรงดึง {pull} นิวตันไปทางขวา และแรงเสียดทาน {friction} นิวตันไปทางซ้าย "
                      f"{thing}จะเคลื่อนที่อย่างไร"),
                correct=f"เคลื่อนที่ไปทางขวาเร็วขึ้น เพราะแรงลัพธ์ {pull - friction} นิวตันไปทางขวา",
                wrongs=(f"เคลื่อนที่ไปทางขวาเร็วขึ้น เพราะแรงลัพธ์ {pull + friction} นิวตันไปทางขวา",
                        f"เคลื่อนที่ไปทางขวาช้าลง เพราะแรงลัพธ์ {pull - friction} นิวตันไปทางซ้าย",
                        "เคลื่อนที่ด้วยความเร็วคงที่ เพราะแรงลัพธ์เป็นศูนย์",
                        f"เคลื่อนที่ไปทางขวาช้าลง เพราะแรงลัพธ์ {pull + friction} นิวตันไปทางซ้าย"),
                hint="แรงดึงลบแรงเสียดทานได้แรงลัพธ์ในแนวราบ วัตถุเร่งไปตามทิศของแรงลัพธ์",
                topic=FRICTION_FORCES_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FRICTION_FORCES_SCENARIOS,
            hint="แรงเสียดทานชี้ตรงข้ามการเคลื่อนที่ และความเร็วคงที่หมายถึงแรงลัพธ์เป็นศูนย์",
        ), FRICTION_FORCES_TOPIC)
