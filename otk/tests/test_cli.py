"""The offline worksheet CLI (thin shim over otk.core, no web app)."""

from __future__ import annotations

import json

import pytest

from otk.cli import main


def _write_config(path, **overrides):
    data = {"title": "ทดสอบ", "font_family": "Tahoma",
            "generators": {"math.one_digit_plus_with_carry": 2, "math.multiplication": 1},
            "num_problems": 12, "seed": 1}
    data.update(overrides)
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_cli_generates_pdf(tmp_path):
    cfg = _write_config(tmp_path / "ws.json")
    out = tmp_path / "out.pdf"
    main([str(cfg), "-o", str(out)])
    assert out.read_bytes()[:5] == b"%PDF-"


def test_cli_defaults_output_and_flags(tmp_path):
    cfg = _write_config(tmp_path / "sheet.json")
    main([str(cfg), "-n", "6", "--seed", "3", "--no-answer-key"])
    assert (tmp_path / "sheet.pdf").read_bytes()[:5] == b"%PDF-"


def test_cli_list(capsys):
    main(["--list"])
    out = capsys.readouterr().out
    assert "math.one_digit_plus_with_carry" in out and "anatomy.skeleton" in out


def test_cli_unknown_type_errors(tmp_path):
    cfg = _write_config(tmp_path / "bad.json", generators={"math.nope": 1})
    with pytest.raises(SystemExit):          # argparse error -> exit
        main([str(cfg)])


def test_cli_resolves_shipped_diagrams(tmp_path, monkeypatch):
    """Offline, an image question used to print as blank space: the CLI passed
    no resolver. It must hand the renderer the assets that ship with the repo."""
    seen = {}

    def fake_render(config, questions, out, asset_resolver=None):
        seen["resolver"] = asset_resolver
        out.write_bytes(b"%PDF-")

    monkeypatch.setattr("otk.cli.render_pdf", fake_render)
    cfg = _write_config(tmp_path / "ws.json")
    main([str(cfg), "-o", str(tmp_path / "out.pdf")])

    resolver = seen["resolver"]
    assert resolver is not None
    found = resolver("p6c_2cell_1series_closed")
    assert found is not None and found.is_file()
    assert resolver("../../secret") is None          # ids cannot escape the dir


def test_cli_choices_flag_turns_on_printed_options(tmp_path, monkeypatch):
    configs = []
    monkeypatch.setattr("otk.cli.render_pdf",
                        lambda config, questions, out, asset_resolver=None:
                        (configs.append(config), out.write_bytes(b"%PDF-")))
    cfg = _write_config(tmp_path / "ws.json")
    main([str(cfg), "-o", str(tmp_path / "a.pdf")])
    main([str(cfg), "-o", str(tmp_path / "b.pdf"), "--choices"])
    assert [c.show_choices for c in configs] == [False, True]
