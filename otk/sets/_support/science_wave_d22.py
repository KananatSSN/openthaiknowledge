"""Wave D, slice 22 — sound and light, opening ``ว 2.3`` at ป.1 and ป.2.

* ``ว 2.3 ป.1/1`` การเกิดเสียงและทิศทางการเคลื่อนที่ของเสียง — all three stages
* ``ว 2.3 ป.2/1`` แนวการเคลื่อนที่ของแสงและการมองเห็นวัตถุ — all three stages
* ``ว 2.3 ป.2/2`` การป้องกันอันตรายจากแสงสว่างไม่เหมาะสม — all three stages

``ป.1/1`` is one verb with evidence, ``บรรยาย...จากหลักฐานเชิงประจักษ์``, so only
its Fluency set is ``exact``. ``ป.2/1`` joins two free verbs — ``บรรยายแนวการ
เคลื่อนที่ของแสง`` (Foundation) and ``อธิบายการมองเห็นวัตถุจากหลักฐานเชิงประจักษ์``
(Fluency) — so both are ``exact``. ``ป.2/2`` is ``ตระหนัก`` whose evidence clause,
``โดยเสนอแนะแนวทางการป้องกันอันตราย``, is a proposal a learner can select on
paper, so its Fluency set is ``exact``, by the rule this wave has used since
``ว 2.1 ป.2/4``.

Wave H slice 2 widened every set here with banks the learner can reason
about: things that are and are not making a sound, children standing round a
source, light sources against lit objects, the card-with-holes experiment,
too-bright and too-dim situations with their fixes. The authored rows stay.
"""

from __future__ import annotations

from random import Random

from otk.core.question import GeneratedQuestion
from otk.sets._support.science_wave_b14 import _labelled

SECOND = {"th": "ป.2"}
KIDS = ("ต้น", "ฝน", "มะลิ", "ภูมิ", "ข้าวหอม", "ปลา", "บอส", "น้ำใส")


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 2.3 ป.1/1 — การเกิดเสียงและทิศทางการเคลื่อนที่ของเสียง ══════════════════════


# ══ ว 2.3 ป.2/1 — แนวการเคลื่อนที่ของแสงและการมองเห็นวัตถุ ═════════════════════════


# ══ ว 2.3 ป.2/2 — การป้องกันอันตรายจากแสงสว่างไม่เหมาะสม ═══════════════════════════


