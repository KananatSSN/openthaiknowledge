"""การประมาณค่า

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.4/7

Sets moved here from: math, math_number, math_p4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p4 import LEVEL, grouped

PROVENANCE = Provenance("original")


_PLACE_WORD = {10: "สิบ", 100: "ร้อย", 1000: "พัน"}


def _n(v: int) -> str:
    return f"{v:,}".replace(",", "{,}")


def _round_to(n: int, place: int) -> int:
    """Round to the nearest place, halves upward, as ป.4 is taught."""
    return (n + place // 2) // place * place


@question_type("math.rounding",
               display_name={"th": "การปัดเศษ"}, level={"th": "ป.4"},
               topic="การประมาณค่า")
class Rounding(WordProblem):
    _PLACES = {"สิบ": 10, "ร้อย": 100, "พัน": 1000}

    def expr(self, rng: Random):
        n = rng.randint(1000, 99999)
        place = rng.choice(list(self._PLACES))
        unit = self._PLACES[place]
        low = (n // unit) * unit
        high = low + unit
        nearest = high if (n - low) * 2 >= unit else low
        return MathDraw("", str(nearest),
                        prompt=f"ปัด {n} ให้เป็นจำนวนเต็มหลัก{place}ที่ใกล้ที่สุด "
                               f"ได้เท่าใด?",
                        distractors=[str(high), str(low),
                                     str(round(n / (unit * 10)) * unit * 10)])


@question_type("math.estimate_sum", display_name={"th": "ประมาณผลบวก"},
               level={"th": "ป.4"}, topic="การประมาณค่า")
class EstimateSum(WordProblem):
    """Round each addend to the place asked, then add: tens with two-digit
    numbers, hundreds with three, thousands with four (ค 1.1 ป.4/7)."""

    def expr(self, rng: Random, lo: int = 12, hi: int = 89):
        place = rng.choice((10, 100, 1000))
        scale = place // 10
        while True:
            a, b = rng.randint(lo * scale, hi * scale), rng.randint(lo * scale, hi * scale)
            ra, rb = _round_to(a, place), _round_to(b, place)
            if ra + rb != a + b:          # an exact sum would make estimating pointless
                break
        word = _PLACE_WORD[place]
        who = rng.choice(_story.NAMES)
        shown, prompt = rng.choice((
            (f"{a} + {b}", f"ปัดเศษแต่ละจำนวนเป็นหลัก{word}ก่อน แล้วหาผลบวกโดยประมาณ"),
            ("", f"{who}ซื้อของราคา {a:,} บาท และ {b:,} บาท ถ้าปัดราคาเป็นหลัก{word} "
                 f"ต้องเตรียมเงินประมาณกี่บาท"),
            ("", f"วันเสาร์มีคนเข้าชมงาน {a:,} คน วันอาทิตย์ {b:,} คน ถ้าปัดเป็นหลัก{word} "
                 f"สองวันมีคนเข้าชมประมาณกี่คน"),
            ("", f"โรงเรียนสองแห่งเก็บขวดพลาสติกได้ {a:,} ใบ และ {b:,} ใบ ถ้าปัดเป็นหลัก{word} "
                 f"รวมกันเก็บได้ประมาณกี่ใบ"),
        ))
        # The exact sum, one place too many or too few.
        return MathDraw(shown, _n(ra + rb), prompt=prompt,
                        hint=rf"{a} \approx {ra}, \; {b} \approx {rb}",
                        distractors=[_n(a + b), _n(ra + rb + place), _n(ra + rb - place)])


@question_type("math.estimate_product", display_name={"th": "ประมาณผลคูณ"},
               level={"th": "ป.4"}, topic="การประมาณค่า")
class EstimateProduct(WordProblem):
    def expr(self, rng: Random, lo: int = 12, hi: int = 79):
        place = rng.choice((10, 100))
        scale = place // 10
        b = rng.randint(3, 9)
        while True:
            a = rng.randint(lo * scale, hi * scale)
            ra = _round_to(a, place)
            if ra != a:
                break
        word = _PLACE_WORD[place]
        frames = [
            (rf"{a} \times {b}", f"ปัดเศษตัวตั้งเป็นหลัก{word}ก่อน แล้วหาผลคูณโดยประมาณ"),
            ("", f"ซื้อของ {b} ชิ้น ราคาชิ้นละ {a:,} บาท ถ้าปัดราคาเป็นหลัก{word} ต้องจ่ายประมาณกี่บาท"),
            ("", f"ลังหนึ่งบรรจุไข่ {a:,} ฟอง มี {b} ลัง ถ้าปัดจำนวนในหนึ่งลังเป็นหลัก{word} มีไข่ประมาณกี่ฟอง"),
        ]
        if place == 10:
            frames.append(("", f"นักเรียนนั่งรถบัสคันละ {a} คน จำนวน {b} คัน ถ้าปัดเป็นหลักสิบ "
                               f"มีนักเรียนประมาณกี่คน"))
        shown, prompt = rng.choice(frames)
        return MathDraw(shown, _n(ra * b), prompt=prompt,
                        hint=rf"{a} \approx {ra}",
                        distractors=[_n(a * b), _n((ra + place) * b), _n(max(ra - place, place) * b)])


@question_type("math.estimate_word_problem_p4",
               display_name={"th": "โจทย์ปัญหาการประมาณค่า"},
               level=LEVEL, topic="การประมาณค่า")
class EstimateWordProblemP4(WordProblem):
    _ITEMS = (("โทรทัศน์", "ตู้เย็น"), ("จักรยาน", "หมวกกันน็อก"), ("โต๊ะ", "เก้าอี้"),
              ("พัดลม", "หม้อหุงข้าว"), ("โทรศัพท์", "หูฟัง"))

    def expr(self, rng: Random):
        x, y = rng.choice(self._ITEMS)
        a, b = rng.randint(5200, 29800), rng.randint(1200, 9800)
        r = lambda n: (n + 500) // 1000 * 1000
        ans = r(a) + r(b)
        return MathDraw("", str(ans),
                        prompt=(f"{x}ราคา {grouped(a)} บาท {y}ราคา {grouped(b)} บาท "
                                f"ประมาณค่าราคาแต่ละอย่างเป็นจำนวนเต็มพันก่อน "
                                f"แล้วหาว่าซื้อทั้งสองอย่างต้องจ่ายประมาณกี่บาท"),
                        # The exact total, and each rounded down instead.
                        distractors=_story.keep(a + b, a // 1000 * 1000 + b // 1000 * 1000,
                                                ans + 1000, answer=ans))


# ── More estimating (2026-11): a difference, a quotient, which number rounds to a value, the largest and
# smallest numbers that round to a value, and a bill rounded to hundreds ──

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402
from otk.core.content import text as _text_block  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _round_half_up(n: int, place: int) -> int:
    return (n + place // 2) // place * place


_PLACE_NAMES = {10: "หลักสิบ", 100: "หลักร้อย", 1000: "หลักพัน"}


@question_type("math.estimate_difference_p4", display_name={"th": "ประมาณผลลบ"},
               level=LEVEL, topic="การประมาณค่า")
class EstimateDifferenceP4(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(30_000, 99_000)
        b = rng.randint(10_000, a - 5_000)
        right = _round_half_up(a, 1000) - _round_half_up(b, 1000)
        prompt = f"ประมาณผลลบของ {a:,} − {b:,} โดยปัดแต่ละจำนวนเป็นจำนวนเต็มพันก่อน"
        # The exact difference rounded; numbers cut down instead of rounded; a thousand off.
        exact = _round_half_up(a - b, 1000)
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(exact if exact != right else exact + 1000, a // 1000 * 1000 - b // 1000 * 1000,
                                        right + 1000, right - 1000, answer=right, lo=0))


@question_type("math.estimate_quotient_p4", display_name={"th": "ประมาณผลหาร"},
               level=LEVEL, topic="การประมาณค่า")
class EstimateQuotientP4(WordProblem):
    def expr(self, rng: Random):
        b = rng.randint(2, 9)
        q = rng.randint(2, 9)
        target = b * q * 100
        n = target + rng.randint(-49, 49)
        right = target // b
        prompt = f"ประมาณผลหารของ {n:,} ÷ {b} โดยปัด {n:,} เป็นจำนวนเต็มร้อยก่อน"
        # Divided by ten too many or too few; the rounded dividend itself.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(right * 10, right // 10, target, right + 100, answer=right, lo=1))


@question_type("math.rounds_to_p4", display_name={"th": "จำนวนใดปัดแล้วได้ค่าที่กำหนด"},
               level=LEVEL, topic="การประมาณค่า")
class RoundsToP4(QuestionType):
    """Fixed choices: a number from another draw could also round to the value."""

    def build(self, rng: Random):
        place = rng.choice((100, 1000))
        value = rng.randint(12, 98) * place
        right = value + rng.randint(-place // 2, place // 2 - 1)
        # Just past each half-way point, and one a whole place away.
        wrongs = [value + place // 2, value - place // 2 - 1, value + place + rng.randint(0, place // 2 - 1)]
        return _fixed_maths([_text_block(f"จำนวนใดเมื่อปัดเป็น{_PLACE_NAMES[place]}แล้วได้ {value:,}")], _g(right),
                            [_g(w) for w in wrongs], self.topic)


@question_type("math.largest_rounding_to_p4", display_name={"th": "จำนวนที่มากที่สุดที่ปัดแล้วได้ค่าที่กำหนด"},
               level=LEVEL, topic="การประมาณค่า")
class LargestRoundingToP4(WordProblem):
    def expr(self, rng: Random):
        place = rng.choice((10, 100))
        value = rng.randint(12, 98) * place
        right = value + place // 2 - 1
        prompt = f"จำนวนนับที่มากที่สุดที่ปัดเป็น{_PLACE_NAMES[place]}แล้วได้ {value:,} คือจำนวนใด"
        # The half-way point itself (it rounds up); the value; one place on.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(value + place // 2, value, value + place - 1, right - 1, answer=right, lo=1))


@question_type("math.smallest_rounding_to_p4", display_name={"th": "จำนวนที่น้อยที่สุดที่ปัดแล้วได้ค่าที่กำหนด"},
               level=LEVEL, topic="การประมาณค่า")
class SmallestRoundingToP4(WordProblem):
    def expr(self, rng: Random):
        place = rng.choice((10, 100))
        value = rng.randint(12, 98) * place
        right = value - place // 2
        prompt = f"จำนวนนับที่น้อยที่สุดที่ปัดเป็น{_PLACE_NAMES[place]}แล้วได้ {value:,} คือจำนวนใด"
        # One below the half-way point (it rounds down); the value; one place back.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(right - 1, value, value - place + 1, right + 1, answer=right, lo=1))


@question_type("math.estimate_bill_p4", display_name={"th": "ประมาณราคารวมโดยปัดเป็นจำนวนเต็มร้อย"},
               level=LEVEL, topic="การประมาณค่า")
class EstimateBillP4(WordProblem):
    def expr(self, rng: Random):
        prices = [rng.randint(110, 980) for _ in range(3)]
        right = sum(_round_half_up(p, 100) for p in prices)
        items = rng.sample(("พัดลม", "หม้อ", "รองเท้า", "กระเป๋า", "เสื้อ", "นาฬิกา"), 3)
        prompt = ("แม่ซื้อ" + " ".join(f"{i}ราคา {p} บาท" for i, p in zip(items, prices))
                  + " ประมาณราคารวมโดยปัดราคาแต่ละอย่างเป็นจำนวนเต็มร้อย ได้ประมาณกี่บาท")
        # Prices cut down instead of rounded; the exact total; a hundred off.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(sum(p // 100 * 100 for p in prices), sum(prices), right + 100, right - 100,
                                        answer=right, lo=1))
