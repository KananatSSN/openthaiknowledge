"""การตรวจหาข้อผิดพลาดของโปรแกรม

วิทยาการคำนวณ · ป.2 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.2/2

Sets moved here from: technology_t3s1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import block_programs as bp
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t3s1 import P2, _ask

PROVENANCE = Provenance("original")


BUGS_TOPIC = "การตรวจหาข้อผิดพลาดของโปรแกรม"


REACHED = "ถึงดาว"


BUGS_HINT = "ทำตามบล็อกทีละบล็อกแล้วดูว่าหยุดที่ช่องใด บล็อกที่ผิดคือบล็อกที่พาตัวละครออกห่างจากดาว"


def _missed(pos) -> str:
    return f"ไม่ถึงดาว หยุดที่ช่อง {bp.cell(pos)}"


NO_BUG = "ไม่มีบล็อกที่ผิด"


BUGGED = tuple(s for s in bp.DEBUG if bp.wrong_block(s))


@question_type(
    "comp.block_bugs_foundation",
    display_name={"th": "ตรวจว่าโปรแกรมพาตัวละครไปถึงเป้าหมายหรือไม่"},
    level=P2, subject=SUBJECT, topic=BUGS_TOPIC,
)
class BlockBugsFoundation(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.DEBUG)
        end = spec.end
        # "ถึงดาว" alone was the one short choice beside three "ไม่ถึงดาว หยุดที่ช่อง …";
        # naming the cell keeps every choice the same shape.
        reached = f"ไป{REACHED} หยุดที่ช่อง {bp.cell(spec.target)}"
        correct = reached if end == spec.target else _missed(end)
        near = [p for p in bp.walk(spec.start, spec.blocks)[:-1] if p not in (end, spec.target)]
        ring = [(end[0] + dx, end[1] + dy) for dx in (-1, 0, 1) for dy in (-1, 0, 1) if dx or dy]
        pool = [_missed(p) for p in dict.fromkeys(near + ring)
                if bp.inside(p) and p not in (end, spec.target)]
        if correct == reached:
            wrongs = rng.sample(pool, 3)
        else:
            wrongs = rng.sample(pool, 2) + [reached]
        return _ask(rng, spec, stem="ต้องการให้ตัวละครเดินจากช่อง S ไปที่ดาว โปรแกรมนี้พาไปถึงดาวหรือไม่",
                    correct=correct, wrongs=wrongs, hint=BUGS_HINT, topic=BUGS_TOPIC)


@question_type(
    "comp.block_bugs_fluency",
    display_name={"th": "หาบล็อกคำสั่งที่ผิด"},
    level=P2, subject=SUBJECT, topic=BUGS_TOPIC,
)
class BlockBugsFluency(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(BUGGED)
        bad = bp.wrong_block(spec)
        others = [f"บล็อกที่ {i}" for i in range(1, len(spec.blocks) + 1) if i != bad] + [NO_BUG]
        return _ask(rng, spec, stem="ต้องการให้ตัวละครเดินจากช่อง S ไปที่ดาว แต่โปรแกรมมีบล็อกที่ผิดอยู่หนึ่งบล็อก บล็อกใดผิด",
                    correct=f"บล็อกที่ {bad}", wrongs=rng.sample(others, 3), hint=BUGS_HINT, topic=BUGS_TOPIC)


@question_type(
    "comp.block_bugs_application",
    display_name={"th": "แก้ไขโปรแกรมให้ไปถึงเป้าหมาย"},
    level=P2, subject=SUBJECT, topic=BUGS_TOPIC,
)
class BlockBugsApplication(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(BUGGED)
        bad = bp.wrong_block(spec)
        fix = bp.OPPOSITE[spec.blocks[bad - 1]]

        def change(i: int, move: str) -> str:
            return f"เปลี่ยนบล็อกที่ {i} เป็นลูกศร{bp.SAY[move]}"

        pool = [change(bad, m) for m in "RLUD" if m not in (fix, spec.blocks[bad - 1])]
        pool += [change(i, fix) for i in range(1, len(spec.blocks) + 1) if i != bad]
        # Another block changed to another arrow as well, kept only where the
        # walk really misses the star, so the answer is not the change every
        # wrong shares its block or its arrow with.
        for i in range(1, len(spec.blocks) + 1):
            for m in "RLUD":
                if i == bad or m in (fix, spec.blocks[i - 1]):
                    continue
                blocks = list(spec.blocks)
                blocks[i - 1] = m
                if bp.walk(spec.start, blocks)[-1] != spec.target and change(i, m) not in pool:
                    pool.append(change(i, m))
        return _ask(rng, spec, stem="ต้องการให้ตัวละครเดินจากช่อง S ไปที่ดาว ควรแก้โปรแกรมอย่างไรจึงจะถึงดาว",
                    correct=change(bad, fix), wrongs=rng.sample(pool, len(pool)),
                    hint="หาบล็อกที่พาตัวละครออกห่างจากดาว แล้วเปลี่ยนเป็นลูกศรทิศที่ยังขาดอยู่",
                    topic=BUGS_TOPIC)
