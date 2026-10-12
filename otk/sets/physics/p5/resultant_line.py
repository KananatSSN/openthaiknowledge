"""แรงลัพธ์ในแนวเดียวกัน

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.5/1

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


RESULTANT_TOPIC = "แรงลัพธ์ในแนวเดียวกัน"


def _resultant(left: int, right: int) -> str:
    if left == right:
        return "0 นิวตัน"
    return f"{abs(right - left)} นิวตัน ไป{RIGHT if right > left else LEFT}"


RESULTANT_SCENARIOS = (
    ("ในการชักเย่อ ทีม ก ออกแรงรวม 450 นิวตัน ทีม ข ออกแรงรวม 450 นิวตัน เชือกจะเป็นอย่างไร",
     "เชือกอยู่นิ่ง เพราะแรงลัพธ์เป็น 0 นิวตัน",
     ("เชือกเคลื่อนที่ไปทางทีม ก ด้วยแรง 900 นิวตัน", "เชือกเคลื่อนที่ไปทางทีม ข", "เชือกขาดทันทีเสมอ")),
    ("กล่องอยู่นิ่งบนพื้นลื่น มีแรง 7 นิวตันดึงไปทางขวา ต้องออกแรงไปทางซ้ายเท่าใดกล่องจึงจะอยู่นิ่งต่อไป",
     "7 นิวตัน", ("14 นิวตัน", "0 นิวตัน", "3.5 นิวตัน")),
    ("นักเรียนสองคนผลักตู้ไปทางขวาด้วยแรง 30 และ 25 นิวตัน อีกคนหนึ่งผลักไปทางซ้ายด้วยแรง 40 นิวตัน แรงลัพธ์เป็นเท่าใด",
     "15 นิวตัน ไปทางขวา", ("95 นิวตัน ไปทางขวา", "15 นิวตัน ไปทางซ้าย", "5 นิวตัน ไปทางขวา")),
)


@question_type(
    "phys.resultant_line_foundation",
    display_name={"th": "หาแรงลัพธ์ของแรงสองแรงในแนวเดียวกัน"},
    level=FIFTH, subject=SUBJECT, topic=RESULTANT_TOPIC,
)
class ResultantLineFoundation(QuestionType):
    """Two forces on a line; their resultant, size and direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.sample(range(2, 13), 2)
        same = rng.random() < 0.5
        if same:
            direction = rng.choice((LEFT, RIGHT))
            stem = f"แรง {a} นิวตัน และแรง {b} นิวตัน กระทำต่อวัตถุไป{direction}ทั้งคู่ แรงลัพธ์เป็นเท่าใด"
            correct = f"{a + b} นิวตัน ไป{direction}"
            other = RIGHT if direction == LEFT else LEFT
            wrongs = (f"{abs(a - b)} นิวตัน ไป{direction}", f"{a + b} นิวตัน ไป{other}", "0 นิวตัน",
                      f"{abs(a - b)} นิวตัน ไป{other}")  # wrong size and wrong direction
        else:
            stem = f"แรง {a} นิวตัน กระทำต่อวัตถุไป{LEFT} และแรง {b} นิวตัน ไป{RIGHT} แรงลัพธ์เป็นเท่าใด"
            correct = _resultant(a, b)
            flipped = f"{abs(a - b)} นิวตัน ไป{LEFT if b > a else RIGHT}"
            wrongs = (f"{a + b} นิวตัน ไป{RIGHT if b > a else LEFT}", flipped, "0 นิวตัน",
                      f"{a + b} นิวตัน ไป{LEFT if b > a else RIGHT}")  # wrong size and wrong direction
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="แรงทิศเดียวกันนำมาบวกกัน แรงทิศตรงข้ามนำมาลบกัน แรงลัพธ์ไปทางแรงที่มากกว่า",
            topic=RESULTANT_TOPIC,
        )


