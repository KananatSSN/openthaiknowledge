"""Audit multiple-choice sets for correct-answer length leakage.

The strong-leak rule is intentionally conservative: the correct option must be
uniquely longest, at least eight visible characters longer than every
distractor, and at least 25 percent longer than the longest distractor.

Examples::

    python -X utf8 scripts/audit_answer_length.py --samples 50
    python -X utf8 scripts/audit_answer_length.py --samples 20 --check --max-systemic 90
"""

from __future__ import annotations

import argparse
import re
from collections import Counter
from random import Random

from otk.core import catalog, generate


TEX_COMMAND = re.compile(r"\\[A-Za-z]+")
TEX_LAYOUT = re.compile(r"[{}\s]")


def visible_text(blocks) -> str:
    """Return a stable visible-text proxy for text, math, and media blocks."""
    parts: list[str] = []
    for block in blocks:
        if block.kind == "text":
            parts.append(block.text)
        elif block.kind == "math":
            compact = TEX_LAYOUT.sub("", block.tex)
            parts.append(TEX_COMMAND.sub("§", compact))
        else:
            parts.append(getattr(block, "alt", "") or "ภาพ")
    return " ".join(parts).strip()


def is_strong_length_leak(question) -> bool:
    lengths = [len(visible_text(choice.content)) for choice in question.choices]
    correct = lengths[question.answer]
    distractors = lengths[:question.answer] + lengths[question.answer + 1:]
    longest_wrong = max(distractors, default=0)
    return (
        correct > longest_wrong
        and correct - longest_wrong >= 8
        and correct >= 1.25 * max(longest_wrong, 1)
    )


def audit(samples: int) -> tuple[list[tuple[dict, float]], Counter]:
    results: list[tuple[dict, float]] = []
    subjects: Counter = Counter()
    for index, row in enumerate(catalog()):
        leaks = 0
        for sample in range(samples):
            question = generate(
                row["key"], rng=Random(20260929 + index * 101 + sample),
            )
            leaks += is_strong_length_leak(question)
        rate = leaks / samples
        results.append((row, rate))
        subjects[(row["subject"], "sets")] += 1
        subjects[(row["subject"], "samples")] += samples
        subjects[(row["subject"], "leaks")] += leaks
        subjects[(row["subject"], "systemic")] += rate >= 0.8
    return results, subjects


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=50)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--max-systemic", type=int, default=0)
    args = parser.parse_args()
    if args.samples < 1:
        parser.error("--samples must be at least 1")

    results, subjects = audit(args.samples)
    systemic = [(row, rate) for row, rate in results if rate >= 0.8]
    print(f"Audited {len(results)} sets x {args.samples} samples")
    for subject in sorted({row["subject"] for row, _ in results}):
        total = subjects[(subject, "samples")]
        leak_share = subjects[(subject, "leaks")] / total
        print(
            f"{subject}: strong={leak_share:.1%}; "
            f"systemic={subjects[(subject, 'systemic')]} / "
            f"{subjects[(subject, 'sets')]} sets"
        )
    print(f"Systemic sets: {len(systemic)}")
    for row, rate in sorted(systemic, key=lambda item: item[1], reverse=True):
        print(f"{rate:.0%}\t{row['subject']}\t{row['key']}")

    if args.check and len(systemic) > args.max_systemic:
        raise SystemExit(
            f"answer-length audit failed: {len(systemic)} systemic sets exceeds "
            f"limit {args.max_systemic}"
        )


if __name__ == "__main__":
    main()
