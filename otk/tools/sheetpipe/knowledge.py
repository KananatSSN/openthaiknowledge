"""Stage 3: the knowledge a sheet teaches, as data.

A **knowledge unit** is one thing a student has to know or be able to do to
answer a sheet's questions: a formula, a procedure, a concept, or a fact list.
Units are authored (by a person or an agent) from the converted digests, and
they are the bridge between sheets and generators. Stage 4 diffs them against
the registry to find what has no problem set yet, and stage 5 builds the
missing sets from them.

Units live in ``otk/knowledge/<subject>/<topic>.json``, one file per topic::

    {"subject": "คณิตศาสตร์", "topic": "ความน่าจะเป็น", "level": "ม.5",
     "units": [ {unit}, … ]}

A unit::

    id             "math.probability.classical" — stable, dotted, unique
    kind           formula | procedure | concept | fact-list
    title          Thai, short
    statement      Thai + plain math: what is true / what to do
    level          overrides the file's level when the unit sits elsewhere
    variables      formula: [{"symbol", "meaning", "unit"?}]
    steps          procedure: ["…", …]
    facts          fact-list: {"category": ["member", …], …}
    prerequisites  unit ids this one builds on
    sources        questions that exercise it. A question is named by its
                   exam tag when it has one, which is stable across the many
                   compilations that repeat it:
                   {"tag": "O-NET (มี.ค. 2561/31)"}. Otherwise by position:
                   {"sheet": "<bank path>", "item": 3}, or a whole exercise
                   section of an answer-key digest:
                   {"sheet": "<bank path>", "section": "สูตรผลบวกผลต่างมุม"},
                   or one numbered exercise of it with its sub-items:
                   {"sheet": "<bank path>", "section": "แบบฝึกหัดท้ายบท", "number": 9}.
    covered_by     registry keys of problem sets that already practise it
    new_topic      true if ``topic`` is not a registry topic yet
    note           caveats: a wrong printed key, a trap the questions set

``validate`` checks every reference: sources resolve to digest items, the
``covered_by`` keys exist in the registry, prerequisites exist and do not form
a cycle, and each kind carries its own fields.
"""

from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path

from .convert import DIGEST_ROOT

KNOWLEDGE_ROOT = Path(__file__).resolve().parents[2] / "knowledge"
KINDS = ("formula", "procedure", "concept", "fact-list")


@dataclass
class Unit:
    id: str
    kind: str
    title: str
    statement: str
    level: str = ""
    variables: list[dict] = field(default_factory=list)
    steps: list[str] = field(default_factory=list)
    facts: dict[str, list[str]] = field(default_factory=dict)
    prerequisites: list[str] = field(default_factory=list)
    sources: list[dict] = field(default_factory=list)
    covered_by: list[str] = field(default_factory=list)
    new_topic: bool = False
    note: str = ""


@dataclass
class TopicFile:
    path: Path
    subject: str
    topic: str
    level: str
    units: list[Unit]


def load_file(path: Path) -> TopicFile:
    raw = json.loads(path.read_text("utf-8"))
    units = [Unit(**u) for u in raw.get("units", [])]
    return TopicFile(path, raw["subject"], raw["topic"], raw.get("level", ""), units)


def load_all(root: Path = KNOWLEDGE_ROOT) -> list[TopicFile]:
    return [load_file(p) for p in sorted(root.rglob("*.json"))] if root.is_dir() else []


# ── The bank's questions ─────────────────────────────────────────────────────

@lru_cache(maxsize=1)
def question_index(root: Path = DIGEST_ROOT) -> tuple[dict, dict]:
    """``(by_tag, by_position)`` over every converted digest.

    ``by_tag[tag]`` is the list of ``(bank path, item number)`` where that exam
    question appears. ``by_position[(bank path, item)]`` is the item record.
    """
    by_tag: dict[str, list[tuple[str, int]]] = defaultdict(list)
    by_pos: dict[tuple[str, int], dict] = {}
    for js in sorted(root.rglob("*.json")):
        d = json.loads(js.read_text("utf-8"))
        for it in d["items"]:
            key = (d["source"], it["number"])
            by_pos[key] = it
            if it["tag"]:
                by_tag[it["tag"]].append(key)
    return dict(by_tag), by_pos


def resolve(source: dict) -> list[tuple[str, int]]:
    """Every digest position a source names; empty if it names nothing."""
    by_tag, by_pos = question_index()
    if "tag" in source:
        return list(by_tag.get(source["tag"], []))
    if "section" in source:
        sheet, title = source.get("sheet", ""), source["section"]
        number = str(source.get("number", ""))

        def hit(section: str) -> bool:
            head, _, label = section.rpartition(" ")
            return head == title and (not number or label.split(".")[0] == number)
        return sorted(k for k, it in by_pos.items() if k[0] == sheet and hit(it.get("section", "")))
    key = (source.get("sheet", ""), source.get("item", -1))
    return [key] if key in by_pos else []


# ── Validation ───────────────────────────────────────────────────────────────

