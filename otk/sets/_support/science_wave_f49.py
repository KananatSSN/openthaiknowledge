"""Wave F slice 49 — beyond Mendel, variation, sex linkage and DNA.

Four ``additional_outcome`` indicators, each filed whole:

* ``ชีววิทยาเพิ่มเติม 2 ม.4/3`` — incomplete dominance, codominance, multiple
  alleles, polygenes and pleiotropy;
* ``ชีววิทยาเพิ่มเติม 2 ม.4/4`` — discontinuous and continuous variation;
* ``ชีววิทยาเพิ่มเติม 2 ม.4/5`` — genes on autosomes and on sex chromosomes;
* ``ชีววิทยาเพิ่มเติม 2 ม.4/6`` — what genetic material must do, the
  experiments that found it, the double helix and its replication.

Every cross is worked out by listing the gametes, as in slice 48.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.sets._support.science_wave_f48 import frac_text

SUBJECT = "ชีวะ"
UPPER_FOUR = {"th": "ม.4"}

SIMPLE_FRACTIONS = (Fraction(0), Fraction(1, 4), Fraction(1, 3), Fraction(1, 2), Fraction(2, 3), Fraction(3, 4), Fraction(1))


def _frac_wrongs(rng: Random, right: Fraction) -> tuple[str, ...]:
    pool = [f for f in SIMPLE_FRACTIONS if f != right]
    near = sorted(pool, key=lambda x: abs(x - right))[:5]
    return tuple(frac_text(x) for x in rng.sample(near, 3))


# ══ ชีววิทยาเพิ่มเติม 2 ม.4/3 — ส่วนขยายของพันธุศาสตร์เมนเดล ═══════════════════════════


# ══ ชีววิทยาเพิ่มเติม 2 ม.4/4 — การแปรผันต่อเนื่องและไม่ต่อเนื่อง ═════════════════════════


# ══ ชีววิทยาเพิ่มเติม 2 ม.4/5 — ยีนบนออโตโซมและโครโมโซมเพศ ═════════════════════════


# ══ ชีววิทยาเพิ่มเติม 2 ม.4/6 — สมบัติ โครงสร้าง และการจำลอง DNA ═══════════════════════


