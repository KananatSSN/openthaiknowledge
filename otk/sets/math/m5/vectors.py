"""เวกเตอร์

คณิตศาสตร์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ค เพิ่มเติม การวัดและเรขาคณิต 2 ม.5/1

Sets moved here from: math, math_apply_add, math_bank_vectors, math_chapters, math_geometry, math_m5, math_pictures_add.
"""

from __future__ import annotations

from fractions import Fraction
from math import isqrt
from random import Random

from otk.core.content import image, text
from otk.core.content import math as content_math
from otk.core.distractors import fixed, redraw_until_full
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem, frac_tex, sqrt_tex
from otk.sets._support.math_apply_add import M5 as M5_math_apply_add
from otk.sets._support.math_apply_add import _c
from otk.sets._support.math_bank_trig import simplify_root, surd_tex
from otk.sets._support.math_bank_vectors import Vec, cross, dot
from otk.sets._support.math_chapters import M6, _distinct, _surd_bump, _surd_tex
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_geometry import _TRIPLES as _TRIPLES_math_geometry
from otk.sets._support.math_m4 import maths as _maths_math_m5
from otk.sets._support.math_m5 import _vec
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_pictures_add import VECTOR_GRIDS, _q, _sqrt

_TRIPLES = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (7, 24, 25), (9, 12, 15), (12, 16, 20))


def _hyp(x: int, y: int) -> int:
    """The whole-number hypotenuse if there is one, else x + y (a distractor slot)."""
    h = isqrt(x * x + y * y)
    return h if h * h == x * x + y * y else x + y + 1


M5 = {"th": "ม.5"}


TOPIC = "เวกเตอร์"


E = {"i": (1, 0, 0), "j": (0, 1, 0), "k": (0, 0, 1)}


def _tex_q(stem: list, right: str, wrongs: list[str], topic: str) -> GeneratedQuestion:
    """Named mistakes first; duplicates and the answer itself dropped; three kept."""
    wrongs = [w for w in dict.fromkeys(wrongs) if w != right][:3]
    return GeneratedQuestion(stem=stem, correct=[content_math(right)],
                             distractors=fixed(*[[content_math(w)] for w in wrongs]), topic=topic)


def _frac_q(stem: list, right: Fraction, named: list, topic: str) -> GeneratedQuestion:
    out: list[str] = []
    for w in [*named, -right, right + 1, right - 1, right + 2, right * 2, right - 2]:
        t = frac_tex(Fraction(w))
        if t != frac_tex(right) and t not in out:
            out.append(t)
    return _tex_q(stem, frac_tex(right), out, topic)


def sub(b, a) -> Vec:
    return tuple(x - y for x, y in zip(b, a))


def add(*vs) -> Vec:
    return tuple(sum(c) for c in zip(*vs))


def length_tex(n2: int, half: bool = False) -> str:
    """√n2 (or ½√n2) simplified; a zero length (a degenerate distractor) is 0."""
    if n2 == 0:
        return "0"
    k, m = simplify_root(n2)
    return surd_tex(Fraction(k, 2 if half else 1), m)


def ijk_tex(v) -> str:
    """2\\vec{i} - \\vec{j} + \\vec{k}; zero components dropped."""
    out = ""
    for c, e in zip(v, "ijk"):
        if c == 0:
            continue
        mag = "" if abs(c) == 1 else str(abs(c))
        if not out:
            out = ("-" if c < 0 else "") + rf"{mag}\vec{{{e}}}"
        else:
            out += f" {'-' if c < 0 else '+'} " + rf"{mag}\vec{{{e}}}"
    return out or r"\vec{0}"


def pt_tex(name: str, p) -> str:
    return f"{name}({p[0]}, {p[1]}, {p[2]})"


def _small(rng: Random, lo: int = -3, hi: int = 3) -> Vec:
    return tuple(rng.randint(lo, hi) for _ in range(3))


#: (TeX with a, b, c; its value as a multiple of D = a · (b × c)).
TRIPLE_FORMS = (
    (r"(\vec{a} \times \vec{c}) \cdot (\vec{a} + \vec{b} + \vec{c})", -1),
    (r"(\vec{a} \times \vec{b}) \cdot (\vec{a} + \vec{c})", 1),
    (r"(\vec{c} \times \vec{a}) \cdot (\vec{b} - \vec{a})", 1),
    (r"(\vec{b} \times \vec{a}) \cdot (2\vec{c})", -2),
    (r"\vec{b} \cdot (\vec{a} \times \vec{c})", -1),
    (r"(\vec{a} + \vec{b}) \cdot (\vec{b} \times \vec{c})", 1),
)