def validate(files: list[TopicFile], registry: dict | None = None) -> list[str]:
    """Every problem found, as ``"<file>: <unit>: <problem>"`` lines."""
    if registry is None:
        from otk.core import REGISTRY as registry
    topics = {(q.subject, q.topic) for q in registry.values()}
    problems: list[str] = []
    units: dict[str, Unit] = {}

    for tf in files:
        where = tf.path.name
        for u in tf.units:
            say = lambda msg, u=u: problems.append(f"{where}: {u.id}: {msg}")
            if u.id in units:
                say("duplicate id")
            units[u.id] = u
            if u.kind not in KINDS:
                say(f"unknown kind {u.kind!r}")
            if not (u.title.strip() and u.statement.strip()):
                say("needs a title and a statement")
            if u.kind == "formula" and not u.variables:
                say("a formula names its variables")
            if u.kind == "procedure" and len(u.steps) < 2:
                say("a procedure has at least two steps")
            if u.kind == "fact-list" and len(u.facts) < 2:
                say("a fact list has at least two categories")
            if not u.sources:
                say("no source question")
            for s in u.sources:
                if not resolve(s):
                    say(f"source {s} is not in any digest")
            for key in u.covered_by:
                if key not in registry:
                    say(f"covered_by {key!r} is not a registry key")
            if not u.new_topic and (tf.subject, tf.topic) not in topics:
                say(f"topic {tf.topic!r} is not a registry topic (set new_topic)")

    for u in units.values():
        for p in u.prerequisites:
            if p not in units:
                problems.append(f"{u.id}: prerequisite {p!r} does not exist")
    problems += [f"prerequisite cycle through {c}" for c in _cycles(units)]
    return problems


def _cycles(units: dict[str, Unit]) -> list[str]:
    state: dict[str, int] = {}              # 1 visiting, 2 done
    found: list[str] = []

    def walk(uid: str) -> None:
        state[uid] = 1
        for p in units[uid].prerequisites:
            if p not in units:
                continue
            if state.get(p) == 1:
                found.append(p)
            elif p not in state:
                walk(p)
        state[uid] = 2

    for uid in units:
        if uid not in state:
            walk(uid)
    return found


# ── Stage 4: what has no problem set yet ─────────────────────────────────────

@dataclass
class PlanRow:
    unit: Unit
    topic: str
    level: str
    questions: int                  # distinct bank questions that exercise it
    status: str                     # covered | uncovered
    candidates: list[str]           # same-topic registry keys to check by hand


def plan(files: list[TopicFile], registry: dict | None = None) -> list[PlanRow]:
    """Every unit with its coverage status, the most-exercised gaps first.

    A unit is ``covered`` when an author has named the problem sets that
    practise it (``covered_by``). An uncovered unit lists the registry types
    filed under the same subject and topic. They are candidates to check
    before building anything new, since a match may exist under another
    name.
    """
    if registry is None:
        from otk.core import REGISTRY as registry
    by_topic: dict[tuple[str, str], list[str]] = defaultdict(list)
    for key, q in registry.items():
        by_topic[(q.subject, q.topic)].append(key)

    def rank(key: str, level: str) -> tuple:
        # School types first, nearest grade first; types built from an exam
        # sheet (olympiad) last, since they drill one question each.
        q = registry[key]
        lv = q.level.get("th", "") if isinstance(q.level, dict) else str(q.level)
        return (bool(getattr(q, "sheet_id", "")), _grade_gap(lv, level), key)

    rows = []
    for tf in files:
        for u in tf.units:
            level = u.level or tf.level
            questions = len({pos for s in u.sources for pos in _question_ids(s)})
            status = "covered" if u.covered_by else "uncovered"
            cands = [] if u.covered_by else sorted(
                by_topic.get((tf.subject, tf.topic), []), key=lambda k: rank(k, level))
            rows.append(PlanRow(u, tf.topic, level, questions, status, cands))
    rows.sort(key=lambda r: (r.status == "covered", -r.questions, r.unit.id))
    return rows


def _grade_gap(a: str, b: str) -> int:
    """Distance between two grade labels (ป.1 … ม.6); unknown labels sort last."""
    order = [f"ป.{n}" for n in range(1, 7)] + [f"ม.{n}" for n in range(1, 7)]
    if a in order and b in order:
        return abs(order.index(a) - order.index(b))
    return 99


def _question_ids(source: dict) -> list[str]:
    """One id per distinct exam question (its tag), or per position if untagged."""
    if "tag" in source:
        return [source["tag"]] if resolve(source) else []
    return [f"{p}#{n}" for p, n in resolve(source)]


# ── Coverage of the bank ─────────────────────────────────────────────────────

def mapped_positions(files: list[TopicFile]) -> dict[tuple[str, int], list[str]]:
    """Digest position → the unit ids that claim it."""
    out: dict[tuple[str, int], list[str]] = defaultdict(list)
    for tf in files:
        for u in tf.units:
            for s in u.sources:
                for pos in resolve(s):
                    out[pos].append(u.id)
    return out


def sheet_coverage(bank_path: str, files: list[TopicFile]) -> tuple[int, int, list[int]]:
    """``(mapped, total, unmapped item numbers)`` for one converted sheet."""
    _, by_pos = question_index()
    mine = sorted(n for (p, n) in by_pos if p == bank_path)
    mapped = mapped_positions(files)
    missing = [n for n in mine if (bank_path, n) not in mapped]
    return len(mine) - len(missing), len(mine), missing
