"""เศษส่วน

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.3/*

Sets moved here from: math, math_diagrams, math_number, math_p3, math_pictures_p2.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import FRACTION_PICTURES, _img, _math_q
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p3 import LEVEL
from otk.sets._support.math_pictures_p2 import P3, SHADED

PROVENANCE = Provenance("original")


FRACTION_ALT = "รูปที่แบ่งเป็นส่วนเท่า ๆ กัน และแรเงาไว้บางส่วน"


def _inline(*parts) -> list:
    """Text with fractions set as fractions: strings become text blocks, and
    an ``(n, d)`` pair becomes a stacked \\frac."""
    return [text(x.strip()) if isinstance(x, str) else content_math(rf"\frac{{{x[0]}}}{{{x[1]}}}")
            for x in parts if not isinstance(x, str) or x.strip()]


def frac_tex(a: int, b: int) -> str:
    """Unreduced on purpose: 2 of 4 balloons is 2/4 at ป.3."""
    return rf"\frac{{{a}}}{{{b}}}"


@question_type("math.read_fraction",
               display_name={"th": "อ่านเศษส่วนจากรูปแรเงา"}, level={"th": "ป.3"},
               topic="เศษส่วน")
class ReadFraction(WordProblem):
    def expr(self, rng: Random):
        d = rng.randint(2, 8)
        n = rng.randint(1, d - 1)
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"รูปแบ่งเป็น {d} ส่วนเท่ากัน แรเงา {n} ส่วน เขียนเป็นเศษส่วนได้เท่าใด?",
            f"{p}ตัดพิซซ่าถาดหนึ่งเป็น {d} ชิ้นเท่า ๆ กัน แล้วกินไป {n} ชิ้น "
            f"{p}กินพิซซ่าไปเศษเท่าใดของถาด",
            f"ช็อกโกแลตแท่งหนึ่งแบ่งเป็น {d} ช่องเท่า ๆ กัน {p}หักไปกิน {n} ช่อง "
            f"{p}กินไปเศษเท่าใดของแท่ง",
            f"ริบบิ้นเส้นหนึ่งแบ่งเป็น {d} ส่วนเท่า ๆ กัน ใช้ไป {n} ส่วน ใช้ไปเศษเท่าใดของริบบิ้น",
        ))
        return MathDraw(
            "", rf"\frac{{{n}}}{{{d}}}", prompt=prompt,
            distractors=[rf"\frac{{{d}}}{{{n}}}", rf"\frac{{{n}}}{{{d - 1}}}",
                         rf"\frac{{{n + 1}}}{{{d}}}"])


@question_type("math.fraction_picture_p3", display_name={"th": "เขียนเศษส่วนแทนส่วนที่แรเงา"},
               level={"th": "ป.3"}, topic="เศษส่วน")
class FractionPictureP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(FRACTION_PICTURES)
        n, d = f.n, f.d
        ask_unshaded = rng.random() < 0.3
        want = d - n if ask_unshaded else n
        tex = lambda a, b: rf"\frac{{{a}}}{{{b}}}"
        # Upside down, shaded over unshaded, and the other part.
        wrongs = [tex(d, want), tex(want, d - want) if d - want else tex(want, d + 1),
                  tex(d - want, d), tex(want, d + 1)]
        ask = "ส่วนที่ไม่แรเงา" if ask_unshaded else "ส่วนที่แรเงา"
        return _math_q([text(f"เศษส่วนใดแทน{ask}ของรูปนี้"), _img(f.asset_id, FRACTION_ALT)],
                       tex(want, d), wrongs, self.topic)


@question_type("math.like_fractions_addsub",
               display_name={"th": "บวก/ลบเศษส่วน (ตัวส่วนเท่ากัน)"},
               level={"th": "ป.3"}, topic="เศษส่วน")
class LikeFractionsAddSub(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, den_hi: int = 12):
        d = rng.randint(3, den_hi)
        n1, n2 = rng.randint(1, d - 1), rng.randint(1, d - 1)
        if rng.random() < 0.5:
            op, res = "+", n1 + n2
        else:
            op, res = "-", abs(n1 - n2)
            n1, n2 = max(n1, n2), min(n1, n2)
        if op == "+":
            res = n1 + n2
        return MathDraw(
            rf"\frac{{{n1}}}{{{d}}} {op} \frac{{{n2}}}{{{d}}}",
            rf"\frac{{{res}}}{{{d}}}",
            distractors=[rf"\frac{{{res}}}{{{2 * d}}}",
                         rf"\frac{{{res + 1}}}{{{d}}}",
                         rf"\frac{{{n1 + n2 if op == '+' else abs(n1 - n2)}}}"
                         rf"{{{d + d}}}"])


@question_type("math.compare_fractions_p3",
               display_name={"th": "เปรียบเทียบเศษส่วน (ตัวส่วนเท่ากัน หรือตัวเศษเท่ากัน)"},
               level=LEVEL, topic="เศษส่วน")
class CompareFractionsP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        most = rng.random() < 0.5
        if rng.random() < 0.5:
            # Kept as (numerator, denominator) pairs, never reduced: 4/8 must
            # stay 4/8 on the page.
            d = rng.randint(5, 12)
            pairs = [(n, d) for n in rng.sample(range(1, d), 4)]
            order = sorted(pairs, key=lambda p: Fraction(*p), reverse=most)
            # For a shared denominator there is no tempting wrong rule, so the
            # neighbour in size goes first.
            pick, lure = order[0], order[1]
        else:
            n = rng.randint(1, 5)
            pairs = [(n, x) for x in rng.sample(range(n + 1, 13), 4)]
            order = sorted(pairs, key=lambda p: Fraction(*p), reverse=most)
            # "Bigger denominator, bigger fraction" picks the opposite end.
            pick, lure = order[0], order[-1]
        tex = lambda p: rf"\frac{{{p[0]}}}{{{p[1]}}}"
        wrongs = [lure] + [p for p in pairs if p not in (pick, lure)]
        return _maths([text(f"เศษส่วนใด{'มากที่สุด' if most else 'น้อยที่สุด'}")],
                      tex(pick), [tex(p) for p in wrongs], self.topic)


@question_type("math.fraction_of_group_p3", display_name={"th": "เศษส่วนของกลุ่มสิ่งของ"},
               level=P3, topic="เศษส่วน")
class FractionOfGroupP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SHADED)
        red = rng.random() < 0.5
        k = s.k if red else s.n - s.k
        colour = "สีแดง" if red else "สีฟ้า"
        img = image(s.asset_id, alt="ภาพลูกโป่งสีแดงและสีฟ้า")
        # The other colour; this colour over the other (part to part); upside down.
        pairs = [(s.n - k, s.n), (k, s.n - k), (s.n, k), (k, s.n + 1), (k + 1, s.n),
                 (k, s.n + 2), (s.n - k + 1, s.n + 1)]
        # "6/1" reads as a slip in the question, not as a tempting answer.
        wrongs = [frac_tex(a, b) for a, b in pairs if b != 1 and (a, b) != (k, s.n)]
        return _math_q([text(f"ลูกโป่ง{colour}คิดเป็นเศษส่วนเท่าใดของลูกโป่งทั้งหมด"), img],
                       frac_tex(k, s.n), wrongs, self.topic)


@question_type("math.equivalent_fraction", display_name={"th": "เศษส่วนที่เท่ากัน"},
               level={"th": "ป.3"}, topic="เศษส่วน")
class EquivalentFraction(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, den_hi: int = 9, scale_hi: int = 6):
        q = rng.randint(2, den_hi)
        p = rng.randint(1, q - 1)
        k = rng.randint(2, scale_hi)
        # Shown as written, not reduced: the point is to see p/q scale to pk/qk.
        return MathDraw(rf"\frac{{{p}}}{{{q}}}", rf"\frac{{{p * k}}}{{{q * k}}}",
                        prompt="เศษส่วนใดเท่ากับเศษส่วนที่กำหนด",
                        distractors=[rf"\frac{{{p * k}}}{{{q}}}",
                                     rf"\frac{{{p}}}{{{q * k}}}",
                                     rf"\frac{{{p + k}}}{{{q + k}}}"])


@question_type("math.fraction_word_problem_p3",
               display_name={"th": "โจทย์ปัญหาการบวกลบเศษส่วน (ตัวส่วนเท่ากัน)"},
               level=LEVEL, topic="เศษส่วน")
class FractionWordProblemP3(QuestionType):
    """Fractions of one whole — a pizza, a fence, a road — with one denominator.
    Answers stay unreduced, as the ป.3 books leave them, and no wrong choice
    has the right value in another form."""

    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(_story.NAMES)
        d = rng.randint(5, 12)
        a = rng.randint(1, d - 3)
        b = rng.choice([x for x in range(1, d - a) if x != a])
        f = lambda n: rf"\frac{{{n}}}{{{d}}}"
        kind = rng.randrange(4)
        # Adding the denominators too is the mistake every kind offers.
        if kind == 0:
            stem = _inline(f"{p}เดินออกกำลังกายวันแรก", (a, d), "กิโลเมตร วันที่สองเดิน", (b, d),
                           f"กิโลเมตร สองวัน{p}เดินได้ทั้งหมดกี่กิโลเมตร")
            n, wrongs = a + b, [rf"\frac{{{a + b}}}{{{2 * d}}}", f(abs(a - b)), f(a + b + 1)]
        elif kind == 1:
            big, small = max(a, b), min(a, b)
            stem = _inline(f"{p}มีเชือกยาว", (big, d), "เมตร ตัดไปใช้", (small, d),
                           "เมตร เหลือเชือกยาวกี่เมตร")
            n, wrongs = big - small, [f(big + small), rf"\frac{{{big + small}}}{{{2 * d}}}",
                                      f(big - small + 1)]
        elif kind == 2:
            stem = _inline(f"แม่แบ่งพิซซ่าถาดหนึ่งเป็น {d} ชิ้นเท่า ๆ กัน {p}กิน", (a, d),
                           "ถาด น้องกิน", (b, d), "ถาด เหลือพิซซ่าเท่าใดของถาด")
            n, wrongs = d - a - b, [f(a + b), f(d - a), rf"\frac{{{d - a - b}}}{{{2 * d}}}"]
        else:
            stem = _inline(f"{p}ทาสีรั้ววันแรกได้", (a, d), "ของรั้ว วันที่สองทาได้", (b, d),
                           "ของรั้ว ยังไม่ได้ทาสีอีกเท่าใดของรั้ว")
            n, wrongs = d - a - b, [f(a + b), f(d - b), rf"\frac{{{a + b}}}{{{2 * d}}}"]
        right = f(n)
        value = Fraction(n, d)

        def val(tex: str) -> Fraction:
            num, den = tex.removeprefix(r"\frac{").removesuffix("}").split("}{")
            return Fraction(int(num), int(den)) if int(den) else Fraction(-1)

        # A neighbour on each side keeps four choices when two mistakes coincide.
        wrongs += [f(n + 1), f(n - 1)]
        wrongs = [w for w in dict.fromkeys(wrongs)
                  if w != right and val(w) > 0 and val(w) != value]
        return _maths(stem, right, wrongs, self.topic)
