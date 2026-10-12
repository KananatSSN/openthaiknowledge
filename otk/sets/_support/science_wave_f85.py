"""Wave F slice 85 — the celestial sphere, star paths, solar time and time zones.

Four ``additional_outcome`` indicators, each filed whole:

* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/13`` — the celestial-sphere model,
  and horizon and equatorial coordinates;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/14`` — the rising and setting paths
  of the Sun and stars;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/15`` — apparent solar time;
* ``โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/16`` — mean solar time and time zones.

Observers are placed at whole-degree latitudes and longitudes (Thai towns are
rounded to the nearest degree and the stem says so), azimuth runs from north
through east, 15° is one hour, and 1° of longitude is 4 minutes.
"""

from __future__ import annotations

SUBJECT = "ดาราศาสตร์"
UPPER_SIX = {"th": "ม.6"}
TOWNS = (("เชียงราย", 20), ("เชียงใหม่", 19), ("ขอนแก่น", 16), ("กรุงเทพมหานคร", 14), ("นครราชสีมา", 15), ("ภูเก็ต", 8),
         ("สงขลา", 7), ("นราธิวาส", 6), ("อุบลราชธานี", 15), ("สุราษฎร์ธานี", 9))


def _clock(minutes: int) -> str:
    minutes %= 24 * 60
    return f"{minutes // 60:02d}:{minutes % 60:02d} น."


# ══ 3 ม.6/13 — ทรงกลมฟ้า ═══════════════════════════════════════════════════════════


# ══ 3 ม.6/14 — เส้นทางการขึ้นตก ══════════════════════════════════════════════════════


# ══ 3 ม.6/15 — เวลาสุริยคติปรากฏ ═════════════════════════════════════════════════════


# ══ 3 ม.6/16 — เวลาสุริยคติปานกลางและเขตเวลา ═══════════════════════════════════════════


