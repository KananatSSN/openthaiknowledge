"""Wave A slice 2 — the stages the consolidated topics were still missing.

Consolidating units to one per indicator left several chemistry and physical
science topics holding real Foundation and Fluency material but no Application,
or Foundation only. This module supplies exactly the missing stages:

* ``ว 2.1 ม.2/1`` การแยกสารละลาย — Application
* ``ว 2.3 ม.3/10`` คลื่นและสมบัติของคลื่น — Application
* ``ว 2.1 ม.1/7`` อะตอม ธาตุ และสารประกอบ — Fluency and Application
* ``ว 2.3 ม.3/13`` การสะท้อนของแสง — Application
* ``ว 2.3 ม.3/15`` การหักเหและการกระจายของแสง — Application

Every legacy set keeps its key, stage, and meaning.
"""

from __future__ import annotations

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

PHYSICS = "ฟิสิกส์"
WAVES = "คลื่นและแสง"
CHEMISTRY = "เคมี"
MATTER = "สารในชีวิตประจำวัน"


def _distinct(correct: str, candidates: list[str], want: int = 3) -> tuple[str, ...] | None:
    """`want` distractors that differ from each other and from the answer.

    Symmetric cases make the classic slips collide: NaCl has one atom of each
    element, so "swap the two counts" *is* the right answer. Returning None lets
    the caller pick different numbers rather than emit a duplicated choice.
    """
    out: list[str] = []
    for value in candidates:
        if value != correct and value not in out:
            out.append(value)
    return tuple(out[:want]) if len(out) >= want else None


def _question(*, stem: str, correct: str, wrongs: tuple[str, ...], hint: str,
              topic: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ══ ว 2.1 ม.2/1 — การแยกสารละลาย (Application) ════════════════════════════════


# ══ ว 2.3 ม.3/10 — คลื่นและสมบัติของคลื่น (Application) ═══════════════════════


# ══ ว 2.1 ม.1/7 — อะตอม ธาตุ และสารประกอบ (Fluency + Application) ═════════════


# ══ ว 2.3 ม.3/13 — การสะท้อนของแสง (Application) ══════════════════════════════


# ══ ว 2.3 ม.3/15 — การหักเหและการกระจายของแสง (Application) ═══════════════════

