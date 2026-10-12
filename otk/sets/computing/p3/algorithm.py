"""อัลกอริทึมอย่างง่าย

วิทยาการคำนวณ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.3/1

Sets moved here from: technology_t1s4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import THIRD, _near

PROVENANCE = Provenance("original")


ALGORITHM_TOPIC = "อัลกอริทึมอย่างง่าย"


ACTIONS = (("เดินไปข้างหน้า", "ก้าว"), ("ปรบมือ", "ครั้ง"), ("กระโดด", "ครั้ง"), ("ยกแขน", "ครั้ง"))


REPEAT_HINT = "การทำซ้ำคือการนำขั้นตอนชุดเดียวกันมาทำหลายรอบ ให้หาชุดขั้นตอนที่เกิดซ้ำ แล้วนับจำนวนรอบ"


def _block(rng: Random):
    (first, u1), (second, u2) = rng.sample(ACTIONS, 2)
    return first, u1, rng.randint(1, 3), second, u2, rng.randint(1, 3)


BLOCK_COLOURS = ("สีแดง", "สีฟ้า", "สีเขียว", "สีเหลือง")


@question_type(
    "comp.algorithm_repeat_foundation",
    display_name={"th": "เขียนขั้นตอนที่เกิดซ้ำให้สั้นลงด้วยการทำซ้ำ"},
    level=THIRD, subject=SUBJECT, topic=ALGORITHM_TOPIC,
)
class AlgorithmRepeatFoundation(QuestionType):
    """Spot the repeated block and how many rounds it runs."""

    def build(self, rng: Random, **params):
        first, u1, n1, second, u2, n2 = _block(rng)
        rounds = rng.randint(2, 4)
        once = f"{first} {n1} {u1} {second} {n2} {u2}"
        written = " ".join([once] * rounds)

        def short(r, a, b, x, y):
            return f"ทำซ้ำ {r} รอบ: {a} {x} {u1 if a == first else u2} แล้ว{b} {y} {u2 if b == second else u1}"

        correct = short(rounds, first, second, n1, n2)
        wrongs = {short(rounds + 1, first, second, n1, n2),
                  short(rounds - 1, first, second, n1, n2) if rounds > 2 else short(rounds + 2, first, second, n1, n2),
                  short(rounds, second, first, n2, n1),
                  short(rounds, first, second, n1 + 1, n2),
                  # Two slips at once: rounds and a count, or rounds and the order.
                  short(rounds + 1, first, second, n1 + 1, n2),
                  short(rounds + 1, second, first, n2, n1)} - {correct}
        return _labelled(
            stem=f"ขั้นตอนต่อไปนี้ “{written}” เขียนให้สั้นลงด้วยการทำซ้ำได้อย่างไร",
            correct=correct, wrongs=tuple(sorted(wrongs)),
            hint=REPEAT_HINT, topic=ALGORITHM_TOPIC,
        )


@question_type(
    "comp.algorithm_repeat_fluency",
    display_name={"th": "นับผลของการทำซ้ำในอัลกอริทึม"},
    level=THIRD, subject=SUBJECT, topic=ALGORITHM_TOPIC,
)
class AlgorithmRepeatFluency(QuestionType):
    """How many of one action a repeated block adds up to."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        first, u1, n1, second, u2, n2 = _block(rng)
        rounds = rng.randint(2, 5)
        action, unit, each = (first, u1, n1) if rng.random() < 0.5 else (second, u2, n2)
        total = each * rounds
        wrongs = _near(total, (each + rounds, total + each, (n1 + n2) * rounds, rounds, total - 1))
        return _labelled(
            stem=(f"อัลกอริทึม: ทำซ้ำ {rounds} รอบ: {first} {n1} {u1} แล้ว{second} {n2} {u2} "
                  f"เมื่อทำครบทุกรอบ จะ{action}ทั้งหมดกี่{unit}"),
            correct=f"{total} {unit}",
            wrongs=tuple(f"{w} {unit}" for w in rng.sample(wrongs, 3)),
            hint=f"ในหนึ่งรอบ{action} {each} {unit} ทำ {rounds} รอบ จึงนำ {each} มาคูณกับ {rounds}",
            topic=ALGORITHM_TOPIC,
        )


@question_type(
    "comp.algorithm_condition_application",
    display_name={"th": "ทำตามอัลกอริทึมที่มีเงื่อนไข"},
    level=THIRD, subject=SUBJECT, topic=ALGORITHM_TOPIC,
)
class AlgorithmConditionApplication(QuestionType):
    """Sort blocks by an ถ้า rule and count one box."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        colours = rng.sample(BLOCK_COLOURS, 3)
        blocks = [rng.choice(colours) for _ in range(rng.randint(5, 7))]
        rule = rng.choice(colours)
        if rule not in blocks:
            blocks[rng.randrange(len(blocks))] = rule
        in_a = blocks.count(rule)
        in_b = len(blocks) - in_a
        ask_a = rng.random() < 0.5
        answer = in_a if ask_a else in_b
        wrongs = _near(answer, (in_b if ask_a else in_a, len(blocks), answer + 1, answer - 1))
        return _labelled(
            stem=(f"มีตัวต่อเรียงกัน {len(blocks)} ชิ้น ได้แก่ {' '.join(blocks)} "
                  f"อัลกอริทึมคือ หยิบตัวต่อทีละชิ้น ถ้าเป็น{rule} ให้ใส่กล่อง ก "
                  f"ถ้าไม่ใช่ ให้ใส่กล่อง ข เมื่อทำจนครบ กล่อง {'ก' if ask_a else 'ข'} มีตัวต่อกี่ชิ้น"),
            correct=f"{answer} ชิ้น",
            wrongs=tuple(f"{w} ชิ้น" for w in rng.sample(wrongs, 3)),
            hint=f"ตรวจเงื่อนไขกับตัวต่อทีละชิ้น ชิ้นที่เป็น{rule}ไปกล่อง ก ชิ้นอื่นทุกชิ้นไปกล่อง ข",
            topic=ALGORITHM_TOPIC,
        )
