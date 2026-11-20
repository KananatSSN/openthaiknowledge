"""พื้นที่ผิวและปริมาตร

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 2.1 ม.2/*

Sets moved here from: math, math_m2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_m2 import LEVEL, triple
from otk.sets._support.math_p4 import grouped

PROVENANCE = Provenance("original")


_SV_TOPIC = "พื้นที่ผิวและปริมาตร"


@question_type("math.cylinder_volume",
               display_name={"th": "ปริมาตรทรงกระบอก"}, level={"th": "ม.2"},
               topic="พื้นที่ผิวและปริมาตร")
class CylinderVolume(WordProblem):
    def expr(self, rng: Random):
        r = rng.choice([7, 14])                     # clean with π ≈ 22/7
        h = rng.randint(2, 15)
        vol = 22 * r * r * h // 7
        lateral = 2 * 22 * r * h // 7
        prompt = rng.choice((
            f"ทรงกระบอกรัศมี {r} สูง {h} หน่วย (π ≈ 22/7) มีปริมาตรเท่าใด?",
            f"หม้อทรงกระบอกรัศมี {r} เซนติเมตร สูง {h} เซนติเมตร จุน้ำได้กี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)",
            f"ถังเก็บน้ำทรงกระบอกรัศมี {r} เดซิเมตร สูง {h} เดซิเมตร จุน้ำได้กี่ลูกบาศก์เดซิเมตร (π ≈ 22/7)",
        ))
        return MathDraw("", str(vol), prompt=prompt,
                        distractors=[str(lateral), str(22 * r * h // 7),
                                     str(22 * r * r // 7)])


@question_type("math.prism_surface_area_m2",
               display_name={"th": "พื้นที่ผิวของปริซึม"},
               level=LEVEL, topic=_SV_TOPIC)
class PrismSurfaceAreaM2(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            w, span, h = (rng.randint(2, 15) for _ in range(3))
            sa = 2 * (w * span + span * h + w * h)
            thing = rng.choice(("กล่องของขวัญ", "กล่องนม", "ตู้ไม้", "กล่องรองเท้า"))
            return MathDraw("", str(sa),
                            prompt=(f"{thing}ทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {span} ซม. สูง {h} ซม. "
                                    f"มีพื้นที่ผิวทั้งหมดกี่ตารางเซนติเมตร"),
                            # The volume, and each face counted once.
                            distractors=_story.keep(w * span * h, w * span + span * h + w * h,
                                                    2 * (w * span + span * h), answer=sa))
        a, b, c = triple(rng, 2)
        length = rng.randint(4, 20)
        base = a * b // 2
        sa = 2 * base + (a + b + c) * length
        return MathDraw("", str(sa),
                        prompt=(f"ปริซึมสามเหลี่ยมมีฐานเป็นรูปสามเหลี่ยมมุมฉากที่มีด้านยาว {a}, {b} และ {c} ซม. "
                                f"ปริซึมยาว {length} ซม. มีพื้นที่ผิวทั้งหมดกี่ตารางเซนติเมตร"),
                        distractors=_story.keep((a + b + c) * length, base + (a + b + c) * length,
                                                base * length, 2 * a * b + (a + b + c) * length,
                                                answer=sa))


@question_type("math.cylinder_surface_area_m2",
               display_name={"th": "พื้นที่ผิวของทรงกระบอก"},
               level=LEVEL, topic=_SV_TOPIC)
class CylinderSurfaceAreaM2(WordProblem):
    def expr(self, rng: Random):
        r = rng.choice((7, 14, 21))
        h = rng.randint(3, 30)
        lateral = 2 * 22 * r * h // 7
        total = lateral + 2 * 22 * r * r // 7
        if rng.random() < 0.5:
            can = rng.choice(("กระป๋องนม", "กระป๋องสี", "ถังพลาสติกทรงกระบอก"))
            return MathDraw("", str(lateral),
                            prompt=(f"{can}รัศมี {r} ซม. สูง {h} ซม. ต้องใช้กระดาษฉลากพันรอบ"
                                    f"ด้านข้างพอดี กระดาษมีพื้นที่กี่ตารางเซนติเมตร (π ≈ 22/7)"),
                            distractors=_story.keep(total, 22 * r * h // 7, 22 * r * r * h // 7,
                                                    answer=lateral))
        tank = rng.choice(("ถังทรงกระบอกมีฝาปิดทั้งสองด้าน", "กล่องขนมทรงกระบอกมีฝาปิดหัวท้าย",
                           "ท่อนไม้ทรงกระบอกซึ่งจะทาสีทุกด้าน"))
        return MathDraw("", str(total),
                        prompt=(f"{tank} รัศมี {r} ซม. สูง {h} ซม. "
                                f"มีพื้นที่ผิวทั้งหมดกี่ตารางเซนติเมตร (π ≈ 22/7)"),
                        # Only one lid, and no lids at all.
                        distractors=_story.keep(lateral + 22 * r * r // 7, lateral,
                                                22 * r * r * h // 7, answer=total))


@question_type("math.prism_cylinder_volume_word_m2",
               display_name={"th": "โจทย์ปัญหาปริมาตรของปริซึมและทรงกระบอก"},
               level=LEVEL, topic=_SV_TOPIC)
class PrismCylinderVolumeWordM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(6)
        if kind == 3:
            r, h = rng.choice((7, 14)), 2 * rng.randint(3, 20)
            vol = 22 * r * r * h // 7
            return MathDraw("", str(vol // 2),
                            prompt=(f"ถังน้ำทรงกระบอกรัศมี {r} ซม. สูง {h} ซม. มีน้ำอยู่ครึ่งถัง "
                                    f"มีน้ำกี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)"),
                            distractors=_story.keep(vol, 22 * r * h // 7, vol // 4, answer=vol // 2))
        if kind == 4:
            a, b = rng.randint(2, 8), rng.randint(9, 16)
            h = 2 * rng.randint(2, 6)
            length = rng.randint(10, 50)
            vol = (a + b) * h // 2 * length
            return MathDraw("", str(vol),
                            prompt=(f"รางน้ำทรงปริซึมมีหน้าตัดเป็นรูปสี่เหลี่ยมคางหมู ด้านคู่ขนานยาว {a} ซม. และ "
                                    f"{b} ซม. สูง {h} ซม. รางยาว {length} ซม. จุน้ำได้กี่ลูกบาศก์เซนติเมตร"),
                            # Forgetting the half; the lengths added.
                            distractors=_story.keep((a + b) * h * length, a * b * h * length // 2,
                                                    (a + b + h) * length, answer=vol))
        if kind == 5:
            w, span = rng.randint(20, 40), rng.randint(30, 60)
            depth = rng.randint(10, 35)
            vol = w * span * depth
            return MathDraw("", str(depth),
                            prompt=(f"ตู้ปลาทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {span} ซม. เทน้ำลงไป "
                                    f"{grouped(vol)} ลูกบาศก์เซนติเมตร น้ำสูงกี่เซนติเมตร"),
                            distractors=_story.keep(vol // w, vol // span, depth + 5, answer=depth, lo=1))
        if kind == 0:
            b, h = 2 * rng.randint(2, 10), rng.randint(3, 15)
            length = rng.randint(5, 30)
            vol = b * h // 2 * length
            return MathDraw("", str(vol),
                            prompt=(f"เต็นท์ทรงปริซึมสามเหลี่ยม หน้าตัดเป็นรูปสามเหลี่ยมฐานยาว {b} ดม. สูง {h} ดม. "
                                    f"เต็นท์ยาว {length} ดม. มีปริมาตรกี่ลูกบาศก์เดซิเมตร"),
                            # Forgetting the half of the triangle.
                            distractors=_story.keep(b * h * length, b * h // 2 + length,
                                                    (b + h) * length, answer=vol))
        if kind == 1:
            r = rng.choice((7, 14))
            h = rng.randint(5, 40)
            vol = 22 * r * r * h // 7
            return MathDraw("", str(vol),
                            prompt=(f"แก้วน้ำทรงกระบอกรัศมีภายใน {r} ซม. สูง {h} ซม. จุน้ำได้กี่ลูกบาศก์"
                                    f"เซนติเมตร (π ≈ 22/7)"),
                            # The diameter used as the radius, and the side area.
                            distractors=_story.keep(22 * 4 * r * r * h // 7, 2 * 22 * r * h // 7,
                                                    22 * r * h // 7, answer=vol))
        w, span, depth = rng.randint(2, 10), rng.randint(5, 25), rng.choice((1, 2))
        vol = w * span * depth
        return MathDraw("", str(vol),
                        prompt=(f"สระน้ำทรงสี่เหลี่ยมมุมฉากกว้าง {w} ม. ยาว {span} ม. ลึก {depth} ม. "
                                f"ถ้าเติมน้ำจนเต็มต้องใช้น้ำกี่ลูกบาศก์เมตร"),
                        distractors=_story.keep(w * span, 2 * (w * span + span * depth + w * depth),
                                                w + span + depth, answer=vol))


# ── More surface area and volume (สสวท. ม.2 เล่ม 1 บทที่ 3): a prism from its base area, a cylinder's
# height or radius from its volume, capacity in litres, a pipe, a box with a hole, and scaling ──

_SEVENS = (7, 14, 21)


@question_type("math.prism_volume_base_m2", display_name={"th": "ปริมาตรของปริซึมจากพื้นที่ฐาน"},
               level=LEVEL, topic=_SV_TOPIC)
class PrismVolumeBaseM2(WordProblem):
    """V = base area × height, forwards and back."""

    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            base, h = rng.randint(12, 90), rng.randint(3, 20)
            vol = base * h
            return MathDraw("", str(vol), prompt=(f"ปริซึมรูปหนึ่งมีพื้นที่ฐาน {base} ตารางเซนติเมตร สูง {h} เซนติเมตร "
                                                 f"มีปริมาตรกี่ลูกบาศก์เซนติเมตร"),
                            # Halved as for a pyramid; added; doubled.
                            distractors=_story.keep(vol // 2 if vol % 2 == 0 else 0, base + h, 2 * vol,
                                                    base * (h + 1), answer=vol, lo=1))
        if kind == 1:
            base, h = rng.randint(12, 90), rng.randint(3, 20)
            vol = base * h
            return MathDraw("", str(h), prompt=(f"ปริซึมรูปหนึ่งมีปริมาตร {grouped(vol)} ลูกบาศก์เซนติเมตร "
                                               f"และมีพื้นที่ฐาน {base} ตารางเซนติเมตร ปริซึมสูงกี่เซนติเมตร"),
                            distractors=_story.keep(vol - base, 2 * h, h + 3, h - 2, answer=h, lo=1))
        s, h = rng.randint(3, 12), rng.randint(4, 20)
        vol = s * s * h
        return MathDraw("", str(vol), prompt=(f"ปริซึมฐานเป็นรูปสี่เหลี่ยมจัตุรัสยาวด้านละ {s} เซนติเมตร "
                                             f"สูง {h} เซนติเมตร มีปริมาตรกี่ลูกบาศก์เซนติเมตร"),
                        # The side not squared; the base perimeter used; the four side faces.
                        distractors=_story.keep(s * h, 4 * s * h, 2 * s * h, s * s + h, answer=vol, lo=1))


@question_type("math.cylinder_dimension_m2", display_name={"th": "หาความสูงหรือรัศมีของทรงกระบอกจากปริมาตร"},
               level=LEVEL, topic=_SV_TOPIC)
class CylinderDimensionM2(WordProblem):
    """V = πr²h worked backwards (π ≈ 22/7)."""

    def expr(self, rng: Random):
        r, h = rng.choice(_SEVENS), rng.randint(2, 20)
        vol = 22 * r * r * h // 7
        if rng.random() < 0.5:
            # r not squared (gives rh); the diameter used for r; the volume over r².
            return MathDraw("", str(h), prompt=(f"ทรงกระบอกรัศมี {r} เซนติเมตร มีปริมาตร {grouped(vol)} "
                                               f"ลูกบาศก์เซนติเมตร ทรงกระบอกสูงกี่เซนติเมตร (π ≈ 22/7)"),
                            distractors=_story.keep(r * h, h // 4 if h % 4 == 0 else 0, vol // (r * r), 2 * h,
                                                    h + 2, answer=h, lo=1))
        return MathDraw("", str(r), prompt=(f"ทรงกระบอกสูง {h} เซนติเมตร มีปริมาตร {grouped(vol)} "
                                           f"ลูกบาศก์เซนติเมตร รัศมียาวกี่เซนติเมตร (π ≈ 22/7)"),
                        # The diameter; r² not square-rooted; the other radii.
                        distractors=_story.keep(2 * r, r * r, *[s for s in _SEVENS if s != r], answer=r, lo=1))


@question_type("math.volume_litres_m2", display_name={"th": "ความจุเป็นลิตร"},
               level=LEVEL, topic=_SV_TOPIC)
class VolumeLitresM2(WordProblem):
    """1 litre is 1,000 cubic centimetres."""

    def expr(self, rng: Random):
        w, d, h = (10 * rng.randint(1, 6) for _ in range(3))
        litres = w * d * h // 1000
        if rng.random() < 0.5:
            # Divided by 100; by 10; not converted at all is too big to offer, so the cm² of the base.
            return MathDraw("", str(litres), prompt=(f"ตู้ปลาทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {d} ซม. สูง {h} ซม. "
                                                    f"จุน้ำได้กี่ลิตร (1 ลิตร = 1,000 ลูกบาศก์เซนติเมตร)"),
                            distractors=_story.keep(10 * litres, 100 * litres, w * d // 100, litres + w // 10,
                                                    answer=litres, lo=1))
        return MathDraw("", str(h), prompt=(f"ถังทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {d} ซม. เทน้ำลงไป {litres} ลิตร "
                                           f"น้ำสูงกี่เซนติเมตร (1 ลิตร = 1,000 ลูกบาศก์เซนติเมตร)"),
                        # Litres used as cm³; ten times; litres over the width.
                        distractors=_story.keep(10 * h, h // 10 if h % 10 == 0 else 0, 100 * litres // w,
                                                h + 10, answer=h, lo=1))


_PIPES = ((14, 7), (21, 14), (21, 7), (28, 21), (28, 14), (35, 28))


@question_type("math.hollow_cylinder_m2", display_name={"th": "ปริมาตรของท่อทรงกระบอกกลวง"},
               level=LEVEL, topic=_SV_TOPIC)
class HollowCylinderM2(WordProblem):
    """A pipe: the outer cylinder less the inner, π(R² − r²)h."""

    def expr(self, rng: Random):
        big, small = rng.choice(_PIPES)
        h = rng.randint(5, 30)
        vol = 22 * (big * big - small * small) * h // 7
        prompt = (f"ท่อคอนกรีตทรงกระบอกกลวงยาว {h} ซม. รัศมีภายนอก {big} ซม. รัศมีภายใน {small} ซม. "
                  f"เนื้อคอนกรีตมีปริมาตรกี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)")
        # The radii subtracted before squaring; the outer cylinder only; the hole only.
        return MathDraw("", str(vol), prompt=prompt,
                        distractors=_story.keep(22 * (big - small) ** 2 * h // 7, 22 * big * big * h // 7,
                                                22 * small * small * h // 7, answer=vol, lo=1))


@question_type("math.box_with_hole_m2", display_name={"th": "ปริมาตรของทรงสี่เหลี่ยมมุมฉากที่เจาะรูทรงกระบอก"},
               level=LEVEL, topic=_SV_TOPIC)
class BoxWithHoleM2(WordProblem):
    """A box with a cylindrical hole through its height: the box less the cylinder."""

    def expr(self, rng: Random):
        r = rng.choice((7, 7, 14))
        lo = 16 if r == 7 else 30
        w, d, h = rng.randint(lo, lo + 14), rng.randint(lo, lo + 14), rng.randint(5, 20)
        hole = 22 * r * r * h // 7
        vol = w * d * h - hole
        prompt = (f"แท่งไม้ทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {d} ซม. สูง {h} ซม. ถูกเจาะรูทรงกระบอก"
                  f"รัศมี {r} ซม. ทะลุจากด้านบนถึงด้านล่าง เนื้อไม้ที่เหลือมีปริมาตรกี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)")
        # The box without the hole; the hole itself; the hole added on.
        return MathDraw("", str(vol), prompt=prompt,
                        distractors=_story.keep(w * d * h, hole, w * d * h + hole,
                                                w * d * h - 22 * r * h // 7, answer=vol, lo=1))


@question_type("math.scale_volume_m2", display_name={"th": "ปริมาตรและพื้นที่ผิวเมื่อขยายขนาด"},
               level=LEVEL, topic=_SV_TOPIC)
class ScaleVolumeM2(WordProblem):
    """Every length × k multiplies area by k² and volume by k³; one length × k multiplies volume by k."""

    def expr(self, rng: Random):
        k = rng.choice((2, 3))
        kind = rng.randrange(4)
        if kind == 0:
            prompt = f"ถ้าขยายกล่องทรงสี่เหลี่ยมมุมฉากให้ด้านทุกด้านยาวเป็น {k} เท่าของเดิม ปริมาตรจะเป็นกี่เท่าของเดิม"
            right = k ** 3
        elif kind == 1:
            prompt = f"ถ้าขยายกล่องทรงสี่เหลี่ยมมุมฉากให้ด้านทุกด้านยาวเป็น {k} เท่าของเดิม พื้นที่ผิวจะเป็นกี่เท่าของเดิม"
            right = k ** 2
        elif kind == 2:
            prompt = f"ถ้าทรงกระบอกมีรัศมีเป็น {k} เท่าของเดิม แต่ความสูงเท่าเดิม ปริมาตรจะเป็นกี่เท่าของเดิม"
            right = k ** 2
        else:
            prompt = f"ถ้าทรงกระบอกมีความสูงเป็น {k} เท่าของเดิม แต่รัศมีเท่าเดิม ปริมาตรจะเป็นกี่เท่าของเดิม"
            right = k
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(k, k ** 2, k ** 3, 2 * k, 3 * k, answer=right, lo=1))


# ── To fifteen (2026-11): a cube from its area or volume, the side faces of a prism, cups to fill a tank,
# painting a room, and melting one solid into another ──


@question_type("math.cube_area_volume_m2", display_name={"th": "ลูกบาศก์: จากพื้นที่ผิวหาปริมาตร และกลับกัน"},
               level=LEVEL, topic=_SV_TOPIC)
class CubeAreaVolumeM2(WordProblem):
    """The edge first: from 6e² or from e³, then the other measure."""

    def expr(self, rng: Random):
        e = rng.randint(2, 15)
        if rng.random() < 0.5:
            return MathDraw("", str(e ** 3), prompt=(f"ลูกบาศก์มีพื้นที่ผิวทั้งหมด {grouped(6 * e * e)} ตารางเซนติเมตร "
                                                    f"มีปริมาตรกี่ลูกบาศก์เซนติเมตร"),
                            # The edge itself; the area of one face; the area divided by six cubed wrongly.
                            distractors=_story.keep(e * e, e, 6 * e ** 3, 4 * e * e, answer=e ** 3, lo=1))
        return MathDraw("", str(6 * e * e), prompt=(f"ลูกบาศก์มีปริมาตร {grouped(e ** 3)} ลูกบาศก์เซนติเมตร "
                                                   f"มีพื้นที่ผิวทั้งหมดกี่ตารางเซนติเมตร"),
                        # One face; four faces; the edge times six.
                        distractors=_story.keep(e * e, 4 * e * e, 6 * e, 12 * e, answer=6 * e * e, lo=1))


@question_type("math.prism_lateral_area_m2", display_name={"th": "พื้นที่ผิวข้างของปริซึม"},
               level=LEVEL, topic=_SV_TOPIC)
class PrismLateralAreaM2(WordProblem):
    """The side faces unroll into one rectangle: the base perimeter times the height."""

    def expr(self, rng: Random):
        h = rng.randint(3, 20)
        kind = rng.randrange(3)
        if kind == 0:
            w, d = rng.randint(2, 12), rng.randint(2, 12)
            base, per, area = f"รูปสี่เหลี่ยมผืนผ้ากว้าง {w} ซม. ยาว {d} ซม.", 2 * (w + d), w * d
        elif kind == 1:
            a, b, c = triple(rng, 2)
            base, per, area = f"รูปสามเหลี่ยมมุมฉากที่มีด้านยาว {a}, {b} และ {c} ซม.", a + b + c, a * b // 2
        else:
            n, side = rng.choice((5, 6, 8)), rng.randint(2, 10)
            base, per, area = f"รูป {n} เหลี่ยมด้านเท่ายาวด้านละ {side} ซม.", n * side, 0
        lateral = per * h
        # Both bases added on; the perimeter plus the height; half of it.
        return MathDraw("", str(lateral), prompt=f"ปริซึมฐานเป็น{base} สูง {h} ซม. มีพื้นที่ผิวข้างกี่ตารางเซนติเมตร",
                        distractors=_story.keep(lateral + 2 * area if area else lateral + per, per + h,
                                                lateral // 2 if lateral % 2 == 0 else 0, 2 * lateral, answer=lateral, lo=1))


@question_type("math.cups_to_fill_m2", display_name={"th": "ตักน้ำด้วยแก้วทรงกระบอกกี่แก้วจึงเต็มถัง"},
               level=LEVEL, topic=_SV_TOPIC)
class CupsToFillM2(WordProblem):
    """The tank's volume divided by one cup's (π ≈ 22/7)."""

    def expr(self, rng: Random):
        m, h = rng.randint(1, 4), rng.randint(4, 12)
        w, d = 22, 35 * m
        cups = m * h  # 22 × 35m × 2h = 1,540mh, and one cup holds 22/7 × 7² × 10 = 1,540
        prompt = (f"ตู้ทรงสี่เหลี่ยมมุมฉากกว้าง {w} ซม. ยาว {d} ซม. สูง {2 * h} ซม. ใช้แก้วทรงกระบอกรัศมี 7 ซม. "
                  f"สูง 10 ซม. ตักน้ำเทลงจนเต็ม ต้องตักกี่แก้ว (π ≈ 22/7)")
        # The cup's height left out; the cup taken as a box 14 × 14 × 10; half as many.
        return MathDraw("", str(cups), prompt=prompt,
                        distractors=_story.keep(w * d * 2 * h // 154, w * d * 2 * h // 1960, 2 * cups, cups + 2,
                                                answer=cups, lo=1))


@question_type("math.paint_room_m2", display_name={"th": "พื้นที่ผนังห้องและค่าทาสี"},
               level=LEVEL, topic=_SV_TOPIC)
class PaintRoomM2(WordProblem):
    """Four walls of a room: the lateral area 2(L + W)H, then its cost."""

    def expr(self, rng: Random):
        length, width, height = rng.randint(3, 8), rng.randint(3, 8), rng.randint(2, 4)
        walls = 2 * (length + width) * height
        if rng.random() < 0.5:
            # The ceiling added; two walls only; the volume.
            return MathDraw("", str(walls), prompt=(f"ห้องทรงสี่เหลี่ยมมุมฉากกว้าง {width} ม. ยาว {length} ม. สูง {height} ม. "
                                                   f"ต้องการทาสีผนังทั้งสี่ด้าน ผนังมีพื้นที่รวมกี่ตารางเมตร"),
                            distractors=_story.keep(walls + length * width, (length + width) * height,
                                                    length * width * height, answer=walls, lo=1))
        rate = rng.choice((20, 25, 30, 40, 50))
        cost = walls * rate
        return MathDraw("", grouped(cost), prompt=(f"ห้องทรงสี่เหลี่ยมมุมฉากกว้าง {width} ม. ยาว {length} ม. สูง {height} ม. "
                                                  f"ค่าทาสีตารางเมตรละ {rate} บาท ทาผนังทั้งสี่ด้านเสียค่าทาสีกี่บาท"),
                        # The floor and ceiling painted too; two walls only; the volume used.
                        distractors=[grouped(int(v)) for v in _story.keep(
                            (walls + 2 * length * width) * rate, (length + width) * height * rate,
                            length * width * height * rate, answer=cost, lo=1)])


@question_type("math.melt_recast_m2", display_name={"th": "หลอมทรงหนึ่งเป็นอีกทรงหนึ่ง"},
               level=LEVEL, topic=_SV_TOPIC)
class MeltRecastM2(WordProblem):
    """Melting keeps the volume."""

    def expr(self, rng: Random):
        if rng.random() < 0.5:
            e = rng.choice((1, 2, 3))
            p, q, r = rng.randint(2, 6), rng.randint(2, 6), rng.randint(2, 6)
            count = p * q * r
            prompt = (f"หลอมแท่งโลหะทรงสี่เหลี่ยมมุมฉากกว้าง {e * p} ซม. ยาว {e * q} ซม. สูง {e * r} ซม. "
                      f"เป็นลูกบาศก์เล็กยาวด้านละ {e} ซม. ได้กี่ลูก")
            # The edge not cubed; the bar's volume itself; the edges added.
            return MathDraw("", str(count), prompt=prompt,
                            distractors=_story.keep(count * e * e, count * e ** 3 if e > 1 else count * 2,
                                                    count * e if e > 1 else count + 1, e * (p + q + r),
                                                    answer=count, lo=1))
        k = rng.choice((2, 4, 7))
        h = k * rng.randint(2, 10)
        height = h // k
        prompt = (f"หลอมแท่งโลหะทรงกระบอกรัศมี 7 ซม. สูง {h} ซม. แล้วหล่อเป็นแท่งทรงสี่เหลี่ยมมุมฉาก"
                  f"ที่มีฐานกว้าง 22 ซม. ยาว {7 * k} ซม. แท่งใหม่สูงกี่เซนติเมตร (π ≈ 22/7)")
        # The cylinder's height kept; the diameter used for the radius (four times); twice.
        return MathDraw("", str(height), prompt=prompt,
                        distractors=_story.keep(h, 4 * height, 2 * height, height + 1, answer=height, lo=1))