def perpendicular_parameter(u, v, w1: int, w2: int) -> Fraction | None:
    """a with (u × v) ⊥ (w1, w2, a); None when the third component of u × v is 0."""
    n = cross(u, v)
    if n[2] == 0:
        return None
    return Fraction(-(n[0] * w1 + n[1] * w2), n[2])


def cos_from_sum_ratio(k: int, minus: bool) -> Fraction:
    """cos θ for unit u, v (not parallel) with |u ± v|² = k|u × v|².

    |u + v|² = 2(1 + c), |u × v|² = (1 − c)(1 + c), so 2 = k(1 − c); with minus, 2 = k(1 + c).
    """
    return Fraction(2, k) - 1 if minus else 1 - Fraction(2, k)


#: Statements about arbitrary 3-D vectors: (TeX, always true).
VECTOR_FACTS = (
    (r"(\vec{u} \times \vec{v}) \cdot \vec{w} = \vec{u} \cdot (\vec{v} \times \vec{w})", True),
    (r"(\vec{u} - \vec{v}) \cdot (\vec{u} + \vec{v}) = |\vec{u}|^{2} - |\vec{v}|^{2}", True),
    (r"(\vec{u} - \vec{v}) \times (\vec{u} + \vec{v}) = 2(\vec{u} \times \vec{v})", True),
    (r"\vec{u} \cdot (\vec{u} \times \vec{v}) = 0", True),
    (r"|\vec{u} \cdot \vec{v}|^{2} + |\vec{u} \times \vec{v}|^{2} = |\vec{u}|^{2}|\vec{v}|^{2}", True),
    (r"(\vec{u} + \vec{v}) \times \vec{w} = \vec{u} \times \vec{w} + \vec{v} \times \vec{w}", True),
    (r"\vec{u} \times \vec{v} = -(\vec{v} \times \vec{u})", True),
    (r"(\vec{u} \times \vec{v}) \times \vec{w} = \vec{u} \times (\vec{v} \times \vec{w})", False),
    (r"(\vec{u} + \vec{v}) \times (\vec{u} - \vec{v}) = 2(\vec{u} \times \vec{v})", False),
    (r"\vec{u} \times \vec{v} = \vec{v} \times \vec{u}", False),
    (r"|\vec{u} \times \vec{v}| = |\vec{u}||\vec{v}|", False),
    (r"|\vec{u} + \vec{v}| = |\vec{u}| + |\vec{v}|", False),
    (r"(\vec{u} \cdot \vec{v})\vec{w} = \vec{u}(\vec{v} \cdot \vec{w})", False),
)


def triangle_area_sq4(a, b, c) -> int:
    """(2·area)² = |AB × AC|² for triangle ABC."""
    n = cross(sub(b, a), sub(c, a))
    return dot(n, n)


def perpendicular_x(a, b, c, d_rest: tuple[int, int]) -> Fraction | None:
    """x with AB ⊥ CD for D = (x, d_rest); None if AB has no x-component."""
    ab = sub(b, a)
    if ab[0] == 0:
        return None
    rest = ab[1] * (d_rest[0] - c[1]) + ab[2] * (d_rest[1] - c[2])
    return Fraction(-rest, ab[0]) + c[0]


def angle_cos(a, b, c) -> tuple[int, int, int]:
    """cos ∠ABC = BA · BC / √(|BA|²|BC|²), as (dot, |BA|², |BC|²)."""
    ba, bc = sub(a, b), sub(c, b)
    return dot(ba, bc), dot(ba, ba), dot(bc, bc)


def cos_tex(d: int, n1: int, n2: int) -> str:
    k, m = simplify_root(n1 * n2)
    return surd_tex(Fraction(d, k * m), m)


def _cross(u, v):
    return [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]


VEC_ALT = "ลูกศรสองเส้นบนระนาบพิกัดฉากที่มีเส้นตาราง เริ่มที่จุดกำเนิด กำกับด้วย u และ v"


def _pair(x: int, y: int) -> str:
    return f"({x}, {y})"


