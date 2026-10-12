"""แผนภูมิรูปภาพ

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.2/1

Sets moved here from: math, math_measure_pictures, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_measure_pictures import PICTOGRAPHS_P2, _picto_question
from otk.sets._support.math_p2 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.pictograph",
               display_name={"th": "อ่านแผนภูมิรูปภาพ"}, level={"th": "ป.2"},
               topic="แผนภูมิรูปภาพ")
class Pictograph(WordProblem):
    def expr(self, rng: Random):
        key = rng.choice([2, 5, 10])
        pg = _story.pictograph(rng, key=key, lo=2, hi=9)
        row = rng.choice(list(pg.data))
        value = pg.data[row]
        shown = value // key
        return MathDraw(
            "", rf"{value}",
            prompt=f"{pg.text}\n{pg.label(row)}มีกี่{pg.chart.unit}",
            # Counting the symbols instead of what they stand for comes first.
            distractors=_story.keep(shown, value + key, value - key, shown + key,
                                    answer=value, lo=1))


@question_type("math.pictograph_key_picture_p2",
               display_name={"th": "อ่านแผนภูมิรูปภาพจากภาพ (1 รูปแทนหลายหน่วย)"},
               level={"th": "ป.2"}, topic="แผนภูมิรูปภาพ")
class PictographKeyPictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        return _picto_question(rng.choice(PICTOGRAPHS_P2), rng, self.topic)


@question_type("math.pictograph_compare_p2",
               display_name={"th": "แผนภูมิรูปภาพ (1 รูปแทนหลายหน่วย): เปรียบเทียบและรวม"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographCompareP2(WordProblem):
    def expr(self, rng: Random):
        key = rng.choice([2, 5, 10])
        pg = _story.pictograph(rng, key=key, lo=2, hi=9)
        x, y = rng.sample(list(pg.data), 2)
        if pg.data[x] < pg.data[y]:
            x, y = y, x
        a, b, unit = pg.data[x], pg.data[y], pg.chart.unit
        if rng.random() < 0.5:
            ans = a - b
            return MathDraw("", str(ans),
                            prompt=f"{pg.text}\n{pg.label(x)}มากกว่า{pg.label(y)}กี่{unit}",
                            # The difference in symbols, not in what they stand for.
                            distractors=_story.keep(ans // key, a + b, ans + key, answer=ans,
                                                    lo=1))
        ans = a + b
        return MathDraw("", str(ans),
                        prompt=f"{pg.text}\n{pg.label(x)}และ{pg.label(y)}รวมกันมีกี่{unit}",
                        distractors=_story.keep(ans // key, a - b, ans + key, answer=ans, lo=1))


@question_type("math.pictograph_symbols_p2",
               display_name={"th": "แผนภูมิรูปภาพ: ต้องใช้รูปกี่รูป"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographSymbolsP2(WordProblem):
    def expr(self, rng: Random):
        key = rng.choice([2, 5, 10])
        pg = _story.pictograph(rng, key=key, lo=2, hi=8)
        row = rng.choice(list(pg.data))
        extra = key * rng.randint(1, 4)
        after = pg.data[row] + extra
        unit = pg.chart.unit
        return MathDraw("", str(after // key),
                        prompt=(f"{pg.text}\nถ้า{pg.label(row)}เพิ่มขึ้นอีก {extra} {unit} "
                                f"แถวของ{row}จะมี ● ทั้งหมดกี่รูป"),
                        distractors=_story.keep(after, extra // key, pg.data[row] // key + extra,
                                                after // key + 1, answer=after // key, lo=1))
