"""Tests for the separate-answer-key splitter (``answerkey.py``).

The rules are exercised on text lines shaped like the ``(rath)`` notes and
their ``เฉลย`` file. One test converts the real files when the bank PDFs are
fetched and skips otherwise (they are Git LFS objects).
"""

from __future__ import annotations

from pathlib import Path

import pytest

from otk.tools.sheetpipe import answerkey as ak
from otk.tools.sheetpipe import bank as bk

KEY = """สูตรผลบวกผลต่างมุม
1. 1. −
7
25
2. −1
2. 1. 17
6
3. 19
= working that continues the answer
ฟังก์ชันอาร์ค
1. 1. 45°
2. 4""".splitlines()

EXERCISE = """ฟังก์ชันอาร์ค
สูตรผลบวกผลต่างมุม
คำอธิบายก่อนแบบฝึกหัด
แบบฝึกหัด
1. กำหนดให้ sin A =
4
5 จงหาค่าของ
1. sin(A + B)
2. cos(A − B)
2. จงหาค่าของ
1. tan(A + B)
3.
sin 25° sin 85°
ตรงกับข้อใดต่อไปนี้    [PAT 1 (พ.ย. 57)/6]""".splitlines()


def test_key_sections_join_continuations():
    keys = ak.key_sections(KEY)
    assert list(keys) == ["สูตรผลบวกผลต่างมุม", "ฟังก์ชันอาร์ค"]
    toks = keys["สูตรผลบวกผลต่างมุม"]
    assert [(t.a, t.b) for t in toks] == [(1, 1), (2, None), (2, 1), (3, None)]
    assert toks[0].text == "− 7 25"
    assert toks[3].text == "19 = working that continues the answer"


def test_exercise_blocks_take_the_last_title_above():
    blocks = ak.exercise_blocks(EXERCISE, {"สูตรผลบวกผลต่างมุม", "ฟังก์ชันอาร์ค"})
    assert [t for t, _ in blocks] == ["สูตรผลบวกผลต่างมุม"]


def _body():
    return ak.exercise_blocks(EXERCISE, {"สูตรผลบวกผลต่างมุม"})[0][1]


def test_items_are_thai_instructions_and_subs_restart():
    exs, _ = ak.exercises(_body())                  # no key: the Thai heuristic alone
    assert [e.number for e in exs] == [1, 2, 3]
    assert exs[0].stem == "กำหนดให้ sin A = 4 5 จงหาค่าของ"
    assert exs[0].subs == ["sin(A + B)", "cos(A − B)"]
    assert exs[1].subs == ["tan(A + B)"]
    # A bare "3." whose Thai comes after the maths is still an item, with its exam tag.
    assert exs[2].tag == "PAT 1 (พ.ย. 57)/6"


def test_a_maths_sub_item_with_a_sidebar_note_stays_a_sub_item():
    body = ["1. จงหาค่า", "1. sin π", "2. cos(−π) =", "sin θ จะหาจาก พิกัด y ของ P(θ)", "3. tan π"]
    exs, _ = ak.exercises(body)
    assert len(exs) == 1 and len(exs[0].subs) == 3


def test_an_interval_is_not_an_exam_tag():
    assert ak.Exercise(1, "กำหนดให้ θ ∈ [0 , 3π 2 ] จงแก้สมการ").tag == ""
    assert ak.Exercise(1, "ข้อใดถูกต้อง [A-NET 49/1-7]").tag == "A-NET 49/1-7"


def test_answers_follow_the_aligned_structure():
    exs, answers = ak.exercises(_body(), ak.key_sections(KEY)["สูตรผลบวกผลต่างมุม"])
    assert [len(e.subs) for e in exs] == [2, 1, 0]
    assert answers == [["− 7 25", "−1"], ["17 6"], ["19 = working that continues the answer"]]