@question_type(
    "phys.resultant_line_fluency",
    display_name={"th": "อธิบายวิธีหาแรงลัพธ์เมื่อวัตถุอยู่นิ่งจากผลการทดลอง"},
    level=FIFTH, subject=SUBJECT, topic=RESULTANT_TOPIC,
)
class ResultantLineFluency(QuestionType):
    """Spring scales pulling a block that stays still; explain the resultant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.sample(range(2, 9), 2)
        total = a + b
        stem = (f"นักเรียนใช้เครื่องชั่งสปริง 3 อันดึงกล่องบนพื้นลื่น อันที่ 1 ดึงไป{LEFT} อ่านได้ {a} นิวตัน "
                f"อันที่ 2 ดึงไป{LEFT} อ่านได้ {b} นิวตัน อันที่ 3 ดึงไป{RIGHT} อ่านได้ {total} นิวตัน "
                "กล่องอยู่นิ่ง จากหลักฐานนี้ ข้อใดอธิบายการหาแรงลัพธ์ได้ถูกต้อง")
        return _labelled(
            stem=stem,
            correct=(f"แรงไป{LEFT}รวมกันได้ {a} + {b} = {total} นิวตัน ลบกับแรงไป{RIGHT} {total} นิวตัน "
                     "ได้แรงลัพธ์ 0 นิวตัน กล่องจึงอยู่นิ่ง"),
            wrongs=(f"นำแรงทั้งสามมาบวกกันได้แรงลัพธ์ {2 * total} นิวตัน กล่องจึงอยู่นิ่ง",
                    f"นำแรงไป{RIGHT}ลบแรงอันที่ 1 ได้แรงลัพธ์ {total - a} นิวตัน ไป{RIGHT} กล่องจึงอยู่นิ่ง",
                    f"แรงไป{LEFT}รวมกันได้ {total} นิวตัน ลบกับแรงไป{RIGHT} ได้แรงลัพธ์ 0 นิวตัน กล่องจึงเคลื่อนที่ไป{LEFT}",
                    # A wrong sum and a wrong conclusion.
                    f"นำแรงทั้งสามมาบวกกันได้แรงลัพธ์ {2 * total} นิวตัน กล่องจึงเคลื่อนที่ไป{RIGHT}",
                    f"นำแรงไป{RIGHT}ลบแรงอันที่ 1 ได้แรงลัพธ์ {total - a} นิวตัน ไป{RIGHT} กล่องจึงเคลื่อนที่ไป{RIGHT}"),
            hint="รวมแรงที่มีทิศเดียวกันก่อน แล้วลบด้วยแรงทิศตรงข้าม ถ้าแรงลัพธ์เป็นศูนย์ วัตถุที่อยู่นิ่งจะอยู่นิ่งต่อไป",
            topic=RESULTANT_TOPIC,
        )


@question_type(
    "phys.resultant_line_application",
    display_name={"th": "ใช้แรงลัพธ์วิเคราะห์สถานการณ์ในชีวิตประจำวัน"},
    level=FIFTH, subject=SUBJECT, topic=RESULTANT_TOPIC,
)
class ResultantLineApplication(QuestionType):
    """Authored cases, the pull that keeps a box still, and three pushers on a cupboard."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            pulls = rng.sample(range(2, 16), rng.choice((1, 2)))
            side = rng.choice((LEFT, RIGHT))
            other = RIGHT if side == LEFT else LEFT
            said = " และ ".join(f"{f} นิวตัน" for f in pulls)
            total = sum(pulls)
            return _labelled(
                stem=f"กล่องอยู่นิ่งบนพื้นลื่น มีแรง {said} ดึงไป{side} ต้องออกแรงไป{other}เท่าใดกล่องจึงจะอยู่นิ่งต่อไป",
                correct=f"{total} นิวตัน",
                wrongs=tuple(f"{w} นิวตัน" for w in dict.fromkeys((total * 2, max(pulls), 0, total + 1, total + 2))
                             if w != total)[:3],
                hint="วัตถุอยู่นิ่งเมื่อแรงลัพธ์เป็นศูนย์ แรงสองทิศต้องรวมกันได้เท่ากัน",
                topic=RESULTANT_TOPIC,
            )
        if roll < 0.7:
            a, b = rng.sample(range(10, 61, 5), 2)
            c = rng.randrange(10, 91, 5)
            net = a + b - c
            answer = "0 นิวตัน ตู้อยู่นิ่ง" if net == 0 else f"{abs(net)} นิวตัน ไป{RIGHT if net > 0 else LEFT}"
            options = [f"{a + b + c} นิวตัน ไป{RIGHT}", f"{abs(net) or a} นิวตัน ไป{LEFT if net >= 0 else RIGHT}",
                       "0 นิวตัน ตู้อยู่นิ่ง", f"{abs(a - c)} นิวตัน ไป{RIGHT}", f"{a + b} นิวตัน ไป{RIGHT}"]
            return _labelled(
                stem=(f"นักเรียนสองคนผลักตู้ไป{RIGHT}ด้วยแรง {a} และ {b} นิวตัน อีกคนหนึ่งผลักไป{LEFT}ด้วยแรง {c} นิวตัน "
                      "แรงลัพธ์เป็นเท่าใด"),
                correct=answer,
                wrongs=tuple(o for o in dict.fromkeys(options) if o != answer)[:3],
                hint="รวมแรงแต่ละทิศ แล้วหาผลต่าง แรงลัพธ์ไปทางด้านที่มีแรงรวมมากกว่า",
                topic=RESULTANT_TOPIC,
            )
        return _retopic(scenario_question(
            rng, RESULTANT_SCENARIOS,
            hint="รวมแรงแต่ละทิศ แล้วหาผลต่าง ถ้าแรงลัพธ์เป็นศูนย์ วัตถุที่อยู่นิ่งจะไม่เคลื่อนที่",
        ), RESULTANT_TOPIC)
