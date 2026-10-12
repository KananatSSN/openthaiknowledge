"""ปริมาตรและพื้นที่ผิว

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.6/*

Sets moved here from: math, math_geometry, math_p6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


_VOL_TOPIC = "ปริมาตรและพื้นที่ผิว"


@question_type("math.prism_volume",
               display_name={"th": "ปริมาตรของปริซึม"}, level={"th": "ป.6"},
               topic="ปริมาตรและพื้นที่ผิว")
class PrismVolume(WordProblem):
    def expr(self, rng: Random):
        area = rng.randint(6, 50)
        h = rng.randint(2, 15)
        prompt = rng.choice((
            f"ปริซึมพื้นที่ฐาน {area} สูง {h} หน่วย มีปริมาตรเท่าใด?",
            f"ถังน้ำทรงปริซึมมีพื้นที่ฐาน {area} ตารางเดซิเมตร สูง {h} เดซิเมตร "
            f"ถังนี้จุน้ำได้กี่ลูกบาศก์เดซิเมตร",
            f"เสาคอนกรีตทรงปริซึมมีพื้นที่หน้าตัด {area} ตารางเดซิเมตร ยาว {h} เดซิเมตร "
            f"ต้องใช้คอนกรีตกี่ลูกบาศก์เดซิเมตร",
        ))
        return MathDraw("", str(area * h), prompt=prompt,
                        distractors=[str(area + h), str(area * h // 3),
                                     str(2 * area + h)])


@question_type("math.cube_surface_area", display_name={"th": "พื้นที่ผิวของลูกบาศก์"},
               level={"th": "ป.6"}, topic="ปริมาตรและพื้นที่ผิว")
class CubeSurfaceArea(WordProblem):
    def expr(self, rng: Random, side_lo: int = 2, side_hi: int = 15):
        s = rng.randint(side_lo, side_hi)
        prompt = rng.choice((
            f"ลูกบาศก์มีด้านยาว {s} เซนติเมตร มีพื้นที่ผิวกี่ตารางเซนติเมตร",
            f"กล่องของขวัญรูปลูกบาศก์ยาวด้านละ {s} เซนติเมตร ต้องใช้กระดาษห่อให้มิดพอดี"
            f"โดยไม่ซ้อนทับกันกี่ตารางเซนติเมตร",
            f"ทาสีทุกหน้าของลูกเต๋าไม้ที่ยาวด้านละ {s} เซนติเมตร พื้นที่ที่ทาสีเป็นกี่ตารางเซนติเมตร",
        ))
        return MathDraw(
            "", str(6 * s * s), prompt=prompt,
            hint=r"6s^2",
            distractors=[str(s ** 3), str(s * s), str(4 * s * s)])


@question_type("math.composite_box_volume_p6",
               display_name={"th": "ปริมาตรของรูปเรขาคณิตสามมิติที่ประกอบด้วยทรงสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_VOL_TOPIC)
class CompositeBoxVolumeP6(WordProblem):
    def expr(self, rng: Random):
        w1, l1, h1 = rng.randint(2, 12), rng.randint(3, 15), rng.randint(2, 10)
        w2, l2, h2 = rng.randint(2, 10), rng.randint(2, 12), rng.randint(1, 8)
        v1, v2 = w1 * l1 * h1, w2 * l2 * h2
        if rng.random() < 0.5:
            ans = v1 + v2
            thing = rng.choice(("บันไดคอนกรีต", "แท่นรับรางวัล", "ตึกของเล่นจากไม้"))
            prompt = (f"{thing}ประกอบด้วยทรงสี่เหลี่ยมมุมฉากสองก้อน ก้อนแรกกว้าง {w1} ยาว {l1} "
                      f"สูง {h1} เดซิเมตร ก้อนที่สองกว้าง {w2} ยาว {l2} สูง {h2} เดซิเมตร "
                      f"{thing}มีปริมาตรกี่ลูกบาศก์เดซิเมตร")
            # One block only, and the dimensions added before multiplying.
            wrongs = [v1, v2, (w1 + w2) * (l1 + l2) * (h1 + h2)]
        else:
            w2, l2, h2 = min(w2, w1 - 1) or 1, min(l2, l1 - 1) or 1, min(h2, h1 - 1) or 1
            v2 = w2 * l2 * h2
            ans = v1 - v2
            block, stuff = rng.choice((("กล่องไม้", "เนื้อไม้"), ("ก้อนดินน้ำมัน", "ดินน้ำมัน"),
                                       ("แท่งคอนกรีต", "คอนกรีต")))
            prompt = (f"{block}ทรงสี่เหลี่ยมมุมฉากกว้าง {w1} ยาว {l1} สูง {h1} เซนติเมตร "
                      f"ถูกเจาะเป็นช่องทรงสี่เหลี่ยมมุมฉากกว้าง {w2} ยาว {l2} สูง {h2} เซนติเมตร "
                      f"{stuff}ที่เหลือมีปริมาตรกี่ลูกบาศก์เซนติเมตร")
            wrongs = [v1 + v2, v1, (w1 - w2) * (l1 - l2) * (h1 - h2)]
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=_story.keep(*wrongs, ans + 10, answer=ans, lo=1))


@question_type("math.water_level_p6",
               display_name={"th": "ปริมาตรน้ำและระดับน้ำในภาชนะทรงสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_VOL_TOPIC)
class WaterLevelP6(WordProblem):
    def expr(self, rng: Random):
        w, length = rng.choice((20, 25, 30, 40, 50)), rng.choice((20, 30, 40, 50, 60))
        rise = rng.randint(1, 8)
        if rng.random() < 0.5:
            vol = w * length * rise
            tank = rng.choice(("ตู้ปลา", "อ่างน้ำ", "ถังน้ำทรงสี่เหลี่ยมมุมฉาก"))
            thing = rng.choice(("ก้อนหิน", "ลูกเหล็ก", "รูปปั้นดินเผา"))
            return MathDraw("", str(vol),
                            prompt=(f"{tank}กว้าง {w} ซม. ยาว {length} ซม. เมื่อใส่{thing}ลงไปจมมิด "
                                    f"ระดับน้ำสูงขึ้น {rise} ซม. {thing}มีปริมาตรกี่ลูกบาศก์เซนติเมตร"),
                            distractors=_story.keep(w * length, (w + length) * rise, w * length * rise * 10,
                                                    answer=vol))
        litres = w * length * rise * 10 // 1000 or 1
        vol = litres * 1000
        if vol % (w * length):
            return self.expr(rng)
        h = vol // (w * length)
        return MathDraw("", str(h),
                        prompt=(f"เทน้ำ {litres} ลิตร ลงในถังทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {length} ซม. "
                                f"น้ำจะสูงกี่เซนติเมตร (1 ลิตร = 1,000 ลูกบาศก์เซนติเมตร)"),
                        distractors=_story.keep(litres * 100 // (w * length) or h + 1, vol // w,
                                                h * 10, h + 1, answer=h, lo=1))
