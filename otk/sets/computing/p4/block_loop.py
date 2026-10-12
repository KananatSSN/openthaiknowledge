"""โปรแกรมที่มีการทำซ้ำ

วิทยาการคำนวณ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.4/2

Sets moved here from: technology_t3s2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import block_programs as bp
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t3s1 import READ_HINT, _ask, _other_cells
from otk.sets._support.technology_t3s2 import P4

PROVENANCE = Provenance("original")


LOOP_TOPIC = "โปรแกรมที่มีการทำซ้ำ"


LOOP_HINT = READ_HINT + " บล็อก x3 หมายถึงทำลูกศรในบล็อกนั้นซ้ำ 3 รอบ"


@question_type(
    "comp.block_loop_foundation",
    display_name={"th": "นับจำนวนก้าวของโปรแกรมที่มีบล็อกทำซ้ำ"},
    level=P4, subject=SUBJECT, topic=LOOP_TOPIC,
)
class BlockLoopFoundation(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.LOOPS)
        steps = len(bp.expand(spec.blocks))
        blocks = len(spec.blocks)
        repeat = next(b for b in spec.blocks if b.startswith("x"))
        once = blocks - 1 + len(repeat) - 2
        wrongs = _near(steps, (blocks, once, steps + int(repeat[1]), steps - 1))
        return _ask(rng, spec, stem="เมื่อทำตามโปรแกรมครบทุกบล็อก ตัวละครเดินไปทั้งหมดกี่ช่อง (นับทุกก้าว)",
                    correct=f"{steps} ช่อง", wrongs=[f"{w} ช่อง" for w in rng.sample(wrongs, 3)],
                    hint=LOOP_HINT, topic=LOOP_TOPIC)


@question_type(
    "comp.block_loop_fluency",
    display_name={"th": "บอกตำแหน่งสุดท้ายของโปรแกรมที่มีบล็อกทำซ้ำ"},
    level=P4, subject=SUBJECT, topic=LOOP_TOPIC,
)
class BlockLoopFluency(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.LOOPS)
        once = tuple(f"x1{b[2:]}" if b.startswith("x") else b for b in spec.blocks)
        slips = (bp.walk(spec.start, once)[-1], bp.walk(spec.start, spec.blocks)[-2], spec.start)
        wrongs = _other_cells(rng, spec.end, slips)
        return _ask(rng, spec, stem="เมื่อทำตามโปรแกรมครบทุกบล็อก ตัวละครจะอยู่ที่ช่องใด",
                    correct=bp.cell(spec.end), wrongs=wrongs, hint=LOOP_HINT, topic=LOOP_TOPIC)


@question_type(
    "comp.block_loop_application",
    display_name={"th": "แก้จำนวนรอบของบล็อกทำซ้ำให้ถึงเป้าหมาย"},
    level=P4, subject=SUBJECT, topic=LOOP_TOPIC,
)
class BlockLoopApplication(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.LOOP_GOALS)
        repeat, turn = spec.blocks
        move = repeat[2:]
        right = next(k for k in range(1, 6) if bp.walk(spec.start, (f"x{k}{move}", turn))[-1] == spec.target)
        pool = [k for k in range(1, 7) if k != right]
        return _ask(rng, spec,
                    stem="ต้องการให้ตัวละครเดินจากช่อง S ไปที่ดาว แต่จำนวนรอบของบล็อกทำซ้ำยังไม่ถูกต้อง ควรเปลี่ยนจำนวนรอบเป็นเท่าใด",
                    correct=f"{right} รอบ", wrongs=[f"{k} รอบ" for k in rng.sample(pool, 3)],
                    hint="นับว่าต้องเดินในทิศของบล็อกทำซ้ำกี่ช่องจึงจะอยู่แนวเดียวกับดาว",
                    topic=LOOP_TOPIC)
