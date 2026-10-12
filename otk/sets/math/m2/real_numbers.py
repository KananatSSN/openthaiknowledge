"""จำนวนจริง

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ม.2/*

Sets moved here from: math, math_algebra, math_apply_basic, math_m2, math_number.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem, frac_tex
from otk.sets._support.math_algebra import _surd
from otk.sets._support.math_apply_add import _root
from otk.sets._support.math_m2 import LEVEL
from otk.sets._support.math_p4 import grouped

PROVENANCE = Provenance("original")


_REAL_TOPIC = "จำนวนจริง"


@question_type("math.classify_real_number",
               display_name={"th": "จำแนกจำนวนตรรกยะ/อตรรกยะ"}, level={"th": "ม.2"},
               topic="จำนวนจริง")
class ClassifyRealNumber(ChoiceType):
    def compose(self, rng: Random):
        kind = rng.choice(["fraction", "sqrt_nonsquare", "sqrt_square",
                           "repeating", "pi"])
        if kind == "fraction":
            rep, label = f"{rng.randint(1, 9)}/{rng.randint(2, 9)}", "จำนวนตรรกยะ"
        elif kind == "sqrt_nonsquare":
            n = rng.choice([2, 3, 5, 6, 7, 8, 10, 11, 12, 13, 15])
            rep, label = f"√{n}", "จำนวนอตรรกยะ"
        elif kind == "sqrt_square":
            rep, label = f"√{rng.choice([4, 9, 16, 25, 36, 49])}", "จำนวนตรรกยะ"
        elif kind == "repeating":
            d = rng.choice([1, 2, 3, 6, 7])
            rep, label = f"0.{d}{d}{d}...", "จำนวนตรรกยะ"
        else:
            rep, label = "π", "จำนวนอตรรกยะ"
        other = "จำนวนอตรรกยะ" if label == "จำนวนตรรกยะ" else "จำนวนตรรกยะ"
        return f"{rep} เป็นจำนวนชนิดใด?", label, [other]


@question_type("math.nth_root",
               display_name={"th": "รากที่สอง / รากที่สาม"}, level={"th": "ม.2"},
               topic="จำนวนจริง")
class NthRoot(MathType):
    def expr(self, rng: Random):
        root = rng.choice([2, 3])
        n = rng.randint(2, 12 if root == 2 else 6)
        big = n ** root
        problem = rf"\sqrt{{{big}}}" if root == 2 else rf"\sqrt[3]{{{big}}}"
        return MathDraw(problem, str(n),
                        prompt="จงหาค่า",
                        distractors=[str(big // root), str(n + 1), str(n - 1)])


@question_type("math.roots_of_perfect_powers_m2",
               display_name={"th": "รากที่สองและรากที่สามของจำนวนตรรกยะ"},
               level=LEVEL, topic=_REAL_TOPIC)
class RootsOfPerfectPowersM2(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        kind = rng.randrange(4)
        if kind == 0:
            n = rng.randint(2, 10) * rng.choice((1, -1))
            return MathDraw(rf"\sqrt[3]{{{n ** 3}}}", str(n), prompt="จงหาค่า",
                            # A cube root of a negative number is negative.
                            distractors=_story.keep(-n, n * n, 3 * n, n ** 3 // 3 if n ** 3 % 3 == 0
                                                    else n + 1, answer=n, lo=-9999))
        if kind == 1:
            n = rng.randint(2, 9)
            return MathDraw(rf"\sqrt{{0.{n * n:02d}}}" if n * n < 100 else rf"\sqrt{{{n * n}}}",
                            f"0.{n}", prompt="จงหาค่า",
                            distractors=[f"0.0{n}", str(n), f"0.{n * n:02d}".rstrip("0")])
        if kind == 2:
            a, b = rng.sample(range(1, 13), 2)
            f = Fraction(a * a, b * b)
            return MathDraw(rf"\sqrt{{\frac{{{a * a}}}{{{b * b}}}}}", frac_tex(Fraction(a, b)),
                            prompt="จงหาค่า",
                            distractors=[frac_tex(Fraction(a * a, b)) if b != 1 else str(a + 1),
                                         frac_tex(Fraction(a, b * b)), frac_tex(f / 2),
                                         frac_tex(Fraction(a + 1, b))])
        n = rng.randint(2, 6)
        return MathDraw(rf"\sqrt[3]{{-\frac{{{n ** 3}}}{{{(n + 1) ** 3}}}}}",
                        rf"-\frac{{{n}}}{{{n + 1}}}", prompt="จงหาค่า",
                        distractors=[rf"\frac{{{n}}}{{{n + 1}}}", rf"-\frac{{{n * n}}}{{{(n + 1) ** 2}}}",
                                     rf"-\frac{{{n ** 3}}}{{{3 * (n + 1)}}}"])


@question_type("math.square_root_context_m2",
               display_name={"th": "รากที่สองในสถานการณ์ (พื้นที่และความยาวด้าน)"},
               level=LEVEL, topic=_REAL_TOPIC)
class SquareRootContextM2(WordProblem):
    def expr(self, rng: Random):
        s = rng.randint(6, 40)
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(s),
                            prompt=f"สนามหญ้ารูปสี่เหลี่ยมจัตุรัสมีพื้นที่ {grouped(s * s)} ตารางเมตร ด้านยาวด้านละกี่เมตร",
                            # Halving or quartering the area instead of taking its root.
                            distractors=_story.keep(s * s // 2, s * s // 4, s + 1, 2 * s, answer=s))
        if kind == 1:
            return MathDraw("", str(4 * s),
                            prompt=f"ที่ดินรูปสี่เหลี่ยมจัตุรัสมีพื้นที่ {grouped(s * s)} ตารางเมตร ยาวรอบรูปกี่เมตร",
                            distractors=_story.keep(s, s * s // 4, 2 * s, 4 * s + 4, answer=4 * s))
        n = rng.randint(3, 20)
        return MathDraw("", str(n),
                        prompt=(f"ต้องการจัดเก้าอี้ {n * n} ตัว เป็นแถวรูปสี่เหลี่ยมจัตุรัส "
                                f"(จำนวนแถวเท่ากับจำนวนเก้าอี้ในแต่ละแถว) จะได้แถวละกี่ตัว"),
                        distractors=_story.keep(n * n // 2, n + 1, n - 1, 2 * n, answer=n))


@question_type("math.sqrt_between_integers",
               display_name={"th": "รากที่สองอยู่ระหว่างจำนวนเต็มใด"},
               level={"th": "ม.2"}, topic="จำนวนจริง")
class SqrtBetweenIntegers(MathType):
    def expr(self, rng: Random, lo: int = 3, hi: int = 14):
        k = rng.randint(lo, hi)
        # Strictly between two consecutive squares, so the answer is unambiguous.
        n = rng.randint(k * k + 1, (k + 1) ** 2 - 1)
        return MathDraw(rf"\sqrt{{{n}}}", f"{k} < \\sqrt{{{n}}} < {k + 1}",
                        prompt="จำนวนนี้อยู่ระหว่างจำนวนเต็มคู่ใด",
                        distractors=[f"{k - 1} < \\sqrt{{{n}}} < {k}",
                                     f"{k + 1} < \\sqrt{{{n}}} < {k + 2}",
                                     f"{k + 2} < \\sqrt{{{n}}} < {k + 3}"])


@question_type("math.pick_irrational", display_name={"th": "เลือกจำนวนอตรรกยะ"},
               level={"th": "ม.2"}, topic="จำนวนจริง")
class PickIrrational(WordProblem):
    """One surd among three rationals — including a surd that is *not* irrational
    because its radicand is a perfect square, which is the mistake worth making."""

    def expr(self, rng: Random, radicand_hi: int = 40):
        squares = {k * k for k in range(1, 20)}
        n = rng.choice([m for m in range(2, radicand_hi) if m not in squares])
        square = rng.choice(sorted(s for s in squares if 4 <= s <= 144))
        q = Fraction(rng.randint(1, 9), rng.randint(2, 9))
        return MathDraw("", rf"\sqrt{{{n}}}",
                        prompt="จำนวนใดเป็นจำนวนอตรรกยะ",
                        distractors=[rf"\sqrt{{{square}}}", frac_tex(q),
                                     str(rng.randint(2, 99))])


@question_type("math.simplify_sqrt",
               display_name={"th": "รากที่สองในรูปอย่างง่าย"}, level={"th": "ม.2"},
               topic="จำนวนจริง")
class SimplifySqrt(MathType):
    _CANDIDATES = [
        (8, 2, 2), (12, 2, 3), (18, 3, 2), (20, 2, 5),
        (24, 2, 6), (27, 3, 3), (28, 2, 7), (32, 4, 2),
        (40, 2, 10), (45, 3, 5), (48, 4, 3), (50, 5, 2),
        (54, 3, 6), (60, 2, 15), (63, 3, 7), (72, 6, 2),
        (75, 5, 3), (80, 4, 5), (90, 3, 10), (96, 4, 6),
        (98, 7, 2), (108, 6, 3), (125, 5, 5), (128, 8, 2),
        (147, 7, 3), (150, 5, 6), (162, 9, 2), (180, 6, 5),
        (200, 10, 2), (242, 11, 2), (243, 9, 3), (245, 7, 5),
        (250, 5, 10), (252, 6, 7), (288, 12, 2), (300, 10, 3),
        (320, 8, 5), (363, 11, 3), (392, 14, 2),
    ]

    def expr(self, rng: Random):
        n, outside, inside = rng.choice(self._CANDIDATES)
        return MathDraw(rf"\sqrt{{{n}}}", rf"{outside}\sqrt{{{inside}}}",
                        hint=r"\text{pull out pairs of primes}",
                        prompt="จงทำให้เป็นรูปอย่างง่าย")


@question_type("math.sqrt_product", display_name={"th": "คูณรากที่สองแล้วจัดรูป"},
               level={"th": "ม.2"}, topic="จำนวนจริง")
class SqrtProduct(MathType):
    """√a·√b = √(ab), then pull out the square factors — the two halves of
    simplifying a surd, in one item."""

    def expr(self, rng: Random, factor_hi: int = 12):
        a, b = rng.randint(2, factor_hi), rng.randint(2, factor_hi)
        product = a * b
        out, rest, k = 1, product, 2
        while k * k <= rest:
            while rest % (k * k) == 0:
                out *= k
                rest //= k * k
            k += 1
        answer = str(out) if rest == 1 else _surd(out, rest)
        return MathDraw(
            rf"\sqrt{{{a}}} \cdot \sqrt{{{b}}}", answer, prompt="จงจัดรูป",
            # Adding the radicands, and leaving the square factor inside.
            distractors=[_surd(1, a + b), _surd(1, product),
                         _surd(out, product)])


@question_type("math.sqrt_measure_context_m2",
               display_name={"th": "โจทย์ปัญหารากที่สองในการวัด (อยู่ในรูปอย่างง่าย)"},
               level={"th": "ม.2"}, topic="จำนวนจริง")
class SqrtMeasureContextM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(5)
        if kind == 0:
            w, h = rng.choice(((4, 2), (6, 3), (8, 4), (2, 6), (4, 8), (6, 2), (10, 5)))
            return MathDraw("", _root(w * w + h * h),
                            prompt=(f"จอภาพรูปสี่เหลี่ยมผืนผ้ากว้าง {w} ฟุต สูง {h} ฟุต เส้นทแยงมุมของจอยาวกี่ฟุต"),
                            distractors=[_root(abs(w * w - h * h)), str(w + h), str(w * h)])
        if kind == 1:
            k, r = rng.randint(2, 5), rng.choice((2, 3, 5))
            area = k * k * r
            return MathDraw("", _root(16 * area),
                            prompt=(f"สนามรูปสี่เหลี่ยมจัตุรัสมีพื้นที่ {area} ตารางเมตร ต้องล้อมรั้วรอบสนาม "
                                    f"ใช้รั้วยาวกี่เมตร"),
                            distractors=[_root(area), _root(4 * area), str(4 * area)])
        if kind == 2:
            L, d = rng.choice(((6, 2), (8, 4), (9, 3), (10, 4), (12, 6), (7, 3)))
            return MathDraw("", _root(L * L - d * d),
                            prompt=(f"บันไดยาว {L} เมตร พาดกับกำแพง เชิงบันไดอยู่ห่างจากกำแพง {d} เมตร "
                                    f"ปลายบันไดอยู่สูงจากพื้นกี่เมตร"),
                            distractors=[_root(L * L + d * d), str(L - d), _root(L - d)])
        if kind == 3:
            a = rng.choice((3, 5, 6, 7, 10))
            return MathDraw("", _root(2 * a * a),
                            prompt=(f"ที่ดินรูปสี่เหลี่ยมจัตุรัสยาวด้านละ {a} เมตร ทางเดินตัดเฉียงจากมุมหนึ่งไปยังมุมตรงข้าม "
                                    f"ทางเดินยาวกี่เมตร"),
                            distractors=[str(2 * a), _root(a * a), str(a * a)])
        area = rng.choice((20, 30, 45, 50, 70, 90, 110))
        lo = int(area ** 0.5)
        def between(a: int) -> str:
            return rf"{a} < \sqrt{{{area}}} < {a + 1}"

        return MathDraw("", between(lo),
                        prompt=(f"ห้องรูปสี่เหลี่ยมจัตุรัสมีพื้นที่ {area} ตารางเมตร ความยาวด้านของห้อง (√{area} เมตร) "
                                f"อยู่ระหว่างจำนวนเต็มใด"),
                        # one below, one above, and a quarter of the area (the perimeter slip)
                        distractors=[between(lo - 1), between(lo + 1), between(area // 4)])
