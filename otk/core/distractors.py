"""Distractor strategies — how a question type invents plausible wrong choices.

In the old app this logic lived inline in the ``/api/practice`` handler: sample
other generated problems, then pad plain-integer answers with neighbouring
values. Here it is a small set of composable strategies *owned by the type*, so
the behaviour travels with the content instead of the transport.

A strategy is a callable:

    strategy(correct, rng, need) -> list[list[Block]]

It returns up to ``need`` distinct distractor choice-contents (each a list of
blocks), none equal to ``correct``. Returning fewer is allowed — low-variety
types (e.g. ``a^0 = 1``) simply yield fewer choices.
"""

from __future__ import annotations

import re
from difflib import SequenceMatcher
from random import Random
from typing import Callable

from .content import Block, math, text

# A choice's content is a list of blocks; a strategy yields several of them.
Content = list[Block]
DistractorStrategy = Callable[[Content, Random, int], list[Content]]


def _key(content: Content) -> tuple:
    """Hashable identity of a choice's content, for de-duping."""
    return tuple((b.kind, getattr(b, "tex", getattr(b, "text", getattr(b, "code", ""))))
                 for b in content)


def combine(*strategies: DistractorStrategy) -> DistractorStrategy:
    """Run strategies in order until ``need`` distinct distractors are found."""
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        out: list[Content] = []
        seen = {_key(correct)}
        for s in strategies:
            # Ask for the full `need`, not the shortfall. A strategy only knows
            # to avoid `correct` — it cannot see what earlier strategies already
            # supplied, so asking for exactly the shortfall lets it hand back a
            # duplicate, which this loop then drops with nothing left to replace
            # it. That is how a combine of combines silently yielded a
            # three-choice question. Over-asking costs a little sampling and
            # makes the shortfall impossible.
            for cand in s(correct, rng, need):
                k = _key(cand)
                if k not in seen:
                    seen.add(k)
                    out.append(cand)
                if len(out) >= need:
                    return out
        return out
    return strategy


def sibling_answers(sample: Callable[[], Content]) -> DistractorStrategy:
    """Distractors are answers of *other* items from the same type.

    ``sample()`` returns a fresh correct-answer content (the type wires this to
    its own generation), or None when it found no suitable sibling this time.
    Mirrors the old app's default distractor source.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        out: list[Content] = []
        seen = {_key(correct)}
        for _ in range(30):                        # sampling is cheap; bound it
            if len(out) >= need:
                break
            cand = sample()
            if cand is None:
                continue
            k = _key(cand)
            if k not in seen:
                seen.add(k)
                out.append(cand)
        return out
    return strategy


def numeric_neighbors(offsets=(1, -1, 2, -2, 3, -3)) -> DistractorStrategy:
    """Pad an integer answer with nearby integers. No-op for non-integers.

    Salvages low-variety numeric types that can't produce 4 distinct answers.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        if len(correct) != 1 or not isinstance(getattr(correct[0], "tex", None), str):
            return []
        tex = correct[0].tex
        if not re.fullmatch(r"-?\d+", tex):
            return []
        v = int(tex)
        return [[math(str(v + d))] for d in offsets][:need]
    return strategy


def fixed(*contents: Content) -> DistractorStrategy:
    """Hand-picked distractors, offered before any sampled ones.

    Each argument is a full choice-content (a list of blocks). Used by types that
    know the specific wrong answers worth offering — a physics item's classic
    miscalculations, say — with ``combine`` falling back to sampling for the rest.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        # Filter *before* slicing. A hand-picked list often names the same wrong
        # answer twice (two different mistakes that coincide for these numbers),
        # or names one that happens to equal the correct answer; taking the
        # first ``need`` blind would spend a choice slot on it and silently
        # yield a three-choice question.
        out: list[Content] = []
        seen = {_key(correct)}
        for cand in contents:
            k = _key(cand)
            if k not in seen:
                seen.add(k)
                out.append(cand)
            if len(out) >= need:
                break
        return out
    return strategy


def redraw_until_full(need: int = 3):
    """Decorate a ``build`` whose named mistakes can coincide: redraw until ``need``
    distinct wrong answers survive.

    A set built from ``fixed`` mistakes offers fewer than four choices on the
    rare draw where two mistakes give the same value (or one gives the answer).
    Redrawing keeps every draw that was already full exactly as it was.
    """
    def decorate(build):
        def wrapped(self, rng: Random):
            while True:
                q = build(self, rng)
                if len(q.distractors(q.correct, Random(0), need)) >= need:
                    return q
        wrapped.__name__, wrapped.__doc__ = build.__name__, build.__doc__
        return wrapped
    return decorate


def label_pool(labels: list[str]) -> DistractorStrategy:
    """Distractors are other labels from a fixed pool (Thai text).

    The strategy for labelled-diagram (anatomy) questions: wrong choices are
    real part names, just not the one the arrow points at.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        correct_key = _key(correct)
        pool = [[text(lbl)] for lbl in labels if _key([text(lbl)]) != correct_key]
        rng.shuffle(pool)
        return pool[:need]
    return strategy


