"""Wave E slice 9 — redox, radioactive decay, and the uses of radioisotopes.

Closes the last three core indicators of ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/23`` อธิบายความหมายของปฏิกิริยารีดอกซ์ — a single verb, default
  filing: Foundation ``standard_scope``, Fluency ``exact``, Application
  ``standard_scope``.
* ``ว 2.1 ม.5/24`` อธิบายสมบัติของสารกัมมันตรังสี และคำนวณครึ่งชีวิตและปริมาณ
  ของสารกัมมันตรังสี — two free verbs joined by "และ", each with its own
  object, so Foundation (the properties) and Fluency (the calculation) are both
  ``exact``.
* ``ว 2.1 ม.5/25`` สืบค้นข้อมูลและนำเสนอตัวอย่างประโยชน์ของสารกัมมันตรังสีและ
  การป้องกันอันตรายที่เกิดจากกัมมันตภาพรังสี — สืบค้นข้อมูล is not itself
  assessable, so นำเสนอตัวอย่าง carries the record: default filing.

The core course names electron transfer, not oxidation numbers, so every redox
item is argued from who gives and who takes electrons. Where an item needs the
order in which metals give up electrons, the stem states it rather than
assuming the เคมีเพิ่มเติม reactivity series.

Half-lives are the real values, and every calculated amount is a whole number
of halvings so the arithmetic is exact.
"""

from __future__ import annotations

from fractions import Fraction
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}


def _labelled(*, stem, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)] if isinstance(stem, str) else stem,
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


def _show(x) -> str:
    """A number as a learner would write it: no trailing zeros, thousands grouped."""
    value = float(x)
    if value == int(value):
        return f"{int(value):,}"
    return f"{value:,.2f}".rstrip("0").rstrip(".")


# ══ ว 2.1 ม.5/23 — ปฏิกิริยารีดอกซ์ ═══════════════════════════════════════════


# ══ ว 2.1 ม.5/24 — สมบัติของสารกัมมันตรังสีและครึ่งชีวิต ═════════════════════════

ALPHA, BETA, GAMMA = "รังสีแอลฟา", "รังสีบีตา", "รังสีแกมมา"
RAYS = (ALPHA, BETA, GAMMA)


class Isotope(NamedTuple):
    name: str        # e.g. "ไอโอดีน-131"
    half_life: Fraction
    unit: str        # วัน, ชั่วโมง, ปี
    ray: str
    use: str         # what it is used for


ISOTOPES: tuple[Isotope, ...] = (
    Isotope("ไอโอดีน-131", Fraction(8), "วัน", BETA, "ตรวจและรักษาโรคต่อมไทรอยด์"),
    Isotope("เทคนีเชียม-99m", Fraction(6), "ชั่วโมง", GAMMA, "ถ่ายภาพการทำงานของอวัยวะในร่างกาย"),
    Isotope("ฟอสฟอรัส-32", Fraction(14), "วัน", BETA, "ศึกษาการดูดซึมปุ๋ยฟอสเฟตของพืช"),
    Isotope("โคบอลต์-60", Fraction(53, 10), "ปี", GAMMA, "ฉายรังสีรักษาโรคมะเร็ง"),
    Isotope("คาร์บอน-14", Fraction(5730), "ปี", BETA, "หาอายุของซากสิ่งมีชีวิตโบราณ"),
    Isotope("ซีเซียม-137", Fraction(30), "ปี", GAMMA, "วัดระดับของเหลวและความหนาในโรงงาน"),
    Isotope("เรดอน-222", Fraction(38, 10), "วัน", ALPHA, "ศึกษาการรั่วของแก๊สใต้ดิน"),
    Isotope("ทอง-198", Fraction(27, 10), "วัน", BETA, "ติดตามการไหลของตะกอนในแม่น้ำ"),
    Isotope("สตรอนเชียม-90", Fraction(29), "ปี", BETA, "ใช้เป็นแหล่งรังสีในเครื่องวัดความหนา"),
    Isotope("อะเมริเซียม-241", Fraction(432), "ปี", ALPHA, "ใช้ในเครื่องตรวจจับควัน"),
)


def remaining(start: Fraction, halvings: int) -> Fraction:
    return start / 2 ** halvings


# ══ ว 2.1 ม.5/25 — ประโยชน์และการป้องกันอันตราย ═══════════════════════════════════


