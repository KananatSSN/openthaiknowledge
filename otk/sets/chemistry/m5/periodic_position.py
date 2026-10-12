"""หมู่ คาบ และการจัดกลุ่มธาตุจากตารางธาตุ

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/5

Sets moved here from: science_wave_e2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.chemistry import Element, full_name, iupac_group
from otk.sets._support.science_wave_a5 import (
    METAL,
    METALLOID,
    NONMETAL,
    REPRESENTATIVE,
    TABLE_POOL,
    TRANSITION_BLOCK,
    _position_label,
    block_class,
    metal_class,
    period_of,
)
from otk.sets._support.science_wave_e2 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_TABLE = "หมู่ คาบ และการจัดกลุ่มธาตุจากตารางธาตุ"


POSITIONS_TABLE: dict[tuple[int, int], Element] = {
    (iupac_group(el), period_of(el)): el for el in TABLE_POOL  # type: ignore[misc]
}


TRANSITION_ELEMENTS: tuple[Element, ...] = tuple(
    el for el in TABLE_POOL if block_class(el) == TRANSITION_BLOCK
)


REPRESENTATIVE_ELEMENTS: tuple[Element, ...] = tuple(
    el for el in TABLE_POOL if block_class(el) == REPRESENTATIVE
)


@question_type(
    "chem.periodic_position_foundation",
    display_name={"th": "ธาตุ → หมู่และคาบ"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_TABLE,
)
class PeriodicPositionFoundation(QuestionType):
    """หมู่และคาบ alone — the narrower half of ม.5/5."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        el = rng.choice(TABLE_POOL)
        group, period = iupac_group(el), period_of(el)
        assert group is not None
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
                # Both coordinates moved, so the answer is not the choice every
                # wrong shares a coordinate with.
                _position_label(near_group, near_period),
                _position_label(near_group, far_period),
            ),
            topic=TOPIC_TABLE,
            hint="คาบคือแถวในแนวนอน นับจากแถวบนสุดเป็นคาบ 1 ส่วนหมู่คือสดมภ์ในแนวตั้ง",
        )


@question_type(
    "chem.periodic_position_fluency",
    display_name={"th": "ตำแหน่งในตารางธาตุ → ธาตุและกลุ่มของธาตุ"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_TABLE,
)
class PeriodicPositionFluency(QuestionType):
    """The whole ม.5/5 indicator: locate the element, then classify it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        (group, period), el = rng.choice(sorted(POSITIONS_TABLE.items()))
        kind, block = metal_class(el), block_class(el)

        def label(target: Element, target_kind: str, target_block: str) -> str:
            return f"{full_name(target)} จัดเป็น{target_kind} และอยู่ในกลุ่ม{target_block}"

        other_kind = next(name for name in (METAL, NONMETAL, METALLOID) if name != kind)
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


@question_type(
    "chem.periodic_position_application",
    display_name={"th": "กลุ่มธาตุสามชนิดที่อยู่ในกลุ่มเดียวกันทั้งหมด"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_TABLE,
)
class PeriodicPositionApplication(QuestionType):
    """Pick the trio of elements that all belong to the named block."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        block = rng.choice((REPRESENTATIVE, TRANSITION_BLOCK))
        same_pool = TRANSITION_ELEMENTS if block == TRANSITION_BLOCK else REPRESENTATIVE_ELEMENTS
        other_pool = REPRESENTATIVE_ELEMENTS if block == TRANSITION_BLOCK else TRANSITION_ELEMENTS
        trio = list(rng.sample(same_pool, 3))
        swaps = rng.sample(other_pool, 3)

        def label(elements: list[Element]) -> str:
            return " และ ".join(el.symbol for el in elements)

        correct = label(trio)
        wrongs = []
        for index, swap in enumerate(swaps):
            variant = list(trio)
            variant[index] = swap
            wrongs.append(label(variant))
        # Two of the three swapped out: wrong twice over, so the answer is not
        # the trio every wrong shares two elements with.
        for first, second in ((0, 1), (1, 2)):
            variant = list(trio)
            variant[first], variant[second] = swaps[first], swaps[second]
            wrongs.append(label(variant))

        return _labelled(
            stem=f"ธาตุชุดใดต่อไปนี้จัดอยู่ในกลุ่ม{block}ทั้งสามชนิด",
            correct=correct,
            wrongs=tuple(wrongs),
            topic=TOPIC_TABLE,
            hint=("ธาตุแทรนซิชันคือธาตุหมู่ 3-12 ของตารางธาตุ "
                  "ส่วนธาตุเรพรีเซนเททีฟคือธาตุหมู่ 1-2 และ 13-18"),
        )