def test_the_key_overrules_a_thai_sub_item():
    # "2. (−1, −4) และ (−6, 8)" reads like an item, but the key says item 1 has three subs.
    body = ["1. จงหาระยะทางระหว่างจุดต่อไปนี้", "1. (0, 0) และ (3, 4)", "2. (−1, −4) และ (−6, 8)",
            "3. (1, 1) และ (1, 3)", "2. ถ้าวงกลมผ่านจุด A จงหารัศมี"]
    toks = [ak.Token(1, 1, "5"), ak.Token(2, None, "13"), ak.Token(3, None, "2"), ak.Token(2, None, "√10")]
    exs, answers = ak.exercises(body, toks)
    assert [len(e.subs) for e in exs] == [3, 0]
    assert answers == [["5", "13", "2"], ["√10"]]


def test_a_sidebar_step_is_dropped_as_noise():
    body = ["1. จงหาจุดยอด", "1. y = x²", "2. เอากลุ่มตัวแปรเข้าสูตร", "2. y = x² + 1", "2. จงหาโฟกัส"]
    toks = [ak.Token(1, 1, "(0, 0)"), ak.Token(2, None, "(0, 1)"), ak.Token(2, None, "(0, 1/4)")]
    exs, answers = ak.exercises(body, toks)
    assert answers == [["(0, 0)", "(0, 1)"], ["(0, 1/4)"]]


def test_a_choice_question_takes_one_answer():
    body = ["1. ข้อใดถูกต้อง [PAT 1 (มี.ค. 57)/11]", "1. ก ถูก", "2. ข ถูก", "3. ค ถูก", "4. ง ถูก"]
    exs, answers = ak.exercises(body, [ak.Token(1, None, "3")])
    assert exs[0].choices == ["ก ถูก", "ข ถูก", "ค ถูก", "ง ถูก"] and answers == [["3"]]


def test_key_chunks_split_at_each_new_block():
    toks = [ak.Token(1, 1, "a"), ak.Token(2, None, "b"), ak.Token(1, None, "c"), ak.Token(2, None, "d")]
    assert [[t.text for t in c] for c in ak.key_chunks(toks)] == [["a", "b"], ["c", "d"]]


def test_running_header_is_stripped_but_a_heading_under_it_is_kept():
    pages = ["ฟังก์ชันตรีโกณมิติ\n5\nฟังก์ชันตรีโกณมิติ\nเนื้อหา", "6    ฟังก์ชันตรีโกณมิติ\n1. ข้อ",
             "ฟังก์ชันตรีโกณมิติ\n7\nอื่น ๆ"]
    assert ak.clean_pages(pages) == [["ฟังก์ชันตรีโกณมิติ", "เนื้อหา"], ["1. ข้อ"], ["อื่น ๆ"]]


RATH = Path("rathcenter/8 ตรีโกณมิติ")


def test_a_section_source_resolves_to_every_item_of_that_section():
    from otk.tools.sheetpipe import knowledge as kn
    sheet = "rathcenter/8 ตรีโกณมิติ/(rath) 6 แปลงผลคูณกับผลบวกลบ.pdf"
    hits = kn.resolve({"sheet": sheet, "section": "สูตรแปลงผลคูณกับผลบวกลบ"})
    assert len(hits) == 26 and {p for p, _ in hits} == {sheet}
    assert kn.resolve({"sheet": sheet, "section": "ไม่มีหัวข้อนี้"}) == []


def test_real_rath_files_pair_fully():
    root = bk.default_root()
    key = root / RATH / "(rath) เฉลย.pdf"
    src = root / RATH / "(rath) 4 ผลบวกผลต่างมุม.pdf"
    if not (bk.present(key) and bk.present(src)):
        pytest.skip("bank PDFs not fetched (Git LFS)")
    items = ak.split(src, key)
    assert len(items) == 36 and all(it.answer for it in items)
    assert items[0].section == "สูตรผลบวกผลต่างมุม 1.1"
