"""The ป.1 sets added so every unit has at least ten: each answer worked out again from the stem alone.

Numbers are read back out of the question and the answer recomputed here by its own route; text answers are
checked against facts written out here independently (the sides of a shape, which solid an object is, the
order of a pattern).
"""

from __future__ import annotations

import re
from random import Random

from otk.core import generate

SEEDS = range(300)


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _q(key: str, seed: int):
    q = generate(f"math.{key}", Random(seed))
    texts = [_text(c.content) for c in q.choices]
    assert len(set(texts)) == len(texts), (key, seed, texts)
    return _text(q.stem), texts[q.answer], texts


def _ints(s: str) -> list[int]:
    return [int(v) for v in re.findall(r"\d+", s.replace(",", " "))]


SIDES = {"รูปสามเหลี่ยม": 3, "รูปสี่เหลี่ยม": 4, "รูปห้าเหลี่ยม": 5, "รูปหกเหลี่ยม": 6, "รูปวงกลม": 0}
SOLID_OF = {
    "ลูกฟุตบอล": "ทรงกลม", "ส้ม": "ทรงกลม", "ลูกแก้ว": "ทรงกลม", "ลูกปิงปอง": "ทรงกลม",
    "กระป๋องนม": "ทรงกระบอก", "แก้วน้ำ": "ทรงกระบอก", "ท่อน้ำ": "ทรงกระบอก", "ถ่านไฟฉาย": "ทรงกระบอก",
    "กล่องนม": "ทรงสี่เหลี่ยมมุมฉาก", "หนังสือ": "ทรงสี่เหลี่ยมมุมฉาก", "ตู้เย็น": "ทรงสี่เหลี่ยมมุมฉาก",
    "กล่องดินสอ": "ทรงสี่เหลี่ยมมุมฉาก", "กรวยจราจร": "กรวย", "หมวกวันเกิด": "กรวย", "โคนไอศกรีม": "กรวย",
}
SHAPE_OF = {
    "เหรียญ": "รูปวงกลม", "นาฬิกาแขวนผนัง": "รูปวงกลม", "จานข้าว": "รูปวงกลม", "ล้อจักรยาน": "รูปวงกลม",
    "ธงสามเหลี่ยม": "รูปสามเหลี่ยม", "ชิ้นพิซซ่า": "รูปสามเหลี่ยม", "ไม้แขวนเสื้อ": "รูปสามเหลี่ยม",
    "ประตู": "รูปสี่เหลี่ยม", "หน้าต่าง": "รูปสี่เหลี่ยม", "กระดานดำ": "รูปสี่เหลี่ยม", "ธนบัตร": "รูปสี่เหลี่ยม",
}


def _pictograph(stem: str) -> dict[str, int]:
    """Row label -> number of ● (each ● is 1 in ป.1)."""
    rows = {}
    for line in stem.split("\n"):
        if ":" in line and "●" in line:
            label, marks = line.split(":", 1)
            rows[label.strip()] = marks.count("●")
    return rows


def test_comparing():
    for seed in SEEDS:
        stem, right, _ = _q("more_less_than_p1", seed)
        n, step = _ints(stem)
        assert int(right) == (n + step if "มากกว่า" in stem else n - step)
        stem, right, texts = _q("number_between_p1", seed)
        a, b = _ints(stem)
        assert a < int(right) < b
        assert all(not a < int(t) < b for t in texts if t != right)
        stem, right, _ = _q("sorted_position_p1", seed)
        nums = _ints(stem.split("จาก")[0])
        ordered = sorted(nums, reverse="มากไปน้อย" in stem)
        place = ["แรก", "ที่สอง", "ที่สาม", "ที่สี่"].index(stem.rsplit("ลำดับ", 1)[1])
        assert int(right) == ordered[place]
        stem, right, texts = _q("two_digit_from_digits_p1", seed)
        a, b = _ints(stem)[:2]
        made = [10 * a + b, 10 * b + a]
        assert int(right) == (max(made) if "มากที่สุด" in stem else min(made))
        stem, right, _ = _q("count_between_p1", seed)
        a, b = _ints(stem)
        assert int(right) == len(range(a + 1, b))