@question_type("math.vector_add", display_name={"th": "การบวกเวกเตอร์"},
               level={"th": "ม.6"}, topic="เวกเตอร์")
class VectorAdd(MathType):
    def expr(self, rng: Random, lo: int = -9, hi: int = 9):
        a = (rng.randint(lo, hi), rng.randint(lo, hi))
        b = (rng.randint(lo, hi), rng.randint(lo, hi))
        s = rng.randint(2, 4)
        total = (a[0] + s * b[0], a[1] + s * b[1])
        return MathDraw(
            rf"\vec{{u}} = ({a[0]}, {a[1]}), \; \vec{{v}} = ({b[0]}, {b[1]})",
            f"({total[0]}, {total[1]})",
            prompt=f"จงหา u + {s}v",
            distractors=[f"({a[0] + b[0]}, {a[1] + b[1]})",
                         f"({s * a[0] + b[0]}, {s * a[1] + b[1]})",
                         f"({a[0] - s * b[0]}, {a[1] - s * b[1]})"])
VectorAdd.PROVENANCE = Provenance("original")


@question_type("math.vector_magnitude", display_name={"th": "ขนาดของเวกเตอร์"},
               level={"th": "ม.6"}, topic="เวกเตอร์")
class VectorMagnitude(MathType):
    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 5):
        a, b, c = rng.choice(_TRIPLES_math_geometry)
        k = rng.randint(k_lo, k_hi)
        x, y = a * k, b * k
        if rng.random() < 0.5:
            x = -x
        if rng.random() < 0.5:
            y = -y
        return MathDraw(rf"\vec{{u}} = ({x}, {y})", str(c * k),
                        prompt="จงหาขนาดของเวกเตอร์นี้",
                        distractors=[str(abs(x) + abs(y)), str((c * k) ** 2),
                                     str(abs(abs(x) - abs(y)))])
VectorMagnitude.PROVENANCE = Provenance("original")


@question_type("math.vector_grid_picture_m5",
               display_name={"th": "อ่านเวกเตอร์จากภาพบนตาราง"},
               level={"th": "ม.5"}, topic="เวกเตอร์")
class VectorGridPictureM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(VECTOR_GRIDS)
        ux, uy, vx, vy = s
        img = image(s.asset_id, alt=VEC_ALT)
        ask = rng.randrange(4)
        if ask == 0:
            return _q([text("จากภาพ จงหา"), content_math(r"\vec{u} + \vec{v}"), img],
                      _pair(ux + vx, uy + vy),
                      [_pair(ux - vx, uy - vy), _pair(ux + vy, uy + vx), _pair(ux * vx, uy * vy),
                       _pair(-(ux + vx), -(uy + vy))], self.topic, [])
        if ask == 1:
            return _q([text("จากภาพ จงหา"), content_math(r"\vec{u} - \vec{v}"), img],
                      _pair(ux - vx, uy - vy),
                      [_pair(vx - ux, vy - uy), _pair(ux + vx, uy + vy), _pair(ux - vy, uy - vx)],
                      self.topic, [_pair(ux - vx + 1, uy - vy)])
        if ask == 2:
            n = ux * ux + uy * uy
            return _q([text("จากภาพ จงหาขนาดของ"), content_math(r"\vec{u}"), img], _sqrt(n),
                      [str(abs(ux) + abs(uy)), _sqrt(abs(ux * ux - uy * uy)) if ux * ux != uy * uy else "0",
                       _sqrt(n + 1), str(n)], self.topic, [])
        dot = ux * vx + uy * vy
        return _math_q([text("จากภาพ จงหา"), content_math(r"\vec{u} \cdot \vec{v}"), img], str(dot),
                       [str(ux * vy + uy * vx), str(ux * vx - uy * vy), str(-dot)], self.topic)
VectorGridPictureM5.PROVENANCE = Provenance("original")


@question_type("math.vectors",
               display_name={"th": "เวกเตอร์ 2 มิติ"}, level={"th": "ม.6"}, topic="เวกเตอร์")
