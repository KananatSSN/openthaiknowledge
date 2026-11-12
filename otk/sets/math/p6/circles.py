"""วงกลม

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.6/3

Sets moved here from: math, math_geometry, math_p6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.circle_parts",
               display_name={"th": "ส่วนประกอบของวงกลม"}, level={"th": "ป.6"},
               topic="วงกลม")
class CircleParts(ConceptBankType):
    ITEMS = [
        Concept("เส้นที่ลากจากจุดศูนย์กลางไปยังขอบวงกลมเรียกว่าอะไร?", "รัศมี",
                ("เส้นผ่านศูนย์กลาง", "คอร์ด", "เส้นรอบวง")),
        Concept("เส้นที่ลากผ่านจุดศูนย์กลางและมีปลายทั้งสองอยู่บนวงกลม"
                "เรียกว่าอะไร?", "เส้นผ่านศูนย์กลาง",
                ("รัศมี", "คอร์ด", "เส้นรอบวง")),
        Concept("เส้นที่เชื่อมจุดสองจุดบนวงกลมโดยไม่ผ่านจุดศูนย์กลาง"
                "เรียกว่าอะไร?", "คอร์ด",
                ("รัศมี", "เส้นผ่านศูนย์กลาง", "เส้นรอบวง")),
        Concept("ความยาวรอบวงกลมเรียกว่าอะไร?", "เส้นรอบวง",
                ("รัศมี", "เส้นผ่านศูนย์กลาง", "คอร์ด")),
    ]


@question_type("math.circle_area_circumference",
               display_name={"th": "พื้นที่/เส้นรอบวงของวงกลม"}, level={"th": "ป.6"},
               topic="วงกลม")
class CircleAreaCircumference(WordProblem):
    def expr(self, rng: Random):
        r = rng.choice([7, 14, 21])                 # clean with π ≈ 22/7
        area = 22 * r * r // 7
        circ = 2 * 22 * r // 7
        if rng.random() < 0.5:
            ask, ans, other = "พื้นที่", area, circ
        else:
            ask, ans, other = "เส้นรอบวง", circ, area
        if ask == "พื้นที่":
            scenes = (f"โต๊ะกลมตัวหนึ่งมีหน้าโต๊ะรัศมี {r} นิ้ว หน้าโต๊ะมีพื้นที่กี่ตารางนิ้ว (ใช้ π ≈ 22/7)",
                      f"สระน้ำรูปวงกลมรัศมี {r} เมตร มีพื้นที่ผิวน้ำกี่ตารางเมตร (ใช้ π ≈ 22/7)")
        else:
            scenes = (f"ล้อจักรยานรัศมี {r} นิ้ว หมุนครบหนึ่งรอบ จักรยานเคลื่อนที่ได้กี่นิ้ว (ใช้ π ≈ 22/7)",
                      f"สระน้ำรูปวงกลมรัศมี {r} เมตร เดินรอบสระหนึ่งรอบได้ระยะทางกี่เมตร (ใช้ π ≈ 22/7)")
        prompt = rng.choice((f"วงกลมรัศมี {r} หน่วย (ใช้ π ≈ 22/7) มี{ask}เท่าใด?",) + scenes)
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=[str(other), str(22 * r // 7), str(r * r)])


@question_type("math.circle_radius_from_circumference",
               display_name={"th": "หารัศมีจากเส้นรอบวง"},
               level={"th": "ป.6"}, topic="วงกลม")
class CircleRadiusFromCircumference(WordProblem):
    """Uses 22/7 with radii that are multiples of 7, the ป.6 convention — the
    answer stays a whole number instead of a rounded decimal."""

    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 8):
        r = 7 * rng.randint(k_lo, k_hi)
        circumference = 2 * 22 * r // 7
        prompt = rng.choice((
            f"วงกลมวงหนึ่งมีเส้นรอบวงยาว {circumference} เซนติเมตร รัศมียาวกี่เซนติเมตร (ใช้ π = 22/7)",
            f"ดัดลวดยาว {circumference} เซนติเมตร เป็นวงกลมได้พอดี วงกลมมีรัศมียาวกี่เซนติเมตร "
            f"(ใช้ π = 22/7)",
            f"ล้อรถเข็นหมุนครบหนึ่งรอบเคลื่อนที่ได้ {circumference} เซนติเมตร ล้อมีรัศมียาวกี่เซนติเมตร "
            f"(ใช้ π = 22/7)",
        ))
        return MathDraw(
            "", str(r), prompt=prompt,
            hint=r"C = 2\pi r",
            distractors=[str(2 * r), str(circumference // 2), str(r * 7)])


@question_type("math.circle_word_problem_p6",
               display_name={"th": "โจทย์ปัญหาความยาวรอบวงและพื้นที่วงกลม"},
               level=LEVEL, topic="วงกลม")
class CircleWordProblemP6(WordProblem):
    def expr(self, rng: Random):
        r = 7 * rng.randint(1, 10)
        circ = 44 * r // 7
        area = 22 * r * r // 7
        kind = rng.randrange(6)
        if kind == 3:
            return MathDraw("", str(circ),
                            prompt=(f"นาฬิกาแขวนรูปวงกลมมีรัศมี {r} เซนติเมตร ต้องการติดขอบรอบนาฬิกา "
                                    f"ต้องใช้ขอบยาวกี่เซนติเมตร (ใช้ π ≈ 22/7)"),
                            distractors=_story.keep(circ // 2, area, 2 * r, answer=circ))
        if kind == 4:
            cost = rng.randint(5, 40)
            return MathDraw("", str(area * cost),
                            prompt=(f"ต้องการปูหญ้าสนามรูปวงกลมรัศมี {r} เมตร ค่าหญ้าตารางเมตรละ {cost} บาท "
                                    f"ต้องจ่ายกี่บาท (ใช้ π ≈ 22/7)"),
                            distractors=_story.keep(circ * cost, area + cost, 22 * 4 * r * r * cost // 7,
                                                    answer=area * cost))
        if kind == 5:
            return MathDraw("", str(r),
                            prompt=(f"ลวดยาว {circ} เซนติเมตร ดัดเป็นวงกลมพอดี วงกลมมีรัศมีกี่เซนติเมตร "
                                    f"(ใช้ π ≈ 22/7)"),
                            distractors=_story.keep(2 * r, circ // 22, r + 7, answer=r, lo=1))
        if kind == 0:
            turns = rng.randint(5, 50)
            return MathDraw("", str(circ * turns),
                            prompt=(f"ล้อรถจักรยานมีรัศมี {r} เซนติเมตร ถ้าล้อหมุน {turns} รอบ "
                                    f"รถจะเคลื่อนที่ได้กี่เซนติเมตร (ใช้ π ≈ 22/7)"),
                            # Using the radius where the diameter belongs.
                            distractors=_story.keep(circ * turns // 2, area * turns, r * turns,
                                                    answer=circ * turns))
        if kind == 1:
            cost = rng.randint(10, 60)
            return MathDraw("", str(circ * cost),
                            prompt=(f"สระน้ำรูปวงกลมมีรัศมี {r} เมตร ต้องการล้อมรั้วรอบสระ ค่ารั้วเมตรละ "
                                    f"{cost} บาท ต้องจ่ายกี่บาท (ใช้ π ≈ 22/7)"),
                            distractors=_story.keep(area * cost, circ * cost // 2, circ + cost,
                                                    answer=circ * cost))
        return MathDraw("", str(area),
                        prompt=(f"สนามหญ้ารูปวงกลมมีเส้นผ่านศูนย์กลาง {2 * r} เมตร มีพื้นที่กี่ตารางเมตร "
                                f"(ใช้ π ≈ 22/7)"),
                        # The diameter used as the radius, and the circumference.
                        distractors=_story.keep(22 * 4 * r * r // 7, circ, area // 2, answer=area))

from fractions import Fraction  # noqa: E402

from otk.core.registry import question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import WordProblem  # noqa: E402
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


# ── More circles (2026-11): radius and diameter, the circumference from a diameter, half a circle's area and
# perimeter, a wheel's turns, and the area of a ring ──


@question_type("math.radius_diameter_p6", display_name={"th": "รัศมีและเส้นผ่านศูนย์กลาง"},
               level=LEVEL, topic="วงกลม")
class RadiusDiameterP6(WordProblem):
    def expr(self, rng: Random):
        r = rng.randint(2, 60)
        to_d = rng.random() < 0.5
        right = 2 * r if to_d else r
        prompt = (f"วงกลมวงหนึ่งมีรัศมียาว {r} เซนติเมตร เส้นผ่านศูนย์กลางยาวกี่เซนติเมตร" if to_d
                  else f"วงกลมวงหนึ่งมีเส้นผ่านศูนย์กลางยาว {2 * r} เซนติเมตร รัศมียาวกี่เซนติเมตร")
        # The other way round; the length itself; four times.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(r if to_d else 2 * r, 4 * r, r // 2 if r > 3 else r + 3, right + 1,
                                                answer=right, lo=1))


@question_type("math.circumference_from_diameter_p6", display_name={"th": "ความยาวรอบวงจากเส้นผ่านศูนย์กลาง"},
               level=LEVEL, topic="วงกลม")
class CircumferenceFromDiameterP6(WordProblem):
    def expr(self, rng: Random):
        d = 7 * rng.randint(1, 20)
        right = 22 * d // 7
        prompt = f"วงกลมมีเส้นผ่านศูนย์กลางยาว {d} เซนติเมตร ยาวรอบวงกี่เซนติเมตร (ใช้ π ≈ 22/7)"
        # Using the radius as the diameter, twice the diameter; the area formula.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(11 * d // 7, 44 * d // 7, 2 * d, 22 * d * d // 28, answer=right, lo=1))


@question_type("math.semicircle_area_p6", display_name={"th": "พื้นที่ครึ่งวงกลม"},
               level=LEVEL, topic="วงกลม")
class SemicircleAreaP6(WordProblem):
    def expr(self, rng: Random):
        r = 7 * rng.randint(1, 6)
        right = 11 * r * r // 7
        prompt = f"ครึ่งวงกลมมีรัศมียาว {r} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร (ใช้ π ≈ 22/7)"
        # The whole circle; the curved edge; the diameter in place of the radius.
        return MathDraw("", _g6(right), prompt=prompt,
                        distractors=_gk6(22 * r * r // 7, 22 * r // 7, 44 * r * r // 7, right + r, answer=right, lo=1))


@question_type("math.semicircle_perimeter_p6", display_name={"th": "ความยาวรอบรูปครึ่งวงกลม"},
               level=LEVEL, topic="วงกลม")
class SemicirclePerimeterP6(WordProblem):
    def expr(self, rng: Random):
        d = 14 * rng.randint(1, 8)
        arc = 11 * d // 7
        right = arc + d
        prompt = f"ครึ่งวงกลมมีเส้นผ่านศูนย์กลางยาว {d} เซนติเมตร ยาวรอบรูปกี่เซนติเมตร (ใช้ π ≈ 22/7)"
        # The curved part only; the whole circle; the radius added instead of the diameter.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(arc, 2 * arc, arc + d // 2, 2 * arc + d, answer=right, lo=1))


@question_type("math.wheel_turns_p6", display_name={"th": "ล้อหมุนกี่รอบ"},
               level=LEVEL, topic="วงกลม")
class WheelTurnsP6(WordProblem):
    def expr(self, rng: Random):
        r = 7 * rng.randint(1, 5)
        turns = rng.randint(5, 60)
        c = 44 * r // 7
        distance = c * turns
        prompt = (f"ล้อรถมีรัศมี {r} เซนติเมตร รถแล่นไปได้ระยะทาง {distance:,} เซนติเมตร "
                  "ล้อหมุนไปกี่รอบ (ใช้ π ≈ 22/7)")
        # Divided by the diameter as the circumference, by half of it, or by the radius.
        return MathDraw("", str(turns), prompt=prompt,
                        distractors=_story.keep(2 * turns, turns + 1, turns - 1, distance // (2 * r), answer=turns, lo=1))


@question_type("math.ring_area_p6", display_name={"th": "พื้นที่ระหว่างวงกลมสองวง"},
               level=LEVEL, topic="วงกลม")
class RingAreaP6(WordProblem):
    def expr(self, rng: Random):
        r, big = sorted(rng.sample(range(1, 7), 2))
        r, big = 7 * r, 7 * big
        right = 22 * (big * big - r * r) // 7
        prompt = (f"วงกลมสองวงมีจุดศูนย์กลางเดียวกัน รัศมี {big} และ {r} เซนติเมตร "
                  "พื้นที่ระหว่างวงกลมทั้งสองเป็นกี่ตารางเซนติเมตร (ใช้ π ≈ 22/7)")
        # The radii subtracted before squaring; the larger circle; both added.
        return MathDraw("", _g6(right), prompt=prompt,
                        distractors=_gk6(22 * (big - r) ** 2 // 7, 22 * big * big // 7, 22 * (big * big + r * r) // 7,
                                         right + 22, answer=right, lo=1))
