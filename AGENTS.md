# Working in openthaiknowledge

Instructions for coding agents (and the people running them). Read this before
changing anything; `CONTRIBUTING.md` covers the human side of a contribution.

## What this repository is

Thai curriculum problem sets as code. Each set is a Python class registered
under a permanent key that draws a multiple-choice question from a seed: stem,
choices, answer, hint, and the named mistake each wrong choice stands for.
Consumers (TutorRank first) install a tagged release and call `otk.api` only.

Sets live in `otk/sets/<subject>/<level>/<unit>.py`, one file per curriculum
unit; [`otk/sets/INDEX.md`](otk/sets/INDEX.md) says which file holds a key. A
new unit file is imported in its level's `__init__.py`, and after adding sets
run `python -m otk.tools.sets_index` (`test_sets_layout.py` checks both).
Shared authoring tools are in `otk/kit/`.

## Rules that CI enforces

| Rule | Test | When it fails |
|---|---|---|
| Same seed, same question; keys are permanent | `otk/tests/test_golden_draws.py` | Record a new set: `python -m otk.tools.golden_draws --update KEY`. Changing an existing set's draws is a breaking change: only with the maintainer's agreement, noted in the PR. Removing a set: `--retire KEY`. |
| Every set says where it came from | `otk/tests/test_provenance.py` | Add `PROVENANCE = Provenance("original")` (or `"adapted"` with `sources=` citing what it adapts) to the class or module. Import it from `otk.core.provenance`. |
| Set code only computes | `otk/tests/test_set_safety.py` | Only plain maths/stdlib imports; no `open`, `eval`, `exec`, network, files or processes. Do not add `# otk: allow` markers yourself: ask. |
| A set draws fast | same file | Five draws within 10 s. |
| Answers are right | the set's own tests | Compute answers from a solver; check them by an independent route (SymPy, brute force). Never hard-code an answer you did not derive. |
| Choices do not give the answer away | `otk/tests/test_per_set.py` | Distractors are named mistakes, not padding; see `docs/for_admin/MCQ_GUESSABILITY.md`. |

Run before you finish:

```bash
python -m pytest otk/tests -q -n auto      # ~8 min on 8 cores
python -m ruff check otk
```

For a quick loop on one new set, run `test_golden_draws.py`, `test_provenance.py`,
`test_set_safety.py`, `test_per_set.py -k KEY` and the set's own test file.

## Skills

Step-by-step procedures live in `.agents/skills/` (Claude Code also finds them
through `.claude/skills/`):

- `sheet-bank` — digest sources in `sheet_database/` end to end (maintainers only: the bank is a private repository cloned there).
- `sheet-to-generator` — turn one exam paper into per-question generators.
- `sheet-transcriber` — transcribe one picture-maths PDF and verify its answers.

## Boundaries

- Do not change `otk/api.py` without the maintainer: it is the contract with
  every consumer.
- Do not commit source PDFs or text copied from copyrighted material beyond
  what a set needs; cite sources in `PROVENANCE` instead.
- Keep a contribution to one topic or one source, so it can be reviewed.
