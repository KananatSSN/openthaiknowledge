"""Show sample draws for numeric sets whose answer keeps one sorted position.

    python scripts/debug_rank.py KEY [KEY ...]
"""
import sys
from random import Random

sys.path.insert(0, ".")
from otk.core.registry import generate  # noqa: E402
from scripts.audit_answer_length import visible_text  # noqa: E402
from otk.core.distractors import _plain_number  # noqa: E402

for key in sys.argv[1:]:
    print(f"== {key}")
    shown = 0
    for sample in range(60):
        q = generate(key, rng=Random(7919 * sample + 17))
        nums = [_plain_number(c.content) for c in q.choices]
        if len(nums) < 3 or None in nums:
            continue
        order = sorted(range(len(nums)), key=lambda i: nums[i][0])
        texts = [visible_text(c.content) for c in q.choices]
        print(f"  rank {order.index(q.answer)}: answer {texts[q.answer]!r}  all {[texts[i] for i in order]}")
        shown += 1
        if shown == 3:
            break
