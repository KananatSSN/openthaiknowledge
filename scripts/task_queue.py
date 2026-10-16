"""The open work, as tasks a contributor can claim: one GitHub issue each.

Two sources, both computed from the repository:

* **digest** — a file in the source bank (``otk/sheets/bank.json``) that has
  not been digested yet (no stage, or stopped before ``generated``);
* **indicator** — an official curriculum indicator
  (``docs/curriculum_sources/_md/indicators.jsonl``) that no set practises.
  A catalog code ending in ``/*`` (``ค 1.3 ม.1/*``) covers every indicator of
  that standard and level. Indicators multiple choice cannot assess
  (``otk/core/indicator_exclusions.py``) are left out.

    python scripts/task_queue.py                 # list the tasks
    python scripts/task_queue.py --json          # one JSON object per task
    python scripts/task_queue.py --create-issues # open an issue per new task (needs gh)

``--create-issues`` skips tasks whose title an issue (open or closed) already
has, so it is safe to re-run after the catalog grows.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict, dataclass
from pathlib import Path

from otk.api import catalog
from otk.core.indicator_exclusions import NOT_ASSESSABLE_BY_MCQ

ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "otk" / "sheets" / "bank.json"
INDICATORS = ROOT / "docs" / "curriculum_sources" / "_md" / "indicators.jsonl"
DONE = {"generated", "green", "ignored"}
# The additional-mathematics sets carry no indicator codes yet, so these
# indicators may well be practised already: say so rather than invite a duplicate.
UNMAPPED_PREFIX = "ค เพิ่มเติม"
UNMAPPED_NOTE = ("**Check first:** the additional-mathematics sets carry no indicator codes"
                 " yet, so an existing set may already practise this. If one does, map it"
                 " (`indicator_codes` in `otk/core/curriculum_math.py`) instead.\n\n")
SUBJECT_LABEL = {"math": "คณิตศาสตร์", "science": "วิทยาศาสตร์"}


@dataclass(frozen=True)
class Task:
    kind: str     # "digest" | "indicator"
    title: str
    body: str
    label: str


def digest_tasks() -> list[Task]:
    tasks = []
    for entry in json.loads(BANK.read_text("utf-8"))["entries"]:
        if entry.get("stage") in DONE:
            continue
        path = entry["path"]
        stage = entry.get("stage") or "new"
        tasks.append(Task(
            "digest", f"Digest: {path}",
            f"Bank file `openthaiknowledge-bank/{path}` ({entry.get('kind', '?')}, stage `{stage}`)"
            " has not been turned into problem sets yet.\n\n"
            "Follow the `sheet-bank` skill (`.agents/skills/sheet-bank/SKILL.md`). The PDF"
            " itself is in the maintainer's private store: ask on this issue if you"
            " need access.\n\n"
            + (f"Note from the bank: {entry['note']}\n" if entry.get("note") else ""),
            "task: digest"))
    return tasks


def _covered() -> tuple[set[str], set[str]]:
    exact, wildcard = set(), set()
    for row in catalog():
        for code in row.get("indicator_codes") or []:
            (wildcard.add(code[:-1]) if code.endswith("/*") else exact.add(code))
    return exact, wildcard


def indicator_tasks() -> list[Task]:
    exact, wildcard = _covered()
    tasks = []
    for line in INDICATORS.read_text("utf-8").splitlines():
        indicator = json.loads(line)
        code = indicator["code"]
        if code in exact or any(code.startswith(prefix) for prefix in wildcard):
            continue
        if code in NOT_ASSESSABLE_BY_MCQ:
            continue
        subject = SUBJECT_LABEL.get(indicator.get("subject"), indicator.get("subject", ""))
        tasks.append(Task(
            "indicator", f"Problem set for {code}",
            f"No problem set practises the {subject} indicator **{code}** "
            f"({indicator.get('level', '')}):\n\n> {indicator.get('text', '')}\n\n"
            f"Source: `docs/curriculum_sources/{indicator.get('source', '')}`, "
            f"page {indicator.get('page', '?')}.\n\n"
            + (UNMAPPED_NOTE if code.startswith(UNMAPPED_PREFIX) else "")
            + "Write an original set for it (see `AGENTS.md` and `CONTRIBUTING.md`), or"
            " explain on this issue why multiple-choice practice does not fit it.\n",
            "task: indicator"))
    return tasks


def existing_titles() -> set[str]:
    out = subprocess.run(
        ["gh", "issue", "list", "--state", "all", "--limit", "5000", "--json", "title"],
        capture_output=True, text=True, check=True, cwd=ROOT).stdout
    return {issue["title"] for issue in json.loads(out)}


def create_issues(tasks: list[Task]) -> int:
    have = existing_titles()
    for label in {task.label for task in tasks}:
        subprocess.run(["gh", "label", "create", label, "--force"], cwd=ROOT,
                       capture_output=True, check=False)
    created = 0
    for task in tasks:
        if task.title in have:
            continue
        subprocess.run(["gh", "issue", "create", "--title", task.title, "--body", task.body,
                        "--label", task.label], cwd=ROOT, check=True)
        created += 1
    return created


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--json", action="store_true", help="print one JSON object per task")
    parser.add_argument("--create-issues", action="store_true",
                        help="open a GitHub issue for each task that has none yet")
    args = parser.parse_args(argv)

    tasks = digest_tasks() + indicator_tasks()
    if args.create_issues:
        print(f"{create_issues(tasks)} issues created ({len(tasks)} tasks)")
    elif args.json:
        for task in tasks:
            print(json.dumps(asdict(task), ensure_ascii=False))
    else:
        for task in tasks:
            print(f"[{task.kind}] {task.title}")
        print(f"\n{sum(t.kind == 'digest' for t in tasks)} files to digest, "
              f"{sum(t.kind == 'indicator' for t in tasks)} indicators without a set")


if __name__ == "__main__":
    main()
