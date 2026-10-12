"""Tests for the sheet bank index (``sheetpipe bank``).

The property that matters most is :func:`test_rescan_keeps_owned_fields`: the
index is where multi-session digestion progress lives, so a rescan — run on any
machine, with or without the gitignored PDFs — must never erase it.
"""

from __future__ import annotations

import pytest

from otk.tests._bank import needs_bank
from otk.tools.sheetpipe import bank as bk
from otk.tools.sheetpipe.spec import sheet_ids


def fake_probe(path):
    return {"pages": 1, "text_chars": 500, "layout": "numbered", "glyph_damage": 0}


def make_bank(root):
    (root / "rath" / "set").mkdir(parents=True)
    (root / "rath" / "set" / "a.pdf").write_bytes(b"pdf-a")
    (root / "notes.md").write_text("# notes", encoding="utf-8")
    (root / "facts.py").write_text("x = {}", encoding="utf-8")
    (root / "archive.zip").write_bytes(b"zip")
    (root / "HANDOFF.md").write_text("bookkeeping", encoding="utf-8")
    (root / ".hidden").mkdir()
    (root / ".hidden" / "b.pdf").write_bytes(b"pdf-b")
    return root


def test_scan_classifies_and_skips_bookkeeping(tmp_path):
    bank, tally = bk.scan(make_bank(tmp_path), probe=fake_probe)
    assert sorted(bank) == ["archive.zip", "facts.py", "notes.md", "rath/set/a.pdf"]
    assert {k: e.kind for k, e in bank.items()} == {
        "archive.zip": "other", "facts.py": "fact-data",
        "notes.md": "notes", "rath/set/a.pdf": "exam"}
    assert bank["archive.zip"].stage == "ignored"
    assert bank["rath/set/a.pdf"].layout == "numbered"
    assert bank["notes.md"].layout == ""          # only PDFs are probed
    assert tally["added"] == 4


def test_rescan_keeps_owned_fields(tmp_path):
    root = make_bank(tmp_path)
    bank, _ = bk.scan(root, probe=fake_probe)
    bk.set_fields([bank["rath/set/a.pdf"]], sheet_id="rath_set", stage="extracted",
                  note="items 1-12 checked")
    bank["notes.md"].note = "untouched note"

    (root / "rath" / "set" / "a.pdf").write_bytes(b"pdf-a, revised")
    bank, tally = bk.scan(root, bank, probe=fake_probe)

    a = bank["rath/set/a.pdf"]
    assert (a.sheet_id, a.stage, a.note) == ("rath_set", "extracted", "items 1-12 checked")
    assert a.stale, "a file that changed after progressing must be flagged"
    assert not bank["notes.md"].stale
    assert bank["notes.md"].note == "untouched note"
    assert (tally["changed"], tally["unchanged"]) == (1, 3)


def test_reprobe_refreshes_without_staling(tmp_path):
    root = make_bank(tmp_path)
    bank, _ = bk.scan(root, probe=fake_probe)
    bk.set_fields([bank["rath/set/a.pdf"]], stage="extracted", note="kept")
    better = lambda p: {**fake_probe(p), "glyph_damage": 7}
    bank, tally = bk.scan(root, bank, probe=better, reprobe=True)
    a = bank["rath/set/a.pdf"]
    assert (a.glyph_damage, a.stage, a.note, a.stale) == (7, "extracted", "kept", False)
    assert tally["changed"] == 0


def test_lfs_pointer_counts_as_absent(tmp_path):
    # CI checks out without LFS, so a bank PDF is a pointer there. Scanning it
    # must not replace the real record's hash with the pointer's.
    root = make_bank(tmp_path)
    bank, _ = bk.scan(root, probe=fake_probe)
    real = bank["rath/set/a.pdf"].sha256
    (root / "rath" / "set" / "a.pdf").write_bytes(
        b"version https://git-lfs.github.com/spec/v1\noid sha256:abc\nsize 5\n")
    bank, tally = bk.scan(root, bank, probe=fake_probe)
    assert bank["rath/set/a.pdf"].sha256 == real
    assert tally["absent"] == 1 and tally["changed"] == 0
    assert not bk.present(root / "rath" / "set" / "a.pdf")
    assert bk.present(root / "notes.md")


def test_changed_new_file_is_not_stale(tmp_path):
    root = make_bank(tmp_path)
    bank, _ = bk.scan(root, probe=fake_probe)
    (root / "notes.md").write_text("# notes v2", encoding="utf-8")
    bank, _ = bk.scan(root, bank, probe=fake_probe)
    assert not bank["notes.md"].stale


def test_absent_records_survive_a_scan(tmp_path):
    # A worktree has no PDFs (they are gitignored); scanning there must not
    # drop the committed records for them.
    root = make_bank(tmp_path)
    bank, _ = bk.scan(root, probe=fake_probe)
    (root / "rath" / "set" / "a.pdf").unlink()
    bank, tally = bk.scan(root, bank, probe=fake_probe)
    assert "rath/set/a.pdf" in bank
    assert tally["absent"] == 1


def test_duplicates_point_at_first_copy(tmp_path):
    root = make_bank(tmp_path)
    (root / "copy.pdf").write_bytes(b"pdf-a")
    bank, _ = bk.scan(root, probe=fake_probe)
    assert bank["rath/set/a.pdf"].duplicate_of == "copy.pdf"
    assert bank["copy.pdf"].duplicate_of == ""


