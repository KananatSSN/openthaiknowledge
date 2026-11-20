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


# ── More volume (2026-11): a cube's volume, a stone from the water's rise, small cubes in a box, litres and
# cubic centimetres, the largest box, and how long to fill a tank ──


@question_type("math.cube_volume_p5", display_name={"th": "ปริมาตรของลูกบาศก์"},
               level=LEVEL, topic="ปริมาตร")
class CubeVolumeP5(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(2, 15)
        right = a ** 3
        prompt = f"ลูกบาศก์มีสันยาว {a} เซนติเมตร มีปริมาตรกี่ลูกบาศก์เซนติเมตร"
        # The area of one face; the edge times three; all the edges.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(a * a, 3 * a, 12 * a, 6 * a * a, answer=right, lo=1))


@question_type("math.water_rise_volume_p5", display_name={"th": "หาปริมาตรสิ่งของจากระดับน้ำที่สูงขึ้น"},
               level=LEVEL, topic="ปริมาตร")
class WaterRiseVolumeP5(WordProblem):
    def expr(self, rng: Random):
        w, length = rng.randint(10, 40), rng.randint(15, 50)
        rise = rng.randint(1, 6)
        water = rng.randint(10, 30)
        right = w * length * rise
        prompt = (f"ตู้ปลาทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {length} ซม. มีน้ำสูง {water} ซม. "
                  f"เมื่อใส่ก้อนหินลงไป น้ำสูงขึ้นเป็น {water + rise} ซม. ก้อนหินมีปริมาตรกี่ลูกบาศก์เซนติเมตร")
        # The water after, or before; the base area alone.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(w * length * (water + rise), w * length * water, w * length,
                                        right + w * length, answer=right, lo=1))


@question_type("math.cubes_in_box_p5", display_name={"th": "บรรจุลูกบาศก์ลงในกล่องได้กี่ลูก"},
               level=LEVEL, topic="ปริมาตร")
class CubesInBoxP5(WordProblem):
    def expr(self, rng: Random):
        e = rng.choice((2, 3, 5))
        a, b, c = rng.randint(2, 8), rng.randint(2, 8), rng.randint(1, 6)
        right = a * b * c
        prompt = (f"กล่องทรงสี่เหลี่ยมมุมฉากกว้าง {a * e} ซม. ยาว {b * e} ซม. สูง {c * e} ซม. "
                  f"บรรจุลูกบาศก์ที่มีสันยาว {e} ซม. ได้เต็มพอดีกี่ลูก")
        # The box's volume; divided by the edge only once; one layer fewer.
        vol = a * b * c * e ** 3
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(vol, vol // e, a * b * (c - 1) if c > 1 else a * b + 1, right + a * b,
                                        answer=right, lo=1))


@question_type("math.litres_cubic_cm_p5", display_name={"th": "ลิตร มิลลิลิตร และลูกบาศก์เซนติเมตร"},
               level=LEVEL, topic="ปริมาตร")
class LitresCubicCmP5(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            v = rng.randint(11, 99) * 100
            right = v
            prompt = f"{_dec(v, 3)} ลิตร เท่ากับกี่ลูกบาศก์เซนติเมตร"
            return MathDraw("", _g(right), prompt=prompt,
                            distractors=_gk(right // 10, right * 10, v // 100, right + 100, answer=right, lo=1))
        if kind == 1:
            v = rng.randint(11, 99) * 100
            prompt = f"{v:,} มิลลิลิตร เท่ากับกี่ลิตร"
            right = _dec(v, 3)
            wrongs = [_dec(v, 2), _dec(v, 4), _dec(v + 100, 3)]
            return MathDraw("", right, prompt=prompt, distractors=[w for w in dict.fromkeys(wrongs) if w != right])
        v = rng.randint(2, 900)
        prompt = f"{v} ลูกบาศก์เซนติเมตร เท่ากับกี่มิลลิลิตร"
        return MathDraw("", str(v), prompt=prompt,
                        distractors=_story.keep(v * 1000, v * 10, v * 100, v + 10, answer=v, lo=1))


@question_type("math.largest_box_volume_p5", display_name={"th": "กล่องใดมีปริมาตรมากที่สุด"},
               level=LEVEL, topic="ปริมาตร")
class LargestBoxVolumeP5(ChoiceType):
    def compose(self, rng: Random):
        while True:
            dims = [(rng.randint(2, 12), rng.randint(2, 12), rng.randint(2, 12)) for _ in range(4)]
            vols = [a * b * c for a, b, c in dims]
            if len(set(vols)) == 4:
                break
        texts = [f"กว้าง {a} ซม. ยาว {b} ซม. สูง {c} ซม." for a, b, c in dims]
        most = rng.random() < 0.5
        pick = vols.index(max(vols) if most else min(vols))
        return (f"กล่องทรงสี่เหลี่ยมมุมฉากใดมีปริมาตร{'มากที่สุด' if most else 'น้อยที่สุด'}", texts[pick],
                [t for i, t in enumerate(texts) if i != pick])


@question_type("math.fill_tank_time_p5", display_name={"th": "เปิดน้ำใส่ถังกี่นาทีจึงเต็ม"},
               level=LEVEL, topic="ปริมาตร")
class FillTankTimeP5(WordProblem):
    def expr(self, rng: Random):
        rate = rng.choice((2, 4, 5, 10))
        while True:
            w, length, h = rng.randint(2, 10) * 10, rng.randint(2, 12) * 10, rng.randint(2, 8) * 10
            litres = w * length * h // 1000
            if litres % rate == 0:
                break
        right = litres // rate
        prompt = (f"ถังน้ำทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {length} ซม. สูง {h} ซม. "
                  f"เปิดน้ำไหลลงถังนาทีละ {rate} ลิตร กี่นาทีน้ำจึงเต็มถัง")
        # The litres; the cubic centimetres divided by the rate; times instead of divided.
        return MathDraw("", _g(right), prompt=prompt,
                        distractors=_gk(litres, w * length * h // rate, litres * rate, right + 1,
                                        answer=right, lo=1))
