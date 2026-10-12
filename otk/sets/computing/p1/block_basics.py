"""การเขียนโปรแกรมด้วยบล็อกคำสั่ง

วิทยาการคำนวณ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.1/3

Sets moved here from: technology_t3s1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import block_programs as bp
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t3s1 import (
    ARROW_TEXT,
    DIRECTIONS,
    P1,
    READ_HINT,
    _ask,
    _other_cells,
)

PROVENANCE = Provenance("original")


BASICS_TOPIC = "การเขียนโปรแกรมด้วยบล็อกคำสั่ง"


def _arrows(moves) -> str:
    return " ".join(ARROW_TEXT[m] for m in moves)


@question_type(
    "comp.block_basics_foundation",
    display_name={"th": "อ่านคำสั่งจากบล็อกลูกศร"},
    level=P1, subject=SUBJECT, topic=BASICS_TOPIC,
)
class BlockBasicsFoundation(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.SIMPLE)
        k = rng.randrange(len(spec.blocks))
        correct = f"เดิน{bp.SAY[spec.blocks[k]]}"
        return _ask(rng, spec, stem=f"บล็อกที่ {k + 1} สั่งให้ตัวละครทำอะไร",
                    correct=correct, wrongs=[d for d in DIRECTIONS if d != correct],
                    hint=READ_HINT, topic=BASICS_TOPIC)


@question_type(
    "comp.block_basics_fluency",
    display_name={"th": "บอกตำแหน่งที่ตัวละครไปถึงเมื่อทำตามโปรแกรม"},
    level=P1, subject=SUBJECT, topic=BASICS_TOPIC,
)
class BlockBasicsFluency(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.SIMPLE)
        path = bp.walk(spec.start, spec.blocks)
        flipped = bp.walk(spec.start, (bp.OPPOSITE[spec.blocks[0]], *spec.blocks[1:]))[-1]
        wrongs = _other_cells(rng, spec.end, (path[-2], spec.start, flipped))
        return _ask(rng, spec, stem="เมื่อทำตามบล็อกคำสั่งครบทุกบล็อก ตัวละครจะอยู่ที่ช่องใด",
                    correct=bp.cell(spec.end), wrongs=wrongs, hint=READ_HINT, topic=BASICS_TOPIC)


@question_type(
    "comp.block_basics_application",
    display_name={"th": "เลือกโปรแกรมที่พาตัวละครไปถึงดาว"},
    level=P1, subject=SUBJECT, topic=BASICS_TOPIC,
)
class BlockBasicsApplication(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.GOALS)
        dx, dy = spec.target[0] - spec.start[0], spec.target[1] - spec.start[1]
        h, v = ("R" if dx > 0 else "L"), ("U" if dy > 0 else "D")
        correct = [h] * abs(dx) + [v] * abs(dy)
        if rng.random() < 0.5:
            correct = [v] * abs(dy) + [h] * abs(dx)
        candidates = [
            [h] * (abs(dx) - 1) + [v] * abs(dy),
            [h] * abs(dx) + [v] * (abs(dy) + 1),
            [bp.OPPOSITE[h]] * abs(dx) + [v] * abs(dy),
            [h] * abs(dx) + [bp.OPPOSITE[v]] * abs(dy),
            [h] * abs(dy) + [v] * abs(dx),
        ]
        wrongs = []
        for moves in candidates:
            text = _arrows(moves)
            if moves and bp.walk(spec.start, moves)[-1] != spec.target and text not in wrongs:
                wrongs.append(text)
        return _ask(rng, spec,
                    stem="ตัวละครเริ่มที่ช่อง S ต้องการให้เดินไปที่ดาว โปรแกรมใดทำได้ถูกต้อง (อ่านลูกศรจากซ้ายไปขวา)",
                    correct=_arrows(correct), wrongs=rng.sample(wrongs, 3),
                    hint="นับว่าดาวอยู่ห่างจากตัวละครไปทางซ้ายหรือขวากี่ช่อง และขึ้นหรือลงกี่ช่อง",
                    topic=BASICS_TOPIC)
