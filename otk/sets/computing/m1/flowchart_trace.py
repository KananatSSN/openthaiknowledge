"""ผังงาน

วิทยาการคำนวณ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.1/1

Sets moved here from: technology_t3s3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support import flowcharts as fc
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t3s3 import M1, _ask, _flipped, _numbers

PROVENANCE = Provenance("original")


FLOW_TOPIC = "ผังงาน"


READ_HINT = ("เริ่มที่ Start แล้วทำตามลูกศรทีละกล่อง กล่องสี่เหลี่ยมคือคำสั่ง เช่น y = x * 2 "
             "หมายถึงนำค่า x คูณ 2 แล้วเก็บไว้ใน y")


TEST_HINT = ("กล่องรูปข้าวหลามตัดคือการตรวจเงื่อนไข ถ้าเงื่อนไขเป็นจริงไปทาง Yes ถ้าเป็นเท็จไปทาง No "
             "ระวังเครื่องหมาย >= และ <= ซึ่งรวมกรณีที่ค่าเท่ากันด้วย")


def _fills(statement: str) -> list[str]:
    """Statements that look like ``statement``: another operator or a nearby number."""
    head, source, op, number = statement.rsplit(" ", 3)[0], *statement.split()[2:]
    n = int(number)
    found = [f"{head} {source} {other} {n}" for other in "+-*" if other != op]
    found += [f"{head} {source} {op} {m}" for m in (n - 1, n + 1, n + 2) if m > 0]
    if source == "y":
        found.append(f"{head} x {op} {n}")
    return found


@question_type(
    "comp.flowchart_trace_foundation",
    display_name={"th": "ไล่ผังงานแบบลำดับเพื่อหาผลลัพธ์"},
    level=M1, subject=SUBJECT, topic=FLOW_TOPIC,
)
class FlowchartTraceFoundation(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(fc.SEQUENCES)
        x = rng.choice(fc.SEQ_INPUTS)
        out = fc.run(spec, x).output
        first, second = spec.setup
        swapped = (second.replace("y = y", "y = x"), first.replace("y = x", "y = y"))
        slips = (fc.run(spec, x, (first,)).output, fc.run(spec, x, swapped).output, x)
        return _ask(spec, stem=f"จากผังงาน ถ้ารับค่า x = {x} ผังงานนี้จะแสดงผลเป็นเท่าใด",
                    correct=str(out), wrongs=_numbers(rng, out, slips), hint=READ_HINT, topic=FLOW_TOPIC)


@question_type(
    "comp.flowchart_trace_fluency",
    display_name={"th": "ไล่ผังงานที่มีการตัดสินใจ"},
    level=M1, subject=SUBJECT, topic=FLOW_TOPIC,
)
class FlowchartTraceFluency(QuestionType):
    def build(self, rng: Random, **params):
        spec = rng.choice(fc.BRANCHES)
        k = int(spec.test.split()[2])
        x = rng.choice((k - 2, k - 1, k, k, k + 1, k + 2))
        out = fc.run(spec, x).output
        other = fc.run(spec._replace(yes=spec.no, no=spec.yes), x).output
        slips = (other, fc.run(_flipped(spec), x).output, x)
        return _ask(spec, stem=f"จากผังงาน ถ้ารับค่า x = {x} ผังงานนี้จะแสดงผลเป็นเท่าใด",
                    correct=str(out), wrongs=_numbers(rng, out, slips), hint=TEST_HINT, topic=FLOW_TOPIC)


@question_type(
    "comp.flowchart_trace_application",
    display_name={"th": "เติมคำสั่งที่หายไปในผังงาน"},
    level=M1, subject=SUBJECT, topic=FLOW_TOPIC,
)
class FlowchartTraceApplication(QuestionType):
    """The statement that belongs in the "?" box, given one input and its output."""

    def build(self, rng: Random, **params):
        spec = rng.choice(fc.HOLES)
        x = rng.choice(fc.SEQ_INPUTS)
        out = fc.run(spec, x).output
        correct = spec.setup[spec.hole]

        def with_fill(statement: str) -> int:
            setup = list(spec.setup)
            setup[spec.hole] = statement
            return fc.run(spec, x, tuple(setup)).output

        wrongs = [s for s in _fills(correct) if with_fill(s) != out]
        return _ask(spec,
                    stem=f"จากผังงาน เมื่อรับค่า x = {x} ผังงานแสดงผลเป็น {out} คำสั่งในกล่อง ? ควรเป็นคำสั่งใด",
                    correct=correct, wrongs=rng.sample(wrongs, len(wrongs)),
                    hint="ลองนำแต่ละตัวเลือกไปใส่แทน ? แล้วไล่ผังงานด้วย x ที่กำหนด ตัวเลือกที่ถูกต้องต้องได้ผลตรงกับที่แสดง",
                    topic=FLOW_TOPIC)