class Vectors(MathType):
    def expr(self, rng: Random):
        ax, ay = rng.randint(-6, 6), rng.randint(-6, 6)
        bx, by = rng.randint(-6, 6), rng.randint(-6, 6)
        kind = rng.choice(["mag", "dot", "combo"])
        if kind == "mag":
            while ax == 0 and ay == 0:
                ax, ay = rng.randint(-6, 6), rng.randint(-6, 6)
            return MathDraw(
                rf"\vec{{a}} = ({ax}, {ay}): \quad |\vec{{a}}|",
                sqrt_tex(ax * ax + ay * ay), topic="ขนาดของเวกเตอร์",
                hint=r"|\vec{a}| = \sqrt{a_x^2 + a_y^2}")
        if kind == "dot":
            return MathDraw(
                rf"\vec{{a}} = ({ax}, {ay}), \; \vec{{b}} = ({bx}, {by}): "
                rf"\quad \vec{{a}} \cdot \vec{{b}}",
                rf"{ax * bx + ay * by}", topic="ผลคูณเชิงสเกลาร์",
                hint=r"\vec{a} \cdot \vec{b} = a_x b_x + a_y b_y")
        k = rng.randint(2, 3)
        return MathDraw(
            rf"\vec{{a}} = ({ax}, {ay}), \; \vec{{b}} = ({bx}, {by}): "
            rf"\quad \vec{{a}} + {k}\vec{{b}}",
            rf"({ax + k * bx}, {ay + k * by})", topic="การบวกเวกเตอร์")
Vectors.PROVENANCE = Provenance("original")


@question_type("math.vector_points_m5",
               display_name={"th": "เวกเตอร์ระหว่างจุดในสามมิติ: พื้นที่ มุม และการตั้งฉาก"},
               level=M5, topic=TOPIC)
class VectorPointsM5(QuestionType):
    @redraw_until_full()
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            while True:
                a, b, c = _small(rng, -4, 4), _small(rng, -4, 4), _small(rng, -4, 4)
                n2 = triangle_area_sq4(a, b, c)
                if n2:
                    break
            stem = [text("รูปสามเหลี่ยม ABC ในระบบพิกัดฉากสามมิติมีจุดยอดที่"),
                    content_math(f"{pt_tex('A', a)}, {pt_tex('B', b)}"), text("และ"), content_math(pt_tex("C", c)),
                    text("รูปสามเหลี่ยม ABC มีพื้นที่กี่ตารางหน่วย")]
            # Forgetting ½; forgetting the root; position vectors B × C instead of AB × AC.
            pos = cross(b, c)
            wrongs = [length_tex(n2), frac_tex(Fraction(n2, 2)), length_tex(dot(pos, pos), half=True)
                      if any(pos) else length_tex(4 * n2, half=True), length_tex(4 * n2)]
            return _tex_q(stem, length_tex(n2, half=True), wrongs, self.topic)
        if kind == 1:
            while True:
                a, b, c = _small(rng), _small(rng), _small(rng)
                rest = (rng.randint(-3, 6), rng.randint(-3, 6))
                x = perpendicular_x(a, b, c, rest)
                if (x is not None and x.denominator == 1 and abs(x) <= 15 and (int(x), *rest) != a
                        and len({a, b, c}) == 3):      # four points, not three named twice
                    break
            d = (int(x), *rest)
            ad = sub(d, a)
            stem = [text("ให้จุด"), content_math(f"{pt_tex('A', a)}, {pt_tex('B', b)}, {pt_tex('C', c)}"),
                    text("และ"), content_math(pt_tex("D", ("x", *rest))),
                    text("อยู่ในระบบพิกัดฉากสามมิติ เมื่อ x เป็นจำนวนจริง ถ้า"), content_math(r"\overrightarrow{AB}"),
                    text("ตั้งฉากกับ"), content_math(r"\overrightarrow{CD}"), text("แล้วขนาดของ"),
                    content_math(r"\overrightarrow{AD}"), text("เท่ากับเท่าใด")]
            # x solved with the wrong sign; |CD| instead; forgetting the root.
            ab = sub(b, a)
            x_bad = 2 * c[0] - int(x)
            bad = sub((x_bad, *rest), a)
            cd = sub(d, c)
            wrongs = [length_tex(dot(bad, bad)), length_tex(dot(cd, cd)), str(dot(ad, ad)),
                      length_tex(dot(ad, ad) + dot(ab, ab))]
            return _tex_q(stem, length_tex(dot(ad, ad)), wrongs, self.topic)
        while True:
            a, b, c = _small(rng), _small(rng), _small(rng)
            dd, n1, n2 = angle_cos(a, b, c)
            if dd and n1 and n2 and dd * dd != n1 * n2:
                break
        stem = [text("กำหนดจุด"), content_math(f"{pt_tex('A', a)}, {pt_tex('B', b)}"), text("และ"),
                content_math(pt_tex("C", c)), text("ถ้า"), content_math(r"\theta = A\hat{B}C"),
                text("แล้ว"), content_math(r"\cos\theta"), text("เท่ากับเท่าใด")]
        # AB instead of BA (sign); no root on the lengths; the vertex taken at A.
        d2, m1, m2 = angle_cos(b, a, c)
        wrongs = [cos_tex(-dd, n1, n2), frac_tex(Fraction(dd, n1 * n2)),
                  cos_tex(d2, m1, m2) if d2 and m1 and m2 else frac_tex(Fraction(dd, n1 + n2)),
                  frac_tex(Fraction(dd, n1 + n2))]
        return _tex_q(stem, cos_tex(dd, n1, n2), wrongs, self.topic)
