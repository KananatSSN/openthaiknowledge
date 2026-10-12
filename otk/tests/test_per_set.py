"""Every problem set, drawn once and held to every catalog-wide rule.

Generating questions is what the suite spends its time on, and the per-set
rules used to draw their own samples: 300 draws for the content model, 60 for
the choice count, 60 for the length cue, 80 for Thai in TeX, 30 for hints, and
300 more for a science wave's "four distinct choices" or a variety floor. One
test per set now draws :data:`DRAWS` questions once and checks all of them, so
the rules cost one batch of generation instead of up to six. Splitting by set
rather than by rule also keeps a set's draws in one process when CI shards the
suite (see the rootdir ``conftest.py``).

The draws use ``scripts/audit_mcq_cues.py``'s seeds, and the length cue reads
the first 60 of them, so this test and the audit judge a set on the same items.
When it fails, ``python scripts/debug_length.py KEY`` shows the offending
choices; ``docs/for_admin/MCQ_GUESSABILITY.md`` has how banks are fixed.

The rules:

- **Content model.** A valid question with 2–4 choices, an answer index in range,
  no two choices alike, a public projection that hides the answer, and a JSON
  round trip that keeps it. Named mistakes stay out of every dump, line up with
  the choices, and never label the answer. Math choices group thousands one way,
  braced or plain, never both.
- **Choice count.** The counts the set may produce, from
  ``test_choice_counts.expected_counts`` (four is the norm; the module lists
  the deliberate exceptions and why).
- **No Thai in TeX.** A MathBlock is notation only; Thai belongs in a TextBlock.
- **Hints.** Every early IPST mathematics set shows a strategy on every draw.
- **Length cue.** The answer may not be visibly the longest or shortest choice
  in too many draws.
- **Variety floor.** The widened science sets (Wave H) and the technology sets
  offer at least :data:`FLOOR` distinct items (stem plus choices), counted on
  the shared draws and topped up to 1,000 only when those fall short.
"""

from __future__ import annotations

import re
from random import Random

import pytest

from otk.core import REGISTRY, Question, catalog, generate
from otk.core.curriculum_science import SCIENCE_TECHNOLOGY_KEYS, SCIENCE_WAVE_H_KEYS
from otk.core.distractors import visible_length
from otk.tests.test_choice_counts import expected_counts
from scripts.audit_mcq_cues import CUE_MARGIN, LONGEST_LIMIT, SHORTEST_LIMIT, stands_out

DRAWS = 300
CUE_DRAWS = 60      # the audit's own count; fewer lets sampling noise decide
FLOOR = 25

_THAI = re.compile(r"[฀-๿]")
_IPST = {"สสวท. พื้นฐาน", "สสวท. เพิ่มเติม"}
HINTED = frozenset(
    row["key"] for row in catalog()
    if row["subject"] == "คณิตศาสตร์" and row["course_type"] in _IPST
    and row["learning_stage"] in (1, 2)
)
FLOORED = SCIENCE_WAVE_H_KEYS | SCIENCE_TECHNOLOGY_KEYS


def draws(key: str) -> tuple[Question, ...]:
    """The set's sample, seeded as ``scripts/audit_mcq_cues.py`` seeds it."""
    return tuple(generate(key, rng=Random(7919 * sample + 17)) for sample in range(DRAWS))


def _block_text(block) -> str:
    return str(getattr(block, "text", None) or getattr(block, "tex", None) or getattr(block, "asset_id", None) or "")


def _choice_key(choice) -> tuple:
    return tuple((b.kind, getattr(b, "tex", None), getattr(b, "text", None), getattr(b, "asset_id", None))
                 for b in choice.content)


def _choice_text(choice) -> str:
    return " ".join(getattr(b, "text", getattr(b, "tex", "")) for b in choice.content)


_PLAIN_GROUPED = re.compile(r"\d,\d{3}")


