"""Wave F slice 5 — ฟิสิกส์เพิ่มเติม 1: centre of mass and stability, momentum
and impulse, and collisions in one dimension.

Three ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 1 ม.4/9`` — how a body moves when a force acts through its
  centre of mass, and how the centre of gravity decides stability;
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/14`` — momentum, impulse from the equation and from the
  area under a force-time graph, and impulsive force;
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/15`` — elastic and inelastic collisions and bodies
  pushed apart, all under conservation of momentum.

g = 10 m/s², and every number is drawn so the answer is exact.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FOUR = {"th": "ม.4"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.4/9 — ศูนย์กลางมวลและเสถียรภาพ ═══════════════════════════════════════════


# ══ ม.4/14 — โมเมนตัมและการดล ═══════════════════════════════════════════════════


# ══ ม.4/15 — การชนในหนึ่งมิติ ═══════════════════════════════════════════════════


