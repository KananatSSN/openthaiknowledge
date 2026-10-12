"""ข้อ 3 — ถังน้ำทรงสี่เหลี่ยมมุมฉาก

วันแรกเติมน้ำเต็มถัง วันที่สองใช้ไป 1/4 ของปริมาตรวันแรก วันที่สามใช้เพิ่มอีก 36
ลูกบาศก์เมตร เหลือคิดเป็นร้อยละ 30 ของวันแรก  ถังใบใหม่มีอัตราส่วน กว้าง:ยาว:สูง
= 1:2:1 และความจุเพิ่มขึ้นร้อยละ 60  พื้นที่ฐานภายในของถังใบใหม่เท่ากับกี่ตารางเมตร

Method: the third day's fixed 36 m³ is the whole bridge between two percentages
of the same unknown V —
    (1 − used) · V − extra = (remain%/100) · V   ⟹   V = extra / (1 − used − remain)
Then the new tank is similar with ratio w:l:h, so its capacity w·l·h·k³ fixes the
scale k and the base area is w·l·k².

``check`` goes the other way: it takes the base area back to a tank and replays
the three days, asserting every stated condition — so a sign slip in the algebra
cannot survive.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"used_num": 1, "used_den": 4, "extra": 36, "remain_pct": 30,
          "ratio_w": 1, "ratio_l": 2, "ratio_h": 1, "increase_pct": 60}
ANSWER = 32
VARIANTS = [
    {"extra": 18},
    {"used_num": 1, "used_den": 2, "extra": 30, "remain_pct": 20},
    {"ratio_w": 1, "ratio_l": 1, "ratio_h": 1},
    {"increase_pct": 0},
    {"ratio_w": 2, "ratio_l": 3, "ratio_h": 4, "increase_pct": 25},
]


def _cube_root(x: Fraction) -> Fraction | float:
    """Exact cube root of a rational when it has one, else a float."""
    n, d = x.numerator, x.denominator
    rn, rd = round(abs(n) ** (1 / 3)), round(d ** (1 / 3))
    for cand_n in (rn - 1, rn, rn + 1):
        for cand_d in (rd - 1, rd, rd + 1):
            if cand_d > 0 and cand_n >= 0 and \
                    Fraction(cand_n, cand_d) ** 3 == abs(x):
                return Fraction(cand_n, cand_d) * (1 if x >= 0 else -1)
    return float(x) ** (1 / 3)


def first_day_volume(used_num=1, used_den=4, extra=36, remain_pct=30):
    """V, the volume the tank held on day one."""
    drop = (1 - Fraction(used_num, used_den)) - Fraction(remain_pct, 100)
    if drop <= 0:
        raise ValueError("the two days remove nothing; V is undetermined")
    return Fraction(extra) / drop


def solve(used_num=1, used_den=4, extra=36, remain_pct=30,
          ratio_w=1, ratio_l=2, ratio_h=1, increase_pct=60):
    """Inner base area (w × l) of the new tank."""
    volume = first_day_volume(used_num, used_den, extra, remain_pct)
    new_cap = volume * (1 + Fraction(increase_pct, 100))
    k = _cube_root(new_cap / (ratio_w * ratio_l * ratio_h))
    return ratio_w * ratio_l * k * k


def check(used_num=1, used_den=4, extra=36, remain_pct=30,
          ratio_w=1, ratio_l=2, ratio_h=1, increase_pct=60):
    """Independent: rebuild the tanks from the answer and replay the story."""
    area = solve(used_num, used_den, extra, remain_pct,
                 ratio_w, ratio_l, ratio_h, increase_pct)
    k = (Fraction(area) / (ratio_w * ratio_l)) ** Fraction(1, 2) \
        if isinstance(area, Fraction) else (area / (ratio_w * ratio_l)) ** 0.5
    new_cap = ratio_w * ratio_l * ratio_h * k ** 3
    volume = new_cap / (1 + Fraction(increase_pct, 100))

    day2 = volume - volume * Fraction(used_num, used_den)     # after day two
    day3 = day2 - extra                                       # after day three
    assert abs(float(day3) - float(volume) * remain_pct / 100) < 1e-6, \
        "replayed tank does not leave remain_pct of the first day's water"
    return area
