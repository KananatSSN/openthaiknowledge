"""แผนภาพแสดงแรง

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.5/2

Sets moved here from: science_wave_d16.
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
from otk.sets._support.science_wave_d16 import FIFTH, LEFT, RIGHT

PROVENANCE = Provenance("original")


DIAGRAM_TOPIC = "แผนภาพแสดงแรง"


def _arrow(size: int, direction: str) -> str:
    return f"ลูกศรยาว {size} ช่องชี้ไป{direction}"


OPPOSITE = {f"ไป{LEFT}": f"ไป{RIGHT}", f"ไป{RIGHT}": f"ไป{LEFT}", "ในทิศขึ้น": "ในทิศลง", "ในทิศลง": "ในทิศขึ้น"}


DIAGRAM_FACTS = (
    ("ในแผนภาพแสดงแรง ความยาวและหัวลูกศรแสดงอะไร", "ความยาวของลูกศรแสดงขนาดของแรง และหัวลูกศรแสดงทิศทางของแรง",
     ("ความยาวของลูกศรแสดงทิศทางของแรง และหัวลูกศรแสดงขนาดของแรง", "ความยาวของลูกศรแสดงมวลของวัตถุ และหัวลูกศรแสดงสีของวัตถุ",
      "ลูกศรทุกเส้นต้องยาวเท่ากัน และหัวลูกศรชี้ขึ้นเสมอ", "ความยาวของลูกศรแสดงเวลาที่แรงกระทำ",
      "หัวลูกศรแสดงจุดที่วัตถุจะหยุด")),
    ("ในแผนภาพ แรงสองแรงที่มีขนาดเท่ากันควรวาดอย่างไร", "ลูกศรยาวเท่ากัน โดยหัวลูกศรชี้ตามทิศของแต่ละแรง",
     ("ลูกศรยาวไม่เท่ากันเสมอ", "วาดเพียงลูกศรเดียว", "ไม่ต้องมีหัวลูกศร", "ลูกศรหนึ่งยาวเป็นสองเท่า", "ลูกศรทั้งสองชี้ขึ้นเสมอ")),
    ("ทำไมต้องกำหนดมาตราส่วน เช่น 1 ช่องแทน 2 นิวตัน ในแผนภาพแสดงแรง", "เพื่อให้ความยาวลูกศรแสดงขนาดของแรงได้ถูกสัดส่วน",
     ("เพื่อให้แผนภาพมีสีสวยงาม", "เพื่อบอกมวลของวัตถุ", "เพื่อให้ลูกศรยาวเท่ากันทุกเส้น", "เพื่อบอกเวลาที่แรงกระทำ",
      "ไม่จำเป็นต้องกำหนด")),
    ("แรงลัพธ์เป็นศูนย์ ในแผนภาพควรแสดงอย่างไร", "ไม่มีลูกศรแรงลัพธ์ เพราะแรงหักล้างกันหมด",
     ("ลูกศรแรงลัพธ์ยาวที่สุด", "ลูกศรแรงลัพธ์ชี้ขึ้น", "ลูกศรแรงลัพธ์ยาวเท่าผลรวมทุกแรง", "ลูกศรแรงลัพธ์ชี้ลง",
      "ลูกศรแรงลัพธ์ยาว 1 ช่องเสมอ")),
)


def _scaled(rng: Random, scale: int, boxes: int, where: str, arrow: str) -> GeneratedQuestion:
    """How long a force is drawn at a given scale."""
    wrongs = [f"ลูกศรยาว {scale * boxes} ช่องชี้{where}" if scale != 1 else f"ลูกศรยาว {boxes + 2} ช่องชี้{where}",
              f"ลูกศรยาว {boxes} ช่องชี้{OPPOSITE[where]}", f"ลูกศรยาว {boxes + scale} ช่องชี้{where}",
              f"ลูกศรยาว {boxes + 1} ช่องชี้{where}"]
    return _labelled(
        stem=f"ถ้าใช้ 1 ช่องแทนแรง {scale} นิวตัน แรง {scale * boxes} นิวตันที่กระทำ{where} ควรวาดอย่างไร",
        correct=arrow,
        wrongs=tuple(w for w in dict.fromkeys(wrongs) if w != arrow)[:3],
        hint="จำนวนช่อง = ขนาดแรง ÷ ค่าที่ 1 ช่องแทน หัวลูกศรชี้ไปทางที่แรงกระทำ",
        topic=DIAGRAM_TOPIC,
    )


DIAGRAM_SCENARIOS = (
    ("แผนภาพหนึ่งมีลูกศรยาว 4 ช่องชี้ไปทางขวาและลูกศรยาว 4 ช่องชี้ไปทางซ้ายกระทำต่อวัตถุที่อยู่นิ่ง ข้อใดสรุปได้ถูกต้อง",
     "แรงลัพธ์เป็นศูนย์ วัตถุจึงอยู่นิ่งต่อไป", ("แรงลัพธ์ยาว 8 ช่องไปทางขวา", "วัตถุจะเคลื่อนที่ไปทางซ้าย", "แผนภาพนี้ผิดเพราะลูกศรยาวเท่ากันไม่ได้")),
    ("นักเรียนวาดแรง 6 นิวตันยาว 3 ช่อง ถ้าใช้มาตราส่วนเดิม แรง 10 นิวตันควรวาดยาวกี่ช่อง",
     "5 ช่อง", ("10 ช่อง", "3 ช่อง", "20 ช่อง")),
    ("เพื่อนวาดแรงลัพธ์ของแรง 5 นิวตันไปทางขวา และ 2 นิวตันไปทางซ้าย เป็นลูกศรยาว 7 ช่องชี้ไปทางขวา ข้อใดแก้ไขได้ถูกต้อง",
     "ลูกศรแรงลัพธ์ควรยาว 3 ช่องชี้ไปทางขวา เพราะแรงทิศตรงข้ามต้องนำมาลบกัน",
     ("ลูกศรควรยาว 7 ช่องชี้ไปทางซ้าย", "ถูกต้องแล้ว", "ลูกศรควรยาว 3 ช่องชี้ไปทางซ้าย")),
)


@question_type(
    "phys.force_diagram_foundation",
    display_name={"th": "บอกสิ่งที่ลูกศรในแผนภาพแรงแสดง"},
    level=FIFTH, subject=SUBJECT, topic=DIAGRAM_TOPIC,
)
class ForceDiagramFoundation(QuestionType):
    """What an arrow stands for, and how long a force is drawn at a given scale."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            stem, right, wrongs = rng.choice(DIAGRAM_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                             hint="ลูกศรยาวกว่าหมายถึงแรงมากกว่า และลูกศรชี้ไปทางที่แรงกระทำ", topic=DIAGRAM_TOPIC)
        if roll < 0.8:
            scale, boxes = rng.choice((1, 2, 5)), rng.randint(2, 9)
            side = rng.choice((LEFT, RIGHT, "ขึ้น", "ลง"))
            where = f"ไป{side}" if side in (LEFT, RIGHT) else f"ใน{'ทิศขึ้น' if side == 'ขึ้น' else 'ทิศลง'}"
            return _scaled(rng, scale, boxes, where, f"ลูกศรยาว {boxes} ช่องชี้{where}")
        return _labelled(
            stem="ในแผนภาพแสดงแรง ความยาวและหัวลูกศรแสดงอะไร",
            correct="ความยาวของลูกศรแสดงขนาดของแรง และหัวลูกศรแสดงทิศทางของแรง",
            wrongs=("ความยาวของลูกศรแสดงทิศทางของแรง และหัวลูกศรแสดงขนาดของแรง",
                    "ความยาวของลูกศรแสดงมวลของวัตถุ และหัวลูกศรแสดงสีของวัตถุ",
                    "ลูกศรทุกเส้นต้องยาวเท่ากัน และหัวลูกศรชี้ขึ้นเสมอ"),
            hint="ลูกศรยาวกว่าหมายถึงแรงมากกว่า และลูกศรชี้ไปทางที่แรงกระทำ",
            topic=DIAGRAM_TOPIC,
        )


