"""The explorer's one-page sheets: always two pages, laid out to fill the page without
one question running into the next, and the server's 30-second limit."""

from __future__ import annotations

import json
import re
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import fitz
import pytest

from otk.core.content import MathBlock, TextBlock
from otk.core.question import Choice, Question
from otk.core.render.assets import shipped_asset
from otk.tools import explorer_pdf, explorer_sheet
from otk.tools.explorer_pdf import Cooldown, SheetHandler, one_page_sheet, plan_sheet, sheet_info

#: One set per kind of page: long Thai text, a drawn diagram beside its words,
#: formulas inside sentences, a chart, a program.
SAMPLE = (
    "sci.process_skill_m3_application",
    "cell.cell_diagram",
    "ecology.food_web_diagram",
    "chem.chemical_equation_fluency",
    "math.linear_graph_read_m1",
    "comp.code_trace_fluency",
)


def _pages(pdf: bytes) -> int:
    return len(re.findall(rb"/Type\s*/Page[^s]", pdf))


@pytest.mark.parametrize("key", SAMPLE)
def test_a_sheet_is_one_page_of_problems_and_one_of_answers(key):
    pdf = one_page_sheet(key, seed=7)
    assert pdf.startswith(b"%PDF")
    assert _pages(pdf) == 2


def test_an_unknown_set_is_refused():
    with pytest.raises(KeyError):
        one_page_sheet("no.such_set", seed=1)


@pytest.mark.parametrize("key", SAMPLE)
def test_questions_sit_on_the_page_in_order_without_touching(key):
    plan = plan_sheet(key, seed=7)
    assert plan.questions and len(plan.placements) == len(plan.questions)
    for column in range(plan.columns):
        placed = [p for p in plan.placements if p.column == column]
        for p in placed:
            assert p.y_top <= plan.top + 1e-9
            assert p.y_top - p.height >= explorer_sheet.BOTTOM - 1e-9
        for above, below in zip(placed, placed[1:]):
            assert below.index == above.index + 1
            assert below.y_top <= above.y_top - above.height + 1e-9


@pytest.mark.parametrize("key", SAMPLE)
def test_the_printed_page_matches_the_plan(key):
    """Every line of text in the PDF ends above the next question and inside the page.

    Laying lines out with matplotlib's multi-line text measured them at one size
    and printed them at another, and a long Thai stem ran into its own options.
    """
    plan = plan_sheet(key, seed=7)
    page = fitz.open(stream=one_page_sheet(key, seed=7), filetype="pdf")[0]
    W, H = page.rect.width, page.rect.height
    # TeX's extension font (the radical sign's) reports a box far taller than its ink.
    spans = [s["bbox"] for b in page.get_text("dict")["blocks"]
             for line in b.get("lines", []) for s in line["spans"]
             if not s["font"].lower().startswith("cmex")]
    for p in plan.placements:
        x0, x1 = p.x * W, (p.x + plan.width) * W
        top, bottom = (1 - p.y_top) * H, (1 - (p.y_top - p.height)) * H
        after = [q for q in plan.placements if q.column == p.column and q.index == p.index + 1]
        limit = (1 - after[0].y_top) * H if after else (1 - explorer_sheet.BOTTOM) * H
        for sx0, sy0, sx1, sy1 in spans:
            if x0 <= (sx0 + sx1) / 2 <= x1 and top - 1 <= sy0 < bottom + 1:
                assert sy1 <= limit + 0.5, f"question {p.index + 1} runs into the next"
                assert sx1 <= explorer_sheet.RIGHT * W + 1, f"question {p.index + 1} runs off the page"


def test_a_sheet_fills_its_page_in_two_columns():
    plan = plan_sheet("chem.chemical_equation_fluency", seed=7)
    assert plan.columns == 2
    assert len(plan.questions) >= 12


def test_a_sheet_never_repeats_a_question():
    plan = plan_sheet("sci.process_skill_m3_application", seed=7)
    stems = [json.dumps(q.model_dump(mode="json", include={"stem"}), sort_keys=True)
             for q in plan.questions]
    assert len(stems) == len(set(stems))


