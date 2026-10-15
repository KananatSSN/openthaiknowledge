"""ความคล้าย

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.3/1

Sets moved here from: math, math_diagrams_geo, math_geometry, math_m3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, frac_tex
from otk.sets._support.math_diagrams import _img, _math_q
from otk.sets._support.math_diagrams_geo import SIMILAR_PAIRS, SimilarPair
from otk.sets._support.math_m3 import LEVEL
from otk.sets._support.math_p2 import _maths

PROVENANCE = Provenance("original")


def similar_alt(s: SimilarPair) -> str:
    big = [v * s.k for v in s.small]
    small = [str(v) for v in s.small]
    large = [str(v) for v in big]
    (large if s.unknown < 3 else small)[s.unknown % 3] = "x"
    return ("รูปสามเหลี่ยม ABC คล้ายกับรูปสามเหลี่ยม DEF ด้าน AB BC CA ยาว {} {} {} หน่วย "
            "ด้าน DE EF FD ยาว {} {} {} หน่วย").format(*small, *large)


@question_type("math.similar_triangle",
               display_name={"th": "ความคล้ายของรูปสามเหลี่ยม"}, level={"th": "ม.3"},
               topic="ความคล้าย")
class SimilarTriangle(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.sample(range(2, 8), 2)
        k = rng.randint(2, 6)
        length = a * k
        prompt = rng.choice((
            f"สามเหลี่ยมสองรูปคล้ายกันด้วยอัตราส่วน {a} : {b} ถ้าด้านหนึ่งยาว {length} "
            f"ด้านที่สมนัยยาวเท่าใด?",
            # Height : shadow is the same for everything at one moment.
            f"ในเวลาเดียวกัน ไม้ที่ปักตั้งตรงยาว {a} เมตร ทอดเงายาว {b} เมตร "
            f"เสาต้นหนึ่งสูง {length} เมตร จะทอดเงายาวกี่เมตร",
            f"ย่อหรือขยายรูปสามเหลี่ยมด้วยอัตราส่วนด้านเดิม : ด้านใหม่ = {a} : {b} "
            f"ถ้าด้านเดิมด้านหนึ่งยาว {length} เซนติเมตร ด้านใหม่ที่สมนัยกันยาวกี่เซนติเมตร",
        ))
        return MathDraw("", str(b * k), prompt=prompt,
                        distractors=[str(length), str(length + (b - a)),
                                     str(length * a // b)])


@question_type("math.similar_triangle_picture_m3", display_name={"th": "หาความยาวด้านของรูปสามเหลี่ยมคล้ายจากรูป"},
               level={"th": "ม.3"}, topic="ความคล้าย")
class SimilarTrianglePictureM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SIMILAR_PAIRS)
        i = s.unknown % 3
        ans = s.answer
        known = s.small[i] if s.unknown < 3 else s.small[i] * s.k
        # Adding the difference instead of scaling, and scaling the wrong way.
        diff = s.small[(i + 1) % 3] * (s.k - 1)
        wrongs = [known + diff, known * s.k if s.unknown >= 3 else Fraction(known, s.k), ans + s.k]
        return _math_q([text("รูปสามเหลี่ยม ABC คล้ายกับรูปสามเหลี่ยม DEF จงหาค่า x"),
                        _img(s.asset_id, similar_alt(s))], str(ans),
                       [str(w) if not isinstance(w, Fraction) or w.denominator == 1 else f"{float(w):g}"
                        for w in wrongs], self.topic)


@question_type("math.similar_shadow", display_name={"th": "ความคล้าย: เงาและความสูง"},
               level={"th": "ม.3"}, topic="ความคล้าย")
class SimilarShadow(WordProblem):
    _TALL = ("เสาไฟ", "ต้นมะพร้าว", "เสาธง", "ตึก", "หอระฆัง")

    def expr(self, rng: Random, height_lo: int = 6, height_hi: int = 30):
        pole = rng.randint(height_lo, height_hi)   # metres
        k = rng.randint(2, 5)                      # shadow : height
        person = rng.randrange(150, 191, 5)        # a plausible human height, cm
        # Work in centimetres so the answer stays whole.
        person_shadow = person * k
        tall = rng.choice(self._TALL)
        if rng.random() < 0.5:
            return MathDraw(
                "", str(pole * k),
                prompt=(f"ในเวลาเดียวกัน คนสูง {person} เซนติเมตร มีเงายาว "
                        f"{person_shadow} เซนติเมตร ถ้า{tall}สูง {pole} เมตร "
                        f"เงาของ{tall}ยาวกี่เมตร"),
                distractors=[str(pole), str(pole * (k + 1)), str(pole + k)])
        return MathDraw(
            "", str(pole),
            prompt=(f"ในเวลาเดียวกัน คนสูง {person} เซนติเมตร มีเงายาว {person_shadow} เซนติเมตร "
                    f"ถ้าเงาของ{tall}ยาว {pole * k} เมตร {tall}สูงกี่เมตร"),
            # Multiplying by the ratio instead of dividing.
            distractors=[str(pole * k * k), str(pole * k), str(pole + k)])


@question_type("math.similar_figures_ratio_m3",
               display_name={"th": "ความคล้าย: อัตราส่วนของความยาว เส้นรอบรูป และพื้นที่"},
               level=LEVEL, topic="ความคล้าย")
class SimilarFiguresRatioM3(WordProblem):
    def expr(self, rng: Random):
        a, k = rng.randint(2, 9), rng.randint(2, 5)
        b = a * k
        kind = rng.randrange(3)
        if kind == 0:
            small = rng.randint(3, 30)
            return MathDraw("", str(small * k * k),
                            prompt=(f"รูปสามเหลี่ยมสองรูปคล้ายกัน ด้านที่สมนัยกันยาว {a} ซม. และ {b} ซม. "
                                    f"ถ้ารูปเล็กมีพื้นที่ {small} ตารางเซนติเมตร รูปใหญ่มีพื้นที่กี่ตารางเซนติเมตร"),
                            # Scaling the area by k instead of k².
                            distractors=_story.keep(small * k, small * k ** 3, small + b - a,
                                                    answer=small * k * k))
        if kind == 1:
            per = rng.randint(10, 60)
            return MathDraw("", str(per * k),
                            prompt=(f"รูปหลายเหลี่ยมสองรูปคล้ายกัน ด้านที่สมนัยกันยาว {a} ซม. และ {b} ซม. "
                                    f"ถ้ารูปเล็กยาวรอบรูป {per} ซม. รูปใหญ่ยาวรอบรูปกี่เซนติเมตร"),
                            distractors=_story.keep(per * k * k, per + b - a, per * a, answer=per * k))
        scale = rng.choice((10, 20, 24, 25, 40, 50))
        model = rng.randint(4, 30)
        return MathDraw("", str(model * scale),
                        prompt=(f"รถยนต์จำลองสร้างตามอัตราส่วน 1 : {scale} ถ้ารถจำลองยาว {model} ซม. "
                                f"รถจริงยาวกี่เซนติเมตร"),
                        distractors=_story.keep(model * scale * scale, model + scale,
                                                model * scale // 10, answer=model * scale))


@question_type("math.similar_ratio_area",
               display_name={"th": "อัตราส่วนพื้นที่ของรูปคล้าย"},
               level={"th": "ม.3"}, topic="ความคล้าย")
class SimilarRatioArea(WordProblem):
    """Lengths scale by k, areas by k² — the step almost everyone forgets."""

    def expr(self, rng: Random, k_lo: int = 2, k_hi: int = 5, area_lo: int = 3,
             area_hi: int = 30):
        k = rng.randint(k_lo, k_hi)
        small = rng.randint(area_lo, area_hi)
        big = small * k * k
        prompt = rng.choice((
            f"รูปสามเหลี่ยมสองรูปคล้ายกัน โดยด้านของรูปใหญ่ยาวเป็น {k} เท่าของรูปเล็ก "
            f"ถ้ารูปเล็กมีพื้นที่ {small} ตารางเซนติเมตร รูปใหญ่มีพื้นที่กี่ตารางเซนติเมตร",
            f"ขยายรูปถ่ายให้ด้านทุกด้านยาวเป็น {k} เท่าของเดิม ถ้ารูปเดิมมีพื้นที่ {small} ตารางนิ้ว "
            f"รูปที่ขยายแล้วมีพื้นที่กี่ตารางนิ้ว",
            f"แปลงผักสองแปลงมีรูปร่างคล้ายกัน ด้านของแปลงใหญ่ยาวเป็น {k} เท่าของแปลงเล็ก "
            f"ถ้าแปลงเล็กมีพื้นที่ {small} ตารางเมตร แปลงใหญ่มีพื้นที่กี่ตารางเมตร",
        ))
        return MathDraw(
            "", str(big), prompt=prompt,
            distractors=[str(small * k), str(small * k ** 3), str(small + k)])


@question_type("math.similar_parallel_segment_m3",
               display_name={"th": "ส่วนของด้านที่เหลือในสามเหลี่ยมคล้าย"},
               level=LEVEL, topic="ความคล้าย")
class SimilarParallelSegmentM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            a, b = rng.sample(range(2, 9), 2)
            k, m = rng.sample(range(2, 8), 2)
            ad, db, ae, ec = a * k, b * k, a * m, b * m
            candidates = (str(ae + ec), str(db), frac_tex(Fraction(ad * ae, db)))
            if len({str(ec), *candidates}) == 4:
                break
        wrongs = [named(key, value) for key, value in zip((
            "similar.used_whole_side", "similar.copied_corresponding_segment",
            "similar.reversed_ratio"), candidates)]
        return _maths([text("ในสามเหลี่ยม ABC จุด D อยู่บนด้าน AB และจุด E อยู่บนด้าน AC "
                            f"โดย DE ขนานกับ BC ถ้า AD = {ad}, DB = {db}, AE = {ae} หน่วย "
                            "ส่วน EC ยาวกี่หน่วย")], str(ec), wrongs, self.topic)


@question_type("math.similar_remaining_area_m3",
               display_name={"th": "พื้นที่ส่วนที่เหลือจากสามเหลี่ยมคล้าย"},
               level=LEVEL, topic="ความคล้าย")
class SimilarRemainingAreaM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        while True:
            p = rng.randint(2, 16)
            q = rng.randint(p + 2, p + 14)
            ratio = Fraction(p, q)
            answer = frac_tex(1 - ratio ** 2)
            candidates = (frac_tex(1 - ratio), frac_tex(ratio ** 2), frac_tex(ratio))
            if len({answer, *candidates}) == 4:
                break
        wrongs = [named(key, value) for key, value in zip((
            "similar.used_length_ratio_for_area", "similar.found_inner_area",
            "similar.reported_length_ratio"), candidates)]
        return _maths([text("ในสามเหลี่ยม ABC จุด D อยู่บนด้าน AB และจุด E อยู่บนด้าน AC "
                            f"โดย DE ขนานกับ BC และ AD : AB = {p} : {q} "
                            "พื้นที่สี่เหลี่ยม DBCE เป็นส่วนเท่าใดของพื้นที่สามเหลี่ยม ABC")],
                      answer, wrongs, self.topic)


@question_type("math.similar_side_from_areas_m3",
               display_name={"th": "ความยาวด้านรูปคล้ายจากอัตราส่วนพื้นที่"},
               level=LEVEL, topic="ความคล้าย")
class SimilarSideFromAreasM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        small_root = rng.randint(2, 6)
        large_root = rng.randint(small_root + 1, small_root + 5)
        area_unit = rng.randint(2, 7)
        side_unit = rng.randint(2, 8)
        small_area = area_unit * small_root ** 2
        large_area = area_unit * large_root ** 2
        small_side = small_root * side_unit
        large_side = large_root * side_unit
        wrongs = [
            named("similar.used_area_ratio_for_length",
                  frac_tex(Fraction(small_side * large_area, small_area))),
            named("similar.kept_length_unchanged", str(small_side)),
            named("similar.reversed_length_ratio", frac_tex(Fraction(small_side * small_root,
                                                                     large_root))),
        ]
        return _maths([text(f"รูปสามเหลี่ยมสองรูปคล้ายกัน รูปเล็กมีพื้นที่ {small_area} ตารางเซนติเมตร "
                            f"รูปใหญ่มีพื้นที่ {large_area} ตารางเซนติเมตร "
                            f"ถ้าด้านหนึ่งของรูปเล็กยาว {small_side} เซนติเมตร "
                            "ด้านที่สมนัยกันของรูปใหญ่ยาวกี่เซนติเมตร")],
                      str(large_side), wrongs, self.topic)
