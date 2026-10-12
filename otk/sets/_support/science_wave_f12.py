"""Wave F slice 12 — ฟิสิกส์เพิ่มเติม 3: batteries in circuits, renewable
electricity, magnetic fields and flux, and the magnetic force.

Four ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 3 ม.5/10`` — the equivalent emf of batteries in series and
  in parallel, and DC circuits of batteries and resistors;
* ``ฟิสิกส์เพิ่มเติม 3 ม.5/11`` — turning renewable energy into electricity, and
  weighing efficiency and cost;
* ``ฟิสิกส์เพิ่มเติม 3 ม.6/1`` — field lines, magnetic flux, and the field round
  a straight wire and a solenoid;
* ``ฟิสิกส์เพิ่มเติม 3 ม.6/2`` — the magnetic force on a moving charge and on a
  current, the radius of a charge's circle, and parallel currents.

Directions are worked out as vectors in the page's frame (x to the right, y
up the page, z out of it), so the right-hand rule is a cross product.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}
UPPER_SIX = {"th": "ม.6"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.5/10 — อีเอ็มเอฟสมมูลและวงจรกระแสตรง ═════════════════════════════════════════


# ══ ม.5/11 — พลังงานทดแทนเป็นไฟฟ้า ═══════════════════════════════════════════════


# ══ ม.6/1 — สนามแม่เหล็กและฟลักซ์ ═════════════════════════════════════════════════

DIRECTIONS = {
    "ไปทางขวา": (1, 0, 0), "ไปทางซ้าย": (-1, 0, 0), "ขึ้นด้านบนของหน้ากระดาษ": (0, 1, 0),
    "ลงด้านล่างของหน้ากระดาษ": (0, -1, 0), "พุ่งออกจากกระดาษ": (0, 0, 1), "พุ่งเข้าไปในกระดาษ": (0, 0, -1),
}
NAME_OF = {v: k for k, v in DIRECTIONS.items()}


def cross(a: tuple, b: tuple) -> tuple:
    return (a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0])


# ══ ม.6/2 — แรงแม่เหล็ก ═══════════════════════════════════════════════════════════


