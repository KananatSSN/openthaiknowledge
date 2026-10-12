"""การใช้ไฟฟ้าอย่างประหยัดและปลอดภัย

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.3/3

Sets moved here from: science_wave_d23.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d23 import THIRD

PROVENANCE = Provenance("original")


ELECTRICITY_SAFETY_TOPIC = "การใช้ไฟฟ้าอย่างประหยัดและปลอดภัย"


SAFE_ACTS = ("เช็ดมือให้แห้งก่อนจับปลั๊กไฟ", "ดึงปลั๊กโดยจับที่หัวปลั๊ก ไม่กระชากที่สายไฟ", "ปิดไฟเมื่อออกจากห้อง",
             "บอกผู้ใหญ่เมื่อเห็นสายไฟชำรุด", "ไม่เสียบปลั๊กหลายตัวบนปลั๊กพ่วงเดียวจนร้อน", "ถอดปลั๊กเตารีดทันทีเมื่อรีดผ้าเสร็จ")


UNSAFE_ACTS = ("ใช้นิ้วแหย่รูปลั๊กไฟ", "จับสวิตช์ไฟขณะมือเปียก", "ปีนเสาไฟฟ้าเพื่อเก็บว่าว", "ใช้สายไฟที่เปลือกฉนวนแตกต่อไป",
               "เสียบปลั๊กเครื่องใช้ไฟฟ้าหลายชิ้นบนปลั๊กพ่วงเดียวจนสายร้อน", "เปิดเครื่องปรับอากาศทิ้งไว้ทั้งวันทั้งที่ไม่มีคนอยู่")


SAFETY_FACTS = (
    ("การใช้ไฟฟ้าอย่างประหยัดและปลอดภัยมีประโยชน์อย่างไร", "ลดค่าไฟฟ้าที่ต้องจ่าย และลดความเสี่ยงจากอันตราย เช่น ไฟฟ้าลัดวงจรหรือไฟฟ้าดูด",
     ("ทำให้เครื่องใช้ไฟฟ้าทุกชนิดมีอายุการใช้งานสั้นลง", "เพิ่มปริมาณไฟฟ้าที่โรงไฟฟ้าต้องผลิตให้มากขึ้น", "ไม่มีผลใด ๆ ต่อค่าใช้จ่ายหรือความปลอดภัยของผู้ใช้",
      "ทำให้ต้องซื้อเครื่องใช้ไฟฟ้าใหม่บ่อยขึ้น", "ทำให้ไฟฟ้าแรงขึ้น")),
)


SAFETY_HINT = "ประหยัดไฟช่วยเรื่องค่าใช้จ่าย ส่วนความปลอดภัยช่วยป้องกันอุบัติเหตุจากไฟฟ้า เช่น ไฟดูด ไฟลัดวงจร"


class ElectricityProblem(NamedTuple):
    case: str
    method: str


ELECTRICITY_PROBLEMS = (
    ElectricityProblem("เปิดไฟและเครื่องใช้ไฟฟ้าทิ้งไว้แม้ไม่มีคนอยู่ในห้อง",
                        "ปิดสวิตช์ไฟและถอดปลั๊กเครื่องใช้ไฟฟ้าทุกครั้งที่ไม่ใช้งาน"),
    ElectricityProblem("ใช้ปลั๊กพ่วงเสียบเครื่องใช้ไฟฟ้าหลายชิ้นจนเกินกำลังไฟที่ปลั๊กรับได้",
                        "แยกเสียบเครื่องใช้ไฟฟ้ากำลังไฟสูงไม่ให้เกินพิกัดของปลั๊กพ่วง"),
    ElectricityProblem("มือเปียกแล้วไปจับสวิตช์ไฟหรือปลั๊กไฟ",
                        "เช็ดมือให้แห้งสนิทก่อนสัมผัสสวิตช์ไฟหรือปลั๊กไฟทุกครั้ง"),
    ElectricityProblem("ใช้สายไฟที่ฉนวนชำรุดจนเห็นลวดทองแดงโดยไม่เปลี่ยนสาย",
                        "เปลี่ยนสายไฟที่ฉนวนชำรุดทันทีก่อนใช้งานต่อ"),
    ElectricityProblem("เปิดตู้เย็นค้างไว้นาน ๆ ขณะเลือกของ",
                        "คิดก่อนว่าจะหยิบอะไร แล้วเปิดตู้เย็นเท่าที่จำเป็นและปิดให้สนิท"),
    ElectricityProblem("ว่าวติดสายไฟฟ้าหน้าบ้าน",
                        "ไม่ปีนหรือดึงว่าวเอง ให้แจ้งการไฟฟ้าหรือผู้ใหญ่มาจัดการ"),
    ElectricityProblem("ดึงปลั๊กออกจากเต้ารับโดยกระชากที่สายไฟ",
                        "จับที่หัวปลั๊กแล้วดึงออกตรง ๆ เพื่อไม่ให้สายไฟชำรุด"),
    ElectricityProblem("เปิดไฟทุกดวงในห้องตอนกลางวันทั้งที่แสงแดดส่องถึง",
                        "เปิดหน้าต่างรับแสงธรรมชาติและปิดไฟดวงที่ไม่จำเป็น"),
)


ELECTRICITY_SAFETY_SCENARIOS = (
    ("นักเรียนเห็นน้องเล็กกำลังจะเอานิ้วแหย่เข้าไปในรูปลั๊กไฟที่ผนัง ควรทำอย่างไรก่อนเป็นอันดับแรก",
     "รีบห้ามและพาน้องออกจากจุดนั้นทันที แล้วอธิบายอันตรายของไฟฟ้าดูด",
     ("ปล่อยให้น้องลองเองเพื่อเรียนรู้ด้วยตัวเอง", "รอดูอยู่ห่าง ๆ โดยไม่ทำอะไร", "บอกให้น้องรอผู้ใหญ่มาก่อนโดยไม่เข้าไปช่วย")),
    ("บ้านหลังหนึ่งเปิดเครื่องปรับอากาศทิ้งไว้ทั้งวันแม้ไม่มีคนอยู่บ้าน ส่งผลอย่างไรและควรแก้ไขอย่างไร",
     "สิ้นเปลืองค่าไฟฟ้าโดยไม่จำเป็น ควรปิดเครื่องปรับอากาศทุกครั้งที่ออกจากบ้าน",
     ("ไม่มีผลใด ๆ เพราะเครื่องปรับอากาศใช้ไฟฟ้าน้อยมาก", "ควรเปิดเพิ่มอีกเครื่องเพื่อความเย็นสม่ำเสมอ", "ควรถอดปลั๊กเครื่องใช้ไฟฟ้าอื่นทั้งหมดแทนการปิดเครื่องปรับอากาศ")),
    ("นักเรียนเห็นสายไฟของพัดลมมีรอยขาดจนเห็นลวดทองแดงด้านใน แต่พัดลมยังใช้งานได้ปกติ ควรทำอย่างไร",
     "หยุดใช้งานทันทีและแจ้งผู้ใหญ่ให้เปลี่ยนสายไฟก่อนนำมาใช้ใหม่",
     ("ใช้งานต่อไปได้ตามปกติเพราะพัดลมยังทำงานอยู่", "พันเทปกาวธรรมดาทับรอยขาดแล้วใช้งานต่อ", "ใช้งานต่อแต่ระวังไม่ให้มือโดนบริเวณที่ขาด")),
)


PURPOSE = (
    ("ปิดไฟเมื่อออกจากห้อง", "ช่วยประหยัดไฟฟ้า"), ("ถอดปลั๊กเครื่องชาร์จเมื่อชาร์จเสร็จ", "ช่วยประหยัดไฟฟ้า"),
    ("ตั้งเครื่องปรับอากาศที่ 25-26 องศาเซลเซียส", "ช่วยประหยัดไฟฟ้า"), ("ใช้หลอดไฟ LED แทนหลอดไส้", "ช่วยประหยัดไฟฟ้า"),
    ("เช็ดมือให้แห้งก่อนจับปลั๊ก", "ช่วยให้ปลอดภัยจากไฟฟ้าดูด"), ("ไม่ปีนเสาไฟฟ้า", "ช่วยให้ปลอดภัยจากไฟฟ้าดูด"),
    ("ปิดฝาครอบเต้ารับเมื่อมีเด็กเล็กในบ้าน", "ช่วยให้ปลอดภัยจากไฟฟ้าดูด"), ("เปลี่ยนสายไฟที่ฉนวนชำรุด", "ช่วยให้ปลอดภัยจากไฟฟ้าดูด"),
)


@question_type(
    "phys.electricity_safety_foundation",
    display_name={"th": "บอกประโยชน์ของการใช้ไฟฟ้าอย่างประหยัดและปลอดภัย"},
    level=THIRD, subject=SUBJECT, topic=ELECTRICITY_SAFETY_TOPIC,
)
class ElectricitySafetyFoundation(QuestionType):
    """Why save and stay safe, and which acts are safe or unsafe."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            stem, right, wrongs = SAFETY_FACTS[0]
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=SAFETY_HINT, topic=ELECTRICITY_SAFETY_TOPIC)
        good = roll < 0.6
        return _labelled(stem=f"การกระทำใด{'ถูกต้อง ปลอดภัยและประหยัด' if good else 'ไม่ถูกต้อง อาจเกิดอันตรายหรือสิ้นเปลือง'}",
                         correct=rng.choice(SAFE_ACTS if good else UNSAFE_ACTS), wrongs=tuple(UNSAFE_ACTS if good else SAFE_ACTS),
                         hint=SAFETY_HINT, topic=ELECTRICITY_SAFETY_TOPIC)


