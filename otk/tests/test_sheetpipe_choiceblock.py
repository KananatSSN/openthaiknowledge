"""Tests for the margin-label question splitter (``sheetpipe convert``).

Pages are built from :class:`fontfix.Block` objects laid out the way the
rathcenter PDFs lay them out. That is margin labels as narrow blocks at
x = 72, content from x = 72 to the right, and the solutions run repeating
every question with ``ตอบ``. Page geometry is what the splitter reads, so
nothing here needs a Thai-capable PDF font.
"""

from __future__ import annotations

from otk.tools.sheetpipe import choiceblock as cb
from otk.tools.sheetpipe.convert import inline
from otk.tools.sheetpipe.fontfix import Block


def label(page: int, n: int, y: float) -> Block:
    return Block(page, (72, y, 80, y + 16), f"{n}.")


def text(page: int, y: float, body: str, x: float = 72) -> Block:
    return Block(page, (x, y, 450, y + 12 * (body.count("\n") + 1)), body)


Q1 = ("ในกล่องมีเสื้อ 100 ตัว ถ้าสุ่มหยิบ 1 ตัว ความน่าจะเป็นเท่ากับข้อใด\n"
      "[กสพท คณิต2 (มี.ค. 2561/10)]\n1.\n1\n5\n2.\n7\n20\n3.\n9\n20\n4.\n11\n20\n5.\n13\n20")
Q2_TOP = "กำหนดให้"
Q2_SETS = "𝐴 = { 1, 2 }\n𝐵 = { 2, 3 }"
Q2_ASK = "จำนวนสมาชิกของ 𝐴 ∪ 𝐵 เท่ากับเท่าใด    [O-NET (มี.ค. 2561/31)]"


def question_page() -> cb.Page:
    return ([label(1, 1, 74), text(1, 74, Q1),
             label(1, 2, 400), text(1, 400, Q2_TOP), text(1, 440, Q2_ASK),
             # Emitted last by the text layer, but it sits between the two lines above.
             text(1, 418, Q2_SETS, x=136)],
            [])


def solution_page(label_q2: bool = True) -> cb.Page:
    blocks = [label(2, 1, 74), text(2, 74, Q1), text(2, 300, "ตอบ 5\nM หรือ L มี 65 ตัว"),
              text(2, 400, Q2_TOP), text(2, 418, Q2_SETS, x=136), text(2, 440, Q2_ASK),
              text(2, 470, "ตอบ 3\n𝐴 ∪ 𝐵 = { 1, 2, 3 }")]
    if label_q2:
        blocks.append(label(2, 2, 400))
    return blocks, []


def test_questions_read_top_to_bottom_with_tags_and_choices():
    items = cb.items_from(cb.assign([question_page(), solution_page()]))
    assert [it.number for it in items] == [1, 2]
    q1, q2 = items
    assert q1.tag == "กสพท คณิต2 (มี.ค. 2561/10)"
    assert [inline(c) for c in q1.choices.values()] == ["1/5", "7/20", "9/20", "11/20", "13/20"]
    assert "[" not in q1.stem
    # Geometry, not text-layer order: the set definitions sit mid-stem.
    assert q2.stem.splitlines() == ["กำหนดให้", "𝐴 = { 1, 2 }", "𝐵 = { 2, 3 }",
                                    "จำนวนสมาชิกของ 𝐴 ∪ 𝐵 เท่ากับเท่าใด"]
    assert q2.choices == {}                                   # open answer


def test_answers_come_from_the_solutions_run():
    q1, q2 = cb.items_from(cb.assign([question_page(), solution_page()]))
    assert (q1.answer, q2.answer) == ("5", "3")
    assert q1.solution == "M หรือ L มี 65 ตัว"
    assert "กำหนดให้" not in q1.solution        # q2's repeated stem is not q1's working


def test_a_missing_solution_label_is_bridged_by_the_tag():
    q1, q2 = cb.items_from(cb.assign([question_page(), solution_page(label_q2=False)]))
    assert (q1.answer, q2.answer) == ("5", "3")
    assert "กำหนดให้" not in q1.solution


def test_unlabelled_solution_pages_are_split_off():
    sol, bands = solution_page()
    sol = [b for b in sol if not cb._is_label(b)]
    runs = cb.assign([question_page(), (sol, bands)])
    assert len(runs) == 2 and runs[1][0].number == 0
    q1, q2 = cb.items_from(runs)
    assert (q1.answer, q2.answer) == ("5", "3")
    assert "ตอบ" not in q2.stem


def test_figure_from_image_or_drawing():
    blocks, _ = question_page()
    blocks.append(Block(1, (300, 90, 400, 150), image=True))
    q1, q2 = cb.items_from(cb.assign([(blocks, [(430, 460)])]))
    assert q1.figure and q2.figure


def test_furniture_is_not_a_question():
    assert cb._is_furniture(Block(1, (72, 36, 533, 50), " คลังโจทย์ "), 842)
    assert cb._is_furniture(Block(1, (530, 34, 535, 51), "1"), 842)
    assert not cb._is_furniture(Block(1, (72, 400, 90, 416), "12"), 842)


def test_inline_choice():
    assert inline("1\n5") == "1/5"
    assert inline("−\n1\n2 −√3\n2 i") == "− / 1 / 2 −√3 / 2 i"
    assert inline("{ 1, 3 }") == "{ 1, 3 }"
