"""Build the Phase 5 Wave A content sample sheet for the wave review gate.

The gate asks for a curriculum review and a content sample review. This writes
both into one document: the filing table every set was reviewed under, then every
distinct question template each set can produce, with worked examples and the
correct choice marked.

Deterministic — the same catalog produces the same document, so a reviewer can
re-run it after a change and read the diff rather than the whole sheet again.

    python scripts/dump_wave_a_review.py
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from random import Random

from otk.core import catalog, generate
from otk.core.curriculum_science import SCIENCE_WAVE_KEYS


# How hard to look for templates, and how much of each to show. A set with six
# branches needs a wide sweep to turn all six up; a reviewer needs only a couple
# of examples of each to judge whether the branch is sound.
SEEDS = 400
EXAMPLES_PER_TEMPLATE = 2
EXAMPLES_PER_SET = 12
# A set that already existed before Wave A is shown only so the reviewer can see
# the whole three-stage path in one place; it is not itself up for approval here,
# so one example of each of its templates is enough.
EXAMPLES_PER_EXISTING_SET = 3

SUBJECT_EN = {
    "เคมี": "Chemistry",
    "ฟิสิกส์": "Physics",
    "ชีวะ": "Biology",
    "ธรณีวิทยา": "Earth science",
    "ดาราศาสตร์": "Astronomy",
}
STAGE_EN = {1: "Foundation", 2: "Fluency", 3: "Application"}
STATUS_TH = {
    "exact": "ตรงตัวชี้วัด",
    "standard_scope": "อยู่ในมาตรฐาน แต่แคบหรือกว้างกว่าตัวชี้วัด",
    "additional_outcome": "ผลการเรียนรู้ของรายวิชาเพิ่มเติม",
    "outside_scope": "นอกขอบเขตที่ทบทวน",
}
CHOICE_LABELS = "ABCDEFGH"
BARE_NUMBER = re.compile(r"^[\d.,+-]+$")
DIGITS = re.compile(r"\d+")


def render(blocks) -> str:
    """One content block list as review-sheet markdown.

    A bare numeric answer reads better unwrapped; anything else with TeX in it —
    a nuclide symbol, a formula in a hint — is wrapped so a markdown preview can
    typeset it.
    """
    out: list[str] = []
    for block in blocks:
        if block.kind == "text":
            out.append(block.text)
        elif block.kind == "math":
            tex = block.tex
            out.append(tex if BARE_NUMBER.fullmatch(tex) else f"${tex}$")
        elif block.kind == "image":
            out.append(f"[รูป: {block.alt or block.asset_id}]")
    return " ".join(part for part in out if part)


def template_of(stem: str) -> str:
    """A stem with its numbers masked — two draws of one branch collapse to this."""
    return DIGITS.sub("#", stem)


def sample(key: str, cap: int) -> tuple[list[tuple[str, list[str], int, str]], int]:
    """Worked examples for one set, plus how many distinct templates it has."""
    seen: dict[str, list[tuple[str, list[str], int, str]]] = {}
    order: list[str] = []
    for seed in range(SEEDS):
        question = generate(key, Random(seed))
        stem = render(question.stem)
        template = template_of(stem)
        if template not in seen:
            seen[template] = []
            order.append(template)
        bucket = seen[template]
        if len(bucket) >= EXAMPLES_PER_TEMPLATE:
            continue
        choices = [render(choice.content) for choice in question.choices]
        example = (stem, choices, question.answer, render(question.hint))
        if example not in bucket:
            bucket.append(example)

    examples: list[tuple[str, list[str], int, str]] = []
    # One example of every template first, so a wide set still shows all of its
    # branches before the cap bites; second examples fill whatever room is left.
    for round_index in range(EXAMPLES_PER_TEMPLATE):
        for template in order:
            bucket = seen[template]
            if len(bucket) > round_index and len(examples) < cap:
                examples.append(bucket[round_index])
    return examples, len(order)


def node_sort_key(row: dict) -> tuple:
    return (row["subject"], row["strand_code"], row["standard_code"],
            row["level"], row["unit"])


def build() -> str:
    catalogue = [row for row in catalog() if row["curriculum_node_id"]]
    wave_nodes = {row["curriculum_node_id"] for row in catalogue
                  if row["key"] in SCIENCE_WAVE_KEYS}
    # Whole nodes, not just the new sets. Judging whether Foundation → Fluency →
    # Application rises in demand is impossible if the stage a legacy set supplies
    # is missing from the page.
    rows = [row for row in catalogue if row["curriculum_node_id"] in wave_nodes]
    new = sum(1 for row in rows if row["key"] in SCIENCE_WAVE_KEYS)
    nodes: dict[str, list[dict]] = {}
    for row in rows:
        nodes.setdefault(row["curriculum_node_id"], []).append(row)
    ordered = sorted(nodes.values(), key=lambda group: node_sort_key(group[0]))

    lines: list[str] = [
        "# Phase 5 Wave A — content sample sheet for the wave review gate",
        "",
        f"The {new} sets Phase 5 Wave A added, in the {len(ordered)} curriculum "
        f"topics they complete — together with the {len(rows) - new} sets that "
        "were already filed under those topics, so each three-stage path can be "
        "read end to end. For every set, each distinct question template it can "
        "produce is shown with worked examples and the correct choice marked.",
        "",
        "**ใหม่** in the table marks a set added by Wave A. Those are the ones "
        "up for approval; the rest are shown for context and were approved "
        "earlier.",
        "",
        "Two things are up for approval here:",
        "",
        "1. **Curriculum filing** — the table below. Is each set filed under the "
        "right course, level, standard and indicator, and is its mapping status "
        "honest? `ตรงตัวชี้วัด` claims the set assesses the named indicator; "
        "anything narrower is filed `อยู่ในมาตรฐาน`.",
        "2. **Content** — the samples. Does each item have exactly one defensible "
        "answer, are the wrong choices real misconceptions rather than filler, "
        "and does the Foundation → Fluency → Application progression actually "
        "increase in demand?",
        "",
        "Generated by `scripts/dump_wave_a_review.py`, deterministically: re-run "
        "it after a content change and read the diff.",
        "",
        "## Filing table",
        "",
        "| Topic | Indicator | Set | Stage | Mapping status | |",
        "|---|---|---|---|---|---|",
    ]
    for group in ordered:
        for row in sorted(group, key=lambda item: item["learning_stage"]):
            fresh = "**ใหม่**" if row["key"] in SCIENCE_WAVE_KEYS else ""
            lines.append(
                f"| {row['unit']} | {' · '.join(row['indicator_codes']) or '—'} "
                f"| `{row['key']}` | {row['learning_stage']} "
                f"{row['learning_stage_label']} "
                f"| {STATUS_TH.get(row['mapping_status'], row['mapping_status'])} "
                f"| {fresh} |"
            )
    lines.append("")

    for group in ordered:
        head = group[0]
        subject = SUBJECT_EN.get(head["subject"], head["subject"])
        # The union across the node, not one member's list: a node is a unit, and
        # different sets under it may cite different indicators of the same
        # standard. Per-set codes are in the filing table.
        codes = " · ".join(sorted(
            {code for row in group for code in row["indicator_codes"]}
        )) or "ไม่มีตัวชี้วัด"
        lines += [
            f"## {subject} — {head['unit']} ({codes})",
            "",
            f"{head['course_type']} · {head['level']} · "
            f"{head['strand_code']} {head['standard_code']}",
            "",
        ]
        for row in sorted(group, key=lambda item: item["learning_stage"]):
            fresh = row["key"] in SCIENCE_WAVE_KEYS
            cap = EXAMPLES_PER_SET if fresh else EXAMPLES_PER_EXISTING_SET
            examples, templates = sample(row["key"], cap)
            note = "ใหม่ใน Wave A" if fresh else "มีอยู่เดิม — แสดงไว้เพื่อดูเส้นทาง"
            lines += [
                f"### {row['display_name']}",
                "",
                f"`{row['key']}` — {STAGE_EN[row['learning_stage']]} / "
                f"{row['learning_stage_label']} — {note}",
                "",
            ]
            for index, (stem, choices, answer, hint) in enumerate(examples, 1):
                lines += [f"**{index}.** {stem}", ""]
                for position, choice in enumerate(choices):
                    mark = " **← เฉลย**" if position == answer else ""
                    lines.append(f"- {CHOICE_LABELS[position]}. {choice}{mark}")
                lines.append("")
                if hint:
                    lines += [f"*คำใบ้:* {hint}", ""]
            # "Distinct stems", not "templates": for a set that names an element
            # or a device in the stem, every draw of a different one counts, so
            # the number says how varied the set is rather than how many branches
            # it has. Branch coverage is what the examples above are ordered for.
            lines += [
                f"_{templates} distinct stems in {SEEDS} draws; "
                f"{len(examples)} shown._",
                "",
            ]
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o", "--output", type=Path,
        default=Path("docs/for_admin/SCIENCE_WAVE_A_REVIEW.md"),
    )
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(build(), encoding="utf-8", newline="\n")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
