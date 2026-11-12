"""พื้นที่รูปสี่เหลี่ยม

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.5/*

Sets moved here from: math, math_diagrams, math_geometry, math_p5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import QUAD_FIGURES, _img, _math_q, _nums, figure_alt
from otk.sets._support.math_p5 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.parallelogram_area",
               display_name={"th": "พื้นที่สี่เหลี่ยมด้านขนาน"}, level={"th": "ป.5"},
               topic="พื้นที่รูปสี่เหลี่ยม")
class ParallelogramArea(WordProblem):
    def expr(self, rng: Random):
        base, h = rng.randint(3, 20), rng.randint(2, 15)
        prompt = rng.choice((
            f"สี่เหลี่ยมด้านขนานฐาน {base} สูง {h} หน่วย มีพื้นที่เท่าใด?",
            f"แปลงผักรูปสี่เหลี่ยมด้านขนานมีฐานยาว {base} เมตร สูง {h} เมตร "
            f"แปลงผักมีพื้นที่กี่ตารางเมตร",
            f"กระเบื้องแผ่นหนึ่งเป็นรูปสี่เหลี่ยมด้านขนาน ฐานยาว {base} เซนติเมตร สูง {h} เซนติเมตร "
            f"กระเบื้องมีพื้นที่กี่ตารางเซนติเมตร",
        ))
        return MathDraw("", str(base * h), prompt=prompt,
                        distractors=[str(base + h), str(2 * (base + h)),
                                     str(base * h // 2)])


@question_type("math.parallelogram_perimeter_p5",
               display_name={"th": "ความยาวรอบรูปสี่เหลี่ยมด้านขนานและขนมเปียกปูน"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class ParallelogramPerimeterP5(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a, b = rng.sample(range(4, 40), 2)
            ans = 2 * (a + b)
            prompt = rng.choice((
                f"รูปสี่เหลี่ยมด้านขนานมีด้านยาว {a} ซม. และ {b} ซม. ยาวรอบรูปกี่เซนติเมตร",
                f"สวนรูปสี่เหลี่ยมด้านขนานมีด้านยาว {a} เมตร และ {b} เมตร "
                f"ต้องใช้รั้วล้อมรอบสวนยาวกี่เมตร",
                f"กรอบรูปทรงสี่เหลี่ยมด้านขนานมีด้านยาว {a} ซม. และ {b} ซม. "
                f"ต้องใช้ริบบิ้นติดรอบกรอบยาวกี่เซนติเมตร",
            ))
            return MathDraw("", str(ans), prompt=prompt,
                            distractors=_story.keep(a + b, a * b, 2 * a + b, answer=ans))
        s = rng.randint(4, 30)
        prompt = rng.choice((
            f"รูปสี่เหลี่ยมขนมเปียกปูนยาวรอบรูป {4 * s} ซม. ด้านยาวด้านละกี่เซนติเมตร",
            f"ดัดลวดยาว {4 * s} ซม. เป็นรูปสี่เหลี่ยมขนมเปียกปูนได้พอดี แต่ละด้านยาวกี่เซนติเมตร",
        ))
        return MathDraw("", str(s), prompt=prompt,
                        distractors=_story.keep(2 * s, 4 * s, s + 4, answer=s, lo=1))


@question_type("math.quadrilateral_area_figure_p5",
               display_name={"th": "หาพื้นที่รูปสี่เหลี่ยมด้านขนานและคางหมูจากรูป"},
               level={"th": "ป.5"}, topic="พื้นที่รูปสี่เหลี่ยม")
class QuadrilateralAreaFigureP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(QUAD_FIGURES)
        if f.kind == "para":
            b, h, s = f.dims
            ans = b * h
            # The slanted side used as the height.
            wrongs = _nums(b * s, (b + s) * 2, b * h // 2 if b * h % 2 == 0 else b + h, answer=ans, lo=1)
            ask = "รูปสี่เหลี่ยมด้านขนานนี้มีพื้นที่กี่ตารางเซนติเมตร"
        else:
            a, b, h = f.dims
            ans = (a + b) * h // 2
            if (a + b) * h % 2:
                ans = None
            wrongs = _nums((a + b) * h, a * b, b * h, answer=ans or 0, lo=1)
            ask = "รูปสี่เหลี่ยมคางหมูนี้มีพื้นที่กี่ตารางเซนติเมตร"
            if ans is None:
                return self.build(rng)
        return _math_q([text(ask), _img(f.asset_id, figure_alt(f))], str(ans), wrongs, self.topic)


@question_type("math.trapezoid_area", display_name={"th": "พื้นที่รูปสี่เหลี่ยมคางหมู"},
               level={"th": "ป.5"}, topic="พื้นที่รูปสี่เหลี่ยม")
class TrapezoidArea(WordProblem):
    def expr(self, rng: Random, side_lo: int = 4, side_hi: int = 20):
        a, b = rng.randint(side_lo, side_hi), rng.randint(side_lo, side_hi)
        h = rng.randrange(2, 16, 2)               # even, so the half is whole
        area = (a + b) * h // 2
        prompt = rng.choice((
            f"รูปสี่เหลี่ยมคางหมูมีด้านคู่ขนานยาว {a} และ {b} เซนติเมตร "
            f"สูง {h} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร",
            f"สนามหญ้ารูปสี่เหลี่ยมคางหมูมีด้านคู่ขนานยาว {a} และ {b} เมตร "
            f"ด้านคู่ขนานห่างกัน {h} เมตร สนามหญ้ามีพื้นที่กี่ตารางเมตร",
            f"ผนังด้านข้างของโรงรถเป็นรูปสี่เหลี่ยมคางหมู มีด้านคู่ขนานยาว {a} และ {b} ฟุต "
            f"สูง {h} ฟุต ต้องทาสีผนังนี้กี่ตารางฟุต",
        ))
        return MathDraw(
            "", str(area), prompt=prompt,
            hint=r"\frac{1}{2}(a + b)h",
            distractors=[str((a + b) * h), str(a * b), str(a * h)])


@question_type("math.rhombus_kite_area_p5",
               display_name={"th": "พื้นที่รูปสี่เหลี่ยมขนมเปียกปูนและรูปว่าว (เส้นทแยงมุม)"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class RhombusKiteAreaP5(WordProblem):
    def expr(self, rng: Random):
        d1, d2 = 2 * rng.randint(2, 15), rng.randint(3, 30)
        shape = rng.choice(("สี่เหลี่ยมขนมเปียกปูน", "รูปว่าว"))
        ans = d1 * d2 // 2
        if rng.random() < 0.6:
            return MathDraw("", str(ans),
                            prompt=(f"รูป{shape.removeprefix('รูป')}มีเส้นทแยงมุมยาว {d1} ซม. และ {d2} ซม. "
                                    f"มีพื้นที่กี่ตารางเซนติเมตร"),
                            # Forgetting the half.
                            distractors=_story.keep(named("area.forgot_half", d1 * d2),
                                                    named("operation.reversed", d1 + d2),
                                                    2 * (d1 + d2), answer=ans))
        return MathDraw("", str(d2),
                        prompt=(f"รูป{shape.removeprefix('รูป')}มีพื้นที่ {ans} ตารางเซนติเมตร "
                                f"เส้นทแยงมุมเส้นหนึ่งยาว {d1} ซม. เส้นทแยงมุมอีกเส้นยาวกี่เซนติเมตร"),
                        distractors=_story.keep(ans // d1 if ans % d1 == 0 else d2 + 2, ans - d1,
                                                2 * ans, answer=d2, lo=1))


from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p5 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _dec(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_dec(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


# ── More quadrilateral areas (2026-11): a parallelogram's height, a trapezoid's missing side, a rhombus from
# its diagonals, the largest of four shapes, and the cost of tiling ──


@question_type("math.parallelogram_height_p5", display_name={"th": "หาความสูงของรูปสี่เหลี่ยมด้านขนาน"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class ParallelogramHeightP5(WordProblem):
    def expr(self, rng: Random):
        base, h = rng.randint(4, 30), rng.randint(3, 25)
        area = base * h
        prompt = f"รูปสี่เหลี่ยมด้านขนานมีพื้นที่ {area} ตารางเซนติเมตร ฐานยาว {base} เซนติเมตร สูงกี่เซนติเมตร"
        # Halved as for a triangle; the area less the base; doubled.
        return MathDraw("", str(h), prompt=prompt,
                        distractors=_story.keep(2 * h, area - base, h // 2 if h > 2 else h + 2, h + 1,
                                                answer=h, lo=1))


@question_type("math.trapezoid_missing_side_p5", display_name={"th": "หาความยาวด้านคู่ขนานของรูปสี่เหลี่ยมคางหมู"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class TrapezoidMissingSideP5(WordProblem):
    def expr(self, rng: Random):
        h = rng.randint(2, 15) * 2
        a, b = rng.sample(range(3, 30), 2)
        area = (a + b) * h // 2
        prompt = (f"รูปสี่เหลี่ยมคางหมูมีพื้นที่ {area} ตารางเซนติเมตร สูง {h} เซนติเมตร "
                  f"ด้านคู่ขนานด้านหนึ่งยาว {a} เซนติเมตร อีกด้านยาวกี่เซนติเมตร")
        # The two sides together; without halving; the known side.
        return MathDraw("", str(b), prompt=prompt,
                        distractors=_story.keep(a + b, area // h - a, a, b + 2, answer=b, lo=1))


@question_type("math.rhombus_from_diagonals_p5", display_name={"th": "พื้นที่รูปสี่เหลี่ยมขนมเปียกปูนจากเส้นทแยงมุม"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class RhombusFromDiagonalsP5(WordProblem):
    def expr(self, rng: Random):
        d1 = rng.randint(2, 15) * 2
        d2 = rng.randint(3, 30)
        right = d1 * d2 // 2
        shape = rng.choice(("ขนมเปียกปูน", "รูปว่าว"))
        name = f"รูปสี่เหลี่ยม{shape}" if shape == "ขนมเปียกปูน" else shape
        prompt = f"{name}มีเส้นทแยงมุมยาว {d1} และ {d2} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร"
        # Not halved; added; the perimeter-like sum doubled.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(d1 * d2, d1 + d2, 2 * (d1 + d2), right + d1, answer=right, lo=1))


@question_type("math.largest_quadrilateral_area_p5", display_name={"th": "รูปสี่เหลี่ยมใดมีพื้นที่มากที่สุด"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class LargestQuadrilateralAreaP5(ChoiceType):
    def compose(self, rng: Random):
        while True:
            pb, ph = rng.randint(4, 15), rng.randint(3, 12)
            ta, tb, th = rng.randint(3, 12), rng.randint(3, 12), rng.randint(1, 6) * 2
            rd1, rd2 = rng.randint(2, 8) * 2, rng.randint(4, 16)
            sq = rng.randint(3, 12)
            areas = [pb * ph, (ta + tb) * th // 2, rd1 * rd2 // 2, sq * sq]
            if len(set(areas)) == 4:
                break
        texts = [f"สี่เหลี่ยมด้านขนาน ฐาน {pb} ซม. สูง {ph} ซม.",
                 f"สี่เหลี่ยมคางหมู ด้านคู่ขนาน {ta} และ {tb} ซม. สูง {th} ซม.",
                 f"สี่เหลี่ยมขนมเปียกปูน เส้นทแยงมุม {rd1} และ {rd2} ซม.",
                 f"สี่เหลี่ยมจัตุรัส ด้านยาว {sq} ซม."]
        most = rng.random() < 0.5
        pick = areas.index(max(areas) if most else min(areas))
        return (f"รูปใดมีพื้นที่{'มากที่สุด' if most else 'น้อยที่สุด'}", texts[pick],
                [t for i, t in enumerate(texts) if i != pick])


@question_type("math.tiling_cost_p5", display_name={"th": "ค่าปูพื้นรูปสี่เหลี่ยม"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class TilingCostP5(WordProblem):
    def expr(self, rng: Random):
        price = rng.choice((150, 200, 250, 300, 350, 400))
        if rng.random() < 0.5:
            base, h = rng.randint(4, 15), rng.randint(3, 10)
            area = base * h
            what = f"รูปสี่เหลี่ยมด้านขนาน ฐานยาว {base} เมตร สูง {h} เมตร"
            wrong_area = base * h // 2 if base * h % 2 == 0 else base + h
        else:
            a, b, h = rng.randint(3, 12), rng.randint(3, 12), rng.randint(1, 6) * 2
            area = (a + b) * h // 2
            what = f"รูปสี่เหลี่ยมคางหมู ด้านคู่ขนานยาว {a} และ {b} เมตร สูง {h} เมตร"
            wrong_area = (a + b) * h
        right = area * price
        prompt = f"ลานจอดรถเป็น{what} ค่าปูพื้นตารางเมตรละ {price} บาท ต้องจ่ายค่าปูพื้นกี่บาท"
        # The area worked out wrongly; the area alone; one square metre too many.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(wrong_area * price, area, right + price, right - price,
                                        answer=right, lo=1))
