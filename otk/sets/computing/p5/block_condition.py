"""โปรแกรมที่มีเงื่อนไข

วิทยาการคำนวณ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.5/2

Sets moved here from: technology_t3s2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import block_programs as bp
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t3s1 import _ask
from otk.sets._support.technology_t3s2 import P5

PROVENANCE = Provenance("original")


RULE_TOPIC = "โปรแกรมที่มีเงื่อนไข"


RULE = "โปรแกรมมีเงื่อนไขว่า ทุกครั้งที่ตัวละครเดินไปหยุดบนช่องที่มีเหรียญ ให้เก็บเหรียญนั้น"


def collected(spec) -> list[tuple[int, int]]:
    landed = set(bp.walk(spec.start, spec.blocks)[1:])
    return [c for c in spec.coins if c in landed]


@question_type(
    "comp.block_condition_foundation",
    display_name={"th": "ทำตามโปรแกรมที่มีเงื่อนไขแล้วนับผลลัพธ์"},
    level=P5, subject=SUBJECT, topic=RULE_TOPIC,
)
class BlockConditionFoundation(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.COIN_RUNS)
        got = len(collected(spec))
        return _ask(rng, spec, stem=f"{RULE} เมื่อทำตามโปรแกรมครบ ตัวละครเก็บเหรียญได้กี่เหรียญ",
                    correct=f"{got} เหรียญ",
                    wrongs=[f"{w} เหรียญ" for w in rng.sample(_near(got, (len(spec.coins), got - 1, got + 1)), 3)],
                    hint="ไล่ตามโปรแกรมทีละบล็อก และตรวจเงื่อนไขทุกครั้งที่ตัวละครไปหยุดที่ช่องใหม่",
                    topic=RULE_TOPIC)


@question_type(
    "comp.block_condition_fluency",
    display_name={"th": "ตัดสินผลของเงื่อนไขซ้อนในโปรแกรม"},
    level=P5, subject=SUBJECT, topic=RULE_TOPIC,
)
class BlockConditionFluency(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(bp.COIN_RUNS)
        got = len(collected(spec))
        need = rng.choice((got - 1, got, got + 1)) if got > 1 else rng.choice((got, got + 1))

        def say(opens: bool, count: int) -> str:
            return f"{'ประตูเปิด' if opens else 'ประตูไม่เปิด'} เพราะเก็บได้ {count} เหรียญ"

        correct = say(got >= need, got)
        pool = {say(not (got >= need), got), say(True, len(spec.coins)), say(False, got - 1 if got else 1),
                say(got >= need, got + 1)} - {correct}
        return _ask(rng, spec,
                    stem=f"{RULE} เมื่อจบโปรแกรม ถ้าเก็บเหรียญได้อย่างน้อย {need} เหรียญ ประตูจะเปิด ถ้าไม่ถึงประตูจะไม่เปิด ข้อใดถูกต้อง",
                    correct=correct, wrongs=rng.sample(sorted(pool), 3),
                    hint="นับเหรียญที่เก็บได้จริงก่อน แล้วจึงเทียบกับเงื่อนไขของประตู",
                    topic=RULE_TOPIC)


@question_type(
    "comp.block_condition_application",
    display_name={"th": "หาส่วนที่เงื่อนไขในโปรแกรมไม่ได้ทำงาน"},
    level=P5, subject=SUBJECT, topic=RULE_TOPIC,
)
class BlockConditionApplication(QuestionType):
    """The one coin that is (or is not) picked up, where exactly one stands apart."""

    def build(self, rng: Random, **params):
        spec = rng.choice([s for s in bp.COIN_RUNS if len(collected(s)) in (1, 3)])
        got = collected(spec)
        missed = [c for c in spec.coins if c not in got]
        if len(got) == 1:
            stem, correct, wrongs = "ถูกเก็บ", got[0], missed
        else:
            stem, correct, wrongs = "ยังไม่ถูกเก็บ", missed[0], got
        return _ask(rng, spec, stem=f"{RULE} เมื่อจบโปรแกรม เหรียญที่ช่องใด{stem}",
                    correct=bp.cell(correct), wrongs=[bp.cell(c) for c in wrongs],
                    hint="เหรียญที่ถูกเก็บคือเหรียญบนช่องที่ตัวละครไปหยุด เหรียญบนช่องที่ไม่เคยไปหยุดจะไม่ถูกเก็บ",
                    topic=RULE_TOPIC)