def length_matched_label_pool(labels: list[str]) -> DistractorStrategy:
    """Prefer authored prose distractors close to the correct answer's length.

    This is intended for scenario banks that can offer more than three valid
    alternatives.  It avoids making a detailed correct explanation stand out
    beside three terse misconceptions while retaining seeded variety between
    candidates of equal distance.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        correct_key = _key(correct)
        pool: list[Content] = []
        seen = {correct_key}
        for label in labels:
            candidate = [text(label)]
            key = _key(candidate)
            if key not in seen:
                seen.add(key)
                pool.append(candidate)
        rng.shuffle(pool)
        if len(correct) == 1 and isinstance(getattr(correct[0], "text", None), str):
            target = len(correct[0].text)
            comparable = [
                candidate for candidate in pool
                if len(candidate[0].text) > target / 1.25
            ]
            anchor = comparable[0] if comparable else min(
                pool,
                key=lambda candidate: abs(len(candidate[0].text) - target),
                default=None,
            )
            if anchor is not None:
                pool.remove(anchor)
                # One comparable option is enough to remove the visual cue.
                # Keep the other slots random so widened banks retain their
                # authored distractor variety across seeds.
                return [anchor, *pool[:max(need - 1, 0)]]
        return pool[:need]
    return strategy


_PLAIN_NUMBER = re.compile(r"(-?)(\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d+))?(\D.*)?")


def _plain_number(content: Content) -> tuple[float, int, bool, str] | None:
    """Parse a one-block choice that is a number, optionally with a unit after it."""
    if len(content) != 1:
        return None
    raw = getattr(content[0], "tex", getattr(content[0], "text", None))
    if not isinstance(raw, str):
        return None
    m = _PLAIN_NUMBER.fullmatch(raw.strip().replace("{,}", ","))
    if not m:
        return None
    sign, whole, frac, unit = m.groups()
    # A suffix holding another number is an expression (3x + 1), not a unit.
    if unit and re.search(r"\d", unit.replace(r"^{\circ}", "")):
        return None
    value = float(f"{sign}{whole.replace(',', '')}.{frac or '0'}")
    return value, len(frac or ""), "," in whole, unit or ""


def _raw(content: Content) -> str:
    return " ".join(getattr(b, "tex", getattr(b, "text", "")) for b in content)


def _format_number(value: float, places: int, commas: bool, unit: str,
                   like: Content, braced: bool = False) -> Content:
    """``braced`` groups thousands as TeX ``{,}``. TeX reads a bare comma as
    punctuation and spaces after it, so a plain "6,100,000" beside a braced
    "6{,}000{,}000" would set the invented choice visibly apart."""
    body = (f"{value:,.{places}f}" if commas else f"{value:.{places}f}") + unit
    if commas and braced:
        body = body.replace(",", "{,}")
    return [math(body)] if like[0].kind == "math" else [text(body)]


def rank_balanced(inner: DistractorStrategy, *, invent: bool = False) -> DistractorStrategy:
    """Stop the correct number's size order from giving it away.

    Hand-picked mistakes usually err in one direction (adding instead of
    subtracting always overshoots), so the correct value sat at the same rank
    among the sorted choices draw after draw and "pick the smallest" beat
    the mathematics. For a numeric answer (optionally with a unit) this draws
    how many distractors fall below it and fills each side from ``inner``'s
    candidates in their authored order, after the first (most diagnostic) one,
    which is always kept. Anything else passes through unchanged.

    ``invent`` also tops a short side up with near values spaced to the
    answer's size. Only a computed answer may do that: where the choices are
    the stem's own numbers ("which is largest"), an invented one could be right.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        pool = inner(correct, rng, need + 6)
        target = _plain_number(correct)
        parsed = [_plain_number(c) for c in pool]
        # Spares past the ones offered by default may be another shape (a
        # fraction beside whole numbers); leaving them out keeps the set
        # balanced instead of passing every choice through in authored order.
        if (target is not None and 1 <= need <= len(pool)
                and all(p is not None for p in parsed[:need])):
            pool = [c for c, p in zip(pool, parsed) if p is not None]
            parsed = [p for p in parsed if p is not None]
        # A candidate worth the same as the answer ("26.50" beside "26.5") means
        # the item tests notation, not size: leave its choices alone.
        if (target is None or need < 1 or any(p is None for p in parsed)
                or any(p[3] != target[3] or p[0] == target[0] for p in parsed)):
            return pool[:need]
        value = target[0]
        if not pool:
            return pool
        # Keep to the sign range the set itself uses. Fallback candidates (a
        # neighbour of 0 is -1, of 1 is 0) used to be reached only on a
        # shortfall; drawing from them freely must not bring a negative count or
        # a zero divisor beside answers and authored mistakes that avoid them.
        lowest = _lowest_allowed(value, parsed[:need])
        kept = [(c, p) for c, p in zip(pool, parsed) if lowest is None or p[0] >= lowest]
        if len(kept) < len(pool):
            pool, parsed = [c for c, _ in kept], [p for _, p in kept]
            if not pool:
                return pool
        # The first candidate is the set's most diagnostic mistake (authored
        # lists put it first); it is always offered, and the rest balance.
        # With only two slots (three-choice Foundation items) pinning it would
        # leave one free slot and the answer's rank all but fixed, so there it
        # just leads its side and is offered two draws in three.
        pinned = [pool[0]] if need >= 3 else []
        free = need - len(pinned)
        rest, rest_parsed = pool[len(pinned):], parsed[len(pinned):]
        below = [c for c, p in zip(rest, rest_parsed) if p[0] < value]
        above = [c for c, p in zip(rest, rest_parsed) if p[0] > value]
        if invent:
            _top_up(below, above, correct, pool, parsed, rng, need)
        wanted_below = rng.randint(0, free)
        out = [*pinned, *below[:wanted_below], *above[:free - wanted_below]]
        # One side ran dry (an answer of 0 has nothing below): fill from the other.
        for c in below[wanted_below:] + above[free - wanted_below:]:
            if len(out) >= need:
                break
            out.append(c)
        # A spare from the same side of the answer keeps its rank; offering
        # one stops the answer being the choice the others all resemble.
        spare = [c for c in below + above if c not in out]
        return _break_convergence(correct, out, spare, need, rng, keep_side=value)
    strategy.balanced = True
    return strategy


