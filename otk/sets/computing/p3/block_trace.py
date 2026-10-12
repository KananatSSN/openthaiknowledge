"""การไล่ลำดับและแก้ไขโปรแกรม

วิทยาการคำนวณ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.3/2

Sets moved here from: technology_t3s1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import block_programs as bp
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t3s1 import DIRECTIONS, P3, READ_HINT, _ask, _other_cells

PROVENANCE = Provenance("original")


TRACE_TOPIC = "การไล่ลำดับและแก้ไขโปรแกรม"


@question_type(
    "comp.block_trace_foundation",
    display_name={"th": "ไล่ลำดับโปรแกรมทีละบล็อก"},
    level=P3, subject=SUBJECT, topic=TRACE_TOPIC,
)
class BlockTraceFoundation(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.LONG)
        path = bp.walk(spec.start, spec.blocks)
        k = rng.randint(2, len(spec.blocks) - 1)
        wrongs = _other_cells(rng, path[k], (path[k - 1], path[k + 1], path[-1], spec.start))
        return _ask(rng, spec, stem=f"หลังจากทำบล็อกที่ {k} เสร็จ ตัวละครอยู่ที่ช่องใด",
                    correct=bp.cell(path[k]), wrongs=wrongs, hint=READ_HINT, topic=TRACE_TOPIC)


@question_type(
    "comp.block_trace_fluency",
    display_name={"th": "หาบล็อกคำสั่งที่ขาดหายไป"},
    level=P3, subject=SUBJECT, topic=TRACE_TOPIC,
)
class BlockTraceFluency(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.MISSING)
        end = spec.end
        dx, dy = spec.target[0] - end[0], spec.target[1] - end[1]
        move = next(m for m, step in bp.MOVES.items() if step == (dx, dy))
        correct = f"เดิน{bp.SAY[move]}"
        return _ask(rng, spec,
                    stem="โปรแกรมนี้ขาดบล็อกไปหนึ่งบล็อก ตัวละครจึงยังไม่ถึงดาว ต้องเพิ่มบล็อกที่สั่งให้ทำอะไร",
                    correct=correct, wrongs=[d for d in DIRECTIONS if d != correct],
                    hint="ทำตามโปรแกรมให้ครบก่อน แล้วดูว่าจากช่องที่หยุด ดาวอยู่ห่างไปทางใดหนึ่งช่อง",
                    topic=TRACE_TOPIC)


@question_type(
    "comp.block_trace_application",
    display_name={"th": "บอกเส้นทางที่ตัวละครเดินผ่าน"},
    level=P3, subject=SUBJECT, topic=TRACE_TOPIC,
)
class BlockTraceApplication(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.LONG)
        path = bp.walk(spec.start, spec.blocks)
        visited = set(path)
        on_path = [p for p in dict.fromkeys(path[1:]) if p != spec.start]
        off_path = [(c, r) for c in range(bp.SIZE) for r in range(bp.SIZE) if (c, r) not in visited]
        # Squares next to the path are the tempting wrong answers.
        close = [p for p in off_path if any(abs(p[0] - q[0]) + abs(p[1] - q[1]) == 1 for q in path)]
        pool = close if len(close) >= 3 else off_path
        return _ask(rng, spec,
                    stem="เมื่อทำตามโปรแกรมครบ ข้อใดเป็นช่องที่ตัวละครเดินผ่านหรือหยุด (ไม่นับช่องเริ่มต้น)",
                    correct=bp.cell(rng.choice(on_path)),
                    wrongs=[bp.cell(p) for p in rng.sample(pool, 3)],
                    hint="ทำตามทีละบล็อกแล้วจดช่องที่ตัวละครไปถึงทุกช่อง", topic=TRACE_TOPIC)
