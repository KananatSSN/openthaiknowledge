"""แผนภูมิรูปภาพ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.1/1

Sets moved here from: math_measure_pictures, math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_measure_pictures import PICTOGRAPHS_P1, _picto_question
from otk.sets._support.math_p1 import LEVEL, _texts

PROVENANCE = Provenance("original")


@question_type("math.pictograph_picture_p1", display_name={"th": "อ่านแผนภูมิรูปภาพจากภาพ"},
               level={"th": "ป.1"}, topic="แผนภูมิรูปภาพ")
class PictographPictureP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        return _picto_question(rng.choice(PICTOGRAPHS_P1), rng, self.topic)


@question_type("math.pictograph_read_p1",
               display_name={"th": "อ่านแผนภูมิรูปภาพ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographReadP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        row = rng.choice(list(pg.data))
        n = pg.data[row]
        return MathDraw("", str(n),
                        prompt=f"{pg.text}\n{pg.label(row)}มีกี่{pg.chart.unit}",
                        distractors=_story.keep(*[v for c, v in pg.data.items() if c != row],
                                                n + 1, n - 1, answer=n, lo=1))


@question_type("math.pictograph_compare_p1",
               display_name={"th": "แผนภูมิรูปภาพ: มากกว่า น้อยกว่า และรวมกัน"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographCompareP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        x, y = rng.sample(list(pg.data), 2)
        if pg.data[x] < pg.data[y]:
            x, y = y, x
        a, b, unit = pg.data[x], pg.data[y], pg.chart.unit
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(a - b),
                            prompt=f"{pg.text}\n{pg.label(x)}มากกว่า{pg.label(y)}กี่{unit}",
                            distractors=_story.keep(a + b, a, b, a - b + 1, answer=a - b, lo=1))
        if kind == 1:
            return MathDraw("", str(a - b),
                            prompt=f"{pg.text}\n{pg.label(y)}น้อยกว่า{pg.label(x)}กี่{unit}",
                            distractors=_story.keep(a + b, b, a, a - b + 1, answer=a - b, lo=1))
        if kind == 2:
            return MathDraw("", str(a + b),
                            prompt=f"{pg.text}\n{pg.label(x)}และ{pg.label(y)}รวมกันมีกี่{unit}",
                            distractors=_story.keep(a - b, a + b + 1, a + b - 1, answer=a + b))
        total = sum(pg.data.values())
        return MathDraw("", str(total),
                        prompt=f"{pg.text}\nจากแผนภูมิ รวมทั้งหมดมีกี่{unit}",
                        distractors=_story.keep(total - b, total + 1, total - 1,
                                                answer=total))


@question_type("math.pictograph_most_p1",
               display_name={"th": "แผนภูมิรูปภาพ: มากที่สุดและน้อยที่สุด"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographMostP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        pg = _story.pictograph(rng)
        most = rng.random() < 0.5
        pick = (max if most else min)(pg.data, key=pg.data.get)
        q = _texts(pick, [c for c in pg.data if c != pick], self.topic)
        q.stem = [text(pg.text),
                  text(pg.chart.most.format(most="มากที่สุด" if most else "น้อยที่สุด"))]
        return q