def _lowest_allowed(value: float, parsed) -> float | None:
    """The smallest value a candidate may take: above zero when the answer and
    the authored mistakes are all positive, zero when all are non-negative."""
    if value > 0 and all(p[0] > 0 for p in parsed):
        return min(10.0 ** -6, value)
    if value >= 0 and all(p[0] >= 0 for p in parsed):
        return 0.0
    return None


def _top_up(below, above, correct, pool, parsed, rng, need) -> None:
    value, places, commas, unit = _plain_number(correct)
    commas = commas or any(p[2] for p in parsed)
    # Group the way the choices beside it do: the answer, or failing that the
    # candidates that made grouping necessary in the first place.
    braced = any("{,}" in _raw(c) for c in (correct, *pool))
    # Counts stay counts: never invent a negative (or, beside positive
    # choices, a zero) that the set itself would not offer.
    floor = _lowest_allowed(value, parsed)
    # A step of one beside 1,836 (1,835) marks the pair as "the answer and its
    # decoy"; step at the answer's second significant digit instead.
    magnitude = 10.0 ** (len(str(int(abs(value)))) - 2) if abs(value) >= 1 else 0.0
    step = max(10.0 ** -places, magnitude)
    seen = {_key(correct), *(_key(c) for c in pool)}
    offsets = list(range(1, 6))
    rng.shuffle(offsets)
    for d in offsets:
        for side, candidate in ((below, value - d * step), (above, value + d * step)):
            if len(side) >= need or (side is below and floor is not None and candidate < floor):
                continue
            content = _format_number(candidate, places, commas, unit, correct, braced)
            if _key(content) not in seen:
                seen.add(_key(content))
                side.append(content)


