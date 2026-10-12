"""Wave F slice 8 — ฟิสิกส์เพิ่มเติม 2: sound as a wave, how loud it is, and
what it does in pipes, in pairs and on the move.

Three ``additional_outcome`` indicators, each filed whole:

* ``ฟิสิกส์เพิ่มเติม 2 ม.5/5`` — how sound is made and travels, displacement and
  pressure waves, the speed of sound against air temperature, and its
  reflection, refraction, interference and diffraction;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/6`` — intensity, intensity level in decibels, hearing,
  sound quality and noise pollution;
* ``ฟิสิกส์เพิ่มเติม 2 ม.5/7`` — resonance in a pipe closed at one end, beats,
  standing waves, the Doppler effect and shock waves.

The speed of sound in air is v = 331 + 0.6T m/s with T in °C, drawn at
temperatures that keep it exact. Decibel steps use powers of ten, or the
stated log 2 ≈ 0.3.
"""

from __future__ import annotations

from fractions import Fraction

SUBJECT = "ฟิสิกส์"
UPPER_FIVE = {"th": "ม.5"}


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


def speed_at(celsius: int) -> Fraction:
    return 331 + Fraction(3, 5) * celsius


# ══ ม.5/5 — เสียงและสมบัติของคลื่นเสียง ══════════════════════════════════════════


# ══ ม.5/6 — ความเข้มเสียงและการได้ยิน ════════════════════════════════════════════


# ══ ม.5/7 — ท่อ บีต คลื่นนิ่ง ดอปเพลอร์ และคลื่นกระแทก ══════════════════════════════