@question_type(
    "phys.electricity_safety_fluency",
    display_name={"th": "เสนอแนะวิธีใช้ไฟฟ้าอย่างประหยัดและปลอดภัย"},
    level=THIRD, subject=SUBJECT, topic=ELECTRICITY_SAFETY_TOPIC,
)
class ElectricitySafetyFluency(QuestionType):
    """An unsafe or wasteful habit; the method from the same table that fixes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(ELECTRICITY_PROBLEMS))
        problem = ELECTRICITY_PROBLEMS[index]
        others = [p.method for i, p in enumerate(ELECTRICITY_PROBLEMS) if i != index]
        return _labelled(
            stem=f"{problem.case} ควรแก้ไขด้วยวิธีใดจึงจะประหยัดและปลอดภัย",
            correct=problem.method,
            wrongs=tuple(others),
            hint="แยกพิจารณาว่าเป็นปัญหาเรื่องความสิ้นเปลืองหรือเรื่องความปลอดภัย แล้วเลือกวิธีที่ตรงจุด",
            topic=ELECTRICITY_SAFETY_TOPIC,
        )


@question_type(
    "phys.electricity_safety_application",
    display_name={"th": "วิเคราะห์สถานการณ์อันตรายจากไฟฟ้าและเสนอแนวทางป้องกัน"},
    level=THIRD, subject=SUBJECT, topic=ELECTRICITY_SAFETY_TOPIC,
)
class ElectricitySafetyApplication(QuestionType):
    """Authored scenes, and whether a habit saves energy or keeps people safe."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, ELECTRICITY_SAFETY_SCENARIOS,
                                              hint="ความปลอดภัยมาก่อนเสมอ และการประหยัดไฟฟ้าเริ่มจากปิดสิ่งที่ไม่ได้ใช้งาน"), ELECTRICITY_SAFETY_TOPIC)
        act, purpose = rng.choice(PURPOSE)
        kid = rng.choice(("ต้น", "ฝน", "มะลิ", "ภูมิ", "ข้าวหอม", "ปลา", "บอส", "น้ำใส"))
        return _labelled(stem=f"{kid}{act}เป็นประจำ การกระทำนี้มีประโยชน์ข้อใดเป็นหลัก", correct=purpose,
                         wrongs=tuple(o for o in ("ช่วยประหยัดไฟฟ้า", "ช่วยให้ปลอดภัยจากไฟฟ้าดูด", "ทำให้ไฟฟ้าแรงขึ้น", "ทำให้เครื่องใช้ไฟฟ้าเสียเร็วขึ้น")
                                      if o != purpose)[:3],
                         hint=SAFETY_HINT, topic=ELECTRICITY_SAFETY_TOPIC)
