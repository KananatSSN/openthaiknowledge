"""``PhysCalc`` — the shared "compute a value from a Thai scenario" question type.

The third recurring shape after ``ClassifyType`` and ``ConceptBankType``: a word
problem carrying numbers, whose answer is a bare value. A subclass draws one
:class:`Calc` — the Thai scenario, the answer, and the *classic miscalculations*
that make the best distractors (adding instead of multiplying, forgetting to
convert นาที to วินาที, dropping a square). Those hand-picked wrongs come first;
answers of other draws and ±neighbours pad out to four choices.

Physics owns the original; ไฟฟ้า reuses it, so it lives here beside the other
shared bases rather than in one subject module.
"""

from __future__ import annotations

from abc import abstractmethod
from dataclasses import dataclass
from random import Random

from otk.core.content import math, text
from otk.core.distractors import combine, fixed, numeric_neighbors, sibling_answers
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType


def fmt(x) -> str:
    """Format a number for a MathBlock: 2.0 → '2', 1.5 → '1.5'."""
    if isinstance(x, int) or (isinstance(x, float) and x.is_integer()):
        return str(int(x))
    return f"{x:g}"


@dataclass
class Calc:
    """One drawn numeric item: the Thai scenario, the answer, its wrong values."""
    prompt: str                              # scenario + the asked unit
    answer: str                              # bare value, as MathBlock notation
    wrongs: tuple[str, ...] = ()             # diagnostic miscalculations
    hint: str = ""


class PhysCalc(QuestionType):
    """Base: draw a scenario, answer with a bare value, offer classic wrong ones.

    ``draw`` returns a :class:`Calc`; its numeric-default kwargs (if any) become
    tunable ranges, exactly like a math type's ``expr``. Distractors are the
    hand-picked ``wrongs`` first, then answers of *other* draws, then ±neighbours
    for the integer cases — so a full four choices without inventing nonsense.
    """

    def _param_fn(self):
        return self.draw

    @abstractmethod
    def draw(self, rng: Random) -> Calc:
        """Return one :class:`Calc`."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        c = self.draw(rng, **params)

        def sample():
            return [math(self.draw(rng, **params).answer)]

        return GeneratedQuestion(
            stem=[text(c.prompt)],
            correct=[math(c.answer)],
            distractors=combine(fixed(*[[math(w)] for w in c.wrongs]),
                                sibling_answers(sample),
                                numeric_neighbors()),
            topic=self.topic,
            hint=[math(c.hint)] if c.hint else [],
        )


def slips(answer: str, *candidates) -> tuple[str, ...]:
    """Format candidate miscalculations, dropping the useless ones.

    Saves every ``draw`` the same three lines. A diagnostic wrong value is only
    wrong for *some* draws (``a·L`` equals ``a·L/b`` when ``b`` is 1), and a
    duplicate would be silently dropped by the distractor combiner anyway.
    Non-positive candidates go too: subtracting where the formula multiplies is a
    real mistake, but a resistance of −3 โอห์ม is not a choice anyone weighs. What
    survives is rounded to two places, because an inverted ratio like 0.0833333
    is eliminated on sight — the wrong choice has to look like something a
    student would actually write down.
    """
    out: list[str] = []
    for c in candidates:
        c = round(c, 2)                      # round first: 2/440 must not reach 0
        if c <= 0:
            continue
        s = fmt(c)
        if s != answer and s not in out:
            out.append(s)
    return tuple(out)
