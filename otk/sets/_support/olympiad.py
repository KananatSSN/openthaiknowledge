"""Olympiad (สอวน.) question types, generated from digested exam sheets.

Every type here is the *second half* of one question of a real exam sheet. The
first half — the mathematics — lives in :mod:`otk.sheets`, one solver module
per question, each carrying an independently cross-checked ``solve()``; see
``otk/tools/sheetpipe`` and ``.agents/skills/sheet-to-generator``.

The split is the point. A type here never re-derives an answer: it draws fresh
constants, hands them to the solver, and spends its own code on the *question* —
Thai wording, exact TeX, and distractors that name the specific mistake the item
is built to catch. So "does this generator give the right answer for constants
nobody has checked?" is answered by
``python -m otk.tools.sheetpipe verify``, not by reading this file.

Two consequences worth knowing when adding to it:

* **Constants come from pools, not free ranges.** Most of these questions are
  only well posed for some constants — an interval collapses, a data set stops
  being unique, a radical stops being writable. The ``_pool_*`` helpers scan a
  small grid once at import and keep the constants that survive, so a generator
  can never emit an item whose answer is ``None``.
* **Solvers are cached.** Several ``solve()`` implementations are searches. They
  are wrapped in ``lru_cache`` and fed from those small pools, so repeated draws
  cost a dictionary lookup.
"""

from __future__ import annotations




# ── TeX helpers ──────────────────────────────────────────────────────────────


# ── Constant pools (built once; only well-posed constants survive) ───────────


# ── ข้อ 1–10 ─────────────────────────────────────────────────────────────────


# ── ข้อ 11–20 ────────────────────────────────────────────────────────────────


# ── ข้อ 21–30 ────────────────────────────────────────────────────────────────


