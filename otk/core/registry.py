"""The question-type registry — the generalization of the old ``@generator``.

A *question type* is a class that knows how to build one item of some kind
(``math.addition``, ``anatomy.skeleton``, …). It carries presentation metadata
(Thai display name, school level) and returns a :class:`GeneratedQuestion` from
:meth:`build`; the base class turns that into a finished, shuffled
:class:`Question`. Types self-register with the :func:`question_type` decorator,
exactly like generators do today.

Tunable parameters are still discovered by introspection: a type exposes the
callable whose numeric-default keyword args are its ranges (``draw`` for math
families), so range controls come for free — no separate metadata.
"""

from __future__ import annotations

import inspect
from abc import ABC, abstractmethod
from random import Random

from .curriculum import curriculum_sort_fields, placement_for
from . import mistakes
from .distractors import balanced, unconverged
from .question import Choice, GeneratedQuestion, Question
from .texfmt import tidy_unit_coefficients

DEFAULT_LANG = "th"
DEFAULT_LEVEL_SYSTEM = "th"
DEFAULT_SUBJECT = "คณิตศาสตร์"          # the platform's home subject
OTHER_LEVEL = "อื่น ๆ"
GENERAL_TOPIC = "ทั่วไป"                # bucket label for types with no topic
MAX_CHOICES = 4

# Ordered levels per system; the catalog groups types in this order.
LEVEL_SYSTEMS: dict[str, list[str]] = {
    "th": ["ป.1", "ป.2", "ป.3", "ป.4", "ป.5", "ป.6",
           "ม.1", "ม.2", "ม.3", "ม.4", "ม.5", "ม.6",
           "แคลคูลัส 1", "แคลคูลัส 2",     # university calculus (after ม.6)
           "เทคนิคคิดเลขเร็ว",
           "โอลิมปิก (สอวน.)"],          # enrichment track, digested exam sheets
}


