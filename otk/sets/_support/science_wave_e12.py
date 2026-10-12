"""Wave E slice 12 — magnetism from currents, magnetic force, induced emf, and
the strong and weak forces. Closes ``ว 2.2 ม.5``.

* ``ว 2.2 ม.5/7`` สังเกตและอธิบายการเกิดสนามแม่เหล็กเนื่องจากกระแสไฟฟ้า —
  default filing.
* ``ว 2.2 ม.5/8`` สังเกตและอธิบายแรงแม่เหล็กที่กระทำต่ออนุภาคที่มีประจุไฟฟ้าที่
  เคลื่อนที่ในสนามแม่เหล็ก และแรงแม่เหล็กที่กระทำต่อลวดตัวนำที่มีกระแสไฟฟ้า
  ผ่านในสนามแม่เหล็ก รวมทั้งอธิบายหลักการทำงานของมอเตอร์ — ``รวมทั้ง`` joins
  two outcomes, so each half stands free: Foundation (the motor) and Fluency
  (the force, on a moving charge *and* on a wire — its bank spans both) are
  ``exact``.
* ``ว 2.2 ม.5/9`` สังเกตและอธิบายการเกิดอีเอ็มเอฟ รวมทั้งยกตัวอย่างการนำความรู้
  ไปใช้ประโยชน์ — the same conjunction: Foundation (the examples) and Fluency
  (how an emf arises) are ``exact``.
* ``ว 2.2 ม.5/10`` สืบค้นข้อมูลและอธิบายแรงเข้มและแรงอ่อน — default filing; the
  ``exact`` set's bank reaches both forces.

Every direction answer is computed, not labelled: directions are unit vectors
in the page frame (x to the right, y up the page, z out of the page, so
x × y = z) and the magnetic field or force is a cross product.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ── directions in the page frame ─────────────────────────────────────────────

Vec = tuple[int, int, int]

DIRECTION = {
    (1, 0, 0): "ไปทางขวา",
    (-1, 0, 0): "ไปทางซ้าย",
    (0, 1, 0): "ขึ้นไปทางด้านบนของกระดาษ",
    (0, -1, 0): "ลงไปทางด้านล่างของกระดาษ",
    (0, 0, 1): "พุ่งออกจากกระดาษ",
    (0, 0, -1): "พุ่งเข้าไปในกระดาษ",
}


def cross(a: Vec, b: Vec) -> Vec:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


def neg(a: Vec) -> Vec:
    return (-a[0], -a[1], -a[2])


def _perpendicular_pair(rng: Random) -> tuple[Vec, Vec]:
    a = rng.choice(list(DIRECTION))
    b = rng.choice([v for v in DIRECTION if cross(a, v) != (0, 0, 0)])
    return a, b


def _direction_choices(correct: Vec, *avoid: Vec) -> list[str]:
    """The opposite first, then the other directions not already in the stem."""
    order = [neg(correct), *[v for v in DIRECTION if v not in (correct, neg(correct), *avoid)],
             *avoid]
    return [DIRECTION[v] for v in order if v != correct][:3]


# ══ ว 2.2 ม.5/7 — สนามแม่เหล็กเนื่องจากกระแสไฟฟ้า ═══════════════════════════════════


# ══ ว 2.2 ม.5/8 — แรงแม่เหล็กและมอเตอร์ ══════════════════════════════════════════


# ══ ว 2.2 ม.5/9 — อีเอ็มเอฟเหนี่ยวนำ ══════════════════════════════════════════════


# ══ ว 2.2 ม.5/10 — แรงเข้มและแรงอ่อน ════════════════════════════════════════════


