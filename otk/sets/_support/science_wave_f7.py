"""Wave F slice 7 — ฟิสิกส์เพิ่มเติม 2: simple harmonic motion, natural
frequency and resonance, wave basics, and water waves.

Four ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 2 ม.5/1`` — simple harmonic motion of a mass on a spring and
  a simple pendulum;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/2`` — natural frequency and resonance;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/3`` — kinds and parts of waves, Huygens' principle,
  superposition, and v = fλ;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/4`` — reflection, refraction, interference and
  diffraction of water waves.

g = 10 m/s². Where a period needs π, the stem either keeps π in the answer
or states the textbook's π² ≈ 10, so every answer is exact.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


# ══ ม.5/1 — การเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย ═══════════════════════════════════


# ══ ม.5/2 — ความถี่ธรรมชาติและการสั่นพ้อง ═══════════════════════════════════════


# ══ ม.5/3 — คลื่น ═══════════════════════════════════════════════════════════════


# ══ ม.5/4 — คลื่นผิวน้ำ ═══════════════════════════════════════════════════════════


