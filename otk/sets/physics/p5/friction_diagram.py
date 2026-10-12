"""แผนภาพแสดงแรงเสียดทาน

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.5/5

Sets moved here from: science_wave_d17.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d16 import FIFTH

PROVENANCE = Provenance("original")


FRICTION_DIAGRAM_TOPIC = "แผนภาพแสดงแรงเสียดทาน"


FRICTION_DIAGRAM_HINT = "แรงเสียดทานต้านการเคลื่อนที่ จึงมีทิศตรงข้ามกับการเคลื่อนที่ ความยาวลูกศรแสดงขนาดของแรง"


FRICTION_DIAGRAM_FACTS = (
    ("ในแผนภาพแสดงแรง ความยาวของลูกศรแสดงสิ่งใด", "ขนาดของแรง",
     ("ทิศทางของแรง", "มวลของวัตถุ", "ระยะทางที่วัตถุเคลื่อนที่", "เวลาที่แรงกระทำ", "ชนิดของพื้นผิว")),
    ("ในแผนภาพแสดงแรง หัวลูกศรแสดงสิ่งใด", "ทิศทางของแรง",
     ("ขนาดของแรง", "มวลของวัตถุ", "ความเร็วของวัตถุ", "ชนิดของแรง", "ตำแหน่งเริ่มต้นของวัตถุ")),
    ("แรงเสียดทานเกิดขึ้นที่ใด", "ที่ผิวสัมผัสระหว่างวัตถุกับพื้นผิวที่วัตถุเคลื่อนที่หรือพยายามเคลื่อนที่",
     ("ที่จุดศูนย์กลางของวัตถุ", "ในอากาศเหนือวัตถุ", "ที่มือของผู้ดึงเท่านั้น", "ภายในเนื้อของวัตถุ", "ที่ปลายลูกศรแรงดึง")),
    ("กล่องวางนิ่งบนพื้นราบโดยไม่มีใครผลักหรือดึง ต้องวาดแรงเสียดทานหรือไม่", "ไม่ต้อง เพราะไม่มีแรงที่พยายามทำให้กล่องเลื่อน",
     ("ต้องวาด ชี้ไปทางซ้ายเสมอ", "ต้องวาด ชี้ไปทางขวาเสมอ", "ต้องวาด ชี้ขึ้น", "ต้องวาด ยาวเท่าน้ำหนักของกล่อง",
      "ต้องวาด ชี้ลงพื้น")),
    ("แรงสองแรงในแนวเดียวกันที่มีขนาดเท่ากันแต่ทิศตรงข้าม ควรวาดลูกศรอย่างไร", "ยาวเท่ากัน หัวลูกศรชี้ออกในทิศตรงข้ามกัน",
     ("ยาวไม่เท่ากัน ชี้ทางเดียวกัน", "ยาวเท่ากัน ชี้ทางเดียวกัน", "วาดเพียงลูกศรเดียว", "ลูกศรหนึ่งยาวเป็นสองเท่าของอีกลูกศร",
      "ไม่ต้องมีหัวลูกศร")),
)


FRICTION_DIAGRAM_SCENARIOS = (
    ("แผนภาพแสดงแรงดึง 6 ช่องไปทางขวา และแรงเสียดทาน 6 ช่องไปทางซ้าย กระทำต่อกล่องที่กำลังเคลื่อนที่ ข้อใดสรุปได้ถูกต้อง",
     "แรงลัพธ์เป็นศูนย์ กล่องเคลื่อนที่ด้วยความเร็วคงเดิม",
     ("กล่องเร่งขึ้นไปทางขวา", "กล่องหยุดทันที", "แผนภาพผิดเพราะแรงเสียดทานต้องยาวกว่าแรงดึงเสมอ")),
    ("เพื่อนวาดแรงเสียดทานของลูกบอลที่กลิ้งไปทางซ้ายเป็นลูกศรชี้ไปทางซ้าย ข้อใดแก้ไขได้ถูกต้อง",
     "ลูกศรแรงเสียดทานควรชี้ไปทางขวา เพราะต้านการเคลื่อนที่ของลูกบอล",
     ("ถูกต้องแล้ว", "ลูกศรควรชี้ลงพื้น", "ไม่ต้องวาดแรงเสียดทานกับวัตถุที่กลิ้ง")),
    ("กล่องบนพื้นถูกผลักไปทางขวาด้วยแรง 5 นิวตัน แต่ยังอยู่นิ่ง แผนภาพควรแสดงแรงเสียดทานอย่างไร",
     "ลูกศรยาวเท่าแรงผลัก 5 นิวตัน ชี้ไปทางซ้าย เพราะแรงเสียดทานต้านไว้พอดี กล่องจึงอยู่นิ่ง",
     ("ไม่มีแรงเสียดทานเพราะกล่องไม่เคลื่อนที่", "ลูกศรยาว 10 นิวตันชี้ไปทางซ้าย", "ลูกศรยาว 5 นิวตันชี้ไปทางขวา")),
)


@question_type(
    "phys.friction_diagram_foundation",
    display_name={"th": "บอกทิศของแรงเสียดทานในแผนภาพ"},
    level=FIFTH, subject=SUBJECT, topic=FRICTION_DIAGRAM_TOPIC,
)
class FrictionDiagramFoundation(QuestionType):
    """Which way the friction arrow points, how long a force is drawn, and diagram facts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            stem, right, wrongs = rng.choice(FRICTION_DIAGRAM_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                             hint=FRICTION_DIAGRAM_HINT, topic=FRICTION_DIAGRAM_TOPIC)
        if roll < 0.55:
            scale, boxes = rng.choice((1, 2, 5)), rng.randint(2, 8)
            force = scale * boxes
            wrongs = [force, boxes + scale, boxes * 2 if scale != 2 else boxes + 1, boxes + 2, boxes + 3]
            return _labelled(
                stem=f"ถ้าใช้ 1 ช่องแทน {scale} นิวตัน ต้องวาดลูกศรแรงเสียดทาน {force} นิวตันยาวกี่ช่อง",
                correct=f"{boxes} ช่อง",
                wrongs=tuple(f"{w} ช่อง" for w in list(dict.fromkeys(w for w in wrongs if w != boxes))[:3]),
                hint="จำนวนช่อง = ขนาดแรง ÷ ขนาดแรงที่ 1 ช่องแทน",
                topic=FRICTION_DIAGRAM_TOPIC,
            )
        moving = rng.choice(("ทางขวา", "ทางซ้าย"))
        against = "ทางซ้าย" if moving == "ทางขวา" else "ทางขวา"
        thing, verb = rng.choice((("กล่อง", "ไถล"), ("ลูกบอล", "กลิ้ง"), ("รถของเล่น", "แล่น"),
                                  ("หนังสือ", "ไถล"), ("เก้าอี้", "ถูกลาก"), ("ก้อนน้ำแข็ง", "ไถล")))
        return _labelled(
            stem=f"{thing}กำลัง{verb}ไป{moving}บนพื้น ในแผนภาพ ลูกศรแสดงแรงเสียดทานควรชี้ไปทางใด",
            correct=f"ชี้ไป{against} ตรงข้ามกับทิศที่{thing}เคลื่อนที่",
            wrongs=(f"ชี้ไป{moving} ทิศเดียวกับที่{thing}เคลื่อนที่",
                    "ชี้ขึ้นในแนวดิ่ง",
                    "ไม่ต้องวาด เพราะแรงเสียดทานไม่มีทิศ"),
            hint="แรงเสียดทานต้านการเคลื่อนที่ จึงมีทิศตรงข้ามกับการเคลื่อนที่",
            topic=FRICTION_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.friction_diagram_fluency",
    display_name={"th": "เลือกแผนภาพแสดงแรงดึงและแรงเสียดทาน"},
    level=FIFTH, subject=SUBJECT, topic=FRICTION_DIAGRAM_TOPIC,
)
class FrictionDiagramFluency(QuestionType):
    """A pull and a friction force; the diagram drawn to scale."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pull = rng.randint(4, 10)
        friction = rng.randint(1, pull - 1)

        def diagram(p: int, p_dir: str, f: int, f_dir: str) -> str:
            return f"แรงดึง: ลูกศรยาว {p} ช่องชี้ไป{p_dir} / แรงเสียดทาน: ลูกศรยาว {f} ช่องชี้ไป{f_dir}"

        return _labelled(
            stem=(f"นักเรียนดึงกล่องไปทางขวาด้วยแรง {pull} นิวตัน กล่องเคลื่อนที่ไปทางขวา และมีแรงเสียดทาน {friction} นิวตัน "
                  "ถ้าใช้ 1 ช่องแทน 1 นิวตัน แผนภาพใดถูกต้อง"),
            correct=diagram(pull, "ทางขวา", friction, "ทางซ้าย"),
            wrongs=(diagram(pull, "ทางขวา", friction, "ทางขวา"),
                    diagram(friction, "ทางขวา", pull, "ทางซ้าย"),
                    diagram(pull, "ทางซ้าย", friction, "ทางขวา"),
                    # Lengths swapped and a direction wrong as well.
                    diagram(friction, "ทางขวา", pull, "ทางขวา"),
                    diagram(friction, "ทางซ้าย", pull, "ทางขวา")),
            hint="ลูกศรแรงดึงชี้ตามทิศที่ดึง ลูกศรแรงเสียดทานชี้ตรงข้ามการเคลื่อนที่ ความยาวตามขนาดของแรง",
            topic=FRICTION_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.friction_diagram_application",
    display_name={"th": "อ่านและแก้ไขแผนภาพแสดงแรงเสียดทาน"},
    level=FIFTH, subject=SUBJECT, topic=FRICTION_DIAGRAM_TOPIC,
)
class FrictionDiagramApplication(QuestionType):
    """Authored cases, what a pull-and-friction pair does, and reading a scale."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            side = rng.choice(("ทางขวา", "ทางซ้าย"))
            back = "ทางซ้าย" if side == "ทางขวา" else "ทางขวา"
            pull = rng.randint(3, 12)
            friction = rng.choice((pull, max(1, pull - rng.randint(1, 3)), pull + rng.randint(1, 3)))
            answer = ("เคลื่อนที่ด้วยความเร็วคงเดิม" if friction == pull else
                      "เคลื่อนที่เร็วขึ้น" if pull > friction else "เคลื่อนที่ช้าลง")
            return _labelled(
                stem=(f"กล่องกำลังเคลื่อนที่ไป{side} แผนภาพแสดงแรงดึง {pull} ช่องชี้ไป{side} "
                      f"และแรงเสียดทาน {friction} ช่องชี้ไป{back} กล่องจะเคลื่อนที่อย่างไรต่อไป"),
                correct=answer,
                wrongs=tuple(w for w in ("เคลื่อนที่ด้วยความเร็วคงเดิม", "เคลื่อนที่เร็วขึ้น", "เคลื่อนที่ช้าลง",
                                         f"เปลี่ยนไปเคลื่อนที่{back}ทันที") if w != answer),
                hint="เทียบความยาวลูกศรแรงดึงกับแรงเสียดทาน เท่ากันความเร็วคงเดิม แรงดึงยาวกว่าเร็วขึ้น แรงเสียดทานยาวกว่าช้าลง",
                topic=FRICTION_DIAGRAM_TOPIC,
            )
        if roll < 0.7:
            scale, boxes = rng.choice((2, 5, 10)), rng.randint(2, 9)
            force = scale * boxes
            wrongs = [boxes, boxes + scale, force + scale, force * 2]
            return _labelled(
                stem=(f"แผนภาพใช้ 1 ช่องแทน {scale} นิวตัน ลูกศรแรงเสียดทานยาว {boxes} ช่อง "
                      "แรงเสียดทานมีขนาดเท่าใด"),
                correct=f"{force} นิวตัน",
                wrongs=tuple(f"{w} นิวตัน" for w in list(dict.fromkeys(w for w in wrongs if w != force))[:3]),
                hint="ขนาดแรง = จำนวนช่อง × ขนาดแรงที่ 1 ช่องแทน",
                topic=FRICTION_DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FRICTION_DIAGRAM_SCENARIOS,
            hint="แรงเสียดทานชี้ตรงข้ามการเคลื่อนที่หรือแนวโน้มการเคลื่อนที่ และขนาดดูได้จากความยาวลูกศร",
        ), FRICTION_DIAGRAM_TOPIC)
