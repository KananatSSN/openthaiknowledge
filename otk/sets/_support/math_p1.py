"""ป.1 sets that the สสวท. books teach and the catalog did not have.

The grade's word problems were one sentence each — "แก้วมีลูกอม … แม่ให้เพิ่ม
อีก …" — and whole chapters had no set at all: แบบรูป (ค 1.2 ป.1/1), การบวก
ลบระคน, and reading a แผนภูมิรูปภาพ (ค 3.1 ป.1/1). This module adds them in
book order, drawing situations from :mod:`._story` so one set covers many
stories rather than one.

Every number a ป.1 learner sees stays within 0–100, the grade's range.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType

LEVEL = {"th": "ป.1"}


def _texts(correct: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """A question whose choices are Thai text, wrongs offered in order."""
    return GeneratedQuestion(stem=[], correct=[text(correct)],
                             distractors=fixed(*[[text(w)] for w in wrongs]),
                             topic=topic)


# ── โจทย์ปัญหา (ค 1.1 ป.1/5) ─────────────────────────────────────────────────


# ── การบวกลบระคน ─────────────────────────────────────────────────────────────


# ── แบบรูป (ค 1.2 ป.1/1) ─────────────────────────────────────────────────────

def _step_sequence(rng: Random, steps: tuple[int, ...], hi: int, length: int = 5):
    """An arithmetic run within 0..hi, rising or falling by one of ``steps``."""
    step = rng.choice(steps)
    if rng.random() < 0.5:
        step = -step
    span = abs(step) * (length - 1)
    start = rng.randint(0, hi - span)
    terms = [start + abs(step) * i for i in range(length)]
    return (terms if step > 0 else terms[::-1]), step


class NumberPatternType(MathType):
    """Find the missing term of an increasing or decreasing pattern."""

    STEPS: tuple[int, ...] = (1, 10)
    HI = 100

    def expr(self, rng: Random, length: int = 5):
        length = max(4, min(int(length), 7))
        terms, step = _step_sequence(rng, self.STEPS, self.HI, length)
        gap = rng.randrange(length)
        ans = terms[gap]
        shown = [r"\square" if i == gap else str(n) for i, n in enumerate(terms)]
        s = abs(step)
        return MathDraw(
            r",\ ".join(shown), str(ans),
            prompt="จงหาจำนวนที่หายไปในแบบรูป",
            # A neighbour already on show, then a step of the other size.
            distractors=_story.keep(ans + s, ans - s, ans + (1 if s != 1 else 10),
                                    ans - (1 if s != 1 else 10), answer=ans,
                                    hi=self.HI))


_SHAPES = ("○", "△", "□", "☆", "◇", "♡", "●", "▲", "■", "★")


class RepeatingPatternType(QuestionType):
    """A repeating pattern of shapes with one gap: which shape goes there?"""

    UNIT = 2

    def build(self, rng: Random, length: int = 8) -> GeneratedQuestion:
        length = max(self.UNIT * 2 + 1, min(int(length), 12))
        unit = rng.sample(_SHAPES, self.UNIT)
        if self.UNIT == 3 and rng.random() < 0.4:
            # AAB / ABB: a unit of three that uses two shapes.
            a, b = unit[:2]
            unit = rng.choice(([a, a, b], [a, b, b]))
        row = [unit[i % self.UNIT] for i in range(length)]
        gap = rng.choice((length - 1, rng.randrange(self.UNIT, length - 1)))
        ans = row[gap]
        shown = "  ".join("___" if i == gap else s for i, s in enumerate(row))
        others = [s for s in _SHAPES if s not in unit]
        wrongs = [s for s in dict.fromkeys(unit) if s != ans] + rng.sample(others, 3)
        return GeneratedQuestion(
            stem=[text("รูปใดควรอยู่ในช่องว่าง"), text(shown)],
            correct=[text(ans)],
            distractors=fixed(*[[text(w)] for w in wrongs]),
            topic=self.topic,
        )


class PatternRuleType(QuestionType):
    """Name the rule of a number pattern: เพิ่มขึ้น/ลดลงทีละเท่าใด."""

    STEPS: tuple[int, ...] = (1, 10)
    HI = 100

    def build(self, rng: Random) -> GeneratedQuestion:
        terms, step = _step_sequence(rng, self.STEPS, self.HI, 5)

        def rule(k: int) -> str:
            return f"{'เพิ่มขึ้น' if k > 0 else 'ลดลง'}ทีละ {abs(k)}"

        pool = [rule(s * sign) for s in self.STEPS for sign in (1, -1)]
        # A step outside the set keeps four choices when only two sizes exist.
        extra = [rule(s * sign) for s in (2, 5, 100) if s not in self.STEPS
                 for sign in (1, -1)]
        wrongs = [rule(-step)] + [r for r in pool if r not in (rule(step), rule(-step))]
        wrongs += [r for r in extra if abs(int(r.split()[-1])) < self.HI]
        return GeneratedQuestion(
            stem=[text("แบบรูปต่อไปนี้มีความสัมพันธ์แบบใด"),
                  content_math(r",\ ".join(map(str, terms)))],
            correct=[text(rule(step))],
            distractors=fixed(*[[text(w)] for w in wrongs]),
            topic=self.topic,
        )


# ── การนับ: ตัวเลขและตัวหนังสือ (ค 1.1 ป.1/1) ─────────────────────────────────


# ── การเปรียบเทียบ (ค 1.1 ป.1/2) ──────────────────────────────────────────────


# ── การวัด (ค 2.1 ป.1/1–2) ────────────────────────────────────────────────────


# ── แผนภูมิรูปภาพ (ค 3.1 ป.1/1) — 1 รูปแทน 1 หน่วย ──────────────────────────


