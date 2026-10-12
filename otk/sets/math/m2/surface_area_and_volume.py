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
