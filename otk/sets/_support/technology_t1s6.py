"""Phase 7 Technology wave T1, slice 6 — ว 4.2 สิทธิ มารยาท และการทำงานร่วมกัน ป.4-ป.6.

The last three primary outcomes of ``ว 4.2``, each a step on from ``ป.1/5``:

* ``ป.4/5`` — rights and duties: respecting other people's rights, naming the
  right a violation breaks, and reporting what is inappropriate.
* ``ป.5/5`` — the same outcome with มารยาท added: netiquette, the reason for
  each courtesy, and what to do in a group chat.
* ``ป.6/4`` — working together online safely: safe sharing, choosing the
  permission a person needs on a shared file, and what to do when collaboration
  goes wrong.
"""

from __future__ import annotations

from random import Random

from otk.sets._support.science_wave_b14 import _labelled

FOURTH, FIFTH, SIXTH = {"th": "ป.4"}, {"th": "ป.5"}, {"th": "ป.6"}


def _pick_one(rng: Random, *, good: tuple, bad: tuple, good_stem: str, bad_stem: str,
              hint: str, topic: str):
    """One right thing among wrong ones, or one wrong thing among right ones."""
    if rng.random() < 0.5:
        return _labelled(stem=good_stem, correct=rng.choice(good),
                         wrongs=tuple(bad), hint=hint, topic=topic)
    return _labelled(stem=bad_stem, correct=rng.choice(bad),
                     wrongs=tuple(good), hint=hint, topic=topic)


def _pair_either_way(rng: Random, rows: tuple, *, forward: str, backward: str,
                     hint: str, topic: str):
    """Match the two halves of a row, from either side. ``forward``/``backward``
    are stems with ``{}`` for the given half."""
    index = rng.randrange(len(rows))
    left, right = rows[index]
    others = rng.sample([row for i, row in enumerate(rows) if i != index], 3)
    if rng.random() < 0.5:
        return _labelled(stem=forward.format(left), correct=right,
                         wrongs=tuple(r for _, r in others), hint=hint, topic=topic)
    return _labelled(stem=backward.format(right), correct=left,
                     wrongs=tuple(ell for ell, _ in others), hint=hint, topic=topic)


def _situation(rng: Random, bank: tuple, *, hint: str, topic: str):
    situation, correct, wrongs = rng.choice(bank)
    return _labelled(stem=f"{situation} ควรทำอย่างไร", correct=correct,
                     wrongs=tuple(wrongs), hint=hint, topic=topic)


# ══ ว 4.2 ป.4/5 — สิทธิและหน้าที่ ═══════════════════════════════════════════════


# ══ ว 4.2 ป.5/5 — มารยาทในการใช้อินเทอร์เน็ต ══════════════════════════════════════


# ══ ว 4.2 ป.6/4 — ทำงานร่วมกันออนไลน์อย่างปลอดภัย ══════════════════════════════════


