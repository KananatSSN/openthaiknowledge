"""Curriculum-specific successors for mixed legacy science sets.

The five source generators referenced here predate the IPST filing and remain
unchanged for saved-practice compatibility. These additive views pin one
defensible curriculum scope at a time, avoiding grade or formula jumps inside a
single practice target.
"""

from __future__ import annotations


class FoundationStage:
    learning_stage = 1
    learning_stage_key = "foundation"
    learning_stage_label = {"th": "ปูพื้นฐาน", "en": "Foundation"}


class FluencyStage:
    learning_stage = 2
    learning_stage_key = "fluency"
    learning_stage_label = {"th": "ฝึกคล่อง", "en": "Fluency"}