_TEX_COMMAND = re.compile(r"\\[A-Za-z]+")
_TEX_LAYOUT = re.compile(r"[{}\s]")


def visible_length(content: Content) -> int:
    """Roughly how long a choice looks: text as written, TeX with each command
    counted as one glyph, and a picture by its alt text."""
    total = 0
    for block in content:
        if block.kind == "text":
            total += len(block.text.strip())
        elif block.kind == "math":
            total += len(_TEX_COMMAND.sub("§", _TEX_LAYOUT.sub("", block.tex)))
        else:
            total += len(getattr(block, "alt", "") or getattr(block, "code", "") or "ภาพ")
    return total


def _length_gap(size: int) -> float:
    """How far apart two lengths must be before the difference shows: 10% of
    the answer's length, and at least three characters. The audit's
    ``stands_out`` uses the same rule."""
    return max(3, 0.1 * size)


def _is_prose(content: Content) -> bool:
    return bool(content) and all(block.kind == "text" for block in content)


def near_length_sample(rng: Random, pool, correct: str, k: int = 3, key=lambda item: item) -> list:
    """``k`` items from ``pool``, one of them the closest in length to ``correct``.

    For choices drawn from a list of names or formulas, where a random draw can
    leave the answer visibly the longest or shortest. ``key`` maps an item to
    the text it will be shown as.
    """
    items = list(pool)
    closest = min(items, key=lambda item: (abs(len(key(item)) - len(correct)), rng.random()))
    rest = [item for item in items if item is not closest]
    return [closest, *rng.sample(rest, k - 1)]


def _visible_text(content: Content) -> str:
    return " ".join(getattr(b, "text", None) or getattr(b, "tex", None) or getattr(b, "alt", "") or ""
                    for b in content)


def _length_cue(correct: Content, chosen: list[Content]) -> bool:
    """The answer is visibly the longest or the shortest of the choices."""
    size = visible_length(correct)
    gap = _length_gap(size)
    lengths = [visible_length(c) for c in chosen]
    return bool(lengths) and (size - max(lengths) >= gap or min(lengths) - size >= gap)


def _is_centre(scores: list[float]) -> bool:
    return scores[0] == max(scores) and scores.count(scores[0]) == 1


def _break_convergence(correct: Content, chosen: list[Content], spare: list[Content],
                       need: int, rng: Random, *, keep_side: float | None = None) -> list[Content]:
    """Swap one distractor for a spare so the answer is not the centre.

    "Pick the choice the others agree on" finds an answer whose every
    distractor alters one part of it. When the chosen set does that and a spare
    exists, one of the swaps that ends it is taken at random. The first
    candidate stays when three or more are chosen, as elsewhere, and a swap
    that would make the answer stand out by length is not taken. Pairwise
    similarity is computed once for the answer and every candidate.

    ``keep_side`` (a numeric answer's value) allows only swaps between
    numbers on the same side of it, so rank balancing is left as it was.
    """
    if len(chosen) < 2 or not spare:
        return chosen
    items = [correct, *chosen, *spare]
    texts = [_visible_text(c) for c in items]
    size = len(items)
    sim = [[0.0] * size for _ in range(size)]
    for i in range(size):
        for j in range(i + 1, size):
            sim[i][j] = sim[j][i] = SequenceMatcher(None, texts[i], texts[j]).ratio()

    def centre(members: list[int]) -> bool:
        group = [0, *members]
        scores = [round(sum(sim[a][b] for b in group if b != a), 6) for a in group]
        return _is_centre(scores)

    base = list(range(1, len(chosen) + 1))
    if not centre(base):
        return chosen
    spare_ids = range(len(chosen) + 1, size)
    options = []
    def below(i: int) -> bool:
        return _plain_number(items[i])[0] < keep_side

    for slot in range(1 if need >= 3 else 0, len(chosen)):
        for s in spare_ids:
            if keep_side is not None and below(s) != below(base[slot]):
                continue
            members = [*base[:slot], s, *base[slot + 1:]]
            if not centre(members) and not _length_cue(correct, [items[m] for m in members]):
                options.append(members)
    if not options:
        return chosen
    return [items[m] for m in rng.choice(options)]


# An edit that adds or drops a negation can cancel another one out; two such
# slips together may read true again, so they are never combined.
_NEGATIONS = ("ไม่", "not ", "no ", "never")


