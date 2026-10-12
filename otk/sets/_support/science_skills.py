"""Specs and drawings for ทักษะกระบวนการทางวิทยาศาสตร์ (ม.1 บทนำ).

One family, ``ExperimentChartSpec``: a bar chart of a simple controlled
experiment's results. It exists because ``การจัดกระทำและสื่อความหมายข้อมูล`` and
``การตีความหมายข้อมูล`` are skills about a *graph*, and a set that describes the
graph in a sentence tests neither — it tests reading Thai, which the learner can
already do.

Nothing Thai is drawn into the PNG: the bundled matplotlib font (DejaVu Sans) has
no Thai glyphs. The bars are numbered 1-4 and the axes are labelled in ASCII, so
what each number *means* has to come from the stem — which is also what makes the
picture safe to reuse across several different experiments.

**Alt text.** ``chart_alt`` names the axes and says there are four bars, and stops
there. It must not say which bar is tallest: three of the four sets below have
exactly that as their answer, and an image renders as its alt text alone in a
printed worksheet and for a screen reader. This is the rule ``circuit_symbols``
and ``ms1_diagrams`` both follow.
"""

from __future__ import annotations

from typing import NamedTuple


class ExperimentChartSpec(NamedTuple):
    """Four measured values, one per treatment group.

    ``values`` are whole numbers so a learner reads them off the gridlines
    rather than estimating. The groups are deliberately unlabelled in the
    drawing — see the module docstring.
    """
    values: tuple[int, int, int, int]
    axis: str                # what the y-axis counts, in ASCII, for the drawing
    unit_th: str             # the same quantity in Thai, for the stem
    unit_short: str          # just the unit, for an answer that is a number
    y_max: int

    @property
    def asset_id(self) -> str:
        return "expchart_" + "_".join(str(v) for v in self.values)

    @property
    def best(self) -> int:
        """1-based number of the tallest bar."""
        return self.values.index(max(self.values)) + 1

    @property
    def worst(self) -> int:
        return self.values.index(min(self.values)) + 1


#: Every spec has a unique maximum and a unique minimum, so "which group grew
#: most" and "which grew least" both have exactly one answer. A tie would make
#: the item unanswerable from the picture it is drawn from.
EXPERIMENT_CHARTS = tuple(ExperimentChartSpec(*t) for t in (
    ((4, 9, 14, 7), "height (cm)", "ความสูงของต้นถั่ว (เซนติเมตร)", "เซนติเมตร", 20),
    ((12, 6, 18, 9), "height (cm)", "ความสูงของต้นถั่ว (เซนติเมตร)", "เซนติเมตร", 24),
    ((20, 35, 15, 45), "count", "จำนวนฟองแก๊สที่นับได้ (ฟอง)", "ฟอง", 55),
    ((30, 18, 42, 25), "count", "จำนวนฟองแก๊สที่นับได้ (ฟอง)", "ฟอง", 50),
    ((8, 16, 5, 11), "mass (g)", "มวลของผลผลิตที่เก็บได้ (กรัม)", "กรัม", 20),
    ((25, 14, 19, 33), "mass (g)", "มวลของผลผลิตที่เก็บได้ (กรัม)", "กรัม", 40),
))


def chart_alt(spec: ExperimentChartSpec) -> str:
    """Names the axes and the number of bars, never which bar is tallest."""
    return ("กราฟแท่งแสดงผลการทดลอง มีแท่ง 4 แท่ง กำกับหมายเลข 1 ถึง 4 บนแกนนอน "
            "แกนตั้งเป็นค่าที่วัดได้ มีเส้นตารางกำกับค่าเป็นช่วง ๆ")


def diagram_question(asset_id: str, alt: str, *, stem: str, correct: str,
                     wrongs: tuple[str, ...], hint: str, topic: str):
    """A question whose stem *shows* the chart, then asks in Thai."""
    from otk.core.content import image, text
    from otk.core.distractors import label_pool
    from otk.core.question import GeneratedQuestion

    return GeneratedQuestion(
        stem=[image(asset_id, alt=alt), text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )
