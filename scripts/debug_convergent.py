"""Print the draws where the answer is the convergent choice: python scripts/debug_convergent.py KEY [N]"""
import sys
from collections import Counter
from difflib import SequenceMatcher
from random import Random
sys.path.insert(0, ".")
from otk.core.registry import generate
from scripts.audit_answer_length import visible_text

key = sys.argv[1]
shown = Counter()
for sample in range(60):
    q = generate(key, rng=Random(7919 * sample + 17))
    texts = [visible_text(c.content) for c in q.choices]
    sim = [sum(SequenceMatcher(None, t, u).ratio() for j, u in enumerate(texts) if j != i) for i, t in enumerate(texts)]
    best = max(sim)
    if sim.index(best) == q.answer and sim.count(best) == 1:
        head = texts[q.answer][:40]
        shown[head] += 1
        if shown[head] == 1:
            print("*", texts[q.answer], f"{sim[q.answer]:.2f}")
            for i, t in enumerate(texts):
                if i != q.answer:
                    print("  ", t, f"{sim[i]:.2f}")
print(shown.most_common())
