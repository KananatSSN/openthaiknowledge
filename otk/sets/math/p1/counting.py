"""การนับ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.1/1

Sets moved here from: math, math_p1, math_pictures.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q, _text_q
from otk.sets._support.math_p1 import LEVEL, _texts
from otk.sets._support.math_pictures import (
    BUNDLES,
    BY_KEY,
    KINDS,
    LARGE_COUNTS,
    LINES,
    MIXED,
    SMALL_COUNTS,
    _img,
    _near,
)

PROVENANCE = Provenance("original")


def _misread(n: int) -> list[str]:
    """Wrong readings a ป.1 learner writes: สองสิบ for ยี่สิบ, หนึ่ง for เอ็ด."""
    tens, ones = divmod(n, 10)
    ones_word = _story.thai_words(ones) if ones else ""
    out = []
    if tens == 2:
        out.append("สองสิบ" + ones_word)
    if tens == 1:
        out.append("หนึ่งสิบ" + ones_word)
    if ones == 1 and tens >= 2:
        out.append(_story.thai_words(tens * 10) + "หนึ่ง")
    return out


_ORDINAL_WORDS = {1: "ที่หนึ่ง", 2: "ที่สอง", 3: "ที่สาม", 4: "ที่สี่", 5: "ที่ห้า",
                  6: "ที่หก", 7: "ที่เจ็ด"}


@question_type("math.count_objects_p1", display_name={"th": "นับสิ่งของในภาพ (ไม่เกิน 10)"},
               level=LEVEL, topic="การนับ")
class CountObjectsP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SMALL_COUNTS)
        kind = BY_KEY[s.kinds[0]]
        n = s.count(kind.key)
        return _math_q([text(f"ในภาพมี{kind.thai}กี่{kind.unit}"), _img(s.asset_id, [kind.key])],
                       str(n), _near(n, lo=1), self.topic)


@question_type("math.count_objects_20_p1", display_name={"th": "นับสิ่งของในภาพ (11 ถึง 20)"},
               level=LEVEL, topic="การนับ")
class CountObjectsTwentyP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(LARGE_COUNTS)
        kind = BY_KEY[s.kinds[0]]
        n = s.count(kind.key)
        # Missing or double-counting one row of five.
        return _math_q([text(f"ในภาพมี{kind.thai}กี่{kind.unit} (แถวละ 5)"),
                        _img(s.asset_id, [kind.key])],
                       str(n), _near(n, n - 5, n + 5, lo=1), self.topic)


@question_type("math.count_kind_p1", display_name={"th": "นับเฉพาะสิ่งที่โจทย์ถาม"},
               level=LEVEL, topic="การนับ")
class CountKindP1(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(MIXED)
        total = len(s.items)
        if rng.random() < 1 / 6:
            # A kind that is not in the picture: there are none, which is 0.
            kind = BY_KEY[rng.choice([k.key for k in KINDS if k.key not in s.kinds])]
            others = [s.count(k) for k in s.kinds]
            return _math_q([text(f"ในภาพมี{kind.thai}กี่{kind.unit}"), _img(s.asset_id, s.kinds)],
                           "0", _near(0, total, *others, lo=0), self.topic)
        kind = BY_KEY[rng.choice(s.kinds)]
        n = s.count(kind.key)
        others = [s.count(k) for k in s.kinds if k != kind.key]
        # Counting everything, or counting the other kind.
        return _math_q([text(f"ในภาพมี{kind.thai}กี่{kind.unit}"), _img(s.asset_id, s.kinds)],
                       str(n), _near(n, total, *others, lo=1), self.topic)


@question_type("math.next_number",
               display_name={"th": "จำนวนถัดไป"}, level={"th": "ป.1"}, topic = "การนับ")
class NextNumber(MathType):
    def expr(self, rng: Random, lo: int = 1, hi: int = 99):
        # ป.1 counts to 100 (ค 1.1 ป.1/1), so the answer stays within it.
        n = rng.randint(lo, hi)
        return MathDraw(rf"{n}", rf"{n + 1}", topic="จำนวนถัดไป",
                        prompt="จงเขียนจำนวนถัดไป")


@question_type("math.previous_number",
               display_name={"th": "จำนวนก่อนหน้า"}, level={"th": "ป.1"}, topic="การนับ")
class PreviousNumber(WordProblem):
    def expr(self, rng: Random, lo: int = 1, hi: int = 100):
        n = rng.randint(lo, hi)
        # The stem must show n: without it there is nothing to count back from.
        prompt = rng.choice(("จงเขียนจำนวนก่อนหน้า", "จำนวนที่อยู่ก่อนหน้าจำนวนนี้คือจำนวนใด",
                             "จำนวนใดน้อยกว่าจำนวนนี้อยู่หนึ่ง"))
        return MathDraw(rf"{n}", rf"{n - 1}", prompt=prompt,
                        distractors=[str(n + 1), str(n - 2 if n >= 2 else n + 2), str(n)])


@question_type("math.number_words_p1",
               display_name={"th": "อ่านและเขียนตัวหนังสือแสดงจำนวน"},
               level=LEVEL, topic="การนับ")
class NumberWordsP1(QuestionType):
    def build(self, rng: Random, hi: int = 100) -> GeneratedQuestion:
        n = rng.randint(11, max(12, min(int(hi), 100)))
        tens, ones = divmod(n, 10)
        near = [m for m in (ones * 10 + tens, n + 10, n - 10, n + 1, n - 1)
                if 0 <= m <= 100 and m != n]
        if rng.random() < 0.5:
            q = _texts(_story.thai_words(n),
                       list(dict.fromkeys(_misread(n) + [_story.thai_words(m) for m in near])),
                       self.topic)
            q.stem = [text("จำนวนนี้อ่านว่าอย่างไร"), content_math(str(n))]
            return q
        return GeneratedQuestion(
            stem=[text(f"“{_story.thai_words(n)}” เขียนเป็นตัวเลขได้อย่างไร")],
            correct=[content_math(str(n))],
            distractors=fixed(*[[content_math(str(m))] for m in near]),
            topic=self.topic,
        )


@question_type("math.ordinal_position_p1", display_name={"th": "ลำดับที่"},
               level=LEVEL, topic="การนับ")
class OrdinalPositionP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(LINES)
        line = [BY_KEY[k] for k, _, _ in s.items]
        size = len(line)
        from_left = rng.random() < 0.6
        side = "ซ้าย" if from_left else "ขวา"
        img = _img(s.asset_id, [k.key for k in line])
        if rng.random() < 0.5:
            pos = rng.randint(1, size)
            index = pos - 1 if from_left else size - pos
            answer = line[index].thai
            # The neighbours, and the same position counted from the other end.
            mirror = line[size - 1 - index].thai
            wrongs = [mirror] + [line[j].thai for j in (index - 1, index + 1) if 0 <= j < size]
            wrongs += [k.thai for k in line]
            return _text_q([text(f"สิ่งของลำดับ{_ORDINAL_WORDS[pos]}นับจากทาง{side}คืออะไร"), img],
                           answer, [w for w in wrongs if w != answer], self.topic)
        index = rng.randrange(size)
        kind = line[index]
        pos = index + 1 if from_left else size - index
        other_end = size - index if from_left else index + 1
        return _math_q([text(f"{kind.thai}อยู่ลำดับที่เท่าใดเมื่อนับจากทาง{side}"), img],
                       str(pos), _near(pos, other_end, lo=1), self.topic)


@question_type("math.count_bundles_p1", display_name={"th": "นับมัดละสิบ"},
               level=LEVEL, topic="การนับ")
class CountBundlesP1(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        b = rng.choice(BUNDLES)
        img = image(b.asset_id, alt="ภาพหลอดที่มัดเป็นมัด และหลอดที่ไม่ได้มัด")
        swapped = 10 * b.ones + b.tens
        if rng.random() < 0.5:
            # Counting each bundle as one straw; reading ones and tens backwards.
            wrongs = [str(b.tens + b.ones), str(swapped), str(b.value + 10), str(b.value - 1)]
            return _math_q([text("มีหลอดทั้งหมดกี่หลอด (มัดละ 10 หลอด)"), img],
                           str(b.value), wrongs, self.topic)

        def tens_ones(t: int, o: int) -> str:
            return f"{t} สิบ {o} หน่วย"

        wrongs = [tens_ones(b.ones, b.tens), tens_ones(b.tens + 1, b.ones),
                  tens_ones(b.tens, (b.ones + 1) % 10), tens_ones(b.tens - 1, b.ones)]
        return _text_q([text("หลอดในภาพมีกี่สิบ กี่หน่วย (มัดละ 10 หลอด)"), img],
                       tens_ones(b.tens, b.ones), wrongs, self.topic)


@question_type("math.missing_number_in_sequence",
               display_name={"th": "จำนวนที่หายไป"}, level={"th": "ป.1"}, topic="การนับ")
class MissingNumberInSequence(MathType):
    def expr(self, rng: Random, lo: int = 5, hi: int = 20):
        n = rng.randint(lo, hi)
        missing = rng.randint(1, 4)
        valid_numbers = list(set(range(-lo+1, lo)) - {0})
        distractors = rng.sample(valid_numbers, 3)
        if missing == 1:
            return MathDraw(rf"\square,\ {n + 1},\ {n + 2},\ {n + 3}", rf"{n}",
                            prompt="จำนวนที่หายไปคืออะไร",
                            distractors=[str(n + distractors[0]), str(n + distractors[1]), str(n + distractors[2])])
        if missing == 2:
            return MathDraw(rf"{n},\ \square,\ {n + 2},\ {n + 3}", rf"{n + 1}",
                            prompt="จำนวนที่หายไปคืออะไร",
                            distractors=[str(n + distractors[0]), str(n + distractors[1]), str(n + distractors[2])])
        if missing == 3:
            return MathDraw(rf"{n},\ {n + 1},\ \square,\ {n + 3}", rf"{n + 2}",
                            prompt="จำนวนที่หายไปคืออะไร",
                            distractors=[str(n + distractors[0]), str(n + distractors[1]), str(n + distractors[2])])
        if missing == 4:
            return MathDraw(rf"{n},\ {n + 1},\ {n + 2},\ \square", rf"{n + 3}",
                            prompt="จำนวนที่หายไปคืออะไร",
                            distractors=[str(n + distractors[0]), str(n + distractors[1]), str(n + distractors[2])])


@question_type("math.thai_numerals_p1",
               display_name={"th": "ตัวเลขฮินดูอารบิกและตัวเลขไทย"},
               level=LEVEL, topic="การนับ")
class ThaiNumeralsP1(QuestionType):
    def build(self, rng: Random, hi: int = 100) -> GeneratedQuestion:
        n = rng.randint(10, max(11, min(int(hi), 100)))
        tens, ones = divmod(n, 10)
        near = [m for m in (ones * 10 + tens, n + 10, n - 10, n + 1, n - 1)
                if 0 <= m <= 100 and m != n]
        to_thai = rng.random() < 0.5
        show, say = ((str(n), _story.thai_numeral) if to_thai
                     else (_story.thai_numeral(n), str))
        q = _texts(say(n), [say(m) for m in near], self.topic)
        q.stem = [text("เขียนเป็นตัวเลขไทยได้อย่างไร" if to_thai
                       else "เขียนเป็นตัวเลขฮินดูอารบิกได้อย่างไร"), text(show)]
        return q


@question_type("math.tens_and_ones_p1",
               display_name={"th": "หลักสิบ หลักหน่วย และการเขียนในรูปกระจาย"},
               level=LEVEL, topic="การนับ")
class TensAndOnesP1(WordProblem):
    def expr(self, rng: Random):
        n = rng.randint(21, 99)
        tens, ones = divmod(n, 10)
        if ones == 0 or tens == ones:
            n, tens, ones = 47, 4, 7
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(n),
                            prompt=f"จำนวนที่ประกอบด้วย {tens} สิบ กับ {ones} หน่วย คือจำนวนใด",
                            distractors=_story.keep(ones * 10 + tens, tens + ones,
                                                    n + 10, answer=n))
        if kind == 1:
            return MathDraw(str(n), str(tens),
                            prompt="จำนวนนี้มีกี่สิบ",
                            distractors=_story.keep(ones, n, tens * 10, answer=tens))
        if kind == 2:
            return MathDraw(str(n), str(tens * 10),
                            prompt="เลขโดดในหลักสิบมีค่าเท่าใด",
                            distractors=_story.keep(tens, ones, ones * 10, answer=tens * 10))
        return MathDraw(str(n), rf"{tens * 10} + {ones}",
                        prompt="เขียนในรูปกระจายได้อย่างไร",
                        distractors=[rf"{tens} + {ones}", rf"{ones * 10} + {tens}",
                                     rf"{tens * 10} + {ones * 10}"])
