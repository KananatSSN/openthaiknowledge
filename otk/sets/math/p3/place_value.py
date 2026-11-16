"""ค่าประจำหลัก

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/1, ค 1.1 ป.3/2

Sets moved here from: math, math_apply_stage, math_number, math_p3.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_apply_stage import _PlaceValueWord
from otk.sets._support.math_p2 import NumberReadingType, _maths
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.number_reading_p3",
               display_name={"th": "อ่านและเขียนจำนวนไม่เกิน 100,000"},
               level=LEVEL, topic="ค่าประจำหลัก")
class NumberReadingP3(NumberReadingType):
    LO, HI = 1000, 100000


@question_type("math.place_value_expanded",
               display_name={"th": "ค่าประจำหลัก (ค่าของเลข)"}, level={"th": "ป.3"},
               topic="ค่าประจำหลัก")
class PlaceValueExpanded(WordProblem):
    _NAMES = {"หมื่น": 10000, "พัน": 1000, "ร้อย": 100, "สิบ": 10, "หน่วย": 1}

    def expr(self, rng: Random):
        n = rng.randint(10000, 99999)
        pos = rng.choice(list(self._NAMES))
        place = self._NAMES[pos]
        digit = (n // place) % 10
        return MathDraw("", str(digit * place),
                        prompt=f"ค่าของเลขในหลัก{pos}ของ {n} เป็นเท่าใด?",
                        distractors=[str(digit), str(digit * place * 10),
                                     str(digit * (place // 10 or 1))])


@question_type("math.place_value_compose",
               display_name={"th": "ประกอบจำนวนจากค่าประจำหลัก"},
               level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class PlaceValueCompose(MathType):
    """The reverse of expanding: read a sum of place values back as one number."""

    def expr(self, rng: Random, digits_lo: int = 3, digits_hi: int = 4):
        n = rng.randint(digits_lo, digits_hi)
        # No zero digits: every place has to appear in the sum, or the question
        # would silently show fewer terms than the answer has digits.
        ds = [rng.randint(1, 9) for _ in range(n)]
        value = int("".join(str(d) for d in ds))
        parts = [d * 10 ** (n - 1 - i) for i, d in enumerate(ds)]
        return MathDraw(" + ".join(str(p) for p in parts), str(value),
                        prompt="ผลบวกนี้เท่ากับจำนวนใด",
                        distractors=[str(int("".join(str(d) for d in reversed(ds)))),
                                     str(value + 10 ** (n - 1)),
                                     str(sum(ds))])


@question_type("math.place_value_word_p3", display_name={"th": "จำนวนนับไม่เกิน 100,000 ในสถานการณ์"},
               level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class PlaceValueWordP3(_PlaceValueWord):
    lo, hi = 10_000, 99_999
    sentences = ("งานแสดงสินค้ามีผู้เข้าชม {n} คน", "ตำบลแห่งหนึ่งมีประชากร {n} คน",
                 "โครงการปลูกป่าปลูกต้นไม้ได้ {n} ต้น")
    compare = ("จำนวนประชากร", ("ตำบลนาดี", "ตำบลหนองบัว", "ตำบลโคกสูง", "ตำบลบ้านใหม่"))


@question_type("math.order_numbers_p3",
               display_name={"th": "เปรียบเทียบและเรียงลำดับจำนวนไม่เกิน 100,000"},
               level=LEVEL, topic="ค่าประจำหลัก")
class OrderNumbersP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        digits = rng.sample(range(1, 10), 5)
        nums: list[int] = []
        while len(nums) < 4:
            d = digits[:]
            rng.shuffle(d)
            n = int("".join(map(str, d)))
            if n not in nums:
                nums.append(n)
        most = rng.random() < 0.5
        pick = max(nums) if most else min(nums)
        # The number with the largest (smallest) last digit is the glance answer.
        by_ones = (max if most else min)(nums, key=lambda m: m % 10)
        wrongs = [by_ones] + [n for n in nums if n != by_ones]
        return _maths([text(f"จำนวนใด{'มากที่สุด' if most else 'น้อยที่สุด'}")],
                      str(pick), [str(w) for w in dict.fromkeys(wrongs) if w != pick],
                      self.topic)


# ── More place value (2026-11): a thousand or ten thousand more or less, the largest or smallest number from
# five digits, a number between two, the place a digit stands in, and zeros in a number read aloud ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402

_P3_PLACES = ("หลักหน่วย", "หลักสิบ", "หลักร้อย", "หลักพัน", "หลักหมื่น")


def _join(ds) -> int:
    return int("".join(map(str, ds)))


def _swap(ds, i: int, j: int) -> int:
    out = list(ds)
    out[i], out[j] = out[j], out[i]
    return _join(out)


from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType as _QT  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


@question_type("math.more_less_thousand_p3", display_name={"th": "มากกว่าหรือน้อยกว่าอยู่ 1,000 หรือ 10,000"},
               level=LEVEL, topic="ค่าประจำหลัก")
class MoreLessThousandP3(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((1000, 10000))
        more = rng.random() < 0.5
        n = rng.randint(12000, 88000)
        right = n + step if more else n - step
        other = 11000 - step
        prompt = f"จำนวนที่{'มากกว่า' if more else 'น้อยกว่า'} {n} อยู่ {step} คือจำนวนใด"
        # The other direction; the other step; a hundred instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(n - step if more else n + step, n + other if more else n - other,
                                                n + 100 if more else n - 100, answer=right, lo=0))


@question_type("math.number_from_digits_p3", display_name={"th": "สร้างจำนวนห้าหลักที่มากที่สุดหรือน้อยที่สุด"},
               level=LEVEL, topic="ค่าประจำหลัก")
class NumberFromDigitsP3(WordProblem):
    def expr(self, rng: Random):
        digits = rng.sample(range(10), 5)
        most = rng.random() < 0.5
        big = sorted(digits, reverse=True)
        small = sorted(digits)
        if small[0] == 0:
            small[0], small[1] = small[1], small[0]
        if most:
            right = _join(big)
            # The smallest instead; the two leading digits swapped; the two last swapped.
            wrongs = [_join(small), _swap(big, 0, 1), _swap(big, 3, 4)]
        else:
            right = _join(small)
            wrongs = [_join(big), _swap(small, 3, 4), _swap(small, 2, 3)]
        prompt = (f"ใช้เลขโดด {', '.join(map(str, digits))} หลักละหนึ่งตัว สร้างจำนวนห้าหลักที่"
                  f"{'มากที่สุด' if most else 'น้อยที่สุด'} ได้จำนวนใด")
        return MathDraw("", str(right), prompt=prompt, distractors=_story.keep(*wrongs, answer=right, lo=10000))


@question_type("math.number_between_p3", display_name={"th": "จำนวนที่อยู่ระหว่างสองจำนวน (ไม่เกิน 100,000)"},
               level=LEVEL, topic="ค่าประจำหลัก")
class NumberBetweenP3(_QT):
    """Fixed choices: a number from another draw could also lie between the two."""

    def build(self, rng: Random):
        a = rng.randint(10000, 90000)
        b = a + rng.randint(100, 900)
        right = rng.randint(a + 1, b - 1)
        below, above = a - rng.randint(1, 99), b + rng.randint(1, 99)
        # Numbers just outside each end, and one a thousand past.
        wrongs = _story.keep(below, above, b + 1000, answer=right)
        return _fixed_maths([_text_block(f"จำนวนใดอยู่ระหว่าง {a} กับ {b}")], str(right), wrongs, self.topic)


@question_type("math.digit_place_p3", display_name={"th": "เลขโดดอยู่ในหลักใด"},
               level=LEVEL, topic="ค่าประจำหลัก")
class DigitPlaceP3(ChoiceType):
    def compose(self, rng: Random):
        digits = rng.sample(range(1, 10), 5)
        pos = rng.randrange(5)
        right = _P3_PLACES[4 - pos]
        return (f"ในจำนวน {_join(digits)} เลขโดด {digits[pos]} อยู่ในหลักใด", right,
                [p for p in _P3_PLACES if p != right])


@question_type("math.zeros_in_number_p3", display_name={"th": "เขียนจำนวนจากคำอ่านแล้วนับเลข 0"},
               level=LEVEL, topic="ค่าประจำหลัก")
class ZerosInNumberP3(WordProblem):
    def expr(self, rng: Random):
        while True:
            digits = [rng.randint(1, 9)] + [rng.choice((0, 0, rng.randint(1, 9))) for _ in range(4)]
            if 1 <= digits.count(0) <= 3:
                break
        right = digits.count(0)
        prompt = f"จำนวน{_story.thai_words(_join(digits))} เขียนเป็นตัวเลขฮินดูอารบิกจะมีเลข 0 กี่ตัว"
        # One more or fewer; the other digits counted.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + 1, right - 1, 5 - right, right + 2, answer=right, lo=0, hi=5))


@question_type("math.digit_place_value_pair_p3", display_name={"th": "บอกหลักและค่าเลขโดดรวมกรณีศูนย์"}, level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class DigitPlaceValuePairP3(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-3/4355-3-2565-1-2.pdf, ข้อ 5–6",))

    def compose(self,rng: Random):
        digits=rng.sample(range(10),5)
        if digits[0]==0:
            digits[0],digits[1]=digits[1],digits[0]
        number=int("".join(map(str,digits)))
        position=rng.randrange(5)
        digit=digits[position]
        names=("หมื่น","พัน","ร้อย","สิบ","หน่วย")
        def label(i):
            return f"อยู่ในหลัก{names[i]} มีค่า {digit*10**(4-i)}"
        return (f"ในจำนวน {number} เลขโดด {digit} อยู่ในหลักใดและมีค่าเท่าใด",label(position),
                [label(i) for i in rng.sample([i for i in range(5) if i!=position],3)])


@question_type("math.canonical_expansion_p3", display_name={"th": "เลือกรูปกระจายตามค่าประจำหลักไม่เกินแสน"}, level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class CanonicalExpansionP3(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-3/4355-3-2565-1-2.pdf, ข้อ 7–8",))

    def build(self,rng: Random,**params):
        stem,right,wrongs=self.compose(rng)
        return _fixed_maths([text(stem)],right,wrongs,self.topic)

    def compose(self,rng: Random):
        digits=[rng.randint(1,9) for _ in range(5)]
        if rng.choice((False,True)):
            digits[rng.randint(1,3)]=0
        number=int("".join(map(str,digits)))
        terms=[d*10**(4-i) for i,d in enumerate(digits) if d]
        # Two equal-value regroupings are not one digit-value term per place.
        grouped_last=[terms[0]-1000,1000]+terms[1:-2]+[sum(terms[-2:])]
        grouped_first=[terms[0]+terms[1]]+terms[2:-2]+[terms[-2]-1,1,terms[-1]]
        wrong_value=terms[:-1]+[terms[-1]+10]
        label=lambda row:" + ".join(map(str,row))
        return (f"รูปกระจายตามค่าประจำหลักของ {number} คือข้อใด "
                "แต่ละพจน์ต้องเป็นค่าของเลขโดดเพียงหลักเดียว และละหลักที่เป็นศูนย์",label(terms),
                [label(grouped_last),label(grouped_first),label(wrong_value)])


@question_type("math.expanded_comparison_statement_p3", display_name={"th": "ตรวจข้อความเปรียบเทียบกับผลบวกค่าประจำหลัก"}, level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class ExpandedComparisonStatementP3(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-3/4355-3-2565-1-2.pdf, ข้อ 3–4",))

    def compose(self,rng: Random):
        signs=["<",">","=","≠"]
        rng.shuffle(signs)
        correct=rng.randrange(4)
        rows=[]
        for i,sign in enumerate(signs):
            number=rng.randint(12000,88000)
            terms=[int(d)*10**(4-j) for j,d in enumerate(str(number)) if d!="0"]
            true=i==correct
            if (sign=="=" and true) or (sign=="≠" and not true):
                delta=0
            else:
                delta=rng.choice((10,100,1000))
                if (sign=="<" and true) or (sign==">" and not true):
                    delta=-delta
                elif sign in ("=","≠"):
                    delta*=rng.choice((-1,1))
            rows.append(f"{number+delta} {sign} "+" + ".join(map(str,terms)))
        return "ข้อความใดใช้เครื่องหมายเปรียบเทียบได้ถูกต้อง",rows[correct],[r for i,r in enumerate(rows) if i!=correct]


@question_type("math.order_large_sequence_p3", display_name={"th": "เลือกลำดับจำนวนไม่เกินหนึ่งแสนที่เรียงครบถูกต้อง"}, level={"th": "ป.3"}, topic="ค่าประจำหลัก")
class OrderLargeSequenceP3(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=("openthaiknowledge-bank/mathematics/level/primary-3/4355-3-2565-1-2.pdf, ข้อ 9–10",))

    def compose(self,rng: Random):
        values=rng.sample(range(1000,100000),4)
        descending=rng.choice((False,True))
        ordered=sorted(values,reverse=descending)
        wrongs=[ordered[::-1],[ordered[1],ordered[0],ordered[2],ordered[3]],
                [ordered[0],ordered[1],ordered[3],ordered[2]]]
        label=lambda row:", ".join(map(str,row))
        return (f"เรียงจำนวน {label(values)} จาก{'มากไปน้อย' if descending else 'น้อยไปมาก'}ได้ตามข้อใด",
                label(ordered),[label(row) for row in wrongs])
