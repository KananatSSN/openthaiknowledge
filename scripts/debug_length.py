"""Print the draws where the answer is visibly the longest or shortest choice.

    python scripts/debug_length.py KEY [KEY ...]

Each distinct flagged answer is shown once with every choice and its visible
length, so the rows to rewrite can be found without reading the whole bank.
"""
import sys
from collections import Counter
from random import Random

sys.path.insert(0, ".")
from otk.core.distractors import visible_length  # noqa: E402
from otk.core.registry import generate  # noqa: E402
from scripts.audit_answer_length import visible_text  # noqa: E402
from scripts.audit_mcq_cues import stands_out  # noqa: E402

for key in sys.argv[1:]:
    seen: Counter = Counter()
    print(f"== {key}")
    for sample in range(60):
        q = generate(key, rng=Random(7919 * sample + 17))
        lengths = [visible_length(c.content) for c in q.choices]
        cue = stands_out(lengths, q.answer)
        if cue not in ("longest", "shortest"):
            continue
        texts = [visible_text(c.content) for c in q.choices]
        head = texts[q.answer]
        seen[head] += 1
        if seen[head] > 1 or len(seen) > 4:
            continue
        print(f"  [{cue}] {lengths[q.answer]:3} {head}")
        for i, t in enumerate(texts):
            if i != q.answer:
                print(f"         {lengths[i]:3} {t}")
    print(f"  {sum(seen.values())}/60 draws")
