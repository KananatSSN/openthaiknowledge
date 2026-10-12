"""พื้นที่ผิวและปริมาตร

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 2.1 ม.3/*

Sets moved here from: math, math_m3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, frac_answer_tex
from otk.sets._support.math_m3 import LEVEL
from otk.sets._support.math_p4 import grouped

PROVENANCE = Provenance("original")


_SV_TOPIC = "พื้นที่ผิวและปริมาตร"


@question_type("math.cone_volume",
               display_name={"th": "ปริมาตรกรวย"}, level={"th": "ม.3"},
               topic="พื้นที่ผิวและปริมาตร")
class ConeVolume(WordProblem):
    def expr(self, rng: Random):
        r = 7                                       # keeps π ≈ 22/7 exact
        h = rng.choice([3, 6, 9, 12, 15])           # divisible by 3 → integer
        vol = 22 * r * r * h // 21                  # (1/3)πr²h
        prompt = rng.choice((
            f"กรวยรัศมี {r} สูง {h} หน่วย (π ≈ 22/7) มีปริมาตรเท่าใด?",
            f"กองทรายรูปกรวยมีรัศมีฐาน {r} เมตร สูง {h} เมตร มีทรายกี่ลูกบาศก์เมตร (π ≈ 22/7)",
            f"กรวยกระดาษใส่ขนมมีรัศมีปาก {r} เซนติเมตร สูง {h} เซนติเมตร "
            f"จุขนมได้เต็มพอดีกี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)",
        ))
        return MathDraw("", str(vol), prompt=prompt,
                        distractors=[str(vol * 3), str(22 * r * r * h // 7),
                                     str(22 * r * h // 7)])


@question_type("math.pyramid_volume_m3",
               display_name={"th": "ปริมาตรพีระมิด"},
               level=LEVEL, topic=_SV_TOPIC)
class PyramidVolumeM3(WordProblem):
    def expr(self, rng: Random):
        a, h = rng.randint(3, 20), 3 * rng.randint(1, 10)
        vol = a * a * h // 3
        if rng.random() < 0.5:
            thing = rng.choice(("พีระมิดฐานสี่เหลี่ยมจัตุรัส", "ที่ทับกระดาษรูปพีระมิดฐานสี่เหลี่ยมจัตุรัส",
                                "หลังคาทรงพีระมิดฐานสี่เหลี่ยมจัตุรัส"))
            return MathDraw("", str(vol),
                            prompt=(f"{thing}ยาวด้านละ {a} ซม. สูง {h} ซม. "
                                    f"มีปริมาตรกี่ลูกบาศก์เซนติเมตร"),
                            # Forgetting the third, and a × h without squaring.
                            distractors=_story.keep(a * a * h, a * h // 3 if a * h % 3 == 0 else a * h,
                                                    a * a * h // 2 if a * a * h % 2 == 0 else vol * 2,
                                                    answer=vol))
        return MathDraw("", str(h),
                        prompt=(f"พีระมิดฐานสี่เหลี่ยมจัตุรัสยาวด้านละ {a} ซม. มีปริมาตร {grouped(vol)} "
                                f"ลูกบาศก์เซนติเมตร พีระมิดสูงกี่เซนติเมตร"),
                        distractors=_story.keep(h // 3, vol // a if vol % a == 0 else h + 3, h + 3,
                                                answer=h, lo=1))


@question_type("math.sphere_volume",
               display_name={"th": "ปริมาตรทรงกลม"}, level={"th": "ม.3"},
               topic="พื้นที่ผิวและปริมาตร")
class SphereVolume(WordProblem):
    def expr(self, rng: Random):
        r = rng.randint(1, 6)
        vol = Fraction(4, 3) * Fraction(22, 7) * r ** 3     # (4/3)πr³
        cyl = Fraction(22, 7) * r ** 3                      # πr³ (forgot 4/3)
        prompt = rng.choice((
            f"ทรงกลมรัศมี {r} หน่วย (π ≈ 22/7) มีปริมาตรเท่าใด?",
            f"ลูกบอลลูกหนึ่งรัศมี {r} นิ้ว มีปริมาตรกี่ลูกบาศก์นิ้ว (π ≈ 22/7)",
            f"ลูกแก้วลูกหนึ่งรัศมี {r} เซนติเมตร ใช้แก้วกี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)",
        ))
        return MathDraw("", frac_answer_tex(vol), prompt=prompt,
                        distractors=[frac_answer_tex(cyl),
                                     frac_answer_tex(vol * Fraction(3, 4))])


@question_type("math.cone_sphere_surface_area_m3",
               display_name={"th": "พื้นที่ผิวของกรวยและทรงกลม"},
               level=LEVEL, topic=_SV_TOPIC)
class ConeSphereSurfaceAreaM3(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            # Radius a multiple of 7 for π ≈ 22/7, with a whole slant height.
            r, h, length = rng.choice(((7, 24, 25), (14, 48, 50), (21, 72, 75), (21, 20, 29),
                                        (28, 45, 53), (35, 12, 37)))
            lateral = 22 * r * length // 7
            total = lateral + 22 * r * r // 7
            if rng.random() < 0.5:
                return MathDraw("", str(lateral),
                                prompt=(f"กรวยมีรัศมีของฐาน {r} ซม. และสูงเอียง {length} ซม. มีพื้นที่ผิวข้าง"
                                        f"กี่ตารางเซนติเมตร (π ≈ 22/7)"),
                                # Using the height where the slant height belongs.
                                distractors=_story.keep(22 * r * h // 7, total, 2 * lateral,
                                                        answer=lateral))
            return MathDraw("", str(total),
                            prompt=(f"กรวยตันมีรัศมีของฐาน {r} ซม. และสูง {h} ซม. มีพื้นที่ผิวทั้งหมดกี่"
                                    f"ตารางเซนติเมตร (π ≈ 22/7)"),
                            distractors=_story.keep(lateral, 22 * r * h // 7 + 22 * r * r // 7,
                                                    22 * r * (r + h) * 2 // 7, answer=total))
        r = 7 * rng.randint(1, 6)
        if rng.random() < 0.3:
            # A hemisphere's curved surface is half the sphere's: 2πr².
            curved = 2 * 22 * r * r // 7
            return MathDraw("", str(curved),
                            prompt=(f"ชามรูปครึ่งทรงกลมมีรัศมี {r} ซม. มีพื้นที่ผิวโค้งด้านนอกกี่ตารางเซนติเมตร "
                                    f"(π ≈ 22/7)"),
                            distractors=_story.keep(4 * 22 * r * r // 7, 3 * 22 * r * r // 7,
                                                    22 * r * r // 7, answer=curved))
        sa = 4 * 22 * r * r // 7
        return MathDraw("", str(sa),
                        prompt=f"ลูกบอลทรงกลมมีรัศมี {r} ซม. มีพื้นที่ผิวกี่ตารางเซนติเมตร (π ≈ 22/7)",
                        # πr², 2πr², and the volume's 4/3.
                        distractors=_story.keep(22 * r * r // 7, 2 * 22 * r * r // 7,
                                                4 * 22 * r ** 3 // 21, answer=sa))


@question_type("math.solid_word_problem_m3",
               display_name={"th": "โจทย์ปัญหาปริมาตรของกรวย ทรงกลม และทรงกระบอก"},
               level=LEVEL, topic=_SV_TOPIC)
class SolidWordProblemM3(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(6)
        if kind == 3:
            r, h = rng.randint(3, 10), 3 * rng.randint(2, 10)
            return MathDraw("", str(h // 3),
                            prompt=(f"ตักน้ำด้วยกรวยรัศมี {r} ซม. สูง {h} ซม. จนเต็ม แล้วเทใส่ทรงกระบอกที่มีรัศมี "
                                    f"{r} ซม. เท่ากัน น้ำในทรงกระบอกสูงกี่เซนติเมตร"),
                            distractors=_story.keep(h, h // 2 if h % 2 == 0 else h + 3, 3 * h,
                                                    answer=h // 3, lo=1))
        if kind == 4:
            r = rng.randint(2, 12)
            return MathDraw("", str(4 * r),
                            prompt=(f"หลอมลูกเหล็กทรงกลมรัศมี {r} ซม. แล้วหล่อเป็นกรวยที่มีรัศมีฐาน {r} ซม. "
                                    f"เท่ากัน กรวยสูงกี่เซนติเมตร (ไม่มีเนื้อเหล็กสูญหาย)"),
                            distractors=_story.keep(r, 2 * r, 3 * r, answer=4 * r, lo=1))
        if kind == 5:
            h = 3 * rng.randint(2, 8)
            vol = 154 * h // 3
            return MathDraw("", str(vol),
                            prompt=(f"ถ้วยน้ำดื่มกระดาษทรงกรวยมีรัศมีปากถ้วย 7 ซม. สูง {h} ซม. "
                                    f"จุน้ำได้กี่ลูกบาศก์เซนติเมตร (π ≈ 22/7)"),
                            distractors=_story.keep(154 * h, 44 * h, vol * 2, answer=vol))
        if kind == 0:
            big, small = rng.choice(((6, 2), (6, 3), (9, 3), (8, 2), (8, 4), (10, 5), (12, 4)))
            n = (big // small) ** 3
            return MathDraw("", str(n),
                            prompt=(f"หลอมลูกเหล็กทรงกลมรัศมี {big} ซม. แล้วหล่อเป็นลูกเหล็กทรงกลมรัศมี "
                                    f"{small} ซม. ได้กี่ลูก (ไม่มีเนื้อเหล็กสูญหาย)"),
                            # Radii compared instead of volumes, or squared.
                            distractors=_story.keep(big // small, (big // small) ** 2, n * 2,
                                                    answer=n, lo=1))
        if kind == 1:
            cups = 3 * rng.randint(1, 5)
            return MathDraw("", str(cups),
                            prompt=(f"กรวยและทรงกระบอกมีรัศมีและความสูงเท่ากัน ถ้าตักน้ำด้วยกรวยจนเต็มแล้วเทใส่"
                                    f"ทรงกระบอก ต้องเทกี่ครั้งจึงจะเต็มทรงกระบอก {cups // 3} ใบ"),
                            distractors=_story.keep(cups // 3, 2 * cups // 3, cups + 3, 4 * cups // 3,
                                                    answer=cups, lo=1))
        r = 7
        h = 3 * rng.randint(2, 8)
        cone = 22 * r * r * h // 21
        hemi = 2 * 22 * r ** 3 // 21
        total = cone + hemi
        return MathDraw("", str(total),
                        prompt=(f"ไอศกรีมโคนประกอบด้วยกรวยรัศมี {r} ซม. สูง {h} ซม. ที่มีไอศกรีมเต็ม "
                                f"และด้านบนเป็นครึ่งทรงกลมรัศมี {r} ซม. มีไอศกรีมทั้งหมดกี่ลูกบาศก์เซนติเมตร "
                                f"(π ≈ 22/7)"),
                        # A whole sphere on top, and the cone alone.
                        distractors=_story.keep(cone + 2 * hemi, cone, hemi + 3 * cone,
                                                answer=total))
