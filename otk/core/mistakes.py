"""Named mistakes — which misconception a wrong choice stands for.

Types have always hand-picked their most diagnostic wrong answers ("adding
numerators and denominators"), but the name lived only in a comment, so a
learner's stats could say *that* they were wrong and never *how*. A type now
wraps such a value in :func:`named`:

    wrongs = [named("fraction.add_across", as_mixed(naive)), ...]

``named`` returns the value unchanged, so it slots into ``_story.keep``,
``fixed``, ``MathDraw.distractors`` or any other path without touching them.
As a side effect it records value -> mistake in a ledger scoped to the one
``QuestionType.generate`` call that is running. After distractors are drawn,
balanced and shuffled, the assembler labels each final wrong choice by looking
it up in that ledger (:func:`label_for`). A choice the balancer invented or
sampled has no entry and stays unlabelled, which is the truth: nobody can say
which mistake it represents.

Labels are server-only, like the answer index: a label on a choice says it is
wrong, so it must never reach the browser.

Keys are shared across sets on purpose. "Scaled by adding the difference" is
the same misconception in a unit-price set and a recipe set, and the stats page
aggregates by key to show the learner a pattern rather than a one-off.
"""

from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from typing import Iterator, TypeVar

from pydantic import BaseModel

T = TypeVar("T")

# key -> learner-facing name. Written as what the learner did, not as a
# judgement, so the stats page can say "You often: <name>".
MISTAKES: dict[str, dict[str, str]] = {
    "fraction.add_across": {
        "th": "บวกหรือลบเศษกับเศษ และส่วนกับส่วนตรง ๆ โดยไม่ทำส่วนให้เท่ากันก่อน",
        "en": "Added or subtracted numerators and denominators straight across, "
              "without a common denominator",
    },
    "operation.reversed": {
        "th": "ใช้การดำเนินการผิด เช่น บวกแทนลบ หรือคูณแทนหาร",
        "en": "Used the wrong operation, such as adding instead of subtracting "
              "or multiplying instead of dividing",
    },
    "part.complement": {
        "th": "หาส่วนที่เหลือ แทนที่จะหาส่วนที่โจทย์ถาม (หรือกลับกัน)",
        "en": "Found the other part of the whole instead of the part asked for",
    },
    "fraction.unit_share_only": {
        "th": "หารด้วยตัวส่วนแล้วหยุด ลืมคูณด้วยตัวเศษ",
        "en": "Divided by the denominator and forgot to multiply by the numerator",
    },
    "fraction.scaled_both_terms": {
        "th": "คูณทั้งตัวเศษและตัวส่วนด้วยจำนวนนับ",
        "en": "Multiplied both the numerator and the denominator by the whole number",
    },
    "fraction.not_worked_back": {
        "th": "หาเศษส่วนของจำนวนที่ให้มา แทนที่จะย้อนกลับไปหาจำนวนทั้งหมด",
        "en": "Took the fraction of the given part instead of working back to the whole",
    },
    "fraction.digits_as_decimal": {
        "th": "เขียนตัวเศษกับตัวส่วนต่อกันเป็นทศนิยม",
        "en": "Wrote the numerator and denominator side by side as a decimal",
    },
    "fraction.numerator_as_tenths": {
        "th": "อ่านตัวเศษเป็นจำนวนส่วนสิบ โดยไม่สนใจตัวส่วน",
        "en": "Read the numerator as tenths and ignored the denominator",
    },
    "fraction.inverted": {
        "th": "หารตัวส่วนด้วยตัวเศษ (กลับเศษส่วน)",
        "en": "Divided the denominator by the numerator, turning the fraction upside down",
    },
    "mixed.whole_part_only": {
        "th": "ใช้เฉพาะจำนวนเต็มของจำนวนคละ ทิ้งเศษส่วนไป",
        "en": "Used only the whole-number part of a mixed number",
    },
    "decimal.point_misplaced": {
        "th": "วางจุดทศนิยมผิดตำแหน่ง",
        "en": "Put the decimal point in the wrong place",
    },
    "percent.answered_the_percent": {
        "th": "ตอบเป็นร้อยละ แทนที่จะตอบเป็นจำนวน",
        "en": "Gave a percentage as the answer instead of an amount",
    },
    "percent.subtracted_the_number": {
        "th": "ลบตัวเลขร้อยละออกจากจำนวนตรง ๆ",
        "en": "Subtracted the percentage number straight from the amount",
    },
    "percent.part_as_percent": {
        "th": "ตอบจำนวนส่วนย่อยเป็นร้อยละ โดยไม่เทียบกับจำนวนทั้งหมด",
        "en": "Gave the part as the percentage without comparing it to the whole",
    },
    "steps.missed_a_step": {
        "th": "ทำไม่ครบทุกขั้นตอน ข้ามขั้นตอนใดขั้นตอนหนึ่งไป",
        "en": "Left out one of the steps",
    },
    "steps.wrong_order": {
        "th": "ทำขั้นตอนสลับลำดับกัน",
        "en": "Did the steps in the wrong order",
    },
    "units.not_converted": {
        "th": "ไม่ได้แปลงหน่วยตามที่โจทย์ถาม",
        "en": "Left the answer in the original unit instead of converting it",
    },
    "units.wrong_conversion": {
        "th": "ใช้อัตราการแปลงหน่วยผิด",
        "en": "Used the wrong conversion between units",
    },
    "volume.area_not_volume": {
        "th": "หาพื้นที่ (คูณสองด้าน) แทนปริมาตร",
        "en": "Found an area (two measures multiplied) instead of a volume",
    },
    "volume.surface_not_volume": {
        "th": "หาพื้นที่ผิวทั้งหมด แทนปริมาตร",
        "en": "Found the surface area instead of the volume",
    },
    "power.multiplied_by_exponent": {
        "th": "คูณด้วยเลขชี้กำลัง แทนการยกกำลัง",
        "en": "Multiplied by the power instead of raising to it",
    },
    "area.forgot_half": {
        "th": "ลืมคูณด้วยครึ่งหนึ่งในสูตรพื้นที่",
        "en": "Forgot the one half in the area formula",
    },
    "proportion.additive": {
        "th": "ขยายสัดส่วนด้วยการบวกผลต่าง แทนการคูณ",
        "en": "Scaled a proportion by adding the difference instead of multiplying",
    },
    "proportion.no_divide": {
        "th": "คูณจำนวนในโจทย์เข้าด้วยกัน โดยไม่หาค่าต่อหนึ่งหน่วยก่อน",
        "en": "Multiplied the given numbers together without first finding the "
              "amount for one",
    },
    "proportion.unit_rate_only": {
        "th": "หาค่าต่อหนึ่งหน่วยแล้วตอบเลย โดยไม่คูณต่อ",
        "en": "Found the amount for one and stopped there",
    },
    "direction.left_right_swapped": {
        "th": "สลับด้านซ้ายกับด้านขวา",
        "en": "Swapped left and right",
    },
    "direction.opposite": {
        "th": "ตอบทิศตรงข้ามกับทิศที่ถูก",
        "en": "Gave the opposite direction",
    },
    "time.east_west_reversed": {
        "th": "สลับว่าทางตะวันออกหรือทางตะวันตกมีเวลาเร็วกว่า จึงบวกแทนลบหรือลบแทนบวก",
        "en": "Mixed up which side is ahead in time, so added instead of "
              "subtracting or the other way round",
    },
    "count.lines_not_gaps": {
        "th": "นับจำนวนเส้นแทนจำนวนช่วงระหว่างเส้น",
        "en": "Counted the lines instead of the gaps between them",
    },
    "time.date_not_changed": {
        "th": "ไม่ได้เปลี่ยนวันที่ เมื่อเวลาเลยเที่ยงคืนหรือข้ามเส้นวันที่สากล",
        "en": "Kept the same date when the time passed midnight or crossed the date line",
    },
}


