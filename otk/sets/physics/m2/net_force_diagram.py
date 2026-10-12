"""แผนภาพแสดงแรงลัพธ์

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/2

Sets moved here from: science_wave_d18.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.force_diagrams import NETFORCE_SPECS, diagram_question, magnitude_phrase
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


DIAGRAM_TOPIC = "แผนภาพแสดงแรงลัพธ์"


DIAGRAM_SCENARIOS = (
    ("แผนภาพมีลูกศร 5 ช่องและ 3 ช่องชี้ไปทางขวา และลูกศร 8 ช่องชี้ไปทางซ้าย ข้อใดสรุปได้ถูกต้อง",
     "แรงลัพธ์เป็นศูนย์ ไม่ต้องวาดลูกศรแรงลัพธ์", ("แรงลัพธ์ 16 ช่องไปทางขวา", "แรงลัพธ์ 8 ช่องไปทางซ้าย", "แรงลัพธ์ 2 ช่องไปทางขวา")),
    ("เพื่อนวาดแรงลัพธ์ของแรง 9 นิวตันไปทางซ้ายและ 4 นิวตันไปทางขวาเป็นลูกศร 13 ช่องไปทางซ้าย ข้อใดแก้ได้ถูกต้อง",
     "ลูกศรควรยาว 5 ช่องชี้ไปทางซ้าย", ("ลูกศรควรยาว 5 ช่องชี้ไปทางขวา", "ถูกต้องแล้ว", "ลูกศรควรยาว 13 ช่องชี้ไปทางขวา")),
    ("ถ้ามาตราส่วน 1 ช่องแทน 2 นิวตัน ลูกศรแรงลัพธ์ยาว 6 ช่อง แรงลัพธ์มีขนาดเท่าใด",
     "12 นิวตัน", ("6 นิวตัน", "3 นิวตัน", "8 นิวตัน")),
)


@question_type(
    "phys.net_force_diagram_foundation",
    display_name={"th": "บอกหลักการวาดแรงลัพธ์ในแผนภาพ"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=DIAGRAM_TOPIC,
)
class NetForceDiagramFoundation(QuestionType):
    """How a resultant arrow is drawn, in words or for two given forces."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.7:
            a, b = rng.randint(2, 15), rng.randint(2, 15)
            first, second = rng.sample(("ขวา", "ซ้าย"), 2) if rng.random() < 0.7 else (("ขวา",) * 2 if rng.random() < 0.5 else ("ซ้าย",) * 2)
            if first == second:
                answer = f"ยาว {a + b} ช่อง ชี้ไปทาง{first}"
                wrongs = (f"ยาว {abs(a - b) or a + b + 2} ช่อง ชี้ไปทาง{first}", f"ยาว {a + b} ช่อง ชี้ไปทาง{'ซ้าย' if first == 'ขวา' else 'ขวา'}",
                          "ไม่ต้องวาด เพราะแรงลัพธ์เป็นศูนย์", f"ยาว {max(a, b)} ช่อง ชี้ไปทาง{first}")
            else:
                net = a - b
                answer = ("ไม่ต้องวาด เพราะแรงลัพธ์เป็นศูนย์" if net == 0 else
                          f"ยาว {abs(net)} ช่อง ชี้ไปทาง{first if net > 0 else second}")
                wrongs = (f"ยาว {a + b} ช่อง ชี้ไปทาง{first if net >= 0 else second}",
                          f"ยาว {abs(net) or a} ช่อง ชี้ไปทาง{second if net >= 0 else first}",
                          "ไม่ต้องวาด เพราะแรงลัพธ์เป็นศูนย์", f"ยาว {max(a, b)} ช่อง ชี้ไปทาง{first if net >= 0 else second}")
            return _labelled(
                stem=(f"วัตถุถูกแรง {a} นิวตันกระทำไปทาง{first} และแรง {b} นิวตันกระทำไปทาง{second} ในแนวเดียวกัน "
                      "ถ้าใช้ 1 ช่องแทน 1 นิวตัน ควรวาดลูกศรแรงลัพธ์อย่างไร"),
                correct=answer,
                wrongs=tuple([w for w in dict.fromkeys(wrongs) if w != answer]),
                hint="แรงทิศเดียวกันนำมาบวกกัน แรงทิศตรงข้ามนำมาลบกัน ลูกศรแรงลัพธ์ชี้ไปทางแรงที่มากกว่า",
                topic=DIAGRAM_TOPIC,
            )
        return _labelled(
            stem="ในแผนภาพแสดงแรงหลายแรงในแนวเดียวกัน ลูกศรแรงลัพธ์วาดอย่างไร",
            correct="ยาวเท่าผลรวมของแรงที่คิดทิศ (ทิศเดียวกันบวก ทิศตรงข้ามลบ) และชี้ไปในทิศของผลลัพธ์นั้น",
            wrongs=("ยาวเท่าผลรวมของขนาดแรงทุกแรงโดยไม่คิดทิศ",
                    "ยาวเท่าแรงที่มากที่สุดเพียงแรงเดียว",
                    "ชี้ไปทางแรงที่น้อยที่สุดเสมอ"),
            hint="แรงลัพธ์คำนึงถึงทั้งขนาดและทิศของทุกแรง",
            topic=DIAGRAM_TOPIC,
        )


