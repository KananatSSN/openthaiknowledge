"""ปริมาตร

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.5/*

Sets moved here from: math, math_measure_pictures, math_p5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_measure_pictures import CUBES
from otk.sets._support.math_p4 import grouped
from otk.sets._support.math_p5 import LEVEL
from otk.sets._support.math_pictures import _near

PROVENANCE = Provenance("original")


CUBE_ALT = "ภาพทรงสี่เหลี่ยมมุมฉากที่ประกอบด้วยลูกบาศก์ขนาดเท่ากัน"


@question_type("math.rectangular_prism_volume",
               display_name={"th": "ปริมาตรทรงสี่เหลี่ยมมุมฉาก"}, level={"th": "ป.5"},
               topic="ปริมาตร")
class RectangularPrismVolume(WordProblem):
    _THINGS = (("กล่องนม", "เซนติเมตร"), ("ตู้เย็น", "เดซิเมตร"), ("สระว่ายน้ำ", "เมตร"),
               ("กล่องรองเท้า", "เซนติเมตร"), ("ห้องเก็บของ", "เมตร"), ("ตู้ปลา", "เซนติเมตร"))

    def expr(self, rng: Random):
        width, length, height = (rng.randint(2, 12) for _ in range(3))
        thing, unit = rng.choice(self._THINGS)
        vol = width * length * height
        return MathDraw("", str(vol),
                        prompt=(f"{thing}ทรงสี่เหลี่ยมมุมฉากกว้าง {width} {unit} ยาว {length} {unit} "
                                f"สูง {height} {unit} มีปริมาตรกี่ลูกบาศก์{unit}"),
                        # Adding the edges, the surface area, and one face.
                        distractors=_story.keep(width + length + height,
                                                2 * (width * length + length * height + width * height),
                                                width * length, answer=vol))


@question_type("math.unit_cubes_p5", display_name={"th": "นับลูกบาศก์หน่วยหาปริมาตร"},
               level={"th": "ป.5"}, topic="ปริมาตร")
class UnitCubesP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        c = rng.choice(CUBES)
        v = c.w * c.d * c.h
        # Only the faces seen; one layer; adding the edges.
        seen = c.w * c.d + c.w * c.h + c.d * c.h
        return _math_q([text("ทรงสี่เหลี่ยมมุมฉากนี้ประกอบด้วยลูกบาศก์ขนาด 1 ลูกบาศก์หน่วย "
                             "มีปริมาตรกี่ลูกบาศก์หน่วย"), image(c.asset_id, alt=CUBE_ALT)],
                       str(v), _near(v, seen, c.w * c.d, c.w + c.d + c.h, lo=1), self.topic)


@question_type("math.cube_units_p5",
               display_name={"th": "ลูกบาศก์เซนติเมตรและลูกบาศก์เมตร"},
               level=LEVEL, topic="ปริมาตร")
class CubeUnitsP5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            m = rng.randint(2, 9)
            return MathDraw("", grouped(m * 1_000_000).replace(",", "{,}"),
                            prompt=f"{m} ลูกบาศก์เมตร เท่ากับกี่ลูกบาศก์เซนติเมตร", variant="convert",
                            distractors=[named("units.wrong_conversion", f"{m * 100}"),
                                         named("units.wrong_conversion",
                                               grouped(m * 10_000).replace(",", "{,}")),
                                         named("units.wrong_conversion",
                                               grouped(m * 1000).replace(",", "{,}"))])
        if kind == 1:
            s = rng.randint(2, 12)
            return MathDraw("", str(s ** 3),
                            prompt=f"ลูกบาศก์ยาวด้านละ {s} เซนติเมตร มีปริมาตรกี่ลูกบาศก์เซนติเมตร",
                            variant="volume",
                            distractors=_story.keep(named("volume.area_not_volume", s * s),
                                                    named("power.multiplied_by_exponent", 3 * s),
                                                    named("volume.surface_not_volume", 6 * s * s),
                                                    answer=s ** 3))
        n = rng.randint(2, 6)
        return MathDraw("", str(n * n * n),
                        prompt=(f"นำลูกบาศก์ขนาด 1 ลูกบาศก์เซนติเมตรมาเรียงเป็นทรงลูกบาศก์ยาวด้านละ "
                                f"{n} เซนติเมตร ต้องใช้ลูกบาศก์เล็กกี่ลูก"), variant="volume",
                        distractors=_story.keep(named("volume.area_not_volume", n * n),
                                                named("power.multiplied_by_exponent", 3 * n), 4 * n,
                                                named("volume.surface_not_volume", n * n * 6),
                                                answer=n ** 3))


@question_type("math.volume_capacity_p5",
               display_name={"th": "ปริมาตรและความจุของทรงสี่เหลี่ยมมุมฉาก (ลูกบาศก์เซนติเมตร ลิตร)"},
               level=LEVEL, topic="ปริมาตร")
class VolumeCapacityP5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        w, length = rng.choice((10, 20, 25, 30, 40, 50)), rng.choice((20, 40, 50, 60, 80, 100))
        h = rng.choice((10, 20, 25, 30, 40, 50))
        if kind == 0:
            # Whole litres only: redraw the height until the volume is.
            while w * length * h % 1000:
                h = rng.choice((10, 20, 25, 30, 40, 50))
                w = rng.choice((10, 20, 25, 30, 40, 50))
            litres = w * length * h // 1000
            return MathDraw("", str(litres),
                            prompt=(f"ตู้ปลาทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {length} ซม. สูง {h} ซม. "
                                    f"จุน้ำได้กี่ลิตร (1 ลิตร = 1,000 ลูกบาศก์เซนติเมตร)"),
                            distractors=_story.keep(named("units.wrong_conversion", w * length * h // 100),
                                                    named("units.not_converted", w * length * h),
                                                    named("units.wrong_conversion", w * length * h // 10000)
                                                    or litres + 1, litres * 2, answer=litres, lo=1))
        if kind == 1:
            water = rng.randint(2, h // 2)
            vol = w * length * water
            return MathDraw("", str(vol),
                            prompt=(f"ถังทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {length} ซม. มีน้ำสูง {water} ซม. "
                                    f"มีน้ำกี่ลูกบาศก์เซนติเมตร"),
                            distractors=_story.keep(w * length * h,
                                                    named("volume.area_not_volume", w * length),
                                                    named("operation.reversed", w + length + water),
                                                    vol * 10, answer=vol))
        vol = w * length * h
        return MathDraw("", str(h),
                        prompt=(f"กล่องทรงสี่เหลี่ยมมุมฉากมีปริมาตร {grouped(vol)} ลูกบาศก์เซนติเมตร "
                                f"กว้าง {w} ซม. ยาว {length} ซม. สูงกี่เซนติเมตร"),
                        distractors=_story.keep(named("steps.missed_a_step", vol // w),
                                                named("steps.missed_a_step", vol // length),
                                                named("operation.reversed", vol - w * length),
                                                h * 10, answer=h, lo=1))
