"""Wave F slice 81 — reading weather maps, and forecasting from them.

Two ``additional_outcome`` indicators, each filed whole, finishing
``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2``:

* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/12`` — weather symbols on the map:
  pressure centres, isobars, fronts, and the station model;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/13`` — reading a map and other
  information to forecast, and planning work and life around it.

Wind barbs follow the station-model convention (pennant 50 knots, full barb
10, half barb 5); the three-digit pressure code takes a leading 9 from 500 up
and a leading 10 below it. Knots convert at 1.852 km/h and only multiples of
5 knots are drawn, so every answer is exact.
"""

from __future__ import annotations

SUBJECT = "ธรณีวิทยา"
UPPER_FIVE = {"th": "ม.5"}

# ══ 2 ม.5/12 — สัญลักษณ์ลมฟ้าอากาศ ═════════════════════════════════════════════════


# ══ 2 ม.5/13 — การคาดการณ์ลมฟ้าอากาศ ═══════════════════════════════════════════════


