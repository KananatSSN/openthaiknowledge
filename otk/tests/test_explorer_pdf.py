"""The explorer's one-page sheets: always two pages, and the server's 30-second limit."""

from __future__ import annotations

import re
import threading
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer

import pytest

from otk.tools import explorer_pdf
from otk.tools.explorer_pdf import Cooldown, SheetHandler, one_page_sheet

#: One set per kind of page: arithmetic, long Thai text, a drawn diagram, a chart.
SAMPLE = (
    "sci.process_skill_m3_application",
    "cell.cell_diagram",
    "ecology.food_web_diagram",
    "geo.coriolis_foundation",
    "sci.process_skill_p5_fluency",
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
