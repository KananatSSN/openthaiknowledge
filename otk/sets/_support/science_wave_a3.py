"""Wave A slice 3 — the ม.1 matter and particle cluster.

Three core chemistry topics that each held a single stage:

* ``ว 2.1 ม.1/5`` ความหนาแน่นของสาร — Foundation and Application
* ``ว 2.1 ม.1/8`` อนุภาคมูลฐานของอะตอม — Foundation and Application
* ``ว 2.1 ม.1/9`` อนุภาคและสถานะของสสาร — Fluency and Application

Every legacy set keeps its key, stage, and meaning.
"""

from __future__ import annotations

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

CHEMISTRY = "เคมี"
MATTER = "สารในชีวิตประจำวัน"


def _distinct(correct: str, candidates: list[str], want: int = 3) -> tuple[str, ...] | None:
    out: list[str] = []
    for value in candidates:
        if value != correct and value not in out:
            out.append(value)
    return tuple(out[:want]) if len(out) >= want else None


def _question(*, stem: str, correct: str, wrongs: tuple[str, ...],
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=MATTER,
        hint=[text(hint)],
    )


# ══ ว 2.1 ม.1/5 — ความหนาแน่นของสาร ═══════════════════════════════════════════


# ══ ว 2.1 ม.1/8 — อนุภาคมูลฐานของอะตอม ════════════════════════════════════════


# ══ ว 2.1 ม.1/9 — อนุภาคและสถานะของสสาร ═══════════════════════════════════════