def mistake_names() -> dict[str, dict[str, str]]:
    """The catalog of mistake names, for publishing with the catalog snapshot."""
    return {key: dict(names) for key, names in sorted(MISTAKES.items())}


# value-key -> mistake key, for the generate() call in progress; None outside one.
_LEDGER: ContextVar[dict[tuple, str] | None] = ContextVar("mistake_ledger", default=None)


def _value_key(value: object) -> tuple | None:
    """How a named value is matched to a final choice. A content list matches on
    its blocks; anything else (an int, a TeX or Thai string) matches a choice
    that is exactly one block showing ``str(value)``."""
    if isinstance(value, list) and value and all(
        isinstance(b, BaseModel) and hasattr(b, "kind") for b in value
    ):
        return ("content", *(_block_key(b) for b in value))
    if isinstance(value, (str, int)) and not isinstance(value, bool):
        return ("single", str(value))
    return None


def _block_key(block) -> tuple:
    return (block.kind, getattr(block, "tex", getattr(block, "text", getattr(block, "code", ""))))


def _content_keys(content: list) -> list[tuple]:
    keys = [("content", *(_block_key(b) for b in content))]
    if len(content) == 1:
        keys.append(("single", _block_key(content[0])[1]))
    return keys


def named(key: str, value: T) -> T:
    """Mark ``value`` as the wrong answer that mistake ``key`` produces; return it.

    The first naming of a value wins. Two mistakes that land on the same value
    for a draw cannot be told apart from the learner's choice, and the earlier
    one is the more diagnostic by the authoring convention (most diagnostic
    first), the same rule ``fixed`` and ``keep`` use when they drop duplicates.
    """
    if key not in MISTAKES:
        raise KeyError(f"unknown mistake {key!r}; add it to otk.core.mistakes.MISTAKES")
    ledger = _LEDGER.get()
    value_key = _value_key(value)
    if ledger is not None and value_key is not None:
        ledger.setdefault(value_key, key)
    return value


@contextmanager
def recording() -> Iterator[dict[tuple, str]]:
    """Collect :func:`named` calls made while building one question."""
    ledger: dict[tuple, str] = {}
    token = _LEDGER.set(ledger)
    try:
        yield ledger
    finally:
        _LEDGER.reset(token)


def label_for(ledger: dict[tuple, str], content: list) -> str | None:
    """The mistake a final choice stands for, if a type named it."""
    for key in _content_keys(content):
        if key in ledger:
            return ledger[key]
    return None
