"""The answer must not be the choice every distractor is a one-part slip of.

See docs/for_admin/MCQ_GUESSABILITY.md (the ``convergent`` flag).
"""

from __future__ import annotations

import pytest

from otk.core import text
from otk.core.distractors import _double_slips


def _doubles(answer: str, *wrongs: str) -> list[str]:
    return [c[0].text for c in _double_slips([text(answer)], [[text(w)] for w in wrongs])]


def test_two_one_part_slips_combine_into_a_two_part_slip():
    out = _doubles("หมู่ 13 คาบ 6 ของตาราง", "หมู่ 14 คาบ 6 ของตาราง", "หมู่ 13 คาบ 5 ของตาราง")
    assert out == ["หมู่ 14 คาบ 5 ของตาราง"]


def test_edits_stay_whole_words():
    # Char-level splicing gave "ไขสันหน้า"; whole words overlap, so nothing is built.
    assert _doubles("อยู่ใน สมองส่วนหลัง ของคน", "อยู่ใน ไขสันหลัง ของคน",
                    "อยู่ใน สมองส่วนหน้า ของคน") == []


@pytest.mark.parametrize("answer, wrongs", [
    ("1 : 2 : 1", ("2 : 2 : 1", "1 : 2 : 2")),                      # ratio
    ("มี 4 × 10¹¹ ตัว", ("มี 40 × 10¹¹ ตัว", "มี 4 × 10¹⁰ ตัว")),      # powers of ten
    ("← ← ↑ ↑ ↑", ("← ↑ ↑ ↑ ↑", "← ← ← ↑ ↑")),                        # a route
    ("ให้ y = y * 3 แล้วแสดงผล", ("ให้ y = x * 3 แล้วแสดงผล", "ให้ y = y * 5 แล้วแสดงผล")),
    ("H-Cl", ("Cl-H", "H-Br")),                                       # too short
])
def test_no_double_where_two_slips_can_cancel(answer, wrongs):
    assert _doubles(answer, *wrongs) == []


def test_two_word_flips_in_prose_are_not_combined():
    # Both halves flipped reads true again: longer, slower, lower.
    assert _doubles("ยิ่งสั้น ยิ่งสั่นถี่ และให้เสียงสูงขึ้น",
                    "ยิ่งยาว ยิ่งสั่นถี่ และให้เสียงสูงขึ้น",
                    "ยิ่งสั้น ยิ่งสั่นห่าง และให้เสียงต่ำลง") == []


def test_a_scaled_proportion_is_not_offered():
    # 368 : 368 is the same proportion as 184 : 184, so it would be right too.
    assert _doubles("O 184 กรัม กับ S 184 กรัม", "O 368 กรัม กับ S 184 กรัม",
                    "O 184 กรัม กับ S 368 กรัม") == []


def test_a_reordering_of_the_answer_is_not_offered():
    assert _doubles("ขนาด 56 × 48 เซนติเมตร", "ขนาด 48 × 48 เซนติเมตร",
                    "ขนาด 56 × 56 เซนติเมตร") == []


def test_two_disjoint_swaps_in_a_matching_combine():
    answer = "ก → 1 / ข → 2 / ค → 3 / ง → 4 / จ → 5"
    out = _doubles(answer, "ก → 2 / ข → 1 / ค → 3 / ง → 4 / จ → 5",
                   "ก → 1 / ข → 2 / ค → 3 / ง → 5 / จ → 4")
    assert out == ["ก → 2 / ข → 1 / ค → 3 / ง → 5 / จ → 4"]


def test_a_sequence_never_repeats_a_step():
    assert _doubles("แมกมา → หินอัคนี → ตะกอน → หินตะกอน",
                    "แมกมา → หินแปร → ตะกอน → หินตะกอน",
                    "แมกมา → หินอัคนี → ตะกอน → หินแปร") == []


def test_negations_are_never_combined():
    assert _doubles("แก๊สมีมวล และต้องการที่อยู่ เสมอ",
                    "แก๊สไม่มีมวล และต้องการที่อยู่ เสมอ",
                    "แก๊สมีมวล และไม่ต้องการที่อยู่ เสมอ") == []
