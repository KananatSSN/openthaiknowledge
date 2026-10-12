"""หมู่และคาบของธาตุ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/4

Sets moved here from: chemistry, science_wave_a5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import Block, math, text
from otk.core.distractors import sibling_answers
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.chemistry import (
    ELEMENTS,
    SUBJECT,
    TOPIC,
    Element,
    full_name,
    iupac_group,
    symbol_tex,
)
from otk.sets._support.science_wave_a5 import (
    METAL,
    METALLOID,
    NONMETAL,
    TABLE_POOL,
    _labelled,
    _position_label,
    block_class,
    metal_class,
    period_of,
)

PROVENANCE = Provenance("original")


def group_pool(lo: int, hi: int) -> list[Element]:
    """Elements whose หมู่ (IUPAC 1–18) falls in ``lo..hi`` inclusive."""
    pool = [e for e in ELEMENTS
            if (g := iupac_group(e)) is not None and lo <= g <= hi]
    if not pool:
        raise ValueError(f"no elements in groups {lo}–{hi}")
    return pool


def _group_order(content: list[Block]) -> int:
    """Sort key for a 'หมู่ N' choice: the number, so หมู่ 1 sits left of หมู่ 2."""
    return int(content[0].text.rsplit(" ", 1)[-1])


class GroupOfElement(QuestionType):
    """Given a ธาตุ, which หมู่ is it in? Drawn from one band of the table.

    Distractors are the หมู่ of *other* elements in the same band, so every wrong
    choice is a หมู่ the student is actually studying; de-duping means the correct
    หมู่ is never offered twice.

    ``ORDERED`` pins the choices in ascending หมู่ order instead of shuffling them
    — used for the two-choice หมู่ 1–2 band, where a stable left→right layout
    reads like the table itself.
    """

    LO: int = 1
    HI: int = 18
    ORDERED: bool = False

    def build(self, rng: Random) -> GeneratedQuestion:
        pool = group_pool(self.LO, self.HI)

        def answer(el: Element) -> list[Block]:
            return [text(f"หมู่ {iupac_group(el)}")]

        el = rng.choice(pool)
        return GeneratedQuestion(
            stem=[text(f"ธาตุ {full_name(el)} อยู่ในหมู่ใด"), math(symbol_tex(el))],
            correct=answer(el),
            distractors=sibling_answers(lambda: answer(rng.choice(pool))),
            topic=self.topic,
            order=_group_order if self.ORDERED else None,
        )


TOPIC_TABLE = "ธาตุและตารางธาตุ"


# (หมู่, คาบ) → the one element that sits there. Unique within TABLE_POOL, which
# is what lets the Application set ask "which element is at this position".
POSITIONS: dict[tuple[int, int], Element] = {
    (iupac_group(el), period_of(el)): el for el in TABLE_POOL  # type: ignore[misc]
}


@question_type("chem.group_of_element_1_2",
               display_name={"th": "ธาตุ → หมู่ (หมู่ 1–2)"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC)
class GroupOfElement12(GroupOfElement):
    LO, HI = 1, 2
    ORDERED = True


@question_type("chem.group_of_element_3_12",
               display_name={"th": "ธาตุ → หมู่ (หมู่ 3–12)"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC)
class GroupOfElement312(GroupOfElement):
    LO, HI = 3, 12


@question_type("chem.group_of_element_13_18",
               display_name={"th": "ธาตุ → หมู่ (หมู่ 13–18)"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC)
class GroupOfElement1318(GroupOfElement):
    LO, HI = 13, 18


@question_type("chem.element_in_group",
               display_name={"th": "หมู่ → ธาตุในหมู่"},
               level={"th": "ม.1"}, subject=SUBJECT, topic=TOPIC)
class ElementInGroup(QuestionType):
    """Given a หมู่, pick a ธาตุ that belongs to it.

    Exactly one choice is in the asked หมู่ — the distractors are drawn only from
    *other* หมู่, so there is a single correct answer no matter how they shuffle.
    """

    # หมู่ that actually hold at least one element.
    GROUPS = sorted({iupac_group(e) for e in ELEMENTS} - {None})

    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(self.GROUPS)
        in_group = group_pool(g, g)
        others = [e for e in ELEMENTS if iupac_group(e) not in (None, g)]

        def name(el: Element) -> list[Block]:
            return [text(full_name(el))]

        return GeneratedQuestion(
            stem=[text(f"ธาตุใดต่อไปนี้อยู่ในหมู่ {g} ของตารางธาตุ")],
            correct=name(rng.choice(in_group)),
            distractors=sibling_answers(lambda: name(rng.choice(others))),
            topic=self.topic,
        )


@question_type(
    "chem.period_of_element_fluency",
    display_name={"th": "ธาตุ → หมู่และคาบ"},
    level={"th": "ม.4"}, subject=SUBJECT, topic=TOPIC_TABLE,
)
class PeriodOfElementFluency(QuestionType):
    """Read both coordinates of one element off the table at once.

    The older หมู่ sets ask for the หมู่ alone; naming the คาบ in the same breath
    is what ม.4/4 actually asks for, and it is where the row-counting slip shows.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        el = rng.choice(TABLE_POOL)
        group, period = iupac_group(el), period_of(el)
        assert group is not None
        # Each authored wrong moves exactly one coordinate away from the truth,
        # so a learner who has only one of the two right still cannot land on
        # it. Spares move both, or the answer would be the choice every wrong
        # shares a coordinate with.
        near_period = period + 1 if period == 1 else period - 1
        far_period = period + 2 if period <= 5 else period - 2
        near_group = group + 1 if group < 18 else group - 1
        return _labelled(
            stem=f"ธาตุ {full_name(el)} อยู่หมู่ใดและคาบใดของตารางธาตุ",
            correct=_position_label(group, period),
            wrongs=(
                _position_label(group, near_period),
                _position_label(near_group, period),
                _position_label(group, far_period),
                _position_label(near_group, near_period),
                _position_label(near_group, far_period),
            ),
            topic=TOPIC_TABLE,
            hint="คาบคือแถวในแนวนอน นับจากแถวบนสุดเป็นคาบ 1 ส่วนหมู่คือสดมภ์ในแนวตั้ง",
        )


