"""สัญญาอนุญาตและการเผยแพร่ผลงาน

วิทยาการคำนวณ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.2 ม.2/4

Sets moved here from: technology_t1s7.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s6 import _situation
from otk.sets._support.technology_t1s7 import M2

PROVENANCE = Provenance("original")


LICENCE_TOPIC = "สัญญาอนุญาตและการเผยแพร่ผลงาน"


BY, NC, ND, SA = "BY (แสดงที่มา)", "NC (ไม่ใช้เพื่อการค้า)", "ND (ไม่ดัดแปลง)", "SA (อนุญาตแบบเดียวกัน)"


ELEMENTS = (BY, NC, ND, SA)


#: (what the creator wants, the element that says it).
WISHES = (
    ("ต้องการให้ผู้นำไปใช้ระบุชื่อผู้สร้างผลงาน", BY),
    ("ต้องการให้ทุกคนที่ใช้ผลงานให้เครดิตแก่เจ้าของ", BY),
    ("ไม่ต้องการให้ผู้อื่นนำผลงานไปขายหรือหารายได้", NC),
    ("อนุญาตให้ใช้ได้เฉพาะงานที่ไม่แสวงหากำไร", NC),
    ("ไม่ต้องการให้ผู้อื่นตัดต่อหรือแก้ไขผลงาน", ND),
    ("อนุญาตให้เผยแพร่ต่อได้เฉพาะผลงานต้นฉบับที่ไม่ถูกเปลี่ยนแปลง", ND),
    ("ต้องการให้งานที่ดัดแปลงจากผลงานของเราเผยแพร่ด้วยเงื่อนไขเดียวกัน", SA),
    ("ต้องการให้ผู้ที่นำไปดัดแปลงแบ่งปันงานใหม่ด้วยสัญญาอนุญาตแบบเดียวกับต้นฉบับ", SA),
)


LICENCES = {
    "CC BY": set(), "CC BY-SA": {"SA"}, "CC BY-NC": {"NC"}, "CC BY-ND": {"ND"},
    "CC BY-NC-SA": {"NC", "SA"}, "CC BY-NC-ND": {"NC", "ND"},
}


#: (use, gives credit, is commercial, adapts and shares, shares under the same licence).
USES = (
    ("นำภาพไปใช้ในรายงานของโรงเรียน พร้อมระบุชื่อเจ้าของ", True, False, False, False),
    ("นำภาพไปประกอบโปสเตอร์กิจกรรมฟรีของโรงเรียน พร้อมระบุชื่อเจ้าของ", True, False, False, False),
    ("นำภาพไปใช้ในรายงานของโรงเรียน โดยไม่ระบุชื่อเจ้าของ", False, False, False, False),
    ("พิมพ์ภาพลงเสื้อเพื่อขาย พร้อมระบุชื่อเจ้าของ", True, True, False, False),
    ("ตัดต่อภาพแล้วเผยแพร่ในบล็อกส่วนตัวที่ไม่มีโฆษณา พร้อมระบุชื่อเจ้าของ "
     "และใช้สัญญาอนุญาตแบบเดียวกับต้นฉบับ", True, False, True, True),
    ("ตัดต่อภาพแล้วเผยแพร่ในบล็อกส่วนตัวที่ไม่มีโฆษณา พร้อมระบุชื่อเจ้าของ "
     "แต่ห้ามผู้อื่นนำงานใหม่ไปใช้ต่อทุกกรณี", True, False, True, False),
)


ALLOWED = "ทำได้ เพราะการใช้นี้ตรงตามทุกเงื่อนไขของสัญญาอนุญาต"


REASONS = {
    "BY": "ทำไม่ได้ เพราะไม่ได้ระบุชื่อเจ้าของผลงาน",
    "NC": "ทำไม่ได้ เพราะสัญญาอนุญาตห้ามใช้เพื่อการค้า",
    "ND": "ทำไม่ได้ เพราะสัญญาอนุญาตห้ามดัดแปลง",
    "SA": "ทำไม่ได้ เพราะต้องเผยแพร่งานดัดแปลงด้วยสัญญาอนุญาตแบบเดียวกัน",
}


def licence_failures(licence: str, use) -> list[str]:
    _, credit, commercial, adapts, same = use
    terms = LICENCES[licence]
    found = []
    if not credit:
        found.append("BY")
    if commercial and "NC" in terms:
        found.append("NC")
    if adapts and "ND" in terms:
        found.append("ND")
    if adapts and "SA" in terms and not same:
        found.append("SA")
    return found


#: Only pairs a licence breaks for one reason at most, so exactly one choice is right.
LICENCE_CASES = tuple((licence, use) for licence in LICENCES for use in USES
                      if len(licence_failures(licence, use)) <= 1)


PUBLISHING = (
    ("ต้องการเผยแพร่ภาพวาดของตนให้ผู้อื่นใช้ในงานที่ไม่ใช่การค้าได้ โดยต้องให้เครดิต",
     "เลือกสัญญาอนุญาต CC BY-NC แล้วระบุไว้คู่กับผลงาน",
     ("เลือก CC BY เพราะเงื่อนไขนี้ห้ามการค้าอยู่แล้ว",
      "เลือก CC BY-ND เพราะเงื่อนไขนี้ห้ามการค้าอย่างเดียว",
      "ไม่ต้องระบุอะไร เพราะทุกคนรู้อยู่แล้วว่าเป็นของเรา",
      "ลบชื่อของตนออกจากภาพ เพื่อให้คนนำไปใช้ได้ง่ายขึ้น",
      "เลือก CC BY-SA เพราะเงื่อนไขนี้ห้ามการค้าและให้เครดิต")),
    ("ทำคลิปรีวิวหนังสือแล้วจะโพสต์ลงสื่อสังคม",
     "ใช้ภาพและเพลงที่ได้รับอนุญาต ระบุที่มา และไม่เปิดเผยข้อมูลส่วนตัวของผู้อื่นในคลิป",
     ("ใช้เพลงดังเป็นเพลงประกอบได้ทุกเพลง เพราะคลิปรีวิวมีความยาวไม่เกินหนึ่งนาที",
      "ถ่ายหน้าเพื่อนที่ช่วยถือหนังสือลงคลิปได้เลย เพราะเพื่อนอยู่ในเหตุการณ์ด้วย",
      "คัดลอกคลิปรีวิวของผู้อื่นมาโพสต์ในชื่อของตน ถ้าเป็นการรีวิวหนังสือเล่มเดียวกัน",
      "ใส่ที่อยู่บ้านและเบอร์โทรศัพท์ของตนไว้ท้ายคลิป เพื่อให้ผู้ชมติดต่อยืมหนังสือได้",
      "ใช้ภาพปกหนังสือทุกหน้าในคลิปได้ เพราะเป็นการรีวิวหนังสือ จึงไม่ต้องขออนุญาตใดเลย")),
    ("เพื่อนขอนำภาพถ่ายของเราไปใช้ในโปสเตอร์ขายขนม",
     "ตกลงเงื่อนไขกับเพื่อนก่อน เพราะเป็นการใช้เพื่อการค้า และขอให้ระบุชื่อเรา",
     ("ยอมให้ใช้ได้เลยโดยไม่ต้องตกลงเงื่อนไขใด เพราะเพื่อนเป็นคนรู้จักกัน",
      "ให้เพื่อนอ้างว่าเป็นผู้ถ่ายภาพเอง เพื่อให้โปสเตอร์ดูเป็นผลงานของร้าน",
      "ห้ามเพื่อนใช้ แต่นำภาพเดียวกันไปขายให้ร้านขนมร้านอื่นแทนในราคาสูงกว่า",
      "ส่งไฟล์ภาพให้เพื่อนทุกคนในห้อง เพื่อให้ทุกคนนำไปใช้ขายสินค้าได้ด้วย",
      "ยอมให้ใช้ได้เลย เพราะภาพถ่ายที่โพสต์แล้วไม่มีลิขสิทธิ์คุ้มครองอีกต่อไป")),
    ("พบว่ามีคนนำผลงานที่เราเผยแพร่แบบ CC BY ไปใช้โดยไม่ระบุชื่อเรา",
     "แจ้งผู้ใช้ให้ระบุที่มาตามเงื่อนไข หรือรายงานต่อแพลตฟอร์ม",
     ("ปล่อยไว้ เพราะสัญญาอนุญาต CC BY ไม่ต้องระบุที่มา",
      "นำผลงานของเขามาใช้โดยไม่ระบุชื่อคืน ให้เท่ากัน",
      "โพสต์ข้อมูลส่วนตัวของผู้ใช้คนนั้น เพื่อประจาน",
      "ลบผลงานของตนออกจากอินเทอร์เน็ตทั้งหมดทันที",
      "เปลี่ยนสัญญาอนุญาตเป็น CC0 เพื่อไม่ต้องมีใครระบุที่มา")),
    ("จะโพสต์รูปงานกลุ่มที่มีหน้าเพื่อนหลายคน",
     "ขออนุญาตเพื่อนทุกคนในรูปก่อนโพสต์",
     ("โพสต์ได้เลย เพราะเป็นงานของกลุ่ม",
      "โพสต์ก่อน แล้วค่อยถามเพื่อนภายหลัง",
      "ขออนุญาตเฉพาะเพื่อนสนิทในกลุ่มก็พอ",
      "ตัดต่อหน้าเพื่อนที่ไม่อนุญาตให้ตลก",
      "โพสต์ได้ถ้าเบลอหน้าเพื่อนบางคน")),
    ("ต้องการแสดงความเป็นเจ้าของภาพวาดดิจิทัลก่อนเผยแพร่",
     "ใส่ชื่อผู้สร้างและปีที่สร้างบนผลงาน พร้อมระบุสัญญาอนุญาตที่เลือก",
     ("ไม่ต้องใส่อะไรเลย เพราะลิขสิทธิ์ไม่มีผลกับผลงานบนอินเทอร์เน็ต",
      "ใส่ชื่อเพื่อนแทนชื่อตนเอง เพื่อให้เพื่อนช่วยดูแลสิทธิ์ในผลงาน",
      "บอกว่าใครจะนำไปใช้อย่างไรก็ได้ แล้วค่อยประกาศห้ามภายหลัง",
      "ส่งภาพให้คนที่มีผู้ติดตามมากโพสต์แทน เพื่อให้คนรู้จักผลงาน",
      "ใส่รหัสผ่านบัญชีของตนไว้บนภาพ เพื่อยืนยันว่าตนเป็นเจ้าของภาพจริง")),
)


@question_type(
    "comp.work_licence_foundation",
    display_name={"th": "เลือกเงื่อนไขของสัญญาอนุญาตครีเอทีฟคอมมอนส์"},
    level=M2, subject=SUBJECT, topic=LICENCE_TOPIC,
)
class WorkLicenceFoundation(QuestionType):
    def build(self, rng: Random, **params):
        hint = ("BY ให้ระบุชื่อเจ้าของ NC ห้ามใช้เพื่อการค้า ND ห้ามดัดแปลง "
                "SA ให้งานดัดแปลงใช้สัญญาอนุญาตแบบเดียวกัน")
        if rng.random() < 0.5:
            wish, element = rng.choice(WISHES)
            return _labelled(
                stem=f"เจ้าของผลงาน{wish} ควรเลือกเงื่อนไขใดของสัญญาอนุญาตครีเอทีฟคอมมอนส์",
                correct=element, wrongs=tuple(e for e in ELEMENTS if e != element),
                hint=hint, topic=LICENCE_TOPIC,
            )
        element = rng.choice(ELEMENTS)
        wish = rng.choice([w for w, e in WISHES if e == element])
        others = [w for w, e in WISHES if e != element]
        return _labelled(
            stem=f"เงื่อนไข {element} ในสัญญาอนุญาตครีเอทีฟคอมมอนส์ หมายความว่าอย่างไร",
            correct=f"เจ้าของผลงาน{wish}",
            wrongs=tuple(f"เจ้าของผลงาน{w}" for w in rng.sample(others, 3)),
            hint=hint, topic=LICENCE_TOPIC,
        )


@question_type(
    "comp.work_licence_fluency",
    display_name={"th": "พิจารณาการใช้ผลงานตามสัญญาอนุญาต"},
    level=M2, subject=SUBJECT, topic=LICENCE_TOPIC,
)
class WorkLicenceFluency(QuestionType):
    def build(self, rng: Random, **params):
        licence, use = rng.choice(LICENCE_CASES)
        failures = licence_failures(licence, use)
        correct = REASONS[failures[0]] if failures else ALLOWED
        pool = [ALLOWED, *REASONS.values()]
        return _labelled(
            stem=f"ภาพหนึ่งเผยแพร่ด้วยสัญญาอนุญาต {licence} ถ้าต้องการ{use[0]} ทำได้หรือไม่",
            correct=correct, wrongs=tuple([c for c in pool if c != correct]),
            hint=("ทุกสัญญาอนุญาตในข้อนี้มี BY จึงต้องระบุชื่อเจ้าของเสมอ แล้วตรวจทีละเงื่อนไข "
                  "NC ห้ามการค้า ND ห้ามดัดแปลง SA ให้งานดัดแปลงใช้สัญญาอนุญาตเดิม"),
            topic=LICENCE_TOPIC,
        )


@question_type(
    "comp.work_licence_application",
    display_name={"th": "เผยแพร่ผลงานอย่างรับผิดชอบและแสดงสิทธิในผลงาน"},
    level=M2, subject=SUBJECT, topic=LICENCE_TOPIC,
)
class WorkLicenceApplication(QuestionType):
    def build(self, rng: Random, **params):
        return _situation(rng, PUBLISHING, topic=LICENCE_TOPIC,
                          hint="แสดงความเป็นเจ้าของและเงื่อนไขให้ชัด เคารพผลงานและข้อมูลส่วนตัวของผู้อื่น")