class QuestionType(ABC):
    """Base class for all question types. Subclasses implement :meth:`build`."""

    key: str = ""
    display_name: dict[str, str] = {}
    level: dict[str, str] = {}
    subject: str = DEFAULT_SUBJECT                  # top of the Subject→Level→Topic→Type nav
    topic: str = ""
    index: int = 0                                 # registration order
    # Set only by types digested from a past paper (otk/sheets/). ``sheet`` is
    # what a learner reads; ``sheet_id`` is the package name under otk/sheets/
    # and is what the practice pool groups on, so a paper stays
    # one thing even though its thirty questions span two dozen หัวข้อ.
    sheet: str = ""
    sheet_id: str = ""
    # Curriculum learning-curve metadata.  Ordinary/non-math types stay at the
    # neutral fluency stage; the IPST expansion assigns 1 -> 2 -> 3 explicitly.
    learning_stage: int = 2
    learning_stage_key: str = "fluency"
    learning_stage_label: dict[str, str] = {"th": "ฝึกคล่อง", "en": "Fluency"}
    # A staged set may reuse a proven generator with different support.  Filing
    # must then follow the source key so historical curriculum overrides survive.
    source_key: str = ""
    curriculum_key: str = ""
    max_choices: int = MAX_CHOICES
    # A computed numeric answer whose authored mistakes all sit on one side:
    # rank balancing may add near values on the other. Never set it where the
    # choices are the stem's own numbers ("which is largest"), since an added
    # value could then be the right one.
    invent_numbers: bool = False
    # Mistakes that each alter one part of a computed answer (a sign, a
    # constant) make it the choice the others agree on: swap in a spare so it
    # is not. Not where the choices are the stem's own values or a sheet's.
    break_convergence: bool = False
    # Shown after answering when the item carries no hint of its own: the
    # strategy for the whole set (see ``types/math_hints.py``).
    stage_hint: tuple = ()

    @abstractmethod
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        """Return the stem, the correct content, and a distractor strategy."""

    # The callable whose numeric-default kwargs are the tunable params.
    # Families that put ranges on a helper (math's ``draw``) override this.
    def _param_fn(self):
        return self.build

    def params(self) -> dict[str, float]:
        out: dict[str, float] = {}
        for p in inspect.signature(self._param_fn()).parameters.values():
            if (p.default is not inspect.Parameter.empty
                    and isinstance(p.default, (int, float))
                    and not isinstance(p.default, bool)):
                out[p.name] = p.default
        return out

    def display_name_for(self, lang: str = DEFAULT_LANG) -> str:
        return self.display_name.get(lang, self.key)

    def level_for(self, system: str = DEFAULT_LEVEL_SYSTEM) -> str:
        return self.level.get(system, OTHER_LEVEL)

    def generate(self, rng: Random, **params) -> Question:
        """Build one item: draw content, materialize distractors, shuffle."""
        # Named mistakes are recorded while the type builds this draw, and only
        # then: a strategy that samples sibling draws for spare choices calls the
        # type again, and those siblings' mistakes are not this question's.
        # Nothing here touches ``rng``, so every draw is the same either way.
        with mistakes.recording() as ledger:
            gq = self.build(rng, **params)
        strategy = balanced(gq.distractors, invent=self.invent_numbers)
        if self.break_convergence:
            strategy = unconverged(strategy)
        distractors = strategy(gq.correct, rng, self.max_choices - 1)
        tidy = _tidy_math if self.subject == DEFAULT_SUBJECT else list
        correct = tidy(gq.correct)
        # Labels are read off the untidied content, which is what the type named.
        labelled = [(correct, None), *((tidy(d), mistakes.label_for(ledger, d)) for d in distractors)]
        contents = [content for content, _ in labelled]
        if gq.order is not None:
            order = sorted(range(len(labelled)), key=lambda i: gq.order(contents[i]))
        else:
            order = list(range(len(labelled)))
            rng.shuffle(order)
        contents = [labelled[i][0] for i in order]
        labels = [labelled[i][1] for i in order]
        placement = placement_for(
            key=self.curriculum_key or self.key, subject=self.subject,
            level=self.level_for(), topic=gq.topic or self.topic,
        )
        return Question(
            type=self.key,
            topic=gq.topic or self.topic,
            level=placement.level,
            stem=tidy(gq.stem),
            choices=[Choice(content=c) for c in contents],
            answer=contents.index(correct),
            mistakes=labels if any(labels) else [],
            hint=tidy(gq.hint or list(self.stage_hint)),
        )


def _tidy_math(blocks) -> list:
    return [b.model_copy(update={"tex": tidy_unit_coefficients(b.tex)})
            if getattr(b, "kind", "") == "math" else b for b in blocks]


REGISTRY: dict[str, QuestionType] = {}


def question_type(key: str, *,
                  display_name: dict[str, str] | None = None,
                  level: dict[str, str] | None = None,
                  subject: str = DEFAULT_SUBJECT,
                  topic: str = ""):
    """Class decorator: register a QuestionType subclass with its metadata."""
    def deco(cls: type[QuestionType]) -> type[QuestionType]:
        cls.key = key
        cls.display_name = dict(display_name or {})
        cls.level = dict(level or {})
        cls.subject = subject
        cls.curriculum_key = key
        if topic:
            cls.topic = topic
        inst = cls()
        inst.index = len(REGISTRY)
        REGISTRY[key] = inst
        return cls
    return deco


def generate(key: str, rng: Random | None = None, **params) -> Question:
    """Convenience: build one question of ``key`` (fresh RNG if none given)."""
    return REGISTRY[key].generate(rng or Random(), **params)


