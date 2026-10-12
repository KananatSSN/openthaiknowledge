"""Three-stage IPST practice coverage built on the verified math generators.

The historical catalog was broad but uneven: many curriculum topics had only
one or two sets.  This module gives every IPST basic/additional topic a complete
Foundation -> Fluency -> Application path.  Existing generators remain the
independent/application tasks.  Missing earlier stages reuse their mathematics
with deliberately different support: fewer plausible choices and an explicit
strategy hint.  This keeps answers and distractors domain-authored rather than
manufacturing generic arithmetic.

The expansion is registered last so it is additive: old keys, saved worksheets,
attempts, and ratings continue to mean exactly what they meant before.
"""

from __future__ import annotations

from collections import defaultdict
from random import Random

from otk.core.content import text
from otk.core.curriculum import placement_for
from otk.core.question import GeneratedQuestion
from otk.core.registry import DEFAULT_SUBJECT, REGISTRY, QuestionType
from otk.sets._support.math_stages import stage_of

STAGES = {
    1: ("foundation", {"th": "ปูพื้นฐาน", "en": "Foundation"}, 2),
    2: ("fluency", {"th": "ฝึกคล่อง", "en": "Fluency"}, 3),
    3: ("application", {"th": "ประยุกต์", "en": "Application"}, 4),
}

# Choices offered by an authored Foundation set. Two would make a guess right
# half the time; three still lowers the load against the four that follow.
FOUNDATION_CHOICES = 3

_FOUNDATION_SIGNALS = (
    "พื้นฐาน", "รู้จัก", "จำแนก", "ระบุ", "อ่าน", "นับ", "ค่า", "ตรง", "ง่าย",
    "basic", "identify", "classify", "read",
)
_APPLICATION_SIGNALS = (
    "โจทย์ปัญหา", "ระคน", "ประยุกต์", "หลายขั้น", "พิสูจน์", "วิเคราะห์",
    "word problem", "mixed", "application", "proof",
)


def _difficulty_signal(spec: QuestionType) -> tuple[int, int, int]:
    """A stable authoring heuristic used only to seed the first stage labels."""
    name = " ".join(spec.display_name.values()).casefold()
    score = sum(term in name for term in _APPLICATION_SIGNALS)
    score -= sum(term in name for term in _FOUNDATION_SIGNALS)
    # More tunable dimensions usually mean more interacting quantities.
    return score, len(spec.params()), spec.index


def _set_stage(spec: QuestionType, stage: int, *, adjust_choices: bool = False) -> None:
    key, label, choices = STAGES[stage]
    spec.learning_stage = stage
    spec.learning_stage_key = key
    spec.learning_stage_label = dict(label)
    if adjust_choices:
        spec.max_choices = choices


class SupportedPracticeSet(QuestionType):
    """A lower-support-load view of an existing, already tested generator."""

    def __init__(self, source: QuestionType, stage: int):
        self.source = source
        self.key = f"math.ipst.{STAGES[stage][0]}.{source.key.removeprefix('math.')}"
        self.source_key = source.key
        self.curriculum_key = source.curriculum_key or source.key
        self.subject = source.subject
        self.level = dict(source.level)
        self.topic = source.topic
        self.sheet = ""
        self.sheet_id = ""
        suffix_th = STAGES[stage][1]["th"]
        suffix_en = STAGES[stage][1]["en"]
        self.display_name = {
            "th": f"{source.display_name_for('th')} ({suffix_th})",
            "en": f"{source.display_name_for('en')} ({suffix_en})",
        }
        _set_stage(self, stage, adjust_choices=True)

    def _param_fn(self):
        return self.source._param_fn()

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        generated = self.source.build(rng, **params)
        if self.learning_stage == 1:
            guidance = (
                f"เริ่มจากระบุสิ่งที่โจทย์กำหนดในเรื่อง{self.topic or 'นี้'} "
                "แล้วทำทีละขั้นก่อนเลือกคำตอบ"
            )
        else:
            guidance = (
                f"วางแผนวิธีทำเรื่อง{self.topic or 'นี้'}ก่อนคำนวณ "
                "แล้วตรวจคำตอบย้อนกลับหนึ่งครั้ง"
            )
        return GeneratedQuestion(
            stem=list(generated.stem),
            correct=list(generated.correct),
            distractors=generated.distractors,
            topic=generated.topic,
            hint=[*generated.hint, text(guidance)],
            order=generated.order,
        )


def register_ipst_progression_sets() -> int:
    """Fill every IPST topic to three ordered stages; return sets added."""
    groups: dict[tuple[str, str, str, str, str], list[QuestionType]] = defaultdict(list)
    originals = list(REGISTRY.values())
    for spec in originals:
        if spec.subject != DEFAULT_SUBJECT or not spec.key.startswith("math."):
            continue
        placement = placement_for(
            key=spec.curriculum_key or spec.key,
            subject=spec.subject,
            level=spec.level_for(),
            topic=spec.topic,
        )
        if placement.course_type not in {"สสวท. พื้นฐาน", "สสวท. เพิ่มเติม"}:
            continue
        groups[(
            placement.course_type,
            placement.level,
            placement.strand_code,
            placement.standard_code,
            spec.topic,
        )].append(spec)

    authored = stage_of()
    added = 0
    for specs in groups.values():
        ordered = sorted(specs, key=_difficulty_signal)
        count = len(ordered)
        if all(spec.key in authored for spec in ordered):
            # The authored path (math_stages) decides; test_math_stages keeps
            # every IPST set in it. The heuristic below only covers a set that
            # has not been placed yet.
            ordered.sort(key=lambda spec: authored[spec.key])
            assignments = [authored[spec.key] for spec in ordered]
        elif count == 1:
            assignments = [3]
        elif count == 2:
            assignments = [1, 3]
        else:
            assignments = [min(3, 1 + index * 3 // count) for index in range(count)]
        for spec, stage in zip(ordered, assignments):
            _set_stage(spec, stage)
            if stage == 1:
                # Foundation lowers the choice load: the set's first-listed
                # (hand-picked, most diagnostic) distractors are kept and the
                # last is dropped. Fluency and Application keep all of theirs.
                spec.max_choices = min(spec.max_choices, FOUNDATION_CHOICES)

        present = set(assignments)
        for stage in (1, 2, 3):
            if stage in present:
                continue
            if stage == 1:
                source = ordered[0]
            elif stage == 2:
                source = ordered[min(len(ordered) - 1, len(ordered) // 2)]
            else:
                source = ordered[-1]
            variant = SupportedPracticeSet(source, stage)
            variant.index = len(REGISTRY)
            if variant.key in REGISTRY:
                raise RuntimeError(f"duplicate progression set key: {variant.key}")
            REGISTRY[variant.key] = variant
            added += 1
    return added


ADDED_IPST_PROGRESSION_SETS = register_ipst_progression_sets()