def _words(text_: str) -> list[str]:
    """The answer's units with their separators kept, so joining gives the text
    back: the parts of a " / " line (a matching, a many-part explanation), or
    else space-separated words."""
    if " / " in text_:
        return [u for u in re.split(r"( / )", text_) if u]
    return re.findall(r"\S+|\s+", text_)


def _one_edit(correct: list[str], wrong: list[str], *,
              parts: bool = False) -> list[tuple[int, int, list[str]]] | None:
    """The units of ``correct`` that ``wrong`` changes, as (start, end, new units).

    Whole units only: splicing inside a word ("ไขสันหลัง" and "สมองส่วนหน้า"
    giving "ไขสันหน้า") makes words that do not exist. A swap of two matched
    pairs stays two separate changes, so it can combine with another swap."""
    ops = [(i1, i2, wrong[j1:j2])
           for tag, i1, i2, j1, j2 in SequenceMatcher(None, correct, wrong, autojunk=False).get_opcodes()
           if tag != "equal"]
    if not ops:
        return None
    changed = "".join("".join(correct[a:b]) + "".join(new) for a, b, new in ops)
    # A slip changes a part, not most of the answer (that is another answer).
    # A negation cannot cancel across the parts of a " / " line: each part is
    # judged on its own.
    if sum(b - a for a, b, _ in ops) > len(correct) * 0.4 or (
            not parts and any(n in changed for n in _NEGATIONS)):
        return None
    return ops


def _same_proportion(answer: str, other: str) -> bool:
    """Every number scaled by one factor ("O 368 กรัม กับ S 368 กรัม" beside
    "O 184 กรัม กับ S 184 กรัม"): where the answer is a proportion, still right."""
    first = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", answer)]
    second = [float(n) for n in re.findall(r"\d+(?:\.\d+)?", other)]
    if len(first) < 2 or len(first) != len(second) or 0 in first:
        return False
    ratios = {round(b / a, 6) for a, b in zip(first, second)}
    # Unchanged numbers (a factor of 1) mean the slips were in the words.
    return len(ratios) == 1 and ratios != {1.0}


def _double_slips(correct: Content, chosen: list[Content]) -> list[Content]:
    """Wrong choices that make two of the chosen slips at once.

    When every distractor alters one part of the answer (group but not period,
    period but not group), the answer is the choice the others agree on. Two
    slips applied together differ from it in two parts, so offering one breaks
    the tie. Each part reads exactly as it does in the authored wrong it came
    from; edits that overlap, touch, or add or drop a negation are not combined.
    """
    if len(correct) != 1 or getattr(correct[0], "kind", None) != "text":
        return []
    if any(len(c) != 1 or getattr(c[0], "kind", None) != "text" for c in chosen):
        return []
    source = correct[0].text
    # Two slips can cancel into an equivalent answer: short answers ("1 : 1"
    # to "2 : 2"), ratios, powers of ten (a ×10 mantissa and a ÷10 exponent),
    # and routes or code, where another order or expression can still work.
    if (len(source.split()) < 3 or len(source) < 15
            or re.fullmatch(r"[\d\s:.]+", source)
            or "× 10" in source
            or any(ch in source for ch in "←↑↓=") or "ทำซ้ำ" in source):
        return []
    answer = _words(source)
    tokens = sorted(source.split())
    # In a matching ("ก → จ / ข → ค") or a sequence ("ค → ง → ข") the order is
    # the content, so a reordering of the answer's words there is simply wrong.
    ordered_free = " / " not in source and " → " not in source
    edits = [e for e in (_one_edit(answer, _words(c[0].text), parts=" / " in source)
                         for c in chosen) if e]
    # In running prose two flips can cancel into a true statement ("shorter,
    # faster, higher" slipped twice reads "longer, slower, lower"; xylem and
    # "outer" both swapped). Parts of a " / " line are judged one by one, and a
    # matching or sequence is wrong in any other order; elsewhere only changes
    # to numbers are combined.
    if ordered_free:
        edits = [e for e in edits
                 if all(re.search(r"[0-9]", w) for a, b, new in e
                        for w in (*answer[a:b], *new) if not w.isspace())]
    seen = {source, *(c[0].text for c in chosen)}
    out = []
    for i, first in enumerate(edits):
        for second in edits[i + 1:]:
            ops = sorted(first + second, key=lambda op: op[0])
            if any(ops[k][1] >= ops[k + 1][0] for k in range(len(ops) - 1)):
                continue
            units, at = [], 0
            for a, b, new in ops:
                units += answer[at:a] + new
                at = b
            combined = "".join(units + answer[at:])
            # The answer's own words reordered ("48 × 56" for "56 × 48").
            if ordered_free and sorted(combined.split()) == tokens:
                continue
            # A sequence that repeats a step ("แมกมา → หินแปร → หินแปร").
            steps = combined.split(" → ")
            if len(steps) > 2 and len(set(steps)) < len(steps):
                continue
            if combined not in seen and not _same_proportion(source, combined):
                seen.add(combined)
                out.append([text(combined)])
    return out


