"""การบวกและการลบ

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/8

Sets moved here from: math_gaps_primary.
"""

from __future__ import annotations

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.sets._support.math_gaps_primary import _AddSubLarge, _AddSubWordLarge, _MissingAddSubLarge

PROVENANCE = Provenance("original")


@question_type("math.add_sub_large_p4", display_name={"th": "บวกและลบจำนวนนับที่มากกว่า 100,000"},
               level={"th": "ป.4"}, topic="การบวกและการลบ")
class AddSubLargeP4(_AddSubLarge):
    lo, hi = 100_000, 9_000_000


@question_type("math.missing_addsub_large_p4",
               display_name={"th": "หาตัวไม่ทราบค่าในประโยคการบวกและการลบ (มากกว่า 100,000)"},
               level={"th": "ป.4"}, topic="การบวกและการลบ")
class MissingAddSubLargeP4(_MissingAddSubLarge):
    lo, hi = 100_000, 9_000_000


@question_type("math.addsub_word_large_p4",
               display_name={"th": "โจทย์ปัญหาการบวกและการลบ (มากกว่า 100,000)"},
               level={"th": "ป.4"}, topic="การบวกและการลบ")
class AddSubWordLargeP4(_AddSubWordLarge):
    lo, hi = 100_000, 9_000_000