def test_save_load_roundtrip_omits_defaults(tmp_path):
    bank, _ = bk.scan(make_bank(tmp_path / "bank"), probe=fake_probe)
    bank["notes.md"].note = "เรื่องไฟฟ้า"
    out = tmp_path / "bank.json"
    bk.save_bank(bank, out)
    text = out.read_text("utf-8")
    assert "เรื่องไฟฟ้า" in text                     # Thai stays readable
    assert '"stale"' not in text and '"duplicate_of"' not in text
    assert bk.load_bank(out) == bank


def test_select_and_set(tmp_path):
    bank, _ = bk.scan(make_bank(tmp_path), probe=fake_probe)
    assert [e.path for e in bk.select(bank, "rath/*")] == ["rath/set/a.pdf"]
    assert [e.path for e in bk.select(bank, "notes.md")] == ["notes.md"]
    with pytest.raises(ValueError):
        bk.set_fields(bk.select(bank, "*"), stage="done")


def test_link_digested_covers_identical_copies():
    sid = sheet_ids()[0]
    from otk.tools.sheetpipe.spec import load_sheet
    key = bk._bank_key(load_sheet(sid).source_pdf)
    bank = {key: bk.BankEntry(path=key, kind="exam", sha256="aa"),
            "elsewhere/copy.pdf": bk.BankEntry(path="elsewhere/copy.pdf", kind="exam",
                                               sha256="aa", duplicate_of=key)}
    bk.link_digested(bank, stage_of=lambda s: "green")
    assert {(e.sheet_id, e.stage) for e in bank.values()} == {(sid, "green")}


# ── Detectors ────────────────────────────────────────────────────────────────

def test_source_tag():
    assert bk.SOURCE_TAG.search("ข้อใดถูก [กสพท คณิต1 (มี.ค. 2567/1)]")
    assert bk.SOURCE_TAG.search("[O-NET 62/14]")
    assert bk.SOURCE_TAG.search("[A-level 2 (มี.ค. 2567/2)]")
    assert not bk.SOURCE_TAG.search("ช่วง [−1, 2] และ [10, 20]")


def test_glyph_damage():
    from otk.tools.sheetpipe.fontfix import raw_damage
    assert raw_damage("ข้อใดต่อไปนี9ถูกต้อง ดังนั9น ถา") >= 3
    assert raw_damage("ทีLรวม ซึMง จ ำนวน") == 3
    assert raw_damage("ชั้น ม.4 ข้อ 5 นี้ถูกต้อง [กสพท คณิต1 (มี.ค. 2567/1)]") == 0


def test_guess_layout():
    q = "ข้อความโจทย์ยาวพอสมควรเพื่อให้ผ่านเกณฑ์ข้อความขั้นต่ำของหน้า " * 3
    numbered = ["\n".join(f"{n}. {q}" for n in range(1, 7))]
    choice = [f"{q} [O-NET 62/{n}]\n1. 2\n2. 3\n3. 4\n4. 5\n5. 6" for n in range(1, 4)]
    assert bk.guess_layout(numbered) == "numbered"
    assert bk.guess_layout(choice) == "choice-block"
    assert bk.guess_layout(["", " "]) == "no-text"


def test_probe_real_pdf(tmp_path):
    fitz = pytest.importorskip("fitz")
    pdf = tmp_path / "sheet.pdf"
    with fitz.open() as doc:
        page = doc.new_page()
        body = "\n".join(f"{n}. Find the value of x in question number {n} here."
                         for n in range(1, 7))
        page.insert_text((50, 72), body, fontsize=9)
        doc.save(pdf)
    got = bk.probe_pdf(pdf)
    assert got["pages"] == 1 and got["layout"] == "numbered"
    assert got["text_chars"] > 100


# ── The committed index ──────────────────────────────────────────────────────

def test_committed_bank_is_consistent():
    bank = bk.load_bank()
    if not bank:
        pytest.skip("no otk/sheets/bank.json yet")
    for e in bank.values():
        assert e.stage in bk.STAGES, e.path
        assert e.kind in {*bk.KIND_BY_SUFFIX.values(), "other"}, e.path
    linked = {e.sheet_id for e in bank.values() if e.sheet_id}
    assert set(sheet_ids()) <= linked, "a digested sheet is missing from bank.json"


@needs_bank
def test_committed_digests_match_the_bank():
    from otk.tools.sheetpipe.convert import digest_paths, load_digest
    converted = [e for e in bk.load_bank().values() if e.items]
    assert all(e.stage not in ("new", "ignored") for e in converted)
    for e in converted:
        js, md = digest_paths(e.path)
        assert js.is_file() and md.is_file(), f"{e.path}: digest missing"
        d = load_digest(e.path)
        assert d["sha256"] == e.sha256, f"{e.path}: digest is of another version"
        assert len(d["items"]) == e.items > 0, e.path
        assert all(it["stem"].strip() for it in d["items"]), e.path


def test_only_a_clone_of_the_private_bank_counts_as_the_bank(tmp_path):
    own = tmp_path / "own"
    (own / "contrib" / "me").mkdir(parents=True)
    assert not bk.has_private_bank(own)
    clone = tmp_path / "clone"
    (clone / ".git").mkdir(parents=True)
    (clone / ".git" / "config").write_text(
        '[remote "origin"]\n\turl = https://github.com/KananatSSN/openthaiknowledge-bank.git\n', "utf-8")
    assert bk.has_private_bank(clone)


def test_prune_refuses_without_the_private_bank(tmp_path, monkeypatch):
    from otk.tools.sheetpipe.__main__ import main
    saved = []
    monkeypatch.setattr(bk, "save_bank", lambda bank, path=bk.BANK_FILE: saved.append(bank))
    assert main(["bank", "prune", "--root", str(tmp_path)]) == 1
    assert not saved
