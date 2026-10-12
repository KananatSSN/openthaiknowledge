"""Wave A slice 5 — the atomic-structure and periodic-table cluster.

Three chemistry topics that each held only one or two stages:

* ``เคมีเพิ่มเติม 1 ม.4/2`` สัญลักษณ์นิวเคลียร์และโครงสร้างอะตอม — Application
* ``เคมีเพิ่มเติม 1 ม.4/4`` หมู่และคาบของธาตุ — Fluency and Application
* ``ว 2.1 ม.5/3`` จำนวนอนุภาคของอะตอมและไอออน — Foundation and Application

Every legacy set keeps its key, stage, and meaning. The element data is the one
already in :mod:`otk.sets._support.chemistry`, so a fact stated here can never
drift from the fact the older sets drill.
"""

from __future__ import annotations

from otk.core.content import Block, math, text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion
from otk.sets._support.chemistry import ELEMENTS, Element, iupac_group

SUBJECT = "เคมี"
TOPIC_ATOM = "โครงสร้างอะตอม"


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    """A question whose choices are all Thai labels drawn from one pool."""
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ── คาบ ──────────────────────────────────────────────────────────────────────
# The last atomic number in each period. Periods are read off ``z`` rather than
# stored per element so this cannot fall out of step with the element table.
PERIOD_LAST_Z = (2, 10, 18, 36, 54, 86, 118)


def period_of(el: Element) -> int:
    """คาบ 1–7, from the atomic number."""
    return next(index + 1 for index, last in enumerate(PERIOD_LAST_Z) if el.z <= last)


# ── โลหะ / อโลหะ / กึ่งโลหะ ──────────────────────────────────────────────────
# The IPST ม.4 division. Astatine and polonium are left out of the pools below
# because textbooks disagree on which side of the staircase they fall, and a
# contested element cannot have exactly one defensible answer.
METAL = "โลหะ"
NONMETAL = "อโลหะ"
METALLOID = "กึ่งโลหะ"

METALLOID_SYMBOLS = frozenset({"B", "Si", "Ge", "As", "Sb", "Te"})
NONMETAL_SYMBOLS = frozenset({
    "H", "C", "N", "O", "P", "S", "Se",
    "F", "Cl", "Br", "I",
    "He", "Ne", "Ar", "Kr", "Xe", "Rn",
})
CONTESTED_SYMBOLS = frozenset({"At", "Po"})

REPRESENTATIVE = "ธาตุเรพรีเซนเททีฟ"
TRANSITION_BLOCK = "ธาตุแทรนซิชัน"


def metal_class(el: Element) -> str:
    """โลหะ, อโลหะ or กึ่งโลหะ for one element."""
    if el.symbol in METALLOID_SYMBOLS:
        return METALLOID
    if el.symbol in NONMETAL_SYMBOLS:
        return NONMETAL
    return METAL


def block_class(el: Element) -> str:
    """เรพรีเซนเททีฟ or แทรนซิชัน, from the หมู่."""
    group = iupac_group(el)
    assert group is not None
    return TRANSITION_BLOCK if 3 <= group <= 12 else REPRESENTATIVE


# Elements a หมู่/คาบ drill may draw. The f-block has no simple หมู่ and is out;
# so is everything past เรดอน, whose หมู่ is settled but whose metal class is not.
TABLE_POOL: tuple[Element, ...] = tuple(
    el for el in ELEMENTS
    if iupac_group(el) is not None
    and el.z <= 86
    and el.symbol not in CONTESTED_SYMBOLS
)


# ══ เคมีเพิ่มเติม 1 ม.4/2 — สัญลักษณ์นิวเคลียร์และโครงสร้างอะตอม ═══════════════

BY_Z: dict[int, Element] = {el.z: el for el in ELEMENTS}


def _nuclide(mass: int, z: int, symbol: str, charge: int = 0) -> list[Block]:
    r"""Nuclide notation with the mass number and atomic number given explicitly.

    :func:`otk.sets._support.chemistry.nuclide_tex` always writes an element's own
    numbers; the distractors here are deliberately *wrong* pairings, so they need
    a builder that takes both numbers.
    """
    ion = ""
    if charge:
        size = abs(charge) if abs(charge) > 1 else ""
        sign = "+" if charge > 0 else "-"
        ion = f"^{{{size}{{{sign}}}}}"
    return [math(rf"{{}}^{{{mass}}}_{{{z}}}\mathrm{{{symbol}}}{ion}")]


# Nuclide work stops at เลขอะตอม 56. Past แบเรียม the table is lanthanides and
# synthetic elements, whose "mass number" is that of a manufactured isotope — a
# number no ม.4 learner can be expected to reason about.
NUCLIDE_MAX_Z = 56

# Elements whose neutron count is at least one and differs from the proton
# count, so that "swap the two numbers" and "use the neutron count" stay wrong.
WRITEABLE: tuple[Element, ...] = tuple(
    el for el in ELEMENTS
    if el.z <= NUCLIDE_MAX_Z and el.mass - el.z >= 1 and el.mass - el.z != el.z
)

# Elements with a neighbour two places either side, so the isotope branch can
# offer real symbols for its wrong nuclides rather than invented ones.
ISOTOPE_POOL: tuple[Element, ...] = tuple(
    el for el in ELEMENTS if 3 <= el.z <= NUCLIDE_MAX_Z
)


# ══ เคมีเพิ่มเติม 1 ม.4/4 — หมู่และคาบของธาตุ ═════════════════════════════════

def _position_label(group: int, period: int) -> str:
    return f"หมู่ {group} คาบ {period}"


# ══ ว 2.1 ม.5/3 — จำนวนอนุภาคของอะตอมและไอออน ═════════════════════════════════


