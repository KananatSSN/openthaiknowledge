"""มิติสัมพันธ์ของรูปเรขาคณิต

คณิตศาสตร์ · ม.1 · สสวท. พื้นฐาน
Indicators: ค 2.2 ม.1/*

Sets moved here from: math_diagrams, math_m1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import NETS, _img, _text_q
from otk.sets._support.math_m1 import LEVEL

PROVENANCE = Provenance("original")


_SPACE_TOPIC = "มิติสัมพันธ์ของรูปเรขาคณิต"


@question_type("math.net_picture_m1", display_name={"th": "รูปคลี่นี้ประกอบเป็นรูปเรขาคณิตสามมิติใด"},
               level={"th": "ม.1"}, topic="มิติสัมพันธ์ของรูปเรขาคณิต")
class NetPictureM1(QuestionType):
    _NEAR = {"cube": "ทรงสี่เหลี่ยมมุมฉาก", "cuboid": "ทรงลูกบาศก์", "tri_prism": "พีระมิดฐานสามเหลี่ยม",
             "sq_pyramid": "ปริซึมสี่เหลี่ยม", "cylinder": "กรวย", "cone": "ทรงกระบอก"}

    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice(NETS)
        pool = [x.thai for x in NETS if x.thai not in (n.thai, self._NEAR[n.name])]
        rng.shuffle(pool)
        return _text_q([text("เมื่อพับรูปคลี่นี้ จะได้รูปเรขาคณิตสามมิติใด"),
                        _img(n.asset_id, "รูปคลี่ของรูปเรขาคณิตสามมิติ")],
                       n.thai, [self._NEAR[n.name]] + pool, self.topic)


@question_type("math.cross_section_m1",
               display_name={"th": "หน้าตัดและภาพที่ได้จากการมองรูปเรขาคณิตสามมิติ"},
               level=LEVEL, topic=_SPACE_TOPIC)
class CrossSectionM1(ConceptBankType):
    ITEMS = [
        Concept("ตัดทรงกระบอกด้วยระนาบที่ขนานกับฐาน รอยตัดเป็นรูปใด", "วงกลม",
                ("สี่เหลี่ยมผืนผ้า", "วงรี", "สามเหลี่ยม")),
        Concept("ตัดทรงกระบอกด้วยระนาบที่ตั้งฉากกับฐานและผ่านแกนของทรงกระบอก รอยตัดเป็นรูปใด",
                "สี่เหลี่ยมผืนผ้า", ("วงกลม", "วงรี", "สามเหลี่ยม")),
        Concept("ตัดทรงกระบอกด้วยระนาบที่เอียงและไม่ตัดผ่านฐาน รอยตัดเป็นรูปใด", "วงรี",
                ("วงกลม", "สี่เหลี่ยมผืนผ้า", "สามเหลี่ยม")),
        Concept("ตัดกรวยด้วยระนาบที่ขนานกับฐาน รอยตัดเป็นรูปใด", "วงกลม",
                ("สามเหลี่ยม", "วงรี", "สี่เหลี่ยมผืนผ้า")),
        Concept("ตัดกรวยด้วยระนาบที่ผ่านยอดและตั้งฉากกับฐาน รอยตัดเป็นรูปใด", "สามเหลี่ยมหน้าจั่ว",
                ("วงกลม", "สี่เหลี่ยมผืนผ้า", "วงรี")),
        Concept("ตัดทรงกลมด้วยระนาบ รอยตัดเป็นรูปใดเสมอ", "วงกลม",
                ("วงรี", "สี่เหลี่ยมจัตุรัส", "สามเหลี่ยม")),
        Concept("ตัดลูกบาศก์ด้วยระนาบที่ขนานกับหน้าใดหน้าหนึ่ง รอยตัดเป็นรูปใด", "สี่เหลี่ยมจัตุรัส",
                ("สามเหลี่ยม", "หกเหลี่ยม", "วงกลม")),
        Concept("ตัดลูกบาศก์ผ่านจุดยอดสามจุดที่อยู่ติดกับจุดยอดเดียวกัน รอยตัดเป็นรูปใด",
                "สามเหลี่ยมด้านเท่า", ("สี่เหลี่ยมจัตุรัส", "สามเหลี่ยมมุมฉาก", "หกเหลี่ยม")),
        Concept("ตัดพีระมิดฐานสี่เหลี่ยมจัตุรัสด้วยระนาบที่ขนานกับฐาน รอยตัดเป็นรูปใด",
                "สี่เหลี่ยมจัตุรัส", ("สามเหลี่ยม", "ห้าเหลี่ยม", "วงกลม")),
        Concept("ตัดปริซึมสามเหลี่ยมด้วยระนาบที่ขนานกับฐาน รอยตัดเป็นรูปใด", "สามเหลี่ยม",
                ("สี่เหลี่ยมผืนผ้า", "ห้าเหลี่ยม", "วงกลม")),
        Concept("มองทรงกระบอกที่ตั้งอยู่บนโต๊ะจากด้านบน จะเห็นเป็นรูปใด", "วงกลม",
                ("สี่เหลี่ยมผืนผ้า", "วงรี", "สามเหลี่ยม")),
        Concept("มองทรงกระบอกที่ตั้งอยู่บนโต๊ะจากด้านหน้า จะเห็นเป็นรูปใด", "สี่เหลี่ยมผืนผ้า",
                ("วงกลม", "สามเหลี่ยม", "วงรี")),
        Concept("มองกรวยที่ตั้งอยู่บนโต๊ะ (ฐานอยู่ล่าง) จากด้านหน้า จะเห็นเป็นรูปใด", "สามเหลี่ยม",
                ("วงกลม", "สี่เหลี่ยมผืนผ้า", "วงรี")),
        Concept("มองกรวยที่ตั้งอยู่บนโต๊ะจากด้านบน จะเห็นเป็นรูปใด", "วงกลมที่มีจุดอยู่ตรงกลาง",
                ("สามเหลี่ยม", "สี่เหลี่ยมจัตุรัส", "วงรี")),
        Concept("มองพีระมิดฐานสี่เหลี่ยมจัตุรัสจากด้านบน จะเห็นเป็นรูปใด",
                "สี่เหลี่ยมจัตุรัสที่มีเส้นทแยงมุมทั้งสองเส้น",
                ("สามเหลี่ยม", "สี่เหลี่ยมจัตุรัสเปล่า", "วงกลม")),
    ]


@question_type("math.solid_nets_m1",
               display_name={"th": "รูปคลี่ของปริซึมและพีระมิด"},
               level=LEVEL, topic=_SPACE_TOPIC)
class SolidNetsM1(WordProblem):
    _BASES = {3: "สามเหลี่ยม", 4: "สี่เหลี่ยม", 5: "ห้าเหลี่ยม", 6: "หกเหลี่ยม", 8: "แปดเหลี่ยม"}

    def expr(self, rng: Random):
        n = rng.choice(list(self._BASES))
        base = self._BASES[n]
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(n),
                            prompt=f"รูปคลี่ของปริซึมฐาน{base} มีรูปสี่เหลี่ยมผืนผ้าที่เป็นหน้าข้างกี่รูป",
                            distractors=_story.keep(n + 2, 2 * n, n - 1, 2, answer=n, lo=1))
        if kind == 1:
            return MathDraw("", str(n + 2),
                            prompt=f"รูปคลี่ของปริซึมฐาน{base} ประกอบด้วยรูปหลายเหลี่ยมทั้งหมดกี่รูป",
                            distractors=_story.keep(n, n + 1, 2 * n, 3 * n, answer=n + 2, lo=1))
        if kind == 2:
            return MathDraw("", str(n + 1),
                            prompt=f"รูปคลี่ของพีระมิดฐาน{base} ประกอบด้วยรูปหลายเหลี่ยมทั้งหมดกี่รูป",
                            distractors=_story.keep(n, n + 2, 2 * n, answer=n + 1, lo=1))
        return MathDraw("", str(3 * n),
                        prompt=f"ปริซึมฐาน{base} มีสันทั้งหมดกี่สัน",
                        # Pyramid's 2n, and faces n + 2.
                        distractors=_story.keep(2 * n, n + 2, 4 * n, answer=3 * n, lo=1))


@question_type("math.cube_stack_m1",
               display_name={"th": "ลูกบาศก์เล็กที่ประกอบเป็นทรงสี่เหลี่ยมมุมฉาก"},
               level=LEVEL, topic=_SPACE_TOPIC)
class CubeStackM1(WordProblem):
    def expr(self, rng: Random):
        a, b, c = rng.randint(2, 6), rng.randint(3, 7), rng.randint(3, 8)
        total = a * b * c
        stem = (f"นำลูกบาศก์เล็กขนาดเท่ากันมาวางเรียงเป็นทรงสี่เหลี่ยมมุมฉากขนาด {a} × {b} × {c} ลูก "
                f"แล้วทาสีด้านนอกทั้งหมด")
        kind = rng.randrange(4)
        inner = (a - 2) * (b - 2) * (c - 2)
        two = 4 * ((a - 2) + (b - 2) + (c - 2))
        one = 2 * ((a - 2) * (b - 2) + (b - 2) * (c - 2) + (a - 2) * (c - 2))
        if kind == 0:
            return MathDraw("", str(total), prompt=f"{stem} ใช้ลูกบาศก์เล็กทั้งหมดกี่ลูก",
                            distractors=_story.keep(a + b + c, 2 * (a * b + b * c + a * c),
                                                    total - inner, answer=total, lo=1))
        if kind == 1:
            return MathDraw("", "8", prompt=f"{stem} มีลูกบาศก์เล็กที่ถูกทาสี 3 ด้านกี่ลูก",
                            distractors=_story.keep(6, 12, 4, two, answer=8, lo=1))
        if kind == 2:
            return MathDraw("", str(inner), prompt=f"{stem} มีลูกบาศก์เล็กที่ไม่ถูกทาสีเลยกี่ลูก",
                            distractors=_story.keep(total - inner, (a - 1) * (b - 1) * (c - 1),
                                                    one, inner + 1, answer=inner, lo=0))
        return MathDraw("", str(two), prompt=f"{stem} มีลูกบาศก์เล็กที่ถูกทาสี 2 ด้านพอดีกี่ลูก",
                        distractors=_story.keep(one, 4 * (a + b + c), two + 8, 12,
                                                answer=two, lo=0))
