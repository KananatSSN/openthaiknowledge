"""Wave F slice 6 — ฟิสิกส์เพิ่มเติม 1: projectiles, circular motion, where
physics came from, and measurement.

Four ``additional_outcome`` indicators, each filed whole, closing ``ฟิสิกส์ 1``:

* ``ฟิสิกส์เพิ่มเติม 1 ม.4/16`` — projectile motion;
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/17`` — circular motion in a horizontal plane: centripetal
  force, radius, linear and angular speed, mass, and satellite orbits;
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/1`` — how physics knowledge was found and how its ideas
  led to new technology;
* ``ฟิสิกส์เพิ่มเติม 1 ม.4/2`` — reporting a measurement with its uncertainty, and
  reading a straight-line graph.

g = 10 m/s². Launch angles are 37° and 53° with sin 37° = 0.6 and
cos 37° = 0.8, and every number is drawn so the answer is exact.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FOUR = {"th": "ม.4"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.4/16 — การเคลื่อนที่แบบโพรเจกไทล์ ═════════════════════════════════════════


# ══ ม.4/17 — การเคลื่อนที่แบบวงกลม ══════════════════════════════════════════════


# (orbit radius in km, g at that radius in m/s², orbital speed in m/s) with v² = g'r.
ORBITS = ((6400, 10, 8000), (10000, Fraction(49, 10), 7000), (9000, 4, 6000),
          (12500, 2, 5000), (20000, Fraction(4, 5), 4000))
assert all(g * r * 1000 == v * v for r, g, v in ORBITS)


# ══ ม.4/1 — ประวัติและพัฒนาการของฟิสิกส์ ══════════════════════════════════════════


# ══ ม.4/2 — การวัดและการวิเคราะห์กราฟ ══════════════════════════════════════════════


