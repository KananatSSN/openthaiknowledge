"""การบวกและการลบ

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/5

Sets moved here from: math_gaps_primary.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.sets._support.math_gaps_primary import _AddSubLarge, _AddSubWordLarge, _MissingAddSubLarge

PROVENANCE = Provenance("original")


@question_type("math.add_sub_large_p3", display_name={"th": "บวกและลบจำนวนไม่เกิน 100,000"},
               level={"th": "ป.3"}, topic="การบวกและการลบ")
class AddSubLargeP3(_AddSubLarge):
    lo, hi = 1_000, 100_000


@question_type("math.missing_addsub_large_p3",
               display_name={"th": "หาตัวไม่ทราบค่าในประโยคการบวกและการลบ (ไม่เกิน 100,000)"},
               level={"th": "ป.3"}, topic="การบวกและการลบ")
class MissingAddSubLargeP3(_MissingAddSubLarge):
    lo, hi = 1_000, 100_000


@question_type("math.addsub_word_large_p3",
               display_name={"th": "โจทย์ปัญหาการบวกและการลบ (ไม่เกิน 100,000)"},
               level={"th": "ป.3"}, topic="การบวกและการลบ")
class AddSubWordLargeP3(_AddSubWordLarge):
    lo, hi = 1_000, 100_000
