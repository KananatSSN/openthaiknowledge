"""Worksheet model and problem selection.

A worksheet draws its problems from the same question-type registry as the
online quiz — so anything practisable is printable. The renderer
(`core/render/pdf.py`) turns the resulting questions into an A4 PDF.
"""

from __future__ import annotations

from random import Random
from typing import Literal

from pydantic import BaseModel, Field

from .question import Question
from .registry import REGISTRY


class Worksheet(BaseModel):
    title: str = "แบบฝึกหัดคณิตศาสตร์"
    subtitle: str = ""
    school_name: str = ""
    level: str = ""                    # corner badge, e.g. "ป.3"
    instructions: str = ""
    logo: str = ""                     # server-side path; ignored if missing

    # {key: weight} or {key: {"weight": w, "params": {...}}}
    generators: dict[str, object] = Field(default_factory=dict)
    num_problems: int = 20
    shuffle: bool = True               # True: weighted mix; False: cycle in order
    seed: int | None = None

    columns: int = 2
    problems_per_page: int = 20      # ignored when show_choices packs by height
    answer_style: Literal["line", "box", "none"] = "line"
    problem_fontsize: int = 16

    # Print each question's options under its stem, so a multiple-choice type
    # is answerable on paper. Off by default: a math drill wants a blank, not
    # four numbers to pick from. Printed options make every question a
    # different height, so the renderer then packs pages by measured height
    # instead of filling a fixed grid.
    show_choices: bool = False

    answer_key: bool = True
    answer_key_columns: int = 4
    answer_key_title: str = ""

    show_name_date: bool = True
    field_labels: list[str] = Field(
        default_factory=lambda: ["ชื่อ", "วันที่", "เวลา", "คะแนน"])
    font_family: str = ""              # e.g. "Leelawadee UI" for Thai

    def specs(self) -> list[tuple[str, float, dict]]:
        """Normalize both generator shapes into (key, weight, params) tuples."""
        out: list[tuple[str, float, dict]] = []
        for key, value in self.generators.items():
            if isinstance(value, dict):
                out.append((key, float(value.get("weight", 1)),
                            dict(value.get("params", {}))))
            else:
                out.append((key, float(value), {}))
        return out


def build_worksheet(config: Worksheet, rng: Random | None = None) -> list[Question]:
    """Instantiate ``num_problems`` questions from the configured types."""
    specs = config.specs()
    if not specs:
        raise ValueError("worksheet has no generators")
    unknown = [k for k, _, _ in specs if k not in REGISTRY]
    if unknown:
        raise ValueError(f"unknown question type(s): {unknown}")
    for key, _, params in specs:
        bad = set(params) - set(REGISTRY[key].params())
        if bad:
            raise ValueError(
                f"{key!r} has no parameter(s) {sorted(bad)}; "
                f"tunable: {sorted(REGISTRY[key].params()) or 'none'}")

    rng = rng or Random(config.seed)
    weights = [w for _, w, _ in specs]
    out: list[Question] = []
    for i in range(config.num_problems):
        if config.shuffle:
            key, _, params = rng.choices(specs, weights=weights, k=1)[0]
        else:
            key, _, params = specs[i % len(specs)]
        out.append(REGISTRY[key].generate(rng, **params))
    return out