@question_type(
    "chem.element_class_application",
    display_name={"th": "ตำแหน่งในตารางธาตุ → ธาตุและกลุ่มของธาตุ"},
    level={"th": "ม.4"}, subject=SUBJECT, topic=TOPIC_TABLE,
)
class ElementClassApplication(QuestionType):
    """Go from a position to the element, then classify it — two steps, one answer.

    ม.4/4 asks for หมู่, คาบ, ความเป็นโลหะ/อโลหะ/กึ่งโลหะ and เรพรีเซนเททีฟ/แทรนซิชัน
    together. The Fluency set covers the coordinates; this one requires locating
    the element from them and then saying what kind of element it is.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        (group, period), el = rng.choice(sorted(POSITIONS.items()))
        kind, block = metal_class(el), block_class(el)

        def label(target: Element, target_kind: str, target_block: str) -> str:
            return (f"{full_name(target)} จัดเป็น{target_kind} "
                    f"และอยู่ในกลุ่ม{target_block}")

        # First the same element filed under a class it does not belong to —
        # that is the mistake this set is built to catch — then other elements
        # described correctly, so reading the position still matters.
        other_kind = next(name for name in (METAL, NONMETAL, METALLOID)
                          if name != kind)
        wrongs = [label(el, other_kind, block)]
        others = [other for other in TABLE_POOL if other.symbol != el.symbol]
        rng.shuffle(others)
        for other in others:
            if len(wrongs) >= 3:
                break
            wrong = label(other, metal_class(other), block_class(other))
            if wrong not in wrongs:
                wrongs.append(wrong)

        return _labelled(
            stem=(f"ธาตุที่อยู่หมู่ {group} และคาบ {period} ของตารางธาตุคือธาตุใด "
                  "และจัดอยู่ในกลุ่มใด"),
            correct=label(el, kind, block),
            wrongs=tuple(wrongs),
            topic=TOPIC_TABLE,
            hint=("หาตำแหน่งให้ได้ธาตุก่อน แล้วจึงดูว่าธาตุนั้นอยู่ซ้ายหรือขวาของเส้นขั้นบันได "
                  "และอยู่ในสดมภ์กลางตารางหรือไม่"),
        )
