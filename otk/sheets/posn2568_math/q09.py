"""ข้อ 9 — นักเรียนที่ผ่านการคัดเลือกเข้าค่าย 1 สอวน.

ผู้สมัคร 25,680 คน  อัตราส่วน ม.ต้น : ม.ปลาย = 5 : 3  และในกลุ่ม ม.ต้น
อัตราส่วน หญิง : ชาย = 68 : 39  ผู้ผ่านการคัดเลือกรวม 2,025 คน โดย
ชาย ม.ต้น ที่ผ่าน คิดเป็นร้อยละ 14 ของชาย ม.ต้น ที่สมัคร  และความน่าจะเป็นที่สุ่มได้
ชาย ม.ต้น หรือ หญิง ม.ปลาย เท่ากับ 76/135  จงหาจำนวนหญิง ม.ปลาย ที่ผ่านการคัดเลือก

Method: the two given facts about the passers are about *disjoint* groups, so
the union probability is just their sum:
    (ชาย ม.ต้น ผ่าน) + (หญิง ม.ปลาย ผ่าน) = passed × 76/135,
and ชาย ม.ต้น ผ่าน = 14% of the male lower-secondary applicants, which the two
applicant ratios pin down. Subtract.

``check`` rebuilds every headcount from scratch and re-derives the union
probability from it, asserting it comes back to the stated 76/135.
"""

from __future__ import annotations

from fractions import Fraction

PARAMS = {"applicants": 25680, "lower_ratio": 5, "upper_ratio": 3,
          "female_ratio": 68, "male_ratio": 39, "passed": 2025,
          "male_pass_pct": 14, "union_num": 76, "union_den": 135}
ANSWER = 321
VARIANTS = [
    {"passed": 4050, "union_num": 152, "union_den": 135},
    {"male_pass_pct": 20},
    {"applicants": 12840},
    {"union_num": 38, "union_den": 135},
    {"lower_ratio": 3, "upper_ratio": 5, "applicants": 25680},
]


def headcounts(applicants=25680, lower_ratio=5, upper_ratio=3,
               female_ratio=68, male_ratio=39):
    """Applicant headcounts: (lower, upper, lower_female, lower_male)."""
    lower = Fraction(applicants * lower_ratio, lower_ratio + upper_ratio)
    upper = applicants - lower
    parts = female_ratio + male_ratio
    return (lower, upper,
            lower * female_ratio / parts, lower * male_ratio / parts)


def solve(applicants=25680, lower_ratio=5, upper_ratio=3,
          female_ratio=68, male_ratio=39, passed=2025,
          male_pass_pct=14, union_num=76, union_den=135):
    """Upper-secondary female passers."""
    _, _, _, lower_male = headcounts(applicants, lower_ratio, upper_ratio,
                                     female_ratio, male_ratio)
    male_passed = lower_male * Fraction(male_pass_pct, 100)
    union = Fraction(passed) * Fraction(union_num, union_den)
    return union - male_passed


def check(applicants=25680, lower_ratio=5, upper_ratio=3,
          female_ratio=68, male_ratio=39, passed=2025,
          male_pass_pct=14, union_num=76, union_den=135):
    """Independent: rebuild the counts and re-derive the stated probability."""
    lower, upper, lower_f, lower_m = headcounts(
        applicants, lower_ratio, upper_ratio, female_ratio, male_ratio)
    assert lower + upper == applicants
    assert lower_f + lower_m == lower

    male_passed = lower_m * Fraction(male_pass_pct, 100)
    answer = solve(applicants, lower_ratio, upper_ratio, female_ratio,
                   male_ratio, passed, male_pass_pct, union_num, union_den)
    # ชาย ม.ต้น and หญิง ม.ปลาย are disjoint, so P(union) is the plain sum.
    assert (male_passed + answer) / Fraction(passed) \
        == Fraction(union_num, union_den), "reconstruction misses 76/135"
    return answer
