"""ลำดับขั้นตอนด้วยสัญลักษณ์

วิทยาการคำนวณ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.2/1

Sets moved here from: technology_t1s4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import SECOND

PROVENANCE = Provenance("original")


ARROW_TOPIC = "ลำดับขั้นตอนด้วยสัญลักษณ์"


RIGHT, LEFT, UP, DOWN = "→", "←", "↑", "↓"


MOVE = {RIGHT: (1, 0), LEFT: (-1, 0), UP: (0, 1), DOWN: (0, -1)}


SAY = {RIGHT: "ไปทางขวา", LEFT: "ไปทางซ้าย", UP: "ขึ้นข้างบน", DOWN: "ลงข้างล่าง"}


OPPOSITE = {RIGHT: LEFT, LEFT: RIGHT, UP: DOWN, DOWN: UP}


ARROW_HINT = ("ลูกศรหนึ่งตัวคือการเดินหนึ่งช่อง → ไปทางขวา ← ไปทางซ้าย ↑ ขึ้นข้างบน ↓ ลงข้างล่าง "
              "อ่านลูกศรจากซ้ายไปขวาทีละตัว")


def _pair(rng: Random) -> tuple[str, str]:
    """One horizontal and one vertical direction, in either order."""
    across, up_down = rng.choice((RIGHT, LEFT)), rng.choice((UP, DOWN))
    return (across, up_down) if rng.random() < 0.5 else (up_down, across)


def _arrows(seq) -> str:
    return " ".join(seq)


def _where(dx: int, dy: int) -> str:
    across = f"ไปทางขวา {dx} ช่อง" if dx > 0 else f"ไปทางซ้าย {-dx} ช่อง"
    up_down = f"ขึ้นข้างบน {dy} ช่อง" if dy > 0 else f"ลงข้างล่าง {-dy} ช่อง"
    return f"{across} และ{up_down}"


@question_type(
    "comp.arrow_steps_foundation",
    display_name={"th": "เขียนและอ่านลำดับขั้นตอนด้วยลูกศร"},
    level=SECOND, subject=SUBJECT, topic=ARROW_TOPIC,
)
class ArrowStepsFoundation(QuestionType):
    """Words to arrows, or arrows to words."""

    def build(self, rng: Random, **params):
        first, second = _pair(rng)
        a, b = rng.randint(1, 3), rng.randint(1, 3)
        words = f"เดิน{SAY[first]} {a} ช่อง แล้วเดิน{SAY[second]} {b} ช่อง"
        right = [first] * a + [second] * b
        wrong_seqs = {
            _arrows([second] * b + [first] * a),
            _arrows([OPPOSITE[first]] * a + [second] * b),
            _arrows([first] * a + [OPPOSITE[second]] * b),
            _arrows([first] * b + [second] * a) if a != b else _arrows([first] * (a + 1) + [second] * b),
            # Both directions wrong, or the order and a direction wrong.
            _arrows([OPPOSITE[first]] * a + [OPPOSITE[second]] * b),
            _arrows([second] * b + [OPPOSITE[first]] * a),
        } - {_arrows(right)}
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ข้อใดใช้ลูกศรแสดงขั้นตอน “{words}” ได้ถูกต้อง",
                correct=_arrows(right), wrongs=tuple(sorted(wrong_seqs)),
                hint=ARROW_HINT, topic=ARROW_TOPIC,
            )
        wrong_words = [
            f"เดิน{SAY[second]} {b} ช่อง แล้วเดิน{SAY[first]} {a} ช่อง",
            f"เดิน{SAY[OPPOSITE[first]]} {a} ช่อง แล้วเดิน{SAY[second]} {b} ช่อง",
            f"เดิน{SAY[first]} {a} ช่อง แล้วเดิน{SAY[OPPOSITE[second]]} {b} ช่อง",
            f"เดิน{SAY[first]} {a + 1} ช่อง แล้วเดิน{SAY[second]} {b} ช่อง",
            # Two slips at once.
            f"เดิน{SAY[OPPOSITE[first]]} {a + 1} ช่อง แล้วเดิน{SAY[second]} {b} ช่อง",
            f"เดิน{SAY[second]} {b} ช่อง แล้วเดิน{SAY[OPPOSITE[first]]} {a} ช่อง",
        ]
        return _labelled(
            stem=f"ลูกศร {_arrows(right)} แสดงขั้นตอนการเดินแบบใด",
            correct=words, wrongs=tuple(wrong_words),
            hint=ARROW_HINT, topic=ARROW_TOPIC,
        )


@question_type(
    "comp.arrow_steps_fluency",
    display_name={"th": "ทำตามลูกศรแล้วบอกตำแหน่งที่ไปถึง"},
    level=SECOND, subject=SUBJECT, topic=ARROW_TOPIC,
)
class ArrowStepsFluency(QuestionType):
    """Follow a mixed arrow sequence and say where the robot ends."""

    def build(self, rng: Random, **params):
        across, up_down = rng.choice((RIGHT, LEFT)), rng.choice((UP, DOWN))
        a, b = rng.randint(1, 3), rng.randint(1, 3)
        seq = [across] * a + [up_down] * b
        rng.shuffle(seq)
        dx, dy = MOVE[across][0] * a, MOVE[up_down][1] * b
        options = {_where(dx + MOVE[across][0], dy), _where(dx, dy + MOVE[up_down][1]),
                   _where(-dx, dy), _where(dx, -dy)}
        if a != b:
            options.add(_where(MOVE[across][0] * b, MOVE[up_down][1] * a))
        options.discard(_where(dx, dy))
        return _labelled(
            stem=(f"หุ่นยนต์เริ่มที่ช่องเริ่มต้นแล้วเดินตามลูกศร {_arrows(seq)} "
                  f"เมื่อเดินครบ หุ่นยนต์อยู่ที่ใดเมื่อเทียบกับช่องเริ่มต้น"),
            correct=_where(dx, dy), wrongs=tuple(sorted(options)),
            hint=ARROW_HINT + " แล้วนับลูกศรแต่ละทิศรวมกัน",
            topic=ARROW_TOPIC,
        )


@question_type(
    "comp.arrow_steps_application",
    display_name={"th": "หาลูกศรที่เขียนผิดในลำดับขั้นตอน"},
    level=SECOND, subject=SUBJECT, topic=ARROW_TOPIC,
)
class ArrowStepsApplication(QuestionType):
    """One arrow points somewhere the target never goes; find it.

    The wrong arrow is always the opposite of a direction the target uses, so
    exactly one arrow can be changed to reach the target.
    """

    def build(self, rng: Random, **params):
        across, up_down = rng.choice((RIGHT, LEFT)), rng.choice((UP, DOWN))
        # At least three arrows, so there are always three wrong positions to offer.
        a, b = rng.randint(2, 3), rng.randint(1, 2)
        seq = [across] * a + [up_down] * b
        broken = rng.randrange(len(seq))
        seq[broken] = OPPOSITE[seq[broken]]
        positions = [f"ลูกศรตัวที่ {n}" for n in range(1, len(seq) + 1)]
        correct = positions[broken]
        others = [p for p in positions if p != correct] + ["ไม่มีลูกศรตัวใดผิด"]
        return _labelled(
            stem=(f"ต้องการให้หุ่นยนต์เดิน{SAY[across]} {a} ช่อง แล้วเดิน{SAY[up_down]} {b} ช่อง "
                  f"แต่เขียนลูกศรเป็น {_arrows(seq)} ลูกศรตัวใดเขียนผิด"),
            correct=correct, wrongs=tuple(others),
            hint="เทียบลูกศรทีละตัวกับทิศที่ต้องการ ลูกศรที่ชี้ไปทิศที่ไม่ต้องการคือตัวที่ผิด",
            topic=ARROW_TOPIC,
        )