def test_add_and_subtract():
    for seed in SEEDS:
        stem, right, _ = _q("add_three_numbers_p1", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, _ = _q("add_tens_p1", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, _ = _q("add_commutative_p1", seed)
        a, b, b2 = _ints(stem)
        assert b == b2 and int(right) == a
        stem, right, _ = _q("subtract_tens_p1", seed)
        a, b = _ints(stem)
        assert int(right) == a - b
        stem, right, _ = _q("add_sub_inverse_p1", seed)
        a, b, s, s2, b2 = _ints(stem)
        assert a + b == s == s2 and b == b2 and int(right) == s - b
        stem, right, _ = _q("number_line_back_p1", seed)
        start, hop = _ints(stem)
        assert int(right) == start - hop


def test_mixed():
    for seed in SEEDS:
        stem, right, texts = _q("mixed_true_sentence_p1", seed)
        for t in texts:
            a, b, c, r = _ints(t)
            assert (a + b - c == r) == (t == right)
        stem, right, _ = _q("mixed_number_line_p1", seed)
        start, fwd, back = _ints(stem)
        assert int(right) == start + fwd - back
        stem, right, texts = _q("mixed_largest_p1", seed)

        def value(e: str) -> int:
            return eval(e)  # noqa: S307 - only digits, + and - written by the set itself
        assert all(re.fullmatch(r"[\d +-]+", t) for t in texts)
        assert value(right) == max(value(t) for t in texts)
        stem, right, _ = _q("mixed_give_compare_p1", seed)
        a, b, give = _ints(stem)
        assert int(right) == (a - give) - (b + give)
        stem, right, _ = _q("mixed_four_terms_p1", seed)
        a, b, c, d = _ints(stem)
        assert int(right) == a + b - c + d
        stem, right, _ = _q("mixed_start_amount_p1", seed)
        got, used, left = _ints(stem)
        assert int(right) + got - used == left
        stem, right, _ = _q("mixed_change_p1", seed)
        a, b, paid = _ints(stem)
        assert int(right) == paid - a - b


def test_patterns():
    for seed in SEEDS:
        stem, right, _ = _q("pattern_next_term_p1", seed)
        terms = _ints(stem)
        step = terms[1] - terms[0]
        assert all(y - x == step for x, y in zip(terms, terms[1:]))
        assert int(right) == terms[-1] + step
        stem, right, _ = _q("pattern_nth_shape_p1", seed)
        shapes = stem.split("แบบรูป ")[1].split("...")[0].split()
        k = _ints(stem)[-1]
        assert right == shapes[(k - 1) % 2]
        stem, right, _ = _q("pattern_growing_p1", seed)
        _, first, step, n = _ints(stem)
        assert int(right) == first + step * (n - 1)
        stem, right, _ = _q("count_down_tens_p1", seed)
        _, start, k = _ints(stem)
        assert int(right) == start - 10 * (k - 1)
        stem, right, _ = _q("pattern_colours_p1", seed)
        beads = stem.split("แบบรูป ")[1].split(" ลูกปัด")[0].split()
        gap = beads.index("___")
        assert gap >= 2 and right == beads[gap - 2]
        stem, right, _ = _q("pattern_shape_count_p1", seed)
        shapes = stem.split("แบบรูป ")[1].split("...")[0].split()
        total = _ints(stem)[-1]
        asked = stem.split("มีรูป ")[1].split()[0]
        assert int(right) == sum(1 for i in range(total) if shapes[i % 2] == asked)


def test_word_problems():
    for seed in SEEDS:
        stem, right, _ = _q("money_left_p1", seed)
        have, cost = _ints(stem)
        assert int(right) == have - cost
        stem, right, _ = _q("more_needed_p1", seed)
        want, have = _ints(stem)
        assert int(right) == want - have
        stem, right, _ = _q("age_word_p1", seed)
        nums = _ints(stem)
        age, gap = nums[0], nums[1]
        assert int(right) == (age - gap if "น้อยกว่า" in stem else age + gap)
        stem, right, _ = _q("tens_bundles_word_p1", seed)
        tens, ten, ones = _ints(stem)
        assert ten == 10 and int(right) == 10 * tens + ones
        stem, right, _ = _q("line_position_p1", seed)
        place, behind = _ints(stem)
        assert int(right) == place + behind


def test_measuring():
    for seed in SEEDS:
        stem, right, _ = _q("length_difference_p1", seed)
        a, b = _ints(stem)
        assert int(right) == a - b
        stem, right, _ = _q("join_lengths_p1", seed)
        assert int(right) == sum(_ints(stem))
        stem, right, _ = _q("weight_compare_kg_p1", seed)
        a, b = _ints(stem)
        assert int(right) == (a - b if "หนักกว่า" in stem else a + b)
        stem, right, _ = _q("choose_unit_p1", seed)
        assert right in {"เซนติเมตร", "เมตร", "กิโลกรัม", "ขีด"}
        assert (right in ("เซนติเมตร", "เมตร")) == stem.startswith("วัด")


def test_plane_shapes():
    for seed in SEEDS:
        stem, right, _ = _q("shape_corners_p1", seed)
        assert int(right) == SIDES[stem.removesuffix("มีมุมกี่มุม")]
        stem, right, _ = _q("shape_total_sides_p1", seed)
        x, y = re.findall(r"รูป[^\s0-9]+เหลี่ยม", stem)
        assert int(right) == SIDES[x] + SIDES[y]
        stem, right, _ = _q("shape_sides_compare_p1", seed)
        x, y = stem.removesuffix("กี่ด้าน").split("มีด้านมากกว่า")
        assert int(right) == SIDES[x] - SIDES[y] > 0
        stem, right, texts = _q("shape_odd_one_p1", seed)
        kinds = [SHAPE_OF[t] for t in texts]
        assert kinds.count(SHAPE_OF[right]) == 1 and len(set(kinds)) == 2
        stem, right, texts = _q("shape_objects_p1", seed)
        shape = stem.removeprefix("สิ่งของใดมีรูปร่างเป็น")
        assert [SHAPE_OF[t] == shape for t in texts].count(True) == 1 and SHAPE_OF[right] == shape
        _q("shape_description_p1", seed)
        _q("fold_cut_shape_p1", seed)


def test_solids():
    for seed in SEEDS:
        stem, right, _ = _q("solid_sum_p1", seed)
        items = re.findall(r"(\D+?) (\d+) ชิ้น", stem.removeprefix("ในห้องมี"))
        shape = stem.split("ที่เป็น")[1].removesuffix("ทั้งหมดกี่ชิ้น")
        total = sum(int(n) for name, n in items if SOLID_OF[name.strip().removeprefix("และ")] == shape)
        assert int(right) == total
        stem, right, texts = _q("solid_odd_one_p1", seed)
        kinds = [SOLID_OF[t] for t in texts]
        assert kinds.count(SOLID_OF[right]) == 1 and len(set(kinds)) == 2
        stem, right, texts = _q("solid_which_object_p1", seed)
        shape = stem.removeprefix("สิ่งของใดมีรูปทรงเป็น")
        assert [SOLID_OF[t] == shape for t in texts].count(True) == 1 and SOLID_OF[right] == shape
        for key in ("solid_roll_stack_p1", "solid_face_shape_p1", "solid_trace_p1"):
            _q(key, seed)


def test_pictographs():
    for seed in SEEDS:
        stem, right, _ = _q("pictograph_range_p1", seed)
        rows = _pictograph(stem)
        assert int(right) == max(rows.values()) - min(rows.values())
        stem, right, _ = _q("pictograph_add_more_p1", seed)
        rows = _pictograph(stem)
        question = stem.split("\n")[-1]
        row = next(r for r in rows if r in question)
        assert int(right) == rows[row] + _ints(question)[0]
        stem, right, texts = _q("pictograph_order_p1", seed)
        rows = _pictograph(stem)
        ordered = sorted(rows, key=rows.get, reverse="มากไปน้อย" in stem)
        place = 1 if stem.endswith("สอง") else 2
        assert right == ordered[place]
        stem, right, _ = _q("pictograph_count_above_p1", seed)
        rows = _pictograph(stem)
        k = _ints(stem.split("\n")[-1])[0]
        assert int(right) == sum(v > k for v in rows.values())
        stem, right, texts = _q("pictograph_two_rows_p1", seed)
        rows = _pictograph(stem)
        question = stem.split("\n")[-1]
        names = sorted((r for r in rows if r in question), key=question.index)
        x, y, z = names
        assert int(right) == rows[x] + rows[y] - rows[z]
        stem, right, texts = _q("pictograph_true_statement_p1", seed)
        rows = _pictograph(stem)
        for t in texts:
            more = t.split("มากกว่า")
            first = next(r for r in rows if r in more[0])
            second = next(r for r in rows if r in more[1])
            claim = _ints(more[1])[-1]
            assert (rows[first] - rows[second] == claim) == (t == right), (t, rows)
