"""Wave F slice 9 — ฟิสิกส์เพิ่มเติม 2: light as a wave, thin lenses, light in
the sky, and colour.

Four ``additional_outcome`` indicators, each filed whole, closing ``ฟิสิกส์ 2``:

* ``ฟิสิกส์เพิ่มเติม 2 ม.5/8`` — interference through a double slit and a
  grating, and diffraction through a single slit;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/11`` — images in thin lenses, 1/f = 1/s + 1/s′, and
  lenses in use;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/12`` — rainbows, haloes, mirages and the colours of
  the sky;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/13`` — seeing colour, the colour of objects, mixing
  pigments and mixing light, and colour blindness.

Colour is worked out as sets of the three primaries, as in Wave E slice 15:
light adds, pigment and a lit object keep only what they reflect.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.5/8 — การแทรกสอดและการเลี้ยวเบนของแสง ════════════════════════════════════


# ══ ม.5/11 — เลนส์บาง ═══════════════════════════════════════════════════════════


# ══ ม.5/12 — ปรากฏการณ์ธรรมชาติของแสง ═════════════════════════════════════════════


# ══ ม.5/13 — สีและการบอดสี ═══════════════════════════════════════════════════════