def _grouping(choice) -> str | None:
    """How a math choice groups thousands: braced ``{,}``, plain ``,``, or None."""
    tex = " ".join(b.tex for b in choice.content if b.kind == "math")
    if "{,}" in tex:
        return "braced"
    return "plain" if _PLAIN_GROUPED.search(tex) else None


def texts_of(q: Question) -> list[str]:
    return [_choice_text(c) for c in q.choices]


def _signature(q: Question) -> str:
    stem = " ".join(_block_text(b) for b in q.stem)
    return stem + "||" + "|".join(sorted(" ".join(_block_text(b) for b in c.content) for c in q.choices))


@pytest.mark.parametrize("key", sorted(REGISTRY))
def test_set_meets_every_catalog_rule(key):
    sample = draws(key)
    allowed = expected_counts(key)
    counts = set()
    for n, q in enumerate(sample):
        # Content model.
        assert isinstance(q, Question)
        assert 2 <= len(q.choices) <= 4, (key, n)
        assert 0 <= q.answer < len(q.choices), (key, n)
        keys = [_choice_key(c) for c in q.choices]
        assert len(keys) == len(set(keys)), (key, n, "duplicate choices")
        assert "answer" not in q.public().model_dump(), key
        assert Question.model_validate(q.model_dump()).answer == q.answer, (key, n)
        # Named mistakes: server-only, lined up with the choices, never on the answer.
        assert "mistakes" not in q.model_dump() and "mistakes" not in q.public().model_dump(), key
        if q.mistakes:
            assert len(q.mistakes) == len(q.choices), (key, n)
            assert q.mistakes[q.answer] is None, (key, n, "the answer carries a mistake")
        # One way of grouping thousands. TeX spaces after a bare comma, so a braced
        # 6{,}000{,}000 among plain 6,100,000s stands out as the answer.
        styles = {_grouping(c) for c in q.choices} - {None}
        assert len(styles) <= 1, (key, n, "choices group thousands two ways", texts_of(q))
        # Choice count: distinct as text, and a count the set is allowed.
        texts = [_choice_text(c) for c in q.choices]
        assert len(texts) == len(set(texts)), (key, n, texts)
        counts.add(len(texts))
        # No Thai in TeX.
        for block in [*q.stem, *(b for c in q.choices for b in c.content)]:
            if block.kind == "math":
                assert not _THAI.search(block.tex), (key, n, block.tex)
        # Hints.
        if key in HINTED:
            assert q.hint, (key, n, "no hint")
    assert counts <= allowed, (key, sorted(counts), sorted(allowed))

    # Length cue, on the audit's first 60 draws.
    longest = shortest = chance = 0.0
    for q in sample[:CUE_DRAWS]:
        cue = stands_out([visible_length(c.content) for c in q.choices], q.answer)
        longest += cue == "longest"
        shortest += cue == "shortest"
        chance += 1 / len(q.choices)
    longest, shortest, chance = longest / CUE_DRAWS, shortest / CUE_DRAWS, chance / CUE_DRAWS
    assert longest < max(LONGEST_LIMIT, chance + CUE_MARGIN), (key, "longest", longest)
    assert shortest < max(SHORTEST_LIMIT, chance + CUE_MARGIN), (key, "shortest", shortest)

    # Variety floor. A set close to the floor can miss it on 300 draws by luck of
    # the seeds (chem.thermo_polymer_foundation has 26 items; one batch finds
    # 24), so a short count tops up to 1,000 draws before it counts as a failure.
    if key in FLOORED:
        seen = {_signature(q) for q in sample}
        for extra in range(DRAWS, 1000):
            if len(seen) >= FLOOR:
                break
            seen.add(_signature(generate(key, rng=Random(7919 * extra + 17))))
        assert len(seen) >= FLOOR, (key, "variety floor", len(seen))


def test_hinted_and_floored_sets_are_registered():
    """A renamed set must not drop out of the hint or floor rule silently."""
    assert HINTED and HINTED <= set(REGISTRY)
    assert FLOORED <= set(REGISTRY)
