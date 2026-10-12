"""ชุดรวมสูตรพลังงานไฟฟ้า (ความเข้ากันได้)

ฟิสิกส์ · ม.3 · เสริมทักษะ
Indicators: —

Sets moved here from: electricity, science_successors.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math, text
from otk.core.distractors import combine, fixed, numeric_neighbors, sibling_answers
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import question_type
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.electricity import LEVEL, SUBJECT, TOPIC
from otk.sets._support.science_successors import FluencyStage

PROVENANCE = Provenance("original")


@question_type("elec.energy",
               display_name={"th": "พลังงานไฟฟ้า (W = Pt และ W = QV)"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class Energy(PhysCalc):
    """W = Pt (ตัวอย่างที่ 1 ในชีท) และ W = QV เป็นจูล.

    เมื่อโจทย์ให้เวลาเป็น *นาที* คำตอบที่ลืมแปลงเป็นวินาทีจะถูกเสนอเป็นตัวเลือกเสมอ
    นั่นคือกับดักหลักของสูตรนี้ (100 วัตต์ 5 นาที ตอบ 500 แทน 30,000 จูล).
    """

    _P = [40, 60, 100, 200, 500, 1000]       # กำลังไฟฟ้า (วัตต์)
    _MIN = [2, 3, 5, 10]                     # เวลา (นาที)
    _SEC = [30, 60, 120, 300]                # เวลา (วินาที)
    _Q = [2, 3, 5, 10]                       # ประจุไฟฟ้า (คูลอมบ์)
    _V = [6, 12, 24, 220]                    # ความต่างศักย์ (โวลต์)

    def draw(self, rng: Random) -> Calc:
        which = rng.random()
        if which < 0.35:                     # ให้ P กับเวลาเป็นนาที → หา W
            p, mins = rng.choice(self._P), rng.choice(self._MIN)
            w = p * mins * 60
            return Calc(
                f"หลอดไฟฟ้าขนาด {p} วัตต์ เปิดใช้งานนาน {mins} นาที "
                f"สิ้นเปลืองพลังงานไฟฟ้าไปเท่าใด (จูล)",
                fmt(w), wrongs=slips(fmt(w), p * mins, p * 60, mins * 60),
                hint=r"W = Pt")
        if which < 0.6:                      # ให้ P กับเวลาเป็นวินาที → หา W
            p, sec = rng.choice(self._P), rng.choice(self._SEC)
            w = p * sec
            return Calc(
                f"เครื่องใช้ไฟฟ้าขนาด {p} วัตต์ ทำงานนาน {sec} วินาที "
                f"ใช้พลังงานไฟฟ้าไปเท่าใด (จูล)",
                fmt(w), wrongs=slips(fmt(w), p * sec / 60, p + sec, p * 60),
                hint=r"W = Pt")
        if which < 0.8:                      # ให้ W กับเวลา → หา P
            p, sec = rng.choice(self._P), rng.choice(self._SEC)
            w = p * sec
            return Calc(
                f"เครื่องใช้ไฟฟ้าเครื่องหนึ่งใช้พลังงานไฟฟ้า {w} จูล "
                f"ในเวลา {sec} วินาที เครื่องนี้ใช้กำลังไฟฟ้าเท่าใด (วัตต์)",
                fmt(p), wrongs=slips(fmt(p), w * 60 / sec, w / 60, sec),
                hint=r"P = \frac{W}{t}")
        q, v = rng.choice(self._Q), rng.choice(self._V)
        w = q * v
        return Calc(                         # ให้ Q กับ V → หา W
            f"เคลื่อนประจุไฟฟ้า {q} คูลอมบ์ ผ่านความต่างศักย์ {v} โวลต์ "
            f"มีพลังงานไฟฟ้าถ่ายโอนขนาดเท่าใด (จูล)",
            fmt(w), wrongs=slips(fmt(w), q + v, v / q, w * 2),
            hint=r"W = QV")


class _PinnedEnergy(FluencyStage, Energy):
    """Energy base whose distractor sampler cannot cross formula scopes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        calc = self.draw(rng)

        def sample():
            return [math(self.draw(rng).answer)]

        return GeneratedQuestion(
            stem=[text(calc.prompt)],
            correct=[math(calc.answer)],
            distractors=combine(
                fixed(*[[math(value)] for value in calc.wrongs]),
                sibling_answers(sample),
                numeric_neighbors(),
            ),
            topic=self.topic,
            hint=[math(calc.hint)] if calc.hint else [],
        )
