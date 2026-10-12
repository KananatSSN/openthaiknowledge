"""Wave D, slice 32 — the V-I graph, meter use, and resistor circuit diagrams at ม.3.

Closes the diagram and instrument-use rows the Phase 3 pilot and Wave A left
behind in ``ว 2.3 ม.3``, sharing legacy topics with ``ม.3/1`` and ``ม.3/4``
but never carrying their own three stages.

* ``ว 2.3 ม.3/2`` กราฟความสัมพันธ์ระหว่างกระแสไฟฟ้าและความต่างศักย์ไฟฟ้า — all three stages
* ``ว 2.3 ม.3/3`` การใช้โวลต์มิเตอร์และแอมมิเตอร์วัดปริมาณทางไฟฟ้า — all three stages
* ``ว 2.3 ม.3/5`` แผนภาพวงจรไฟฟ้าแสดงการต่อตัวต้านทานแบบอนุกรมและขนาน — all three stages

``ม.3/2`` and ``ม.3/5`` are ``เขียนกราฟ`` / ``เขียนแผนภาพ``: three sets, no
``exact``, the rule this wave has used since ``ว 2.2 ป.5/2``. ``ม.3/3``,
``ใช้โวลต์มิเตอร์ แอมมิเตอร์ในการวัดปริมาณทางไฟฟ้า``, names a bare
instrument-operation skill with no evidence clause an item can carry, so it
holds three sets and none is ``exact``, the rule this wave has used since
``ป.5/4``.

Wave H slice 3 widened every set here: V-I readings drawn from a resistance,
two resistors compared by their data, predicted currents, what each meter
does wired each way, reading a needle on a scale, choosing a range, series
and parallel clues, and total resistance and current. Graph axes are stated
wherever a slope is read. The authored rows stay.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

THIRD_SECONDARY = {"th": "ม.3"}


# ══ ว 2.3 ม.3/2 — กราฟความสัมพันธ์ระหว่างกระแสไฟฟ้าและความต่างศักย์ไฟฟ้า ═════════


VI_GRAPH_COMBOS = ((10, 0.2, 0.4, 0.6), (20, 0.1, 0.2, 0.3), (5, 0.4, 0.8, 1.2), (25, 0.08, 0.16, 0.24))
RESISTANCES = (2, 4, 5, 8, 10, 20, 25, 40, 50, 100)


def _vi_data(rng: Random) -> tuple[int, tuple[int, int, int], tuple[Fraction, Fraction, Fraction]]:
    """A resistance and three voltages whose currents are exact to 0.01 A."""
    while True:
        resistance = rng.choice(RESISTANCES)
        step = rng.choice((1, 2, 3, 4, 5))
        volts = (step, 2 * step, 3 * step)
        amps = tuple(Fraction(v, resistance) for v in volts)
        if all((a * 100).denominator == 1 for a in amps):
            return resistance, volts, amps


# ══ ว 2.3 ม.3/3 — การใช้โวลต์มิเตอร์และแอมมิเตอร์วัดปริมาณทางไฟฟ้า ═══════════════


# ══ ว 2.3 ม.3/5 — แผนภาพวงจรไฟฟ้าแสดงการต่อตัวต้านทานแบบอนุกรมและขนาน ═══════════