def _unconverge_prose(correct: Content, chosen: list[Content], spare: list[Content],
                      need: int, rng: Random) -> list[Content]:
    """The convergence breaker with authored spares first, then double slips."""
    out = _break_convergence(correct, chosen, spare, need, rng)
    if out is chosen:
        doubles = _double_slips(correct, chosen)
        if doubles:
            out = _break_convergence(correct, chosen, doubles, need, rng)
    return out


def length_balanced(inner: DistractorStrategy) -> DistractorStrategy:
    """Stop the correct choice from being the odd one out by length.

    When the chosen distractors are all visibly shorter than the answer (or
    all visibly longer) and the strategy has a spare that is not, the spare
    replaces the chosen one furthest from the answer's length. The first
    candidate stays when three or more are chosen: it is the authored, most
    diagnostic mistake. A bank with no such spare is left alone; the audit's
    ``longest`` flag lists those for rewriting.
    """
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        pool = inner(correct, rng, need + 6)
        chosen, spare = pool[:need], pool[need:]
        # Prose only. Math choices are often the stem's own values ("which of
        # these four fractions is largest"), where a spare would not belong.
        if len(chosen) < 2 or not all(_is_prose(c) for c in (correct, *pool)):
            return chosen
        if not spare:
            return _unconverge_prose(correct, chosen, [], need, rng)
        size = visible_length(correct)
        gap = _length_gap(size)
        lengths = [visible_length(c) for c in chosen]
        swappable = range(1 if need >= 3 else 0, len(chosen))
        if size - max(lengths) >= gap:
            better = [c for c in spare if visible_length(c) > size - gap]
            out_index = min(swappable, key=lambda i: lengths[i])
        elif min(lengths) - size >= gap:
            better = [c for c in spare if visible_length(c) < size + gap]
            out_index = max(swappable, key=lambda i: lengths[i])
        else:
            return _unconverge_prose(correct, chosen, [c for c in spare if c not in chosen], need, rng)
        if better:
            chosen[out_index] = rng.choice(better)
        return _unconverge_prose(correct, chosen, [c for c in spare if c not in chosen], need, rng)
    strategy.balanced = True
    return strategy


def balanced(inner: DistractorStrategy, *, invent: bool = False) -> DistractorStrategy:
    """The registry's pass over every type's distractors: rank balancing for a
    numeric answer, length balancing for everything else. A strategy a type
    has already balanced (math's ``invent=True``) is used as it is: wrapping it
    again would widen its request and let fallback candidates count as authored.

    ``invent`` comes from the type's ``invent_numbers``: set it where the
    answer is computed, so a near value on the short side cannot be right."""
    if getattr(inner, "balanced", False):
        return inner
    by_rank, by_length = rank_balanced(inner, invent=invent), length_balanced(inner)

    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        if _plain_number(correct) is not None:
            return by_rank(correct, rng, need)
        return by_length(correct, rng, need)
    return strategy


def unconverged(inner: DistractorStrategy) -> DistractorStrategy:
    """Break the convergent cue for a type that opts in (``break_convergence``).

    Math mistakes that each flip one sign or constant of the answer make it
    the choice the others agree on. Balanced math strategies skip the prose
    breaker, so this asks ``inner`` for spares (answers from sibling draws)
    and lets ``_break_convergence`` swap one in. A numeric answer is left to
    rank balancing, which a swap would undo."""
    def strategy(correct: Content, rng: Random, need: int) -> list[Content]:
        chosen = inner(correct, rng, need)
        if _plain_number(correct) is not None:
            return chosen
        taken = {_key(correct), *(_key(c) for c in chosen)}
        spare = [c for c in inner(correct, Random(rng.random()), need + 6)
                 if _key(c) not in taken]
        return _break_convergence(correct, chosen, spare, need, rng)
    strategy.balanced = True
    return strategy
