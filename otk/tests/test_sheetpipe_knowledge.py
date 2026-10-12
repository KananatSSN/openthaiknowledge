"""Tests for knowledge units (``otk/knowledge/``, ``sheetpipe knowledge``).

The committed units must validate: each source resolves to a converted
question, each ``covered_by`` key is registered, and there are no
prerequisite cycles. The rest checks that the validator catches each kind
of mistake.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from otk.tools.sheetpipe import knowledge as kn

REAL_TAG = "O-NET (มี.ค. 2561/25)"      # a question in the committed digests


def topic(units: list[kn.Unit], t: str = "ความน่าจะเป็น") -> kn.TopicFile:
    return kn.TopicFile(Path("test.json"), "คณิตศาสตร์", t, "ม.5", units)


def unit(uid: str, **kw) -> kn.Unit:
    base = dict(id=uid, kind="concept", title="t", statement="s",
                sources=[{"tag": REAL_TAG}])
    return kn.Unit(**{**base, **kw})


def test_committed_knowledge_is_valid():
    files = kn.load_all()
    assert files, "no knowledge files under otk/knowledge"
    assert kn.validate(files) == []


def test_reference_topic_accounts_for_every_question():
    # Probability is the worked reference: every converted question in its
    # folder is claimed by some unit.
    files = kn.load_all()
    _, by_pos = kn.question_index()
    sheets = {p for p, _ in by_pos if p.startswith("rathcenter/13 ")}
    assert sheets
    for s in sheets:
        mapped, total, missing = kn.sheet_coverage(s, files)
        assert not missing, f"{s}: {missing}"


def test_a_tag_resolves_across_compilations():
    # The same exam question is repeated in several files; a tag names them all.
    positions = kn.resolve({"tag": "กสพท คณิต1 (เม.ย. 2564/18)"})
    assert len({p for p, _ in positions}) >= 2


@pytest.mark.parametrize("bad, message", [
    (unit("a", kind="theorem"), "unknown kind"),
    (unit("a", kind="formula"), "names its variables"),
    (unit("a", kind="procedure", steps=["one"]), "at least two steps"),
    (unit("a", kind="fact-list", facts={"x": ["1"]}), "at least two categories"),
    (unit("a", sources=[]), "no source question"),
    (unit("a", sources=[{"tag": "O-NET (ไม่มี 9999/99)"}]), "not in any digest"),
    (unit("a", sources=[{"sheet": "nope.pdf", "item": 1}]), "not in any digest"),
    (unit("a", covered_by=["math.no_such_type"]), "not a registry key"),
    (unit("a", prerequisites=["math.missing"]), "does not exist"),
])
def test_validate_catches(bad, message):
    problems = kn.validate([topic([bad])])
    assert any(message in p for p in problems), problems


def test_validate_catches_duplicates_cycles_and_unknown_topics():
    assert any("duplicate id" in p for p in kn.validate([topic([unit("a"), unit("a")])]))
    a = unit("a", prerequisites=["b"])
    b = unit("b", prerequisites=["a"])
    assert any("cycle" in p for p in kn.validate([topic([a, b])]))
    problems = kn.validate([topic([unit("c")], t="หัวข้อที่ไม่มี")])
    assert any("not a registry topic" in p for p in problems)
    assert kn.validate([topic([unit("c", new_topic=True)], t="หัวข้อที่ไม่มี")]) == []