@question_type(
    "phys.force_diagram_fluency",
    display_name={"th": "เลือกแผนภาพแสดงแรงและแรงลัพธ์ในแนวเดียวกัน"},
    level=FIFTH, subject=SUBJECT, topic=DIAGRAM_TOPIC,
)
class ForceDiagramFluency(QuestionType):
    """Two forces described; the diagram, one square per newton, with its resultant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        left, right = rng.sample(range(1, 9), 2)
        size = abs(right - left)
        toward = RIGHT if right > left else LEFT
        away = LEFT if toward == RIGHT else RIGHT

        def diagram(a: str, b: str, r: str) -> str:
            return f"แรง: {a} และ {b} / แรงลัพธ์: {r}"

        return _labelled(
            stem=(f"แรง {left} นิวตัน กระทำต่อกล่องไป{LEFT} และแรง {right} นิวตัน ไป{RIGHT} "
                  "ถ้าใช้ความยาว 1 ช่องแทนแรง 1 นิวตัน แผนภาพใดถูกต้อง"),
            correct=diagram(_arrow(left, LEFT), _arrow(right, RIGHT), _arrow(size, toward)),
            wrongs=(diagram(_arrow(left, LEFT), _arrow(right, RIGHT), _arrow(size, away)),
                    diagram(_arrow(left, RIGHT), _arrow(right, LEFT), _arrow(size, away)),
                    diagram(_arrow(left, LEFT), _arrow(right, RIGHT), _arrow(left + right, toward))),
            hint="วาดลูกศรแต่ละแรงตามขนาดและทิศ แรงลัพธ์ยาวเท่าผลต่างและชี้ไปทางแรงที่มากกว่า",
            topic=DIAGRAM_TOPIC,
        )


@question_type(
    "phys.force_diagram_application",
    display_name={"th": "อ่านและตรวจแผนภาพแสดงแรง"},
    level=FIFTH, subject=SUBJECT, topic=DIAGRAM_TOPIC,
)
class ForceDiagramApplication(QuestionType):
    """Authored cases, rescaling an arrow, and reading forces off two drawn arrows."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            per = rng.choice((2, 3, 4, 5))
            first, second = rng.sample(range(2, 10), 2)
            return _labelled(
                stem=(f"นักเรียนวาดแรง {first * per} นิวตันยาว {first} ช่อง ถ้าใช้มาตราส่วนเดิม "
                      f"แรง {second * per} นิวตันควรวาดยาวกี่ช่อง"),
                correct=f"{second} ช่อง",
                wrongs=tuple(f"{w} ช่อง" for w in dict.fromkeys((second * per, first, second + per, second + 1, second + 2, second + 3, first + second)) if w != second)[:3],
                hint="หาก่อนว่า 1 ช่องแทนกี่นิวตัน แล้วนำไปหารขนาดแรงใหม่",
                topic=DIAGRAM_TOPIC,
            )
        if roll < 0.7:
            scale = rng.choice((1, 2, 5))
            a, b = rng.sample(range(1, 10), 2)
            net = (b - a) * scale
            answer = f"{abs(net)} นิวตัน ไป{RIGHT if net > 0 else LEFT}"
            return _labelled(
                stem=(f"แผนภาพใช้ 1 ช่องแทน {scale} นิวตัน มีลูกศรยาว {a} ช่องชี้ไป{LEFT} และลูกศรยาว {b} ช่องชี้ไป{RIGHT} "
                      "กระทำต่อกล่องเดียวกัน แรงลัพธ์เป็นเท่าใด"),
                correct=answer,
                wrongs=tuple(o for o in dict.fromkeys((f"{abs(net)} นิวตัน ไป{LEFT if net > 0 else RIGHT}",
                                                        f"{(a + b) * scale} นิวตัน ไป{RIGHT if net > 0 else LEFT}",
                                                        f"{abs(b - a)} นิวตัน ไป{RIGHT if net > 0 else LEFT}" if scale != 1
                                                        else "0 นิวตัน",
                                                        "0 นิวตัน")) if o != answer)[:3],
                hint="แปลงความยาวลูกศรเป็นนิวตันด้วยมาตราส่วน แล้วลบกันเพราะชี้ทิศตรงข้าม",
                topic=DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, DIAGRAM_SCENARIOS,
            hint="ความยาวลูกศรต้องเป็นสัดส่วนกับขนาดแรง และแรงลัพธ์หาจากการบวกลบตามทิศ",
        ), DIAGRAM_TOPIC)
