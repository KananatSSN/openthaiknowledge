"""Wave A — complete three-stage paths for chemistry and physical science.

Phase 5 expands the reviewed catalog outward from the Phase 3 pilots. Each path
here adds new keys to an existing curriculum topic and leaves every legacy set
unchanged, exactly as the pilots did.

This slice covers:

* ``ว 2.3 ม.3/4`` — potential difference and current across resistors in series
  and in parallel, from empirical evidence;
* ``ว 2.1 ม.1/4`` — comparing the boiling and melting points of pure substances
  and mixtures by measuring, graphing, and interpreting data;
* ``ว 2.1 ป.6/1`` — explaining and comparing ways to separate mixtures, and
  choosing one for an everyday problem.
"""

from __future__ import annotations

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

CHEMISTRY = "เคมี"
MATTER = "สารในชีวิตประจำวัน"


def _question(*, stem: str, correct: str, wrongs: tuple[str, ...], hint: str,
              topic: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ══ ว 2.3 ม.3/4 — วงจรอนุกรมและขนาน ═══════════════════════════════════════════


# ══ ว 2.1 ม.1/4 — สารบริสุทธิ์และสารผสม ═══════════════════════════════════════


# ══ ว 2.1 ป.6/1 — การเลือกวิธีแยกสารผสม ═══════════════════════════════════════