def sort_key(key: str, system: str = DEFAULT_LEVEL_SYSTEM) -> tuple:
    """Order by course, level, strand, topic and stage, then registration order:
    level folders import their unit files alphabetically, and a unit file
    registers its sets in teaching order.

    Unknown types and levels sort last (the catalog's 'อื่น ๆ' bucket).
    """
    levels = LEVEL_SYSTEMS.get(system, [])
    t = REGISTRY.get(key)
    if t is None:
        return (len(levels), len(REGISTRY), key)
    placement = placement_for(
        key=t.curriculum_key or t.key, subject=t.subject,
        level=t.level_for(system), topic=t.topic,
    )
    lv = placement.level
    rank = levels.index(lv) if lv in levels else len(levels)
    course_rank, strand_rank = curriculum_sort_fields(
        placement.course_type, placement.strand_code,
    )
    # Unfiled subjects keep their historical ordering. Any subject with explicit
    # curriculum metadata uses the shared course/grade/strand order.
    if not placement.curriculum_node_id:
        course_rank = strand_rank = 0
    return (course_rank, rank, strand_rank, t.topic, t.learning_stage, t.index, key)


def catalog(system: str = DEFAULT_LEVEL_SYSTEM,
            lang: str = DEFAULT_LANG) -> list[dict]:
    """Metadata for every registered type, ordered for grouped display."""
    out = []
    for key in sorted(REGISTRY, key=lambda k: sort_key(k, system)):
        t = REGISTRY[key]
        placement = placement_for(
            key=t.curriculum_key or key, subject=t.subject,
            level=t.level_for(system), topic=t.topic,
        )
        out.append({
            "key": key,
            "display_name": t.display_name_for(lang),
            "subject": t.subject,
            "level": placement.level,
            "topic": t.topic,
            "params": t.params(),
            "learning_stage": t.learning_stage,
            "learning_stage_key": t.learning_stage_key,
            "learning_stage_label": t.learning_stage_label.get(lang, t.learning_stage_key),
            "source_key": t.source_key or key,
            **placement.catalog_fields(),
        })
    return out


def types_in(subject: str = "", level: str = "", topic: str = "", key: str = "",
             system: str = DEFAULT_LEVEL_SYSTEM) -> list[str]:
    """Every type key under a node of the Subject → Level → Topic → Type tree.

    Each empty field widens the scope, so ``types_in()`` is the whole platform,
    ``types_in("คณิตศาสตร์", "ม.1")`` is every ชุดโจทย์ in that section, and
    ``key`` narrows to exactly one type. Used by the scoped leaderboards: a rank
    is computed over the solves of every type this returns.

    ``topic=GENERAL_TOPIC`` selects the types that carry no topic of their own —
    the bucket the navigator shows under that name.
    """
    if key:
        return [key] if key in REGISTRY else []
    out = []
    for k in sorted(REGISTRY, key=lambda k: sort_key(k, system)):
        t = REGISTRY[k]
        placement = placement_for(
            key=t.curriculum_key or k, subject=t.subject,
            level=t.level_for(system), topic=t.topic,
        )
        if subject and t.subject != subject:
            continue
        if level and placement.level != level:
            continue
        if topic and (t.topic or GENERAL_TOPIC) != topic:
            continue
        out.append(k)
    return out


def types_in_curriculum_node(node_id: str,
                            system: str = DEFAULT_LEVEL_SYSTEM) -> list[str]:
    """Every type key filed under one curriculum node, in catalog order.

    A curriculum node is narrower than a registry หัวข้อ: กฎของโอห์ม is one node
    inside the ไฟฟ้า topic. Science practice targets the node, so the pool has to
    be addressable by it. Returns [] for an unknown or empty node id rather than
    widening to everything.
    """
    if not node_id:
        return []
    out = []
    for key in sorted(REGISTRY, key=lambda k: sort_key(k, system)):
        t = REGISTRY[key]
        placement = placement_for(
            key=t.curriculum_key or key, subject=t.subject,
            level=t.level_for(system), topic=t.topic,
        )
        if placement.curriculum_node_id == node_id:
            out.append(key)
    return out


