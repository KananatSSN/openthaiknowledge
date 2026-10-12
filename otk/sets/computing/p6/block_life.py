"""โปรแกรมแก้ปัญหาในชีวิตประจำวัน

วิทยาการคำนวณ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.6/2

Sets moved here from: technology_t3s2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import block_programs as bp
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t3s1 import ARROW_TEXT, _ask
from otk.sets._support.technology_t3s2 import P6

PROVENANCE = Provenance("original")


LIFE_TOPIC = "โปรแกรมแก้ปัญหาในชีวิตประจำวัน"


def _repeat_text(count: int, moves) -> str:
    return f"ทำซ้ำ {count} รอบ: {' '.join(ARROW_TEXT[m] for m in moves)}"


ROBOT = "ตัวละครในภาพคือหุ่นยนต์ดูดฝุ่นที่ทำความสะอาดทุกช่องที่ผ่านหรือหยุด รวมทั้งช่องเริ่มต้น"


@question_type(
    "comp.block_life_foundation",
    display_name={"th": "นับผลของโปรแกรมหุ่นยนต์ดูดฝุ่น"},
    level=P6, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BlockLifeFoundation(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.LOOPS)
        path = bp.walk(spec.start, spec.blocks)
        cleaned = len(set(path))
        return _ask(rng, spec, stem=f"{ROBOT} เมื่อทำตามโปรแกรมครบ หุ่นยนต์ทำความสะอาดได้กี่ช่อง (ช่องที่ผ่านซ้ำนับครั้งเดียว)",
                    correct=f"{cleaned} ช่อง",
                    wrongs=[f"{w} ช่อง" for w in rng.sample(
                        _near(cleaned, (len(path), len(path) - 1, cleaned - 1, cleaned + 1)), 3)],
                    hint="ไล่เส้นทางทีละก้าวแล้วนับช่องที่ต่างกันทั้งหมด ช่องที่กลับมาซ้ำนับเพียงครั้งเดียว",
                    topic=LIFE_TOPIC)


@question_type(
    "comp.block_life_fluency",
    display_name={"th": "เขียนบล็อกทำซ้ำให้หุ่นยนต์กลับจุดเริ่มต้น"},
    level=P6, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BlockLifeFluency(QuestionType):
    """The repeat block that takes the robot straight back home."""

    def build(self, rng: Random, **params):
        spec = rng.choice([s for s in bp.LOOPS
                           if (s.end[0] == s.start[0]) != (s.end[1] == s.start[1])])
        dx, dy = spec.start[0] - spec.end[0], spec.start[1] - spec.end[1]
        move = ("R" if dx > 0 else "L") if dx else ("U" if dy > 0 else "D")
        count = abs(dx) or abs(dy)
        pool = {_repeat_text(count, bp.OPPOSITE[move]), _repeat_text(count + 1, move),
                _repeat_text(max(count - 1, 1) if count > 1 else count + 2, move),
                _repeat_text(count, "U" if move in "RL" else "R"),
                # The wrong count and the wrong direction: never back home.
                _repeat_text(count + 1, bp.OPPOSITE[move]),
                _repeat_text(count + 1, "U" if move in "RL" else "R")} - {_repeat_text(count, move)}
        return _ask(rng, spec,
                    stem=f"{ROBOT} เมื่อทำตามโปรแกรมครบแล้ว ต้องเพิ่มบล็อกทำซ้ำใดต่อท้าย หุ่นยนต์จึงจะกลับไปที่ช่องเริ่มต้น S",
                    correct=_repeat_text(count, move), wrongs=rng.sample(sorted(pool), len(pool)),
                    hint="หาช่องที่หุ่นยนต์หยุด แล้วนับว่าช่อง S อยู่ห่างไปทางใดกี่ช่อง",
                    topic=LIFE_TOPIC)


@question_type(
    "comp.block_life_application",
    display_name={"th": "เลือกโปรแกรมที่สั้นที่สุดด้วยบล็อกทำซ้ำ"},
    level=P6, subject=SUBJECT, topic=LIFE_TOPIC,
)
class BlockLifeApplication(QuestionType):
    """A star as far across as up: one staircase repeat is the shortest program."""

    def build(self, rng: Random, **params):
        spec = rng.choice(bp.DIAGONALS)
        dx, dy = spec.target[0] - spec.start[0], spec.target[1] - spec.start[1]
        h, v = ("R" if dx > 0 else "L"), ("U" if dy > 0 else "D")
        n = abs(dx)
        correct = _repeat_text(n, h + v)
        wrongs = [
            _repeat_text(n + 1, h + v),
            _repeat_text(n, h + bp.OPPOSITE[v]),
            " ".join([ARROW_TEXT[h]] * n + [ARROW_TEXT[v]] * n),
            _repeat_text(n, h) if n > 1 else _repeat_text(2 * n, v),
            # The wrong count and a wrong turn: never at the star.
            _repeat_text(n + 1, h + bp.OPPOSITE[v]),
            _repeat_text(n + 1, bp.OPPOSITE[h] + v),
        ]
        return _ask(rng, spec,
                    stem=("หุ่นยนต์ส่งของเริ่มที่ช่อง S ต้องไปส่งของที่ดาว "
                          "โปรแกรมใดสั้นที่สุด (ใช้บล็อกน้อยที่สุด) และไปถึงดาวได้"),
                    correct=correct, wrongs=rng.sample(wrongs, len(wrongs)),
                    hint="ดาวอยู่ห่างทางแนวนอนและแนวตั้งเท่ากัน จึงเดินเป็นขั้นบันไดซ้ำได้ด้วยบล็อกทำซ้ำเพียงบล็อกเดียว",
                    topic=LIFE_TOPIC)
