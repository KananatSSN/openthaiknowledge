"""อัลกอริทึมที่มีการทำซ้ำ

วิทยาการคำนวณ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.2/1

Sets moved here from: technology_t3s3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import flowcharts as fc
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t3s3 import M2, _ask, _flipped, _numbers

PROVENANCE = Provenance("original")


LOOP_TOPIC = "อัลกอริทึมที่มีการทำซ้ำ"


LOOP_HINT = ("ทำตารางไล่ค่าตัวแปรทีละรอบ ก่อนทำทาง Yes ทุกครั้งต้องตรวจเงื่อนไขก่อน "
             "และเมื่อเงื่อนไขเป็นเท็จจึงออกไปแสดงผล")


def _loop_input(rng: Random, spec: fc.Flowchart, low: int, high: int) -> int:
    """An input in 0-40 for which the loop body runs ``low``-``high`` times."""
    return rng.choice([x for x in range(0, 41) if low <= fc.run(spec, x).passes <= high])


def _step_size(spec: fc.Flowchart) -> int:
    return int(spec.yes[0].split()[-1])


@question_type(
    "comp.flowchart_loop_foundation",
    display_name={"th": "นับจำนวนรอบของการทำซ้ำในผังงาน"},
    level=M2, subject=SUBJECT, topic=LOOP_TOPIC,
)
class FlowchartLoopFoundation(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params):
        spec = rng.choice(fc.LOOPS)
        x = _loop_input(rng, spec, 1, 6)
        passes = fc.run(spec, x).passes
        slips = (fc.run(_flipped(spec), x).passes, passes + 1, passes - 1)
        return _ask(spec,
                    stem=f"จากผังงาน ถ้ารับค่า x = {x} คำสั่งในทาง Yes จะถูกทำซ้ำทั้งหมดกี่รอบ ก่อนออกไปแสดงผล",
                    correct=f"{passes} รอบ", wrongs=[f"{w} รอบ" for w in rng.sample(_near(passes, slips)[:4], 3)],
                    hint=LOOP_HINT, topic=LOOP_TOPIC)


@question_type(
    "comp.flowchart_loop_fluency",
    display_name={"th": "ไล่ผังงานที่มีการทำซ้ำเพื่อหาผลลัพธ์"},
    level=M2, subject=SUBJECT, topic=LOOP_TOPIC,
)
class FlowchartLoopFluency(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params):
        spec = rng.choice(fc.LOOPS)
        x = _loop_input(rng, spec, 1, 6)
        result = fc.run(spec, x)
        other = "x" if spec.out == "n" else "n"
        step = 1 if spec.out == "n" else _step_size(spec)
        slips = (fc.run(_flipped(spec), x).output, result.output - step, result.output + step,
                 result.env[other])
        return _ask(spec, stem=f"จากผังงาน ถ้ารับค่า x = {x} ผังงานนี้จะแสดงผลเป็นเท่าใด",
                    correct=str(result.output), wrongs=_numbers(rng, result.output, slips),
                    hint=LOOP_HINT, topic=LOOP_TOPIC)


@question_type(
    "comp.flowchart_loop_application",
    display_name={"th": "หาผลรวมจากผังงานที่ทำซ้ำตามรูปแบบ"},
    level=M2, subject=SUBJECT, topic=LOOP_TOPIC,
)
class FlowchartLoopApplication(QuestionType):
    """A total built over i = 1 .. x: spot the pattern of a few passes, then finish it."""

    def build(self, rng: Random, **params):
        spec = rng.choice(fc.SUMS)
        x = rng.randint(2, 6)
        out = fc.run(spec, x).output
        slips = (fc.run(_flipped(spec), x).output, fc.run(spec, x - 1).output, fc.run(spec, x + 1).output)
        return _ask(spec,
                    stem=(f"จากผังงาน ถ้ารับค่า x = {x} ผังงานนี้จะแสดงผลเป็นเท่าใด "
                          "(ลองไล่ค่า i และ s สองสามรอบแรกเพื่อหารูปแบบ)"),
                    correct=str(out), wrongs=_numbers(rng, out, slips),
                    hint=LOOP_HINT + " สังเกตว่าแต่ละรอบ s เปลี่ยนไปอย่างไร และรอบสุดท้ายคือรอบที่ i มีค่าเท่าใด",
                    topic=LOOP_TOPIC)