VectorPointsM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/10 เวกเตอร์',))


@question_type("math.vector_dot_product_m5", display_name={"th": "ผลคูณเชิงสเกลาร์ของเวกเตอร์"},
               level=M6, topic="เวกเตอร์")
class VectorDotProductM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        dim = rng.choice((2, 3))
        u = [rng.randint(-5, 5) for _ in range(dim)]
        v = [rng.randint(-5, 5) for _ in range(dim)]
        dot = sum(p * q for p, q in zip(u, v))
        kind = rng.randrange(2)
        if kind == 0:
            return _maths_math_m5([text("จงหา u · v เมื่อ"), content_math(rf"u = {_vec(u)},\ v = {_vec(v)}")],
                          str(dot), [str(sum(u) * sum(v)), str(-dot) if dot else "1",
                                     str(sum(p + q for p, q in zip(u, v))), str(dot + 1)], self.topic)
        # Build it perpendicular: choose k first, then solve for v's first entry
        # with u's first entry ±1 so everything stays whole.
        k = rng.choice([x for x in range(-6, 7) if x])
        u[0] = rng.choice((1, -1))
        u[-1] = u[-1] or 2
        others = sum(p * q for p, q in zip(u[1:-1], v[1:-1]))
        v[0] = (-u[-1] * k - others) // u[0]
        rest = sum(p * q for p, q in zip(u[:-1], v[:-1]))
        shown = v[:-1] + ["k"]
        return _maths_math_m5([text("เวกเตอร์ u และ v ตั้งฉากกัน จงหาค่า k"),
                       content_math(rf"u = {_vec(u)},\ v = {_vec(shown)}")],
                      str(k), [str(-k) if k else "1", str(rest), str(k + 1), str(k - 1)], self.topic)
VectorDotProductM5.PROVENANCE = Provenance("original")


@question_type("math.vector_resultant_word_m5",
               display_name={"th": "โจทย์ปัญหาเวกเตอร์ลัพธ์ (เรือข้ามแม่น้ำ แรง การกระจัด)"},
               level=M5_math_apply_add, topic="เวกเตอร์")
