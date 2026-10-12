"""Offline curriculum graph — a local dev tool, never wired into the app.

Reads the question-type registry directly (no server, no network) and writes a
single self-contained HTML file that graphs the catalog rooted at the subjects.
Math follows Course → Level → Strand → Standard → Topic → display_name; other
subjects retain Level → Topic → display_name. Open the file in any browser; it has the
data baked in, so it works with the machine offline and ships in nothing.

Every *type* node also carries a handful of pre-generated sample problems, baked
in at build time. Click a type to open the problem panel; the 🎲 button cycles
through the baked pool ("regenerate"). Math renders with KaTeX, vendored inline
(JS + CSS + woff2 fonts as data URIs) so the page stays fully offline.

**Figures are baked in too**, as data URIs — so the page is where you go to check
that a question's diagram actually matches the question. A type whose samples
carry one is marked 🖼 on the graph, `🖼 เฉพาะที่มีรูป` filters the tree down to
those, and the panel shows the real image with its alt text underneath. That
last part matters: a shipped figure is only correct if it shows what *every*
draw has in common, so cycle the samples and watch the picture against the stem.

**Sets awaiting review are highlighted.** Every key in a cohort listed in
:data:`otk.core.curriculum_science.REVIEW_PENDING` is drawn in amber with a 🔍
badge, its ancestors count how many sit below them, and `🔍 รอตรวจ` prunes the
tree to just those sets — the reviewer's worklist for an open gate.

    python -m otk.tools.curriculum_graph        # writes ./curriculum_graph.html and opens it
    python -m otk.tools.curriculum_graph -o x.html --no-open
    python -m otk.tools.curriculum_graph --samples 10   # more samples per type
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import re
import webbrowser
from functools import lru_cache
from pathlib import Path
from random import Random

from otk.core import catalog, generate
from otk.core.curriculum_science import REVIEW_PENDING
from otk.core.render.assets import shipped_asset

SAMPLES_PER_TYPE = 6            # how many distinct problems to bake per type
_SAMPLE_TRIES = 48             # seeds to try while collecting distinct samples

# KaTeX is borrowed from an npm install for offline vendoring: apps/web's (when
# run inside TutorRank) or the workspace root's. Without it the page still
# builds, with maths left as TeX source.
_ROOT = Path(__file__).resolve().parents[2]
_KATEX_DIST = next(
    (d for d in (_ROOT / "apps" / "web" / "node_modules" / "katex" / "dist",
                 _ROOT / "node_modules" / "katex" / "dist") if (d / "katex.min.js").exists()),
    _ROOT / "apps" / "web" / "node_modules" / "katex" / "dist")

#: Figures are baked as data URIs, so they are downscaled first — the panel is
#: 380 px wide and a 300 dpi crop of an A4 figure is several times that.
FIGURE_MAX_PX = 800


def _asset_file(asset_id: str) -> Path | None:
    """The PNG behind an asset id, without going through the API.

    The same sources the generator serves — a local upload directory, the
    built-in and drawn-on-demand diagrams, a digested sheet's figures — without
    creating a data directory as a side effect (this is a dev tool).
    """
    uploaded = Path(os.environ.get("HW_DATA_DIR", "data")) / "assets" / f"{asset_id}.png"
    if uploaded.is_file():
        return uploaded
    return shipped_asset(asset_id)


@lru_cache(maxsize=512)
def _asset_data_uri(asset_id: str) -> str | None:
    """``data:image/png;base64,…`` for an asset id, or None if it isn't on disk.

    Downscales through Pillow when it is available; without it the file is
    embedded as-is, which is bigger but still correct.
    """
    path = _asset_file(asset_id)
    if path is None:
        return None
    raw = path.read_bytes()
    try:
        from io import BytesIO

        from PIL import Image
        img = Image.open(BytesIO(raw))
        if max(img.size) > FIGURE_MAX_PX:
            img.thumbnail((FIGURE_MAX_PX, FIGURE_MAX_PX))
            buf = BytesIO()
            img.save(buf, format="PNG", optimize=True)
            raw = buf.getvalue()
    except Exception:                                         # noqa: BLE001
        pass                                     # Pillow missing or odd PNG
    return "data:image/png;base64," + base64.b64encode(raw).decode("ascii")


def _asset_ids(rows: list[dict]) -> list[str]:
    """Every asset id any baked sample refers to, in first-seen order."""
    out: dict[str, None] = {}
    for row in rows:
        for sample in row.get("samples", []):
            for block in sample["stem"]:
                if block.get("kind") == "image":
                    out.setdefault(block["asset_id"])
    return list(out)


def assets_for(rows: list[dict]) -> dict[str, str]:
    """``{asset id: data URI}`` for the figures the baked samples actually use.

    Keyed by id rather than baked into each sample, so a figure shared by
    several types — or by several draws of one type — is embedded once.
    """
    found = ((aid, _asset_data_uri(aid)) for aid in _asset_ids(rows))
    return {aid: uri for aid, uri in found if uri}


def _samples_for(key: str, n: int = SAMPLES_PER_TYPE) -> list[dict]:
    """Up to ``n`` distinct sample problems for a type, as block-tree JSON.

    Draws with successive fixed seeds so the baked file is reproducible, dedups
    on the whole item, and quietly skips seeds that raise (a type with a tiny
    output space simply yields fewer than ``n``).
    """
    seen: set[str] = set()
    out: list[dict] = []
    for seed in range(_SAMPLE_TRIES):
        try:
            q = generate(key, Random(seed))
        except Exception:
            continue
        sample = {
            "stem": [b.model_dump() for b in q.stem],
            "choices": [[b.model_dump() for b in c.content] for c in q.choices],
            "answer": q.answer,
        }
        sig = json.dumps(sample, ensure_ascii=False, sort_keys=True)
        if sig in seen:
            continue
        seen.add(sig)
        out.append(sample)
        if len(out) >= n:
            break
    return out


def _inline_katex() -> tuple[str | None, str | None]:
    """KaTeX (css, js) with woff2 fonts embedded as data URIs, or ``(None, None)``.

    Returns ``(None, None)`` when the vendored dist isn't present (e.g. the web
    dependencies were never installed); the page then falls back to showing raw
    TeX, so the tool still works without KaTeX.
    """
    css_path = _KATEX_DIST / "katex.min.css"
    js_path = _KATEX_DIST / "katex.min.js"
    if not (css_path.exists() and js_path.exists()):
        return None, None

    css = css_path.read_text(encoding="utf-8")

    def embed(m: re.Match) -> str:
        raw = (_KATEX_DIST / "fonts" / m.group(1)).read_bytes()
        b64 = base64.b64encode(raw).decode("ascii")
        return f'url(data:font/woff2;base64,{b64}) format("woff2")'

    # Point every woff2 at an inline data URI, then drop the woff/ttf fallbacks
    # so no font file is ever fetched from disk.
    css = re.sub(r'url\(fonts/([\w-]+\.woff2)\) format\("woff2"\)', embed, css)
    css = re.sub(
        r',url\(fonts/[\w-]+\.woff\) format\("woff"\)'
        r',url\(fonts/[\w-]+\.ttf\) format\("truetype"\)',
        "", css,
    )
    return css, js_path.read_text(encoding="utf-8")


def review_cohort(key: str) -> str | None:
    """The open review cohort a key belongs to, or None once its gate has passed."""
    for name, keys in REVIEW_PENDING.items():
        if key in keys:
            return name
    return None


def _rows_with_samples(samples: int = SAMPLES_PER_TYPE) -> list[dict]:
    """The catalog with ``samples`` and its open ``review`` cohort on every entry."""
    rows = catalog()
    for r in rows:
        r["samples"] = _samples_for(r["key"], samples)
        r["review"] = review_cohort(r["key"])
    return rows


def build_html(samples: int = SAMPLES_PER_TYPE,
               rows: list[dict] | None = None) -> str:
    """The full page with the current catalog + baked samples + KaTeX inlined."""
    if rows is None:
        rows = _rows_with_samples(samples)
    data = json.dumps(rows, ensure_ascii=False)
    css, js = _inline_katex()

    html = _TEMPLATE.replace("/*__KATEX_CSS__*/", css or "")
    html = html.replace("/*__KATEX_JS__*/", js or "")
    html = html.replace("/*__ASSETS__*/null", json.dumps(assets_for(rows)))
    html = html.replace("/*__DATA__*/null", data)
    return html


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("-o", "--out", default="curriculum_graph.html",
                    help="output HTML path (default: ./curriculum_graph.html)")
    ap.add_argument("--samples", type=int, default=SAMPLES_PER_TYPE,
                    help=f"sample problems to bake per type (default: {SAMPLES_PER_TYPE})")
    ap.add_argument("--no-open", action="store_true",
                    help="just write the file; don't open a browser")
    args = ap.parse_args(argv)

    rows = _rows_with_samples(args.samples)
    html = build_html(rows=rows)
    out = Path(args.out).resolve()
    out.write_text(html, encoding="utf-8")

    n_samples = sum(len(r["samples"]) for r in rows)
    n_review = sum(1 for r in rows if r.get("review"))
    katex = "with KaTeX" if (_KATEX_DIST / "katex.min.js").exists() else "raw TeX (KaTeX not found)"
    wanted = _asset_ids(rows)
    baked = assets_for(rows)
    missing = [a for a in wanted if a not in baked]
    print(f"wrote {out}  ({len(rows)} question types, "
          f"{n_samples} baked samples, {len(baked)} figures, {katex})")
    if n_review:
        print(f"  {n_review} set(s) awaiting review, highlighted: "
              + ", ".join(REVIEW_PENDING))
    if missing:
        print(f"  {len(missing)} asset(s) referenced but not on disk: "
              + ", ".join(missing[:6]) + ("…" if len(missing) > 6 else ""))
    if not args.no_open:
        webbrowser.open(out.as_uri())


# The page. Data is injected by replacing the `/*__DATA__*/null` token below;
# KaTeX css/js by the `/*__KATEX_CSS__*/` and `/*__KATEX_JS__*/` tokens.
_TEMPLATE = r"""<!doctype html>
<html lang="th">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Curriculum graph — internal</title>
<style>/*__KATEX_CSS__*/</style>
<style>
  :root {
    --bg: #0e1116; --panel: #161b22; --line: #30363d; --ink: #e6edf3;
    --muted: #8b949e; --subject: #f0883e; --course: #d29922; --level: #58a6ff;
    --strand: #39c5cf; --standard: #db6dcb; --topic: #3fb950;
    --type: #bc8cff; --link: #444c56; --good: #3fb950; --review: #e3b341;
  }
  * { box-sizing: border-box; }
  html, body { margin: 0; height: 100%; background: var(--bg); color: var(--ink);
    font: 14px/1.4 -apple-system, "Segoe UI", "Noto Sans Thai", Tahoma, sans-serif; }
  #bar {
    position: fixed; top: 0; left: 0; right: 0; height: 48px; z-index: 5;
    display: flex; align-items: center; gap: 14px; padding: 0 14px;
    background: var(--panel); border-bottom: 1px solid var(--line);
  }
  #bar h1 { font-size: 14px; font-weight: 600; margin: 0; white-space: nowrap; }
  #bar .spacer { flex: 1; }
  #search {
    background: var(--bg); border: 1px solid var(--line); color: var(--ink);
    border-radius: 6px; padding: 6px 10px; width: 240px; outline: none;
  }
  #search:focus { border-color: var(--level); }
  .btn {
    background: var(--bg); border: 1px solid var(--line); color: var(--ink);
    border-radius: 6px; padding: 6px 10px; cursor: pointer; white-space: nowrap;
  }
  .btn:hover { border-color: var(--muted); }
  .btn:disabled { opacity: 0.4; cursor: default; }
  .legend { display: flex; gap: 12px; font-size: 12px; color: var(--muted); }
  .legend span { display: inline-flex; align-items: center; gap: 5px; }
  .dot { width: 9px; height: 9px; border-radius: 50%; display: inline-block; }
  #wrap { position: fixed; inset: 48px 0 0 0; overflow: hidden; cursor: grab; }
  #wrap.grabbing { cursor: grabbing; }
  svg { display: block; width: 100%; height: 100%; }
  .link { fill: none; stroke: var(--link); stroke-width: 1.2px; }
  .node { cursor: pointer; }
  .node text { fill: var(--ink); dominant-baseline: middle; user-select: none; }
  .node .count { fill: var(--muted); font-size: 11px; }
  .node.dim { opacity: 0.18; }
  .node.hit text { font-weight: 700; }
  .node.picked text { fill: var(--type); font-weight: 700; }
  #hint { position: fixed; bottom: 10px; right: 14px; color: var(--muted);
    font-size: 12px; z-index: 5; }
  #tip {
    position: fixed; z-index: 6; pointer-events: none; display: none;
    background: #000c; border: 1px solid var(--line); border-radius: 6px;
    padding: 6px 8px; font-size: 12px; max-width: 320px; color: var(--ink);
  }

  /* ── Problem panel (click a type node) ─────────────────────────────────── */
  #prob {
    position: fixed; top: 48px; right: 0; bottom: 0; width: 380px; z-index: 7;
    display: flex; flex-direction: column;
    background: var(--panel); border-left: 1px solid var(--line);
    box-shadow: -8px 0 24px #0006;
  }
  #prob[hidden] { display: none; }
  .prob-head {
    display: flex; align-items: flex-start; gap: 10px; padding: 14px 14px 10px;
    border-bottom: 1px solid var(--line);
  }
  .prob-head .grow { flex: 1; min-width: 0; }
  .prob-title { font-size: 15px; font-weight: 600; word-break: break-word; }
  .prob-meta { color: var(--muted); font-size: 12px; margin-top: 3px; word-break: break-word; }
  .prob-key { color: var(--type); font-family: ui-monospace, "Cascadia Code", monospace; }
  .prob-close { padding: 4px 9px; line-height: 1; }
  .prob-body { flex: 1; overflow: auto; padding: 16px 14px; }
  .prob-stem {
    font-size: 18px; line-height: 1.5; margin-bottom: 16px;
    display: flex; flex-wrap: wrap; gap: 4px 6px; align-items: baseline;
  }
  .prob-choices { list-style: none; margin: 0; padding: 0;
    display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .prob-choices li {
    border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px;
    font-size: 16px; display: flex; align-items: center; gap: 8px; min-height: 44px;
  }
  .prob-choices li.correct { border-color: var(--good); background: #3fb95018; }
  .prob-choices li .tick { color: var(--good); font-weight: 700; margin-left: auto; }
  .img-ph { color: var(--muted); font-style: italic; }
  /* The figure, at the size you can actually judge it at. White plate because
     the crops come off a white page and would vanish on the dark panel. */
  .prob-fig { flex-basis: 100%; margin: 4px 0 2px; }
  .prob-code { flex-basis: 100%; margin: 4px 0; padding: 6px 8px; background: #f3f5f8; border: 1px solid #d5dae2;
               border-radius: 6px; font: 12px/1.45 ui-monospace, Consolas, monospace; white-space: pre; overflow-x: auto; text-align: left; }
  .prob-fig img {
    display: block; width: 100%; height: auto; border-radius: 6px;
    background: #fff; padding: 8px; border: 1px solid var(--line);
  }
  .prob-fig figcaption {
    color: var(--muted); font-size: 12px; line-height: 1.45; margin-top: 6px;
  }
  .prob-fig .aid { font-family: ui-monospace, "Cascadia Code", monospace; }
  .node .fig { fill: var(--muted); font-size: 11px; }
  .btn.on { border-color: var(--type); color: var(--type); }
  #reviewOnly.on { border-color: var(--review); color: var(--review); }
  .node.review text { fill: var(--review); font-weight: 600; }
  .node .count.review { fill: var(--review); }
  .prob-review { color: var(--review); font-weight: 600; }
  .prob-empty { color: var(--muted); font-style: italic; padding: 8px 0; }
  .prob-foot {
    display: flex; align-items: center; gap: 12px;
    padding: 12px 14px; border-top: 1px solid var(--line);
  }
  .prob-count { color: var(--muted); font-size: 12px; }
  .katex { color: var(--ink); }
</style>
</head>
<body>
  <div id="bar">
    <h1>Curriculum graph</h1>
    <input id="search" type="search" placeholder="ค้นหา หลักสูตร / ชั้น / สาระ / มาตรฐาน / หัวข้อ…" autocomplete="off">
    <button class="btn" id="expand">Expand all</button>
    <button class="btn" id="collapse">Collapse to subjects</button>
    <button class="btn" id="fit">Fit</button>
    <button class="btn" id="figOnly" title="แสดงเฉพาะชุดโจทย์ที่มีรูปประกอบ">🖼 เฉพาะที่มีรูป</button>
    <button class="btn" id="reviewOnly" title="แสดงเฉพาะชุดโจทย์ใหม่ที่รอการตรวจ">🔍 รอตรวจ</button>
    <span class="spacer"></span>
    <div class="legend">
      <span><i class="dot" style="background:var(--subject)"></i>subject</span>
      <span><i class="dot" style="background:var(--course)"></i>course</span>
      <span><i class="dot" style="background:var(--level)"></i>level</span>
      <span><i class="dot" style="background:var(--strand)"></i>strand</span>
      <span><i class="dot" style="background:var(--standard)"></i>standard</span>
      <span><i class="dot" style="background:var(--topic)"></i>topic</span>
      <span><i class="dot" style="background:var(--type)"></i>type</span>
      <span>🖼 มีรูปประกอบ</span>
      <span style="color:var(--review)">🔍 รอตรวจ</span>
    </div>
  </div>

  <div id="wrap">
    <svg id="svg"><g id="scene">
      <g id="links"></g>
      <g id="nodes"></g>
    </g></svg>
  </div>
  <div id="tip"></div>
  <div id="hint">scroll = zoom · drag = pan · click a type = show a problem</div>

  <aside id="prob" hidden>
    <div class="prob-head">
      <div class="grow">
        <div class="prob-title"></div>
        <div class="prob-meta"></div>
      </div>
      <button class="btn prob-close" id="probClose" title="ปิด">✕</button>
    </div>
    <div class="prob-body">
      <div class="prob-stem"></div>
      <ol class="prob-choices"></ol>
      <div class="prob-empty" hidden>ไม่มีตัวอย่างสำหรับชนิดนี้</div>
    </div>
    <div class="prob-foot">
      <button class="btn" id="probRegen">🎲 อีกข้อ</button>
      <span class="prob-count"></span>
    </div>
  </aside>

<script>/*__KATEX_JS__*/</script>
<script>
const ROWS = /*__DATA__*/null;
const ASSETS = /*__ASSETS__*/null;      // asset id → data URI, baked at build time
const SVGNS = "http://www.w3.org/2000/svg";
const COLOR = { subject: "#f0883e", course: "#d29922", level: "#58a6ff",
  strand: "#39c5cf", standard: "#db6dcb", topic: "#3fb950", type: "#bc8cff" };
const COL_X = [40, 270, 500, 730, 960, 1190, 1500];   // left edge per depth
const ROW_H = 26;

let root = null;               // virtual root; its children are subjects
let figOnly = false;           // 🖼 filter: dim everything with no diagram
let reviewOnly = false;        // 🔍 filter: only sets whose review gate is open
const view = { x: 0, y: 0, k: 1 };
const gScene = document.getElementById("scene");
const gLinks = document.getElementById("links");
const gNodes = document.getElementById("nodes");
const tip = document.getElementById("tip");

// ── Build the curriculum tree from the flat catalog ─────────────────────────
function buildTree(rows) {
  const r = { kind: "root", label: "", children: [], _byKey: new Map(), collapsed: false };
  const find = (parent, kind, label) => {
    let n = parent._byKey.get(label);
    if (!n) {
      n = { kind, label, children: [], _byKey: new Map(), collapsed: true };
      parent._byKey.set(label, n);
      parent.children.push(n);
    }
    return n;
  };
  for (const row of rows) {
    const s = find(r, "subject", row.subject);
    const parent = row.subject === "คณิตศาสตร์"
      ? find(s, "course", row.course_type || "ทั่วไป") : s;
    const l = find(parent, "level", row.level);
    const filed = row.subject === "คณิตศาสตร์"
      ? find(find(l, "strand", row.strand || "ไม่ระบุสาระ"),
          "standard", row.standard_code || "ไม่ใช้มาตรฐานแกนกลาง")
      : l;
    const t = find(filed, "topic", row.topic || "ทั่วไป");
    const samples = row.samples || [];
    t.children.push({
      kind: "type", label: row.display_name || row.key, key: row.key,
      topic: row.topic, level: row.level, subject: row.subject,
      course: row.course_type, strand: row.strand, standard: row.standard_code,
      indicators: row.indicator_codes || [],
      params: row.params, samples, review: row.review || null,
      // How many of the baked draws carry a diagram. Not always all of them:
      // a type may show the sheet's figure only for the draws it depicts.
      figs: samples.filter(hasFigure).length,
      children: [], _byKey: new Map(), collapsed: true,
    });
  }
  r.collapsed = false;                 // subjects always visible
  for (const s of r.children) s.collapsed = true;
  return r;
}

function hasFigure(sample) {
  return (sample.stem || []).some((b) => b.kind === "image");
}

// leaf-count of the *whole* subtree, regardless of collapse state
function leafCount(n) {
  if (n.kind === "type") return 1;
  if (!n.children.length) return 1;
  return n.children.reduce((a, c) => a + leafCount(c), 0);
}

// types with a figure anywhere below this node — what the collapsed 🖼 counts
function figTypes(n) {
  if (n.kind === "type") return n.figs > 0 ? 1 : 0;
  return n.children.reduce((a, c) => a + figTypes(c), 0);
}

// Children that survive the current filter. With 530 types on screen, dimming
// the ones without a diagram leaves a wall of grey and the survivors somewhere
// off-viewport — so the 🖼 filter prunes instead.
// types awaiting review anywhere below this node — what the amber 🔍 counts
function reviewTypes(n) {
  if (n.kind === "type") return n.review ? 1 : 0;
  return n.children.reduce((a, c) => a + reviewTypes(c), 0);
}

// The 🖼 and 🔍 filters combine: each prunes what the other left.
function kids(n) {
  return n.children.filter((c) =>
    (!figOnly || figTypes(c) > 0) && (!reviewOnly || reviewTypes(c) > 0));
}
function roots() { return kids(root); }

// ── Layout: x by depth, y packed over currently-visible rows ─────────────────
function layout() {
  let cursor = 0;
  const walk = (n, depth) => {
    n._depth = depth;
    n._x = COL_X[Math.min(depth, COL_X.length - 1)] ?? (depth * 300 + 40);
    const cs = kids(n);
    const open = !n.collapsed && cs.length;
    if (!open) { n._y = cursor * ROW_H; cursor++; return; }
    for (const c of cs) walk(c, depth + 1);
    // center parent against the span of its visible children
    n._y = (cs[0]._y + cs[cs.length - 1]._y) / 2;
  };
  for (const s of roots()) walk(s, 0);         // roots are the subjects
  return cursor;                                // total visible rows
}

function visibleNodes() {
  const out = [];
  const walk = (n, depth) => {
    if (depth >= 0) out.push(n);
    if (!n.collapsed) for (const c of kids(n)) walk(c, depth + 1);
  };
  for (const s of roots()) walk(s, 0);
  return out;
}

function visibleLinks() {
  const out = [];
  const walk = (n) => {
    if (n.collapsed) return;
    for (const c of kids(n)) { out.push([n, c]); walk(c); }
  };
  for (const s of roots()) walk(s);
  return out;
}

// ── Render ───────────────────────────────────────────────────────────────────
function render() {
  layout();
  const nodes = visibleNodes();
  const links = visibleLinks();

  gLinks.textContent = "";
  for (const [a, b] of links) {
    const p = document.createElementNS(SVGNS, "path");
    const x1 = a._x + 12, y1 = a._y, x2 = b._x - 4, y2 = b._y;
    const mx = (x1 + x2) / 2;
    p.setAttribute("d", `M${x1},${y1} C${mx},${y1} ${mx},${y2} ${x2},${y2}`);
    p.setAttribute("class", "link");
    gLinks.appendChild(p);
  }

  gNodes.textContent = "";
  const q = document.getElementById("search").value.trim().toLowerCase();
  for (const n of nodes) {
    const g = document.createElementNS(SVGNS, "g");
    g.setAttribute("class", "node");
    g.setAttribute("transform", `translate(${n._x},${n._y})`);

    const dot = document.createElementNS(SVGNS, "circle");
    dot.setAttribute("r", n.collapsed && n.children.length ? 6 : 4);
    dot.setAttribute("cx", 0); dot.setAttribute("cy", 0);
    dot.setAttribute("fill", COLOR[n.kind] || "#888");
    if (n.collapsed && n.children.length) {
      dot.setAttribute("stroke", "#0e1116"); dot.setAttribute("stroke-width", "2");
    }
    g.appendChild(dot);

    const figs = n.kind === "type" ? n.figs > 0 : figTypes(n) > 0;
    const label = document.createElementNS(SVGNS, "text");
    label.setAttribute("x", 12); label.setAttribute("y", 0);
    label.setAttribute("font-size", n.kind === "subject" ? 14 : 13);
    if (n.kind === "subject") label.setAttribute("font-weight", "600");
    // The badge rides in the label's own text node, so it needs no width
    // measurement — the one thing SVG will not do for you.
    const pending = n.kind === "type" ? (n.review ? 1 : 0) : reviewTypes(n);
    label.textContent = n.kind === "type"
      ? (n.review ? "🔍 " : "") + n.label + (figs ? "  🖼" : "")
      : n.label;
    if (n.kind === "type" && n.review) g.classList.add("review");
    g.appendChild(label);

    if (n.kind !== "type") {
      const c = document.createElementNS(SVGNS, "text");
      c.setAttribute("class", "count");
      c.setAttribute("x", 12 + n.label.length * 8.4 + 8);
      c.setAttribute("y", 1);
      c.textContent = "(" + leafCount(n) + ")" + (figs ? "  🖼" + figTypes(n) : "");
      g.appendChild(c);
      if (pending) {
        // A text node of its own, so only the review count is amber.
        const r = document.createElementNS(SVGNS, "text");
        r.setAttribute("class", "count review");
        r.setAttribute("x", 12 + n.label.length * 8.4 + 8 + c.textContent.length * 6.6 + 10);
        r.setAttribute("y", 1);
        r.textContent = "🔍" + pending;
        g.appendChild(r);
      }
    }

    if (q) {
      const hit = (n.label || "").toLowerCase().includes(q) ||
                  (n.key || "").toLowerCase().includes(q);
      g.classList.add(hit ? "hit" : "dim");
    }
    if (n.kind === "type" && n === probNode) g.classList.add("picked");

    g.addEventListener("click", (e) => {
      e.stopPropagation();
      if (n.kind === "type") openProblem(n); else toggle(n);
    });
    if (n.kind === "type") {
      g.addEventListener("mousemove", (e) => showTip(e, n));
      g.addEventListener("mouseleave", hideTip);
    }
    gNodes.appendChild(g);
  }
  applyView();
}

function toggle(n) {
  if (!n.children.length) return;
  n.collapsed = !n.collapsed;
  render();
}

function setAll(collapsed, repaint = true) {
  const walk = (n, depth) => {
    if (depth >= 0 && n.kind !== "type") n.collapsed = collapsed;
    n.children.forEach((c) => walk(c, depth + 1));
  };
  root.children.forEach((s) => walk(s, 0));
  if (repaint) render();
}

// ── Tooltip for leaf (type) nodes ────────────────────────────────────────────
function showTip(e, n) {
  const params = n.params && Object.keys(n.params).length
    ? "<br>params: " + Object.entries(n.params).map(([k, v]) => k + "=" + v).join(", ")
    : "";
  // n/m, not just "has a figure": a type that illustrates only some of its
  // draws is exactly the case worth looking at.
  const figs = n.figs
    ? `<br><span style="color:#8b949e">🖼 รูปประกอบ</span> ${n.figs}/${n.samples.length} ตัวอย่าง`
    : "";
  tip.innerHTML = `<b>${escapeHtml(n.label)}</b><br>` +
    `<span style="color:#8b949e">key</span> ${escapeHtml(n.key)}<br>` +
    `${escapeHtml(n.subject)} · ${escapeHtml(n.course || "")} · ${escapeHtml(n.level)} · ` +
    `${escapeHtml(n.strand || "")} · ${escapeHtml(n.standard || "")} · ` +
    `${escapeHtml(n.topic || "—")}${params}${figs}` +
    (n.review ? `<br><span style="color:#e3b341">🔍 รอตรวจ · ${escapeHtml(n.review)}</span>` : "");
  tip.style.display = "block";
  tip.style.left = Math.min(e.clientX + 14, innerWidth - 340) + "px";
  tip.style.top = (e.clientY + 14) + "px";
}
function hideTip() { tip.style.display = "none"; }
function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// ── Problem panel: baked samples, 🎲 cycles the pool ─────────────────────────
const prob = document.getElementById("prob");
const probTitle = prob.querySelector(".prob-title");
const probMeta = prob.querySelector(".prob-meta");
const probStem = prob.querySelector(".prob-stem");
const probChoices = prob.querySelector(".prob-choices");
const probEmpty = prob.querySelector(".prob-empty");
const probCount = prob.querySelector(".prob-count");
const probRegen = document.getElementById("probRegen");
let probNode = null, probIdx = 0;

// One content block → DOM: math via KaTeX (raw TeX if KaTeX absent), text as
// text, image as the real picture — baked in as a data URI, with its alt text
// and asset id underneath, because judging a figure means reading both.
function renderBlocks(el, blocks) {
  el.textContent = "";
  for (const b of blocks || []) {
    if (b.kind === "math") {
      const span = document.createElement("span");
      if (window.katex) {
        try { katex.render(b.tex, span, { throwOnError: false }); }
        catch (e) { span.textContent = b.tex; }
      } else { span.textContent = b.tex; }
      el.appendChild(span);
    } else if (b.kind === "text") {
      el.appendChild(document.createTextNode(b.text));
    } else if (b.kind === "image") {
      el.appendChild(figureEl(b));
    } else if (b.kind === "code") {
      // A program as written: monospace, line breaks and indentation kept.
      const pre = document.createElement("pre");
      pre.className = "prob-code";
      pre.textContent = b.code;
      el.appendChild(pre);
    }
  }
}

function figureEl(b) {
  const src = ASSETS && ASSETS[b.asset_id];
  if (!src) {                      // referenced but not on disk at build time
    const span = document.createElement("span");
    span.className = "img-ph";
    span.textContent = "[ไม่พบรูป: " + b.asset_id + "]";
    return span;
  }
  const fig = document.createElement("figure");
  fig.className = "prob-fig";
  const img = document.createElement("img");
  img.src = src;
  img.alt = b.alt || "";
  fig.appendChild(img);
  const cap = document.createElement("figcaption");
  if (b.alt) cap.appendChild(document.createTextNode(b.alt + " · "));
  const aid = document.createElement("span");
  aid.className = "aid";
  aid.textContent = b.asset_id;
  cap.appendChild(aid);
  fig.appendChild(cap);
  return fig;
}

function drawProblem() {
  const n = probNode;
  const paramStr = n.params && Object.keys(n.params).length
    ? "  ·  " + Object.entries(n.params).map(([k, v]) => k + "=" + v).join(", ") : "";
  probTitle.textContent = n.label;
  probMeta.innerHTML = `${escapeHtml(n.subject)} · ${escapeHtml(n.course || "")} · ` +
    `${escapeHtml(n.level)} · ${escapeHtml(n.strand || "")} · ` +
    `${escapeHtml(n.standard || "")} · ${escapeHtml(n.topic || "—")}` +
    `${n.indicators.length ? `<br>${n.indicators.map(escapeHtml).join(" · ")}` : ""}` +
    (n.review ? `<br><span class="prob-review">🔍 รอตรวจ · ${escapeHtml(n.review)}</span>` : "") +
    `<br><span class="prob-key">${escapeHtml(n.key)}</span>` +
    escapeHtml(paramStr);

  const samples = n.samples || [];
  const has = samples.length > 0;
  probEmpty.hidden = has;
  probChoices.hidden = !has;
  probStem.hidden = !has;
  probRegen.disabled = samples.length < 2;
  probCount.textContent = has ? `${(probIdx % samples.length) + 1} / ${samples.length}` : "";
  if (!has) { probStem.textContent = ""; probChoices.textContent = ""; return; }

  const s = samples[probIdx % samples.length];
  renderBlocks(probStem, s.stem);
  probChoices.textContent = "";
  s.choices.forEach((content, i) => {
    const li = document.createElement("li");
    if (i === s.answer) li.classList.add("correct");
    const span = document.createElement("span");
    renderBlocks(span, content);
    li.appendChild(span);
    if (i === s.answer) {
      const tick = document.createElement("span");
      tick.className = "tick"; tick.textContent = "✓";
      li.appendChild(tick);
    }
    probChoices.appendChild(li);
  });
}

function openProblem(n) {
  const same = n === probNode;
  probNode = n;
  probIdx = same ? probIdx + 1 : 0;   // re-click on the open type = regenerate
  prob.hidden = false;
  drawProblem();
  render();                            // repaint to move the .picked highlight
}
function closeProblem() {
  probNode = null; prob.hidden = true; render();
}
probRegen.onclick = () => { if (probNode) { probIdx++; drawProblem(); } };
document.getElementById("probClose").onclick = closeProblem;

// ── Pan / zoom ───────────────────────────────────────────────────────────────
function applyView() {
  gScene.setAttribute("transform",
    `translate(${view.x},${view.y}) scale(${view.k})`);
}
function fit() {
  const rows = layout();
  const wrap = document.getElementById("wrap");
  const W = wrap.clientWidth, H = wrap.clientHeight;
  const contentW = COL_X[COL_X.length - 1] + 340;
  const contentH = Math.max(rows * ROW_H, 1);
  view.k = Math.min(W / contentW, H / contentH, 1.4) * 0.95 || 1;
  view.x = 30;
  view.y = (H - contentH * view.k) / 2 + 10;
  applyView();
}

const wrap = document.getElementById("wrap");
wrap.addEventListener("wheel", (e) => {
  e.preventDefault();
  const rect = wrap.getBoundingClientRect();
  const mx = e.clientX - rect.left, my = e.clientY - rect.top;
  const factor = Math.exp(-e.deltaY * 0.0015);
  const k2 = Math.max(0.15, Math.min(4, view.k * factor));
  view.x = mx - (mx - view.x) * (k2 / view.k);
  view.y = my - (my - view.y) * (k2 / view.k);
  view.k = k2;
  applyView();
}, { passive: false });

let dragging = false, sx = 0, sy = 0, ox = 0, oy = 0;
wrap.addEventListener("mousedown", (e) => {
  dragging = true; sx = e.clientX; sy = e.clientY; ox = view.x; oy = view.y;
  wrap.classList.add("grabbing");
});
window.addEventListener("mousemove", (e) => {
  if (!dragging) return;
  view.x = ox + (e.clientX - sx); view.y = oy + (e.clientY - sy); applyView();
});
window.addEventListener("mouseup", () => {
  dragging = false; wrap.classList.remove("grabbing");
});

document.getElementById("expand").onclick = () => setAll(false);
document.getElementById("collapse").onclick = () => setAll(true);
document.getElementById("fit").onclick = fit;

const figBtn = document.getElementById("figOnly");
figBtn.onclick = () => {
  figOnly = !figOnly;
  figBtn.classList.toggle("on", figOnly);
  // Expanding is the point: the filtered tree is a couple of dozen rows, and
  // leaving it collapsed would hide the very types you turned the filter on for.
  setAll(!figOnly, false);
  render();
  fit();
};
const reviewBtn = document.getElementById("reviewOnly");
reviewBtn.onclick = () => {
  reviewOnly = !reviewOnly;
  reviewBtn.classList.toggle("on", reviewOnly);
  setAll(!reviewOnly, false);          // expanded, for the same reason as 🖼
  render();
  fit();
};
document.getElementById("search").addEventListener("input", render);
window.addEventListener("keydown", (e) => { if (e.key === "Escape") closeProblem(); });

// ── Boot ─────────────────────────────────────────────────────────────────────
root = buildTree(ROWS);
reviewBtn.textContent = `🔍 รอตรวจ (${reviewTypes(root)})`;
reviewBtn.disabled = reviewTypes(root) === 0;
render();
fit();
</script>
</body>
</html>
"""


if __name__ == "__main__":
    main()