@question_type(
    "phys.net_force_diagram_fluency",
    display_name={"th": "อ่านแรงลัพธ์จากแผนภาพแสดงแรงในแนวเดียวกัน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=DIAGRAM_TOPIC,
)
class NetForceDiagramFluency(QuestionType):
    """The student is shown the drawn diagram and reads the resultant off it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(NETFORCE_SPECS)
        net = spec.horizontal
        total = sum(arrow.newtons for arrow in spec.arrows)
        biggest = max(arrow.newtons for arrow in spec.arrows)
        # The three standard misreadings: flipping the direction, adding every
        # arrow regardless of where it points, and reading off the longest one.
        wrongs = [magnitude_phrase(-net) if net else f"แรงลัพธ์ {total} นิวตัน ไปทางขวา",
                  f"แรงลัพธ์ {total} นิวตัน ไปทาง{'ขวา' if net >= 0 else 'ซ้าย'}",
                  f"แรงลัพธ์ {biggest} นิวตัน ไปทาง{'ขวา' if net >= 0 else 'ซ้าย'}",
                  "แรงลัพธ์เป็นศูนย์", f"แรงลัพธ์ {total + 2} นิวตัน ไปทางซ้าย"]
        correct = magnitude_phrase(net)
        return diagram_question(
            spec,
            stem="จากแผนภาพ แรงลัพธ์ที่กระทำต่อวัตถุมีขนาดและทิศทางอย่างไร",
            correct=correct,
            wrongs=tuple(dict.fromkeys(w for w in wrongs if w != correct))[:3],
            hint="ความยาวลูกศรแปรตามขนาดของแรง รวมแรงที่ชี้ไปทางขวา แล้วลบด้วยแรงที่ชี้ไปทางซ้าย",
            topic=DIAGRAM_TOPIC,
        )


@question_type(
    "phys.net_force_diagram_application",
    display_name={"th": "อ่านและแก้ไขแผนภาพแรงลัพธ์"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=DIAGRAM_TOPIC,
)
class NetForceDiagramApplication(QuestionType):
    """Authored cases, reading a resultant off a scale, and correcting a summed arrow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            scale, boxes = rng.choice((2, 5, 10)), rng.randint(2, 9)
            return numeric(
                stem=f"ถ้ามาตราส่วน 1 ช่องแทน {scale} นิวตัน ลูกศรแรงลัพธ์ยาว {boxes} ช่อง แรงลัพธ์มีขนาดเท่าใด",
                answer=scale * boxes, wrongs=(boxes, scale + boxes, boxes * scale // 2 if scale != 2 else boxes + 4),
                unit="นิวตัน", topic=DIAGRAM_TOPIC, hint="ขนาดแรง = จำนวนช่อง × ขนาดแรงที่ 1 ช่องแทน",
            )
        if roll < 0.7:
            a, b = rng.sample(range(3, 16), 2)
            big, small = ("ซ้าย", "ขวา") if a > b else ("ขวา", "ซ้าย")
            answer = f"ลูกศรควรยาว {abs(a - b)} ช่องชี้ไปทาง{big}"
            wrongs = (f"ลูกศรควรยาว {abs(a - b)} ช่องชี้ไปทาง{small}", "ถูกต้องแล้ว",
                      f"ลูกศรควรยาว {a + b} ช่องชี้ไปทาง{small}", f"ลูกศรควรยาว {max(a, b)} ช่องชี้ไปทาง{big}")
            return _labelled(
                stem=(f"เพื่อนวาดแรงลัพธ์ของแรง {a} นิวตันไปทางซ้ายและ {b} นิวตันไปทางขวาเป็นลูกศร {a + b} ช่องไปทาง{big} "
                      "โดยใช้ 1 ช่องแทน 1 นิวตัน ข้อใดแก้ได้ถูกต้อง"),
                correct=answer, wrongs=tuple(wrongs),
                hint="แรงทิศตรงข้ามต้องลบกัน แรงลัพธ์ชี้ไปทางแรงที่มากกว่า", topic=DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, DIAGRAM_SCENARIOS,
            hint="แปลงความยาวเป็นขนาดแรงด้วยมาตราส่วน แล้วรวมแรงโดยคิดทิศ",
        ), DIAGRAM_TOPIC)