class VectorResultantWordM5(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.choice(_TRIPLES)
        kind = rng.randrange(5)
        wrong = _story.keep(a + b, abs(b - a), a * b, answer=c, lo=1)
        if kind == 0:
            return MathDraw("", str(c),
                            prompt=(f"เรือแล่นตั้งฉากกับฝั่งด้วยอัตราเร็ว {b} เมตรต่อวินาทีเมื่อเทียบกับน้ำ "
                                    f"กระแสน้ำไหลขนานฝั่งด้วยอัตราเร็ว {a} เมตรต่อวินาที "
                                    f"เรือเคลื่อนที่เมื่อเทียบกับฝั่งด้วยอัตราเร็วกี่เมตรต่อวินาที"),
                            distractors=wrong)
        if kind == 1:
            w = b * rng.choice((10, 20, 25, 30))
            drift = a * w // b
            return MathDraw("", str(drift),
                            prompt=(f"แม่น้ำกว้าง {w} เมตร เรือแล่นตั้งฉากกับฝั่งด้วยอัตราเร็ว {b} เมตรต่อวินาทีเมื่อเทียบกับน้ำ "
                                    f"กระแสน้ำไหลด้วยอัตราเร็ว {a} เมตรต่อวินาที เรือจะขึ้นฝั่งตรงข้าม"
                                    f"ห่างจากจุดตรงข้ามจุดออกเดินทางกี่เมตร"),
                            distractors=_story.keep(w * b // a if w * b % a == 0 else drift + w, w // b,
                                                    c * w // b, drift * 2, answer=drift, lo=1))
        if kind == 2:
            back = rng.randint(1, 5)
            east = a + back
            return MathDraw("", str(c),
                            prompt=(f"นักสำรวจเดินไปทางทิศตะวันออก {east} กิโลเมตร ทิศเหนือ {b} กิโลเมตร "
                                    f"แล้วเดินกลับไปทางทิศตะวันตก {back} กิโลเมตร "
                                    f"ขณะนี้อยู่ห่างจากจุดเริ่มต้นกี่กิโลเมตร (ขนาดของการกระจัด)"),
                            distractors=_story.keep(east + b + back, east + b - back, _hyp(east, b),
                                                    answer=c, lo=1))
        if kind == 3:
            k = rng.choice((1, 2, 5, 10))
            return MathDraw("", str(c * k),
                            prompt=(f"แรงสองแรงขนาด {a * k} นิวตัน และ {b * k} นิวตัน กระทำต่อวัตถุที่จุดเดียวกัน "
                                    f"โดยทิศของแรงทั้งสองตั้งฉากกัน แรงลัพธ์มีขนาดกี่นิวตัน"),
                            distractors=_story.keep((a + b) * k, abs(b - a) * k, (a * a + b * b) * k * k,
                                                    answer=c * k, lo=1))
        t = rng.choice((2, 3, 4))
        k = rng.choice((10, 20, 50))
        return MathDraw("", _c(c * k * t),
                        prompt=(f"เครื่องบินมุ่งหน้าไปทางทิศเหนือด้วยอัตราเร็ว {b * k} กิโลเมตรต่อชั่วโมงเทียบกับอากาศ "
                                f"ลมพัดไปทางทิศตะวันออกด้วยอัตราเร็ว {a * k} กิโลเมตรต่อชั่วโมง "
                                f"เมื่อบินไป {t} ชั่วโมง เครื่องบินอยู่ห่างจากจุดเริ่มต้นกี่กิโลเมตร"),
                        distractors=[_c((a + b) * k * t), _c(b * k * t), _c(c * k)])
VectorResultantWordM5.PROVENANCE = Provenance("original")


@question_type("math.vector_triple_product_m5",
               display_name={"th": "ผลคูณสามชั้นเชิงสเกลาร์และการตั้งฉากกับผลคูณเชิงเวกเตอร์"},
               level=M5, topic=TOPIC)
class VectorTripleProductM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(4)
        if kind == 0:
            while True:
                v = _small(rng)
                a_name = rng.choice("ijk")
                b_names = rng.sample([e for e in "ijk" if e != a_name] + [a_name], 2)
                sign = rng.choice((1, -1))
                b = add(E[b_names[0]], tuple(sign * x for x in E[b_names[1]]))
                right = dot(cross(v, E[a_name]), b)
                if right and any(v):
                    break
            b_tex = ijk_tex(b)
            stem = [text("กำหนดให้"), content_math(rf"\vec{{v}} = {ijk_tex(v)}"), text("ค่าของ"),
                    content_math(rf"(\vec{{v}} \times \vec{{{a_name}}}) \cdot ({b_tex})"), text("เท่ากับเท่าใด")]
            # The cross product taken the other way; v · b; the cross product's middle sign lost.
            c = cross(v, E[a_name])
            named = [-right, dot(v, b), dot((c[0], -c[1], c[2]), b)]
            return _frac_q(stem, Fraction(right), named, self.topic)
        if kind == 1:
            while True:
                a, bc = _small(rng), _small(rng)
                d = dot(a, bc)
                if d and any(bc):
                    break
            form, mult = rng.choice(TRIPLE_FORMS)
            right = mult * d
            stem = [text("ถ้า"), content_math(rf"\vec{{a}} = {ijk_tex(a)}"), text("และ"),
                    content_math(rf"\vec{{b}} \times \vec{{c}} = {ijk_tex(bc)}"), text("แล้ว"), content_math(form),
                    text("เท่ากับเท่าใด")]
            # The sign of the swap missed; the bare a · (b × c); zero (every term thought to vanish).
            return _frac_q(stem, Fraction(right), [-right, d if d != right else 2 * d, 0], self.topic)
        if kind == 2:
            while True:
                u, v = _small(rng), _small(rng)
                w1, w2 = rng.randint(-4, 5), rng.randint(-4, 5)
                a = perpendicular_parameter(u, v, w1, w2)
                if a is not None and a.denominator == 1 and abs(a) <= 12:
                    break
            stem = [text("กำหนดให้"), content_math(rf"\vec{{u}} = {ijk_tex(u)},\ \vec{{v}} = {ijk_tex(v)}"),
                    text("และ"),
                    content_math(rf"\vec{{w}} = {ijk_tex((w1, w2, 0))} + a\vec{{k}}" if (w1, w2) != (0, 0)
                                 else r"\vec{w} = a\vec{k}"),
                    text("เมื่อ a เป็นจำนวนจริง ถ้า"), content_math(r"\vec{u} \times \vec{v}"),
                    text("ตั้งฉากกับ"), content_math(r"\vec{w}"), text("แล้ว a เท่ากับเท่าใด")]
            n = cross(u, v)
            # The cross product's middle sign lost; the equation's sign lost; u + v used instead.
            named = [Fraction(-(n[0] * w1 - n[1] * w2), n[2]), -a]
            s = add(u, v)
            if s[2]:
                named.append(Fraction(-(s[0] * w1 + s[1] * w2), s[2]))
            return _frac_q(stem, a, named, self.topic)
        while True:
            u = tuple(rng.choice((-2, -1, 1, 2, 3)) for _ in range(3))
            if len(set(map(abs, u))) >= 2 or rng.random() < 0.3:
                break
        k = rng.choice((-1, 2, -2, 3))
        right = tuple(k * x for x in u)
        stem = [text("ให้"), content_math(rf"\vec{{u}} = {ijk_tex(u)}"), text("เวกเตอร์"), content_math(r"\vec{v}"),
                text("ในข้อใดสอดคล้องกับสมการ"), content_math(r"\vec{u} \times \vec{v} = \vec{0}")]
        # One component's sign flipped: not parallel any more.
        wrongs = [tuple(-x if i == j else x for j, x in enumerate(right)) for i in range(3)]
        rng.shuffle(wrongs)
        fmt = lambda v: rf"\vec{{v}} = {ijk_tex(v)}"
        return _tex_q(stem, fmt(right), [fmt(w) for w in wrongs], self.topic)
VectorTripleProductM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/10 เวกเตอร์',))


@question_type("math.vector_identity_m5",
               display_name={"th": "เอกลักษณ์ของผลคูณเชิงสเกลาร์และเชิงเวกเตอร์"},
               level=M5, topic=TOPIC)
class VectorIdentityM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            p, q = rng.sample((2, 3, 5, 6, 7, 10), 2)
            if rng.random() < 0.5:
                right = p * q
                stem = [text("ถ้า"), content_math(r"\vec{u}"), text("และ"), content_math(r"\vec{v}"),
                        text("เป็นเวกเตอร์ในสามมิติ โดยที่"),
                        content_math(rf"|\vec{{u}}| = \sqrt{{{p}}}"), text("และ"),
                        content_math(rf"|\vec{{v}}| = \sqrt{{{q}}}"), text("แล้ว"),
                        content_math(r"|\vec{u} \cdot \vec{v}|^{2} + |\vec{u} \times \vec{v}|^{2}"),
                        text("เท่ากับเท่าใด")]
                # Adding the squares; the product of the lengths; their sum's square.
                wrongs = [str(p + q), length_tex(p * q), str(p * p + q * q), str(2 * p * q)]
                return _tex_q(stem, str(right), wrongs, self.topic)
            # |u| = p, |v| = q (whole), u · v = d → |u × v| = √(p²q² − d²).
            d = rng.randint(1, p * q - 1)
            right = length_tex(p * p * q * q - d * d)
            stem = [text("ถ้า"), content_math(rf"|\vec{{u}}| = {p},\ |\vec{{v}}| = {q}"), text("และ"), content_math(rf"\vec{{u}} \cdot \vec{{v}} = {d}"), text("แล้ว"),
                    content_math(r"|\vec{u} \times \vec{v}|"), text("เท่ากับเท่าใด")]
            # Adding instead of subtracting; forgetting the root; pq − d.
            wrongs = [length_tex(p * p * q * q + d * d), str(p * p * q * q - d * d), str(p * q - d),
                      length_tex(p * p + q * q - d * d) if p * p + q * q > d * d else str(p * q + d)]
            return _tex_q(stem, right, wrongs, self.topic)
        if kind == 1:
            k, minus = rng.choice((3, 4, 5, 6, 8, 10)), rng.random() < 0.5
            right = cos_from_sum_ratio(k, minus)
            op = "-" if minus else "+"
            stem = [text("กำหนดให้"), content_math(r"\vec{u}"), text("และ"), content_math(r"\vec{v}"),
                    text("เป็นเวกเตอร์ในสามมิติที่ไม่ขนานกัน โดยที่"),
                    content_math(r"|\vec{u}| = |\vec{v}| = 1"), text("และ"),
                    content_math(rf"|\vec{{u}} {op} \vec{{v}}|^{{2}} = {k}|\vec{{u}} \times \vec{{v}}|^{{2}}"),
                    text("ถ้า θ เป็นมุมระหว่าง"), content_math(r"\vec{u}"), text("และ"), content_math(r"\vec{v}"),
                    text("แล้ว"), content_math(r"\cos\theta"), text("เท่ากับเท่าใด")]
            # The other sign's answer; 2/k; 1 − 1/k (|u × v|² read as 1 − c).
            named = [cos_from_sum_ratio(k, not minus), Fraction(2, k), 1 - Fraction(1, k), Fraction(1, k)]
            return _frac_q(stem, right, named, self.topic)
        picks = rng.sample(VECTOR_FACTS, 4)
        right = sum(t for _, t in picks)
        stem = [text("ให้"), content_math(r"\vec{u}, \vec{v}"), text("และ"), content_math(r"\vec{w}"),
                text("เป็นเวกเตอร์ใด ๆ ในระบบพิกัดฉากสามมิติ พิจารณาข้อความต่อไปนี้")]
        for lab, (tex, _) in zip(("ก.", "ข.", "ค.", "ง."), picks):
            stem += [text(lab), content_math(tex)]
        stem.append(text("จำนวนข้อความที่ถูกต้องเท่ากับเท่าใด"))
        wrongs = [str(v) for v in sorted(range(5), key=lambda v: abs(v - right)) if v != right]
        return _tex_q(stem, str(right), wrongs, self.topic)
VectorIdentityM5.PROVENANCE = Provenance("adapted", sources=('sheet_database/rathcenter/10 เวกเตอร์',))


@question_type("math.vector_cross_product_m5", display_name={"th": "ผลคูณเชิงเวกเตอร์และพื้นที่"},
               level=M6, topic="เวกเตอร์")
class VectorCrossProductM5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            u = [rng.randint(-4, 4) for _ in range(3)]
            v = [rng.randint(-4, 4) for _ in range(3)]
            c = _cross(u, v)
            if all(c):
                break
        given = [text("กำหนดให้"), content_math(rf"u = {_vec(u)},\ v = {_vec(v)}")]
        if rng.random() < 0.5:
            right = _vec(c)
            # v × u, the entries multiplied pairwise, the middle sign lost.
            wrongs = [_vec([-x for x in c]), _vec([p * q for p, q in zip(u, v)]), _vec([c[0], -c[1], c[2]])]
            return _maths(given + [text("จงหา u × v")], right, _distinct(right, *wrongs), self.topic)
        n = sum(x * x for x in c)
        tri = rng.random() < 0.5
        area = (Fraction(1, 2) if tri else Fraction(1), n)
        right = _surd_tex(area)
        wrongs = _distinct(right, str(n), _surd_tex((Fraction(1) if tri else Fraction(1, 2), n)),
                           str(abs(sum(p * q for p, q in zip(u, v)))), _surd_bump(area))
        shape = "รูปสามเหลี่ยมที่มี u และ v เป็นด้านประกอบมุม" if tri else "รูปสี่เหลี่ยมด้านขนานที่มี u และ v เป็นด้านประชิด"
        return _maths(given + [text(f"จงหาพื้นที่ของ{shape}")], right, wrongs[:3], self.topic)
VectorCrossProductM5.PROVENANCE = Provenance("original")