def test_a_question_too_wide_for_half_the_page_gets_one_column():
    # A formula is never broken, so one longer than half the page needs the whole width.
    wide = " + ".join(f"x_{{{i}}}^{{2}}" for i in range(18))
    made = iter(range(100))

    def draw():
        n = next(made)
        return Question(type="t", topic="t", answer=0,
                        stem=[TextBlock(text=f"ข้อ {n} จงหาค่า"), MathBlock(tex=wide)],
                        choices=[Choice(content=[TextBlock(text=str(v))]) for v in range(4)])

    plan = explorer_sheet.plan_page(sheet_info("chem.chemical_equation_fluency"), draw,
                                    shipped_asset)
    assert plan.columns == 1


def test_tex_that_mathtext_lacks_is_renamed_or_printed_as_written():
    assert explorer_sheet._mathtext(r"x \ge 2 \ne y") == r"x \geq 2 \neq y"
    assert explorer_sheet._mathtext(r"\begin{array}{c} 1 \\ 2 \end{array}") is None
    pieces = explorer_sheet._pieces([("math", r"\begin{array}{c} 1 \end{array}")])
    assert pieces == [(r"\begin{array}{c} 1 \end{array}", False)]   # no $: plain text


def test_short_options_share_a_line():
    four = [[("text", "1 อะตอม")], [("text", "2 อะตอม")], [("text", "3 อะตอม")],
            [("text", "4 อะตอม")]]
    long = [[("text", "สารนี้มีมวล 2 กรัม ตามมวลของสารในสมการเคมีที่ดุลแล้ว")]] * 4
    assert explorer_sheet._choices_per_row(four, 0.38, 0.02, "") == 4
    assert explorer_sheet._choices_per_row(long, 0.38, 0.02, "") == 1

def test_the_cooldown_allows_one_sheet_per_window_per_client():
    now = [0.0]
    cooldown = Cooldown(30, clock=lambda: now[0])
    assert cooldown.take("a") == 0
    assert cooldown.take("a") == pytest.approx(30)
    assert cooldown.take("b") == 0          # another visitor is not held up
    now[0] = 29.5
    assert cooldown.take("a") == pytest.approx(0.5)
    now[0] = 30.0
    assert cooldown.take("a") == 0          # the window has passed
    cooldown.release("a")                   # a failed sheet gives its claim back
    assert cooldown.take("a") == 0


@pytest.fixture
def server(monkeypatch):
    monkeypatch.setattr(explorer_pdf, "COOLDOWN", Cooldown(30))
    monkeypatch.setattr(explorer_pdf, "one_page_sheet", lambda key, seed: b"%PDF-fake")
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), SheetHandler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()


def _get(url: str, client: str = "203.0.113.5"):
    request = urllib.request.Request(url, headers={"X-Client-IP": client})
    try:
        with urllib.request.urlopen(request) as response:
            return response.status, dict(response.headers), response.read()
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), error.read()


def test_the_server_sends_a_pdf_then_holds_the_same_visitor_for_30_seconds(server):
    status, headers, body = _get(f"{server}/api/sheet?key=cell.cell_diagram")
    assert status == 200 and body == b"%PDF-fake"
    assert headers["Content-Type"] == "application/pdf"
    assert "attachment" in headers["Content-Disposition"]
    status, headers, _ = _get(f"{server}/api/sheet?key=cell.cell_diagram")
    assert status == 429 and 1 <= int(headers["Retry-After"]) <= 30
    status, _, _ = _get(f"{server}/api/sheet?key=cell.cell_diagram", client="198.51.100.9")
    assert status == 200


def test_the_server_refuses_unknown_sets_and_paths_without_using_the_window(server):
    assert _get(f"{server}/api/sheet?key=no.such_set")[0] == 404
    assert _get(f"{server}/api/sheet")[0] == 404
    assert _get(f"{server}/elsewhere")[0] == 404
    assert _get(f"{server}/api/sheet?key=cell.cell_diagram")[0] == 200
