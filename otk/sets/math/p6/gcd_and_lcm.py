"""ห.ร.ม. และ ค.ร.น.

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.6/*

Sets moved here from: math, math_gaps_indicators, math_number, math_p6.
"""

from __future__ import annotations

import math
import math as _math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.gcd",
               display_name={"th": "ตัวหารร่วมมาก (ห.ร.ม.)"}, level={"th": "ป.6"},
               topic="ห.ร.ม. และ ค.ร.น.")
class GCD(WordProblem):
    def expr(self, rng: Random):
        # Two random numbers share no factor more often than not, which made
        # 1 the answer to most items. Build the pair from a common factor
        # instead, and keep a coprime pair as the occasional case.
        while True:
            g = 1 if rng.random() < 0.1 else rng.randint(2, 12)
            m, n = rng.sample(range(2, 100 // g + 1), 2)
            a, b = g * m, g * n
            if math.gcd(m, n) == 1 and 12 <= min(a, b) and max(a, b) <= 100:
                break
        prompt = rng.choice((
            f"ห.ร.ม. ของ {a} และ {b} เท่ากับเท่าใด?",
            f"มีดินสอ {a} แท่ง และยางลบ {b} ก้อน แบ่งใส่ถุงให้ทุกถุงมีดินสอเท่ากันและยางลบเท่ากัน"
            f"โดยไม่เหลือเศษ แบ่งได้มากที่สุดกี่ถุง",
            f"ตัดริบบิ้นสองเส้นยาว {a} ซม. และ {b} ซม. เป็นชิ้นยาวเท่ากันให้ยาวที่สุดโดยไม่เหลือเศษ "
            f"แต่ละชิ้นยาวกี่เซนติเมตร",
        ))
        return MathDraw("", str(g), prompt=prompt,
                        distractors=[str(math.lcm(a, b)), str(abs(a - b)),
                                     str(g * 2)])


@question_type("math.lcm",
               display_name={"th": "ผลคูณร่วมน้อย (ค.ร.น.)"}, level={"th": "ป.6"},
               topic="ห.ร.ม. และ ค.ร.น.")
class LCM(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(4, 30), rng.randint(4, 30)
        prompt = rng.choice((
            f"ค.ร.น. ของ {a} และ {b} เท่ากับเท่าใด?",
            f"ไฟดวงหนึ่งกะพริบทุก {a} วินาที อีกดวงหนึ่งกะพริบทุก {b} วินาที ถ้าเพิ่งกะพริบพร้อมกัน "
            f"อีกกี่วินาทีจึงจะกะพริบพร้อมกันอีกครั้ง",
            f"รถโดยสารสายหนึ่งออกทุก {a} นาที อีกสายหนึ่งออกทุก {b} นาที ถ้าเพิ่งออกพร้อมกัน "
            f"อีกกี่นาทีจึงจะออกพร้อมกันอีกครั้ง",
        ))
        return MathDraw("", str(math.lcm(a, b)), prompt=prompt,
                        distractors=[str(math.gcd(a, b)), str(a * b),
                                     str(math.lcm(a, b) + a)])


@question_type("math.lcm_word", display_name={"th": "โจทย์ปัญหา ค.ร.น."},
               level={"th": "ป.6"}, topic="ห.ร.ม. และ ค.ร.น.")
class LcmWord(WordProblem):
    def expr(self, rng: Random, lo: int = 3, hi: int = 15):
        a, b = rng.sample(range(lo, hi + 1), 2)
        lcm = a * b // _math.gcd(a, b)
        p, q = rng.sample(("ต้นกล้า", "ใบเตย", "ภูผา", "น้ำฝน", "ก้องภพ", "แพรวา"), 2)
        prompt = rng.choice((
            f"ระฆังใบแรกตีทุก {a} นาที ใบที่สองตีทุก {b} นาที ถ้าตีพร้อมกันครั้งแรกตอนนี้ "
            f"อีกกี่นาทีจะตีพร้อมกันอีกครั้ง",
            f"ไฟกะพริบดวงแรกกะพริบทุก {a} วินาที ดวงที่สองทุก {b} วินาที ถ้ากะพริบพร้อมกันตอนนี้ "
            f"อีกอย่างน้อยกี่วินาทีจะกะพริบพร้อมกันอีกครั้ง",
            f"{p}ไปห้องสมุดทุก {a} วัน {q}ไปทุก {b} วัน วันนี้ทั้งสองคนไปพร้อมกัน "
            f"อีกอย่างน้อยกี่วันจะไปพร้อมกันอีก",
            f"รถเมล์สายแรกออกจากป้ายทุก {a} นาที สายที่สองทุก {b} นาที ถ้าออกพร้อมกันตอนนี้ "
            f"อีกอย่างน้อยกี่นาทีจะออกพร้อมกันอีกครั้ง",
            f"ต้องการจัดส้มเป็นกองละ {a} ผล หรือกองละ {b} ผล ได้พอดีทั้งสองแบบ "
            f"ต้องมีส้มอย่างน้อยกี่ผล",
        ))
        # The product, ห.ร.ม. instead of ค.ร.น., and the sum.
        return MathDraw("", str(lcm), prompt=prompt,
                        distractors=[str(x) for x in dict.fromkeys(
                            (a * b, _math.gcd(a, b), a + b, 2 * lcm)) if x != lcm])


@question_type("math.gcd_word_problem_p6",
               display_name={"th": "โจทย์ปัญหา ห.ร.ม."},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class GcdWordProblemP6(WordProblem):
    def expr(self, rng: Random):
        g = rng.randint(3, 15)
        a, b = rng.sample(range(2, 10), 2)
        while math.gcd(a, b) != 1:
            a, b = rng.sample(range(2, 10), 2)
        x, y = g * a, g * b
        kind = rng.randrange(6)
        if kind == 3:
            ans = g
            prompt = (f"แม่ค้ามีส้ม {x} ผล และมังคุด {y} ผล ต้องการแบ่งใส่ถุง ถุงละเท่า ๆ กัน "
                      f"โดยแต่ละถุงมีผลไม้ชนิดเดียวและไม่เหลือเศษ ใส่ได้ถุงละมากที่สุดกี่ผล")
        elif kind == 4:
            ans = g
            prompt = (f"พื้นห้องรูปสี่เหลี่ยมผืนผ้ากว้าง {x} เดซิเมตร ยาว {y} เดซิเมตร ต้องการปูกระเบื้อง"
                      f"รูปสี่เหลี่ยมจัตุรัสขนาดเท่ากันที่ใหญ่ที่สุดให้เต็มพอดี กระเบื้องยาวด้านละกี่เดซิเมตร")
        elif kind == 5:
            ans = a * b
            prompt = (f"พื้นห้องรูปสี่เหลี่ยมผืนผ้ากว้าง {x} เดซิเมตร ยาว {y} เดซิเมตร ปูกระเบื้อง"
                      f"รูปสี่เหลี่ยมจัตุรัสขนาดเท่ากันที่ใหญ่ที่สุดให้เต็มพอดี ต้องใช้กระเบื้องกี่แผ่น")
        elif kind == 0:
            ans = g
            prompt = (f"มีเชือกสองเส้นยาว {x} เมตร และ {y} เมตร ต้องการตัดเป็นท่อนยาวเท่า ๆ กัน "
                      f"ให้ยาวที่สุดโดยไม่เหลือเศษ แต่ละท่อนยาวกี่เมตร")
        elif kind == 1:
            ans = g
            prompt = (f"ครูมีดินสอ {x} แท่ง และยางลบ {y} ก้อน ต้องการแบ่งให้นักเรียนกลุ่มละเท่า ๆ กัน "
                      f"ทั้งดินสอและยางลบโดยไม่เหลือเศษ จะแบ่งได้มากที่สุดกี่กลุ่ม")
        else:
            ans = a + b
            prompt = (f"มีเชือกสองเส้นยาว {x} เมตร และ {y} เมตร ตัดเป็นท่อนยาวเท่า ๆ กันให้ยาวที่สุด "
                      f"โดยไม่เหลือเศษ จะได้เชือกทั้งหมดกี่ท่อน")
        lcm = x * y // g
        # ค.ร.น. in place of ห.ร.ม. is the mistake the books warn about.
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(lcm, g if ans != g else a + b, x + y, g // 2 or g + 1,
                                                x * y // (g * g) + a if ans == a * b else a + b + 1,
                                                answer=ans, lo=1))


@question_type("math.gcd_lcm_three_p6", display_name={"th": "ห.ร.ม. และ ค.ร.น. ของจำนวนนับสามจำนวน"},
               level={"th": "ป.6"}, topic="ห.ร.ม. และ ค.ร.น.")
class GcdLcmThreeP6(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            g = rng.randint(2, 12)
            while True:
                ms = rng.sample(range(2, 10), 3)
                if math.gcd(*ms) == 1 and max(ms) * g <= 120:
                    break
            nums = [g * m for m in ms]
            value = math.gcd(*nums)
            two = math.gcd(nums[0], nums[1])
            if rng.random() < 0.5:
                prompt = f"ห.ร.ม. ของ {nums[0]}, {nums[1]} และ {nums[2]} เท่ากับเท่าใด"
            else:
                prompt = (f"มีเชือกสามเส้นยาว {nums[0]}, {nums[1]} และ {nums[2]} เซนติเมตร ต้องการตัดทุกเส้นเป็น"
                          f"ท่อนยาวเท่ากันให้ยาวที่สุดโดยไม่เหลือเศษ แต่ละท่อนยาวกี่เซนติเมตร")
            # Stopping after two numbers, a common factor that is not the
            # greatest, and the ค.ร.น. instead.
            smaller = max(d for d in range(1, value) if value % d == 0) if value > 1 else value + 1
            wrongs = [two, smaller, math.lcm(*nums)]
        else:
            while True:
                nums = rng.sample(range(2, 16), 3)
                value = math.lcm(*nums)
                if value <= 360 and value != max(nums) and value < nums[0] * nums[1] * nums[2]:
                    break
            if rng.random() < 0.5:
                prompt = f"ค.ร.น. ของ {nums[0]}, {nums[1]} และ {nums[2]} เท่ากับเท่าใด"
            else:
                prompt = (f"ไฟสามดวงกะพริบทุก {nums[0]}, {nums[1]} และ {nums[2]} วินาที ถ้าเพิ่งกะพริบพร้อมกัน "
                          f"อีกกี่วินาทีจึงจะกะพริบพร้อมกันทั้งสามดวงอีกครั้ง")
            wrongs = [math.lcm(nums[0], nums[1]), nums[0] * nums[1] * nums[2], math.gcd(*nums), 2 * value]
        return MathDraw("", str(value), prompt=prompt,
                        distractors=_story.keep(*wrongs, answer=value, lo=1)[:3])


@question_type("math.gcd_lcm_relation_p6",
               display_name={"th": "ความสัมพันธ์ของ ห.ร.ม. และ ค.ร.น."},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class GcdLcmRelationP6(WordProblem):
    def expr(self, rng: Random):
        g = rng.randint(2, 12)
        a, b = rng.sample(range(2, 9), 2)
        while math.gcd(a, b) != 1:
            a, b = rng.sample(range(2, 9), 2)
        x, y = g * a, g * b
        lcm = g * a * b
        return MathDraw("", str(y),
                        prompt=(f"จำนวนสองจำนวนมี ห.ร.ม. เท่ากับ {g} และ ค.ร.น. เท่ากับ {lcm} "
                                f"ถ้าจำนวนหนึ่งคือ {x} อีกจำนวนหนึ่งคืออะไร "
                                f"(ผลคูณของสองจำนวนเท่ากับผลคูณของ ห.ร.ม. และ ค.ร.น.)"),
                        distractors=_story.keep(lcm // x if lcm % x == 0 and lcm // x != y else y + g,
                                                lcm - x, g * lcm, lcm // g, answer=y, lo=1))

from fractions import Fraction  # noqa: E402
from math import gcd  # noqa: E402

from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More ห.ร.ม. and ค.ร.น. (2026-11): how many common factors, a common multiple, the smallest square of
# tiles, and buses leaving together ──


@question_type("math.common_factors_count_p6", display_name={"th": "นับตัวประกอบร่วม"},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class CommonFactorsCountP6(WordProblem):
    def expr(self, rng: Random):
        while True:
            g = rng.choice((4, 6, 8, 9, 10, 12, 15, 16, 18, 20, 24))
            a, b = g * rng.randint(1, 6), g * rng.randint(1, 6)
            if a != b and gcd(a, b) == g:
                break
        right = sum(1 for k in range(1, g + 1) if g % k == 0)
        prompt = f"{a} และ {b} มีตัวประกอบร่วมทั้งหมดกี่จำนวน"
        # The ห.ร.ม. itself; one left out (1 or itself); the prime factors of the ห.ร.ม. only.
        primes = sum(1 for p in range(2, g + 1) if g % p == 0 and all(p % q for q in range(2, p)))
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(g, right - 1, primes, right + 1, answer=right, lo=1))


@question_type("math.common_multiple_p6", display_name={"th": "จำนวนใดเป็นพหุคูณร่วม"},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class CommonMultipleP6(QuestionType):
    """Fixed choices: a number from another draw could also be a common multiple."""

    def build(self, rng: Random, **params):
        while True:
            a, b = rng.sample((2, 3, 4, 5, 6, 8, 9, 10, 12), 2)
            if a % b and b % a:
                break
        lcm = a * b // gcd(a, b)
        right = lcm * rng.randint(1, 4)
        # A multiple of one only, the product's neighbour, and a multiple of one near the answer.
        only_a = next(v for v in range(right + a, right + 50 * a, a) if v % b)
        only_b = next(v for v in range(right + b, right + 50 * b, b) if v % a)
        wrongs = [only_a, only_b, right + 1 if (right + 1) % a or (right + 1) % b else right + 2]
        return _fixed_maths([_text_block(f"จำนวนใดเป็นพหุคูณร่วมของ {a} และ {b}")], str(right),
                            [str(w) for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.tiles_to_square_p6", display_name={"th": "เรียงกระเบื้องเป็นรูปสี่เหลี่ยมจัตุรัสที่เล็กที่สุด"},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class TilesToSquareP6(WordProblem):
    def expr(self, rng: Random):
        while True:
            a, b = rng.sample(range(2, 13), 2)
            if a * b // gcd(a, b) <= 60:
                break
        side = a * b // gcd(a, b)
        right = (side // a) * (side // b)
        prompt = (f"นำกระเบื้องรูปสี่เหลี่ยมผืนผ้ากว้าง {a} ซม. ยาว {b} ซม. มาเรียงให้เป็นรูปสี่เหลี่ยมจัตุรัส"
                  "ที่เล็กที่สุดโดยไม่ตัดกระเบื้อง ต้องใช้กระเบื้องกี่แผ่น")
        # The side of the square; the tiles along one side; the product of the sides as the side.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(side, side // a, side // b + side // a, a * b,
                                                answer=right, lo=1))


@question_type("math.buses_together_p6", display_name={"th": "รถออกพร้อมกันอีกครั้งเวลาใด"},
               level=LEVEL, topic="ห.ร.ม. และ ค.ร.น.")
class BusesTogetherP6(ChoiceType):
    def compose(self, rng: Random):
        while True:
            a, b = rng.sample((6, 8, 9, 10, 12, 15, 18, 20, 24, 30), 2)
            lcm = a * b // gcd(a, b)
            if 30 <= lcm <= 120 and lcm not in (a, b):
                break
        start = rng.randint(6, 9)

        def at(minutes: int) -> str:
            h, m = divmod(start * 60 + minutes, 60)
            return f"{h}.{m:02d} น."

        right = at(lcm)
        wrongs = [at(a * b) if a * b != lcm else at(lcm + a), at(a + b), at(lcm - gcd(a, b)), at(lcm + gcd(a, b))]
        stem = (f"รถสายแรกออกทุก {a} นาที รถสายที่สองออกทุก {b} นาที ถ้าออกพร้อมกันเวลา {start}.00 น. "
                "จะออกพร้อมกันอีกครั้งเวลาใด")
        return stem, right, [w for w in dict.fromkeys(wrongs) if w != right][:3]
