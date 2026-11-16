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


# ── More pictographs where one picture stands for several (2026-11): the total, most minus least, pictures
# added, the order, a true statement, and two rows against a third ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p2 import LEVEL  # noqa: E402


def _p2_chart(rng: Random):
    key = rng.choice((2, 5, 10))
    return key, _story.pictograph(rng, key=key, lo=2, hi=9)


@question_type("math.pictograph_total_p2", display_name={"th": "แผนภูมิรูปภาพ: รวมทุกรายการ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographTotalP2(WordProblem):
    def expr(self, rng: Random):
        key, pg = _p2_chart(rng)
        right = sum(pg.data.values())
        symbols = right // key
        # The pictures counted, not multiplied; one row short; one picture off.
        smallest = min(pg.data.values())
        return MathDraw("", str(right), prompt=f"{pg.text}\nรวมทุกรายการมีกี่{pg.chart.unit}",
                        distractors=_story.keep(symbols, right - smallest, right + key, right - key,
                                                answer=right, lo=1))


@question_type("math.pictograph_range_p2", display_name={"th": "แผนภูมิรูปภาพ: มากที่สุดมากกว่าน้อยที่สุดเท่าใด"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographRangeP2(WordProblem):
    def expr(self, rng: Random):
        key, pg = _p2_chart(rng)
        a, b = max(pg.data.values()), min(pg.data.values())
        right = a - b
        # The pictures' difference only; added; one picture off.
        return MathDraw("", str(right),
                        prompt=f"{pg.text}\nรายการที่มีมากที่สุดมากกว่ารายการที่มีน้อยที่สุดกี่{pg.chart.unit}",
                        distractors=_story.keep(right // key, a + b, right + key, right - key, answer=right, lo=1))


@question_type("math.pictograph_add_symbols_p2", display_name={"th": "แผนภูมิรูปภาพ: ถ้าเพิ่มรูปอีก"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographAddSymbolsP2(WordProblem):
    def expr(self, rng: Random):
        key, pg = _p2_chart(rng)
        row = rng.choice(list(pg.data))
        k = rng.randint(1, 4)
        right = pg.data[row] + k * key
        prompt = (f"{pg.text}\nถ้าวาด ● เพิ่มที่{row}อีก {k} รูป {pg.label(row)}จะมีกี่{pg.chart.unit}")
        # Each added picture counted as one; the pictures alone; one picture off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(pg.data[row] + k, right // key, right + key, right - key,
                                                answer=right, lo=1))


@question_type("math.pictograph_order_p2", display_name={"th": "แผนภูมิรูปภาพ: เรียงลำดับ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographOrderP2(ChoiceType):
    def compose(self, rng: Random):
        _, pg = _p2_chart(rng)
        up = rng.random() < 0.5
        ordered = sorted(pg.data, key=pg.data.get, reverse=not up)
        place = rng.choice((1, 2))
        right = ordered[place]
        stem = (f"{pg.text}\nเมื่อเรียงจาก{'น้อยไปมาก' if up else 'มากไปน้อย'} "
                f"รายการใดอยู่ลำดับที่{'สอง' if place == 1 else 'สาม'}")
        return stem, right, [r for r in ordered if r != right]


@question_type("math.pictograph_true_statement_p2", display_name={"th": "แผนภูมิรูปภาพ: ข้อความใดถูกต้อง"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographTrueStatementP2(ChoiceType):
    def compose(self, rng: Random):
        key, pg = _p2_chart(rng)
        x, y = rng.sample(list(pg.data), 2)
        if pg.data[x] < pg.data[y]:
            x, y = y, x
        a, b, unit = pg.data[x], pg.data[y], pg.chart.unit
        lx, ly = pg.label(x), pg.label(y)
        right = f"{lx}มากกว่า{ly} {a - b} {unit}"
        # The pictures' difference read as the amount; the wrong way round; added.
        wrongs = [f"{lx}มากกว่า{ly} {(a - b) // key} {unit}", f"{ly}มากกว่า{lx} {a - b} {unit}",
                  f"{lx}มากกว่า{ly} {a + b} {unit}"]
        return f"{pg.text}\nข้อความใดถูกต้อง", right, wrongs


@question_type("math.pictograph_two_rows_p2", display_name={"th": "แผนภูมิรูปภาพ: สองรายการรวมกันเทียบกับอีกรายการ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographTwoRowsP2(WordProblem):
    def expr(self, rng: Random):
        key, pg = _p2_chart(rng)
        ordered = sorted(pg.data, key=pg.data.get)
        z = ordered[0]
        x, y = rng.sample(ordered[1:], 2)
        a, b, c = pg.data[x], pg.data[y], pg.data[z]
        right = a + b - c
        prompt = f"{pg.text}\n{pg.label(x)}และ{pg.label(y)}รวมกัน มากกว่า{pg.label(z)}กี่{pg.chart.unit}"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right // key, a + b, a - c, right + key, answer=right, lo=1))


_BANK_DAYS_P2 = ("วันจันทร์", "วันอังคาร", "วันพุธ", "วันพฤหัสบดี", "วันศุกร์")


def _bank_week_chart_p2(counts, scale):
    rows = ["แผนภูมิรูปภาพแสดงจำนวนขนมที่ขายได้"]
    rows += [f"{day}: " + " ".join(["●"] * n) for day, n in zip(_BANK_DAYS_P2, counts)]
    return "\n".join(rows + [f"กำหนดให้ ● แทนขนม {scale} ชิ้น"])


@question_type("math.pictograph_selected_total_p2", display_name={"th": "รวมเฉพาะรายการที่ถามจากแผนภูมิรูปภาพ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographSelectedTotalP2(WordProblem):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-2/4175-2-2567-2-3.pdf, ตอนที่ 2 ข้อ 1",))

    def expr(self, rng: Random):
        scale = rng.choice((2, 5, 10))
        counts = [rng.randint(1, 9) for _ in _BANK_DAYS_P2]
        chosen = sorted(rng.sample(range(5), 3))
        symbols = sum(counts[i] for i in chosen)
        answer = symbols * scale
        named_days = " และ ".join(_BANK_DAYS_P2[i] for i in chosen)
        prompt = f"{_bank_week_chart_p2(counts, scale)}\nเฉพาะ{named_days} ขายขนมรวมกี่ชิ้น"
        return MathDraw("", str(answer), prompt=prompt,
                        # Include unasked rows; count icons only; omit a requested row.
                        distractors=_story.keep(sum(counts) * scale, symbols,
                                                sum(counts[i] for i in chosen[:2]) * scale,
                                                answer + scale, answer=answer, lo=1))


@question_type("math.pictograph_matching_rows_p2", display_name={"th": "หาทุกรายการที่มีจำนวนตรงกับค่าที่กำหนด"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographMatchingRowsP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-2/4163-2-2565-2-3.pdf, ตอนที่ 2 ข้อ 1.2",))

    def compose(self, rng: Random):
        scale, target = rng.choice((2, 5, 10)), rng.randint(2, 8)
        matches = sorted(rng.sample(range(5), 2))
        others = [i for i in range(5) if i not in matches]
        counts = [target if i in matches else rng.choice([n for n in range(1, 10) if n != target])
                  for i in range(5)]
        label = lambda pair: " และ ".join(_BANK_DAYS_P2[i] for i in sorted(pair))
        wrongs = [label((matches[0], others[0])), label((matches[1], others[1])),
                  label((others[0], others[2]))]
        return (f"{_bank_week_chart_p2(counts, scale)}\nวันใดบ้างขายขนมได้ {target * scale} ชิ้น",
                label(matches), wrongs)


@question_type("math.pictograph_pair_target_p2", display_name={"th": "หาคู่รายการที่รวมได้ตามเป้าหมาย"}, level={"th": "ป.2"}, topic="แผนภูมิรูปภาพ")
class PictographPairTargetP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-2/4152-2-2564-2-2.pdf, ข้อ 19",))

    def compose(self,rng: Random):
        counts=rng.sample(range(1,10),5)
        pairs=[(i,j) for i in range(5) for j in range(i+1,5)]
        # Only one pair in the entire chart may attain the requested target.
        unique=[pair for pair in pairs if sum(counts[i] for i in pair) not in
                [sum(counts[i] for i in other) for other in pairs if other!=pair]]
        pair=rng.choice(unique)
        scale=rng.choice((2,5,10))
        target=sum(counts[i] for i in pair)*scale
        def label(p):
            return " และ ".join(_BANK_DAYS_P2[i] for i in p)
        return (f"{_bank_week_chart_p2(counts,scale)}\nวันคู่ใดขายขนมรวม {target} ชิ้น",label(pair),
                [label(p) for p in rng.sample([p for p in pairs if p!=pair],3)])


@question_type("math.pictograph_extreme_amount_p2", display_name={"th": "ระบุรายการมากหรือน้อยที่สุดพร้อมจำนวน"}, level={"th": "ป.2"}, topic="แผนภูมิรูปภาพ")
class PictographExtremeAmountP2(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-2/4152-2-2564-2-2.pdf, ข้อ 20",))

    def compose(self,rng: Random):
        counts=rng.sample(range(1,10),5)
        scale=rng.choice((2,5,10))
        most=rng.choice((False,True))
        index=counts.index((max if most else min)(counts))
        amount=counts[index]*scale
        other=rng.choice([i for i in range(5) if i!=index])
        def label(i,v):
            return f"{_BANK_DAYS_P2[i]} จำนวน {v} ชิ้น"
        return (f"{_bank_week_chart_p2(counts,scale)}\nวันใดขายขนม{'มากที่สุด' if most else 'น้อยที่สุด'}และขายกี่ชิ้น",
                label(index,amount),[label(index,counts[index]),label(other,amount),label(other,counts[other]*scale)])