def topics_in(subject: str = "", level: str = "",
              system: str = DEFAULT_LEVEL_SYSTEM) -> list[str]:
    """Ordered, unique topics under a Subject → Level node (catalog order).

    Types with no topic fall into the ``GENERAL_TOPIC`` bucket. Used by the
    mastery board, which aggregates the per-หัวข้อ ratings of a whole ระดับชั้น.
    """
    out: list[str] = []
    for k in types_in(subject=subject, level=level, system=system):
        t = REGISTRY[k].topic or GENERAL_TOPIC
        if t not in out:
            out.append(t)
    return out


def full_level(keys, system: str = DEFAULT_LEVEL_SYSTEM) -> tuple[str, str] | None:
    """``(subject, level)`` if ``keys`` is exactly the complete set of types of a
    single ระดับชั้น, else ``None``.

    This is what marks a practice session as *ranked* (leaderboard-eligible): the
    boards count a solve only when the whole ระดับชั้น was being practised, not a
    hand-picked subset. Selecting the level's "ทั้งระดับชั้น" shortcut produces
    exactly this set; a manual selection of the same complete set qualifies too
    (the server can only trust the set itself, not how it was built).
    """
    ks = set(keys)
    if not ks:
        return None
    sections = set()
    for k in ks:
        t = REGISTRY.get(k)
        if t is None:
            return None
        placement = placement_for(
            key=t.curriculum_key or k, subject=t.subject,
            level=t.level_for(system), topic=t.topic,
        )
        sections.add((t.subject, placement.level))
    if len(sections) != 1:
        return None
    subject, level = next(iter(sections))
    return (subject, level) if ks == set(types_in(subject=subject, level=level,
                                                   system=system)) else None


def search(q: str, system: str = DEFAULT_LEVEL_SYSTEM,
           lang: str = DEFAULT_LANG, limit: int = 12) -> list[dict]:
    """Substring match over display name, topic, subject and level — for the
    Nav auto-suggest. Case-folded; an empty query yields nothing. Results keep
    the catalog's level/registration ordering and share its entry shape.
    """
    needle = q.strip().casefold()
    if not needle:
        return []
    out = []
    for entry in catalog(system, lang):
        hay = " ".join((entry["display_name"], entry["topic"],
                        entry["subject"], entry["level"], entry["course_type"],
                        entry["strand"], entry["standard_code"],
                        " ".join(entry["indicator_codes"]))).casefold()
        if needle in hay:
            out.append(entry)
            if len(out) >= limit:
                break
    return out


def types_in_sheet(sheet_id: str, system: str = DEFAULT_LEVEL_SYSTEM) -> list[str]:
    """Every ชุดโจทย์ digested from one past paper, in catalog order.

    A paper is the one grouping that cuts across the Subject → Level → Topic
    tree: its thirty questions are filed under two dozen different หัวข้อ, but
    the paper is what a learner actually sits down to work through.
    """
    return [k for k in sorted(REGISTRY, key=lambda k: sort_key(k, system))
            if sheet_id and REGISTRY[k].sheet_id == sheet_id]


def sheets(system: str = DEFAULT_LEVEL_SYSTEM) -> list[dict]:
    """The digested past papers, newest first, each with the ชุดโจทย์ it holds."""
    seen: dict[str, dict] = {}
    for k in sorted(REGISTRY, key=lambda k: sort_key(k, system)):
        t = REGISTRY[k]
        if not t.sheet_id:
            continue
        entry = seen.setdefault(t.sheet_id, {
            "sheet_id": t.sheet_id,
            "name": t.sheet or t.sheet_id,
            "subject": t.subject,
            "level": placement_for(
                key=t.curriculum_key or k, subject=t.subject,
                level=t.level_for(system), topic=t.topic,
            ).level,
            "keys": [],
        })
        entry["keys"].append(k)
    return sorted(seen.values(), key=lambda s: s["sheet_id"], reverse=True)
