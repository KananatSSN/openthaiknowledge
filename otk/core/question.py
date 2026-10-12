"""Question, Choice, and the intermediate a generator returns.

A :class:`Question` is a fully-assembled multiple-choice item: a stem, a list of
choices, and the index of the correct one. The correct index is server-only —
:meth:`Question.public` drops it, and only the signed practice token carries it
to the answer endpoint. This preserves today's "the answer never reaches the
browser" property over structured content.

A question *type* does not build a :class:`Question` directly. It returns a
:class:`GeneratedQuestion` — the stem, the correct choice's content, and a
*distractor strategy* — and the registry materializes distractors, shuffles,
and records where the correct choice landed. Keeping shuffling/assembly in one
place means every type gets the same guarantees for free.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, Optional

from pydantic import BaseModel, Field, model_validator

from .content import Block

if TYPE_CHECKING:
    from .distractors import DistractorStrategy


class Choice(BaseModel):
    content: list[Block]


class Question(BaseModel):
    type: str
    topic: str
    level: str = ""
    stem: list[Block]
    choices: list[Choice]
    answer: int                                    # index into choices
    hint: list[Block] = Field(default_factory=list)
    # The named mistake each choice stands for (otk.core.mistakes), aligned with
    # ``choices``; None where nobody named one, and always None at ``answer``.
    # Excluded from every dump: a label says a choice is wrong, so like the
    # answer it is server-only, and leaving it out keeps existing payloads,
    # hashes and contracts byte-identical.
    mistakes: list[Optional[str]] = Field(default_factory=list, exclude=True)

    @model_validator(mode="after")
    def _answer_in_range(self) -> "Question":
        if not 0 <= self.answer < len(self.choices):
            raise ValueError(
                f"answer index {self.answer} out of range for "
                f"{len(self.choices)} choices"
            )
        if self.mistakes:
            if len(self.mistakes) != len(self.choices):
                raise ValueError("mistakes must line up with choices")
            if self.mistakes[self.answer] is not None:
                raise ValueError("the correct choice cannot carry a mistake")
        return self

    def public(self) -> "PublicQuestion":
        """Projection sent to the quiz client — no ``answer`` field."""
        return PublicQuestion(
            type=self.type, topic=self.topic,
            stem=self.stem, choices=self.choices, hint=self.hint,
        )


class PublicQuestion(BaseModel):
    """What the browser receives. Deliberately has no ``answer``."""
    type: str
    topic: str
    stem: list[Block]
    choices: list[Choice]
    hint: list[Block] = Field(default_factory=list)


@dataclass
class GeneratedQuestion:
    """A type's raw output, before distractors are drawn and choices shuffled.

    Internal to the domain (never serialized), so a dataclass, not a Pydantic
    model — it holds a live :class:`DistractorStrategy` callable.
    """
    stem: list[Block]
    correct: list[Block]                           # content of the correct choice
    distractors: "DistractorStrategy"
    topic: str
    hint: list[Block] = field(default_factory=list)
    # By default the assembler shuffles the choices. A type may instead pin their
    # order by supplying a sort key over choice contents — e.g. so หมู่ 1 always
    # sits left of หมู่ 2. When set, choices are sorted by it rather than shuffled.
    order: Optional[Callable[[list[Block]], object]] = None
