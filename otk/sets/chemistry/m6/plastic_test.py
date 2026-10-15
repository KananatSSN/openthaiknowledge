"""การทดสอบและระบุประเภทของพลาสติกและผลิตภัณฑ์ยาง

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/13

Sets moved here from: science_wave_i1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_i1 import CHEMISTRY, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_PLASTIC = "การทดสอบและระบุประเภทของพลาสติกและผลิตภัณฑ์ยาง"


PE_OR_PP = "พอลิเอทิลีน (PE) หรือพอลิโพรพิลีน (PP)"


PS, PVC, PET = "พอลิสไตรีน (PS)", "พอลิไวนิลคลอไรด์ (PVC)", "พอลิเอทิลีนเทเรฟทาเลต (PET)"


THERMOSET = "เมลามีน (เทอร์มอเซต)"


# Burning: PE and PP look and smell the same, so the test names them together.
BURNING = {
    PE_OR_PP: "ติดไฟง่าย เปลวไฟสีน้ำเงินขอบเหลือง เกือบไม่มีเขม่า มีกลิ่นคล้ายเทียนไข",
    PS: "ติดไฟง่าย เปลวไฟสีเหลือง มีเขม่าสีดำมาก",
    PVC: "ติดไฟยาก ดับเองเมื่อนำออกจากเปลวไฟ ขอบเปลวไฟสีเขียว มีกลิ่นฉุนของแก๊สไฮโดรเจนคลอไรด์",
}


# More observations, each enough on its own to name the plastic.
MORE_BURNING = {
    PE_OR_PP: ("เปลวไฟสีน้ำเงินขอบเหลือง พลาสติกหลอมหยดลงมาขณะไหม้ และมีกลิ่นคล้ายเทียนไขที่ดับแล้ว",
               "ไหม้ต่อได้เองหลังนำออกจากเปลวไฟ แทบไม่มีควันดำ และได้กลิ่นคล้ายพาราฟิน"),
    PS: ("ติดไฟง่ายและไหม้ต่อได้เอง มีควันดำเป็นเขม่าลอยเป็นสาย และมีกลิ่นหวานเฉพาะตัว",
         "เปลวไฟสีเหลืองสว่าง มีเขม่าดำเกาะปลายคีมที่จับชิ้นพลาสติกจำนวนมาก"),
    PVC: ("ไม่ไหม้ต่อเมื่อนำออกจากไฟ ควันมีกลิ่นฉุนแสบจมูก "
          "และกระดาษลิตมัสสีน้ำเงินชื้นที่จ่อในควันเปลี่ยนเป็นสีแดง",
          "เมื่อนำลวดทองแดงที่แตะพลาสติกไปลนไฟ เปลวไฟเป็นสีเขียว และชิ้นพลาสติกไม่ไหม้ต่อเอง"),
}

# Float (True) or sink in water (density 1.0 g/cm³), and in a saturated salt
# solution (about 1.2 g/cm³).
IN_WATER = {PE_OR_PP: True, PS: False, PVC: False, PET: False}


IN_BRINE = {PE_OR_PP: True, PS: True, PVC: False, PET: False}


HEATING = (
    ("เทอร์มอพลาสติก", "อ่อนตัวเมื่อได้รับความร้อน และนำมาขึ้นรูปใหม่ได้"),
    ("เทอร์มอเซต", "ไม่อ่อนตัวเมื่อได้รับความร้อน ถ้าร้อนมากจะไหม้เกรียม"),
)


# More responses to heat, keyed by the type each one shows.
MORE_HEATING = {
    "เทอร์มอพลาสติก": ("นิ่มลงจนดัดงอได้เมื่ออังกับน้ำร้อน และแข็งตัวคงรูปใหม่เมื่อเย็นลง",
                       "หลอมเป็นของเหลวหนืดเมื่อร้อน แล้วกลับแข็งตัวได้อีกเมื่อเย็นลง"),
    "เทอร์มอเซต": ("ไม่นิ่มลงเลยแม้แช่ในน้ำเดือดนาน ๆ และยังคงรูปเดิมทุกประการ",
                   "ไม่หลอมเหลวแม้ร้อนจัด แต่แตกร้าวและไหม้เป็นสีดำ"),
}

# (rubber, property, a job only it suits among these, or None). Unvulcanised
# rubber is a raw material, not a product, so it is never the answer to a job.
RUBBERS = (
    ("ยางธรรมชาติที่ยังไม่วัลคาไนซ์", "ยืดหยุ่นได้ แต่เหนียวเยิ้มเมื่อร้อนและแข็งเปราะเมื่อเย็น ไม่ทนน้ำมัน",
     None),
    ("ยางที่ผ่านการวัลคาไนซ์", "ยืดหยุ่นดี คืนรูปได้ ทนร้อนและเย็นได้ดีกว่ายางดิบ",
     "ยางรถยนต์ที่ต้องทนทั้งแดดร้อนและอากาศเย็น"),
    ("ยางนีโอพรีน", "ทนน้ำมันและสารเคมี ไม่ติดไฟง่าย",
     "ท่อส่งน้ำมันและปะเก็นในเครื่องยนต์"),
)


@question_type(
    "chem.plastic_test_foundation",
    display_name={"th": "ระบุชนิดของพลาสติกจากการเผาและการให้ความร้อน"},
    level=UPPER_SIX, subject=CHEMISTRY, topic=TOPIC_PLASTIC,
)
class PlasticTestFoundation(QuestionType):
    """Read the flame, or the response to heat."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            plastic = rng.choice(sorted(BURNING))
            seen = rng.choice((BURNING[plastic], *MORE_BURNING[plastic]))
            return _labelled(stem=f"เมื่อเผาพลาสติกชิ้นหนึ่งพบว่า{seen} พลาสติกนี้น่าจะเป็นชนิดใด",
                             # Not PET: it burns much like PS, so it would be a second right answer.
                             correct=plastic, wrongs=tuple(p for p in BURNING if p != plastic) + (THERMOSET,),
                             topic=TOPIC_PLASTIC,
                             hint="PE กับ PP เผาแล้วเหมือนกัน (เปลวน้ำเงินขอบเหลือง) PS มีเขม่ามาก PVC ติดไฟยากและขอบเปลวสีเขียว")
        kind, behaviour = rng.choice(HEATING)
        other = next(h for h in HEATING if h[0] != kind)
        behaviour = rng.choice((behaviour, *MORE_HEATING[kind]))
        return _labelled(stem=f"ให้ความร้อนแก่ชิ้นพลาสติกแล้วพบว่า{behaviour} พลาสติกนี้เป็นประเภทใด",
                         correct=kind, wrongs=(other[0], "ยางธรรมชาติ", "เส้นใยธรรมชาติ"),
                         topic=TOPIC_PLASTIC, hint="เทอร์มอพลาสติกหลอมขึ้นรูปใหม่ได้ เทอร์มอเซตไม่อ่อนตัว")


@question_type(
    "chem.plastic_test_fluency",
    display_name={"th": "ระบุพลาสติกจากการลอยและจมในน้ำและน้ำเกลือ"},
    level=UPPER_SIX, subject=CHEMISTRY, topic=TOPIC_PLASTIC,
)
class PlasticTestFluency(QuestionType):
    """Density tests: water separates PE/PP from the rest, brine separates PS."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("PE และ PP ลอยน้ำ PS จมน้ำแต่ลอยในน้ำเกลืออิ่มตัว PVC และ PET จมทั้งในน้ำและน้ำเกลืออิ่มตัว")
        words = {True: "ลอย", False: "จม"}
        plastic = rng.choice(sorted(IN_WATER))
        if rng.random() < 0.5:
            liquid, table = rng.choice((("น้ำ", IN_WATER), ("น้ำเกลืออิ่มตัว", IN_BRINE)))
            right = words[table[plastic]]
            return _labelled(stem=f"นำชิ้น{plastic}ใส่ใน{liquid} ชิ้นพลาสติกจะลอยหรือจม",
                             correct=right, wrongs=(words[not table[plastic]], "ละลายหายไป", "ลอยครึ่งหนึ่งจมครึ่งหนึ่งเสมอ"),
                             topic=TOPIC_PLASTIC, hint=hint)
        pattern = (IN_WATER[plastic], IN_BRINE[plastic])
        matches = [p for p in IN_WATER if (IN_WATER[p], IN_BRINE[p]) == pattern]
        if len(matches) > 1:
            # The two tests cannot tell these apart, so the answer names both.
            right = " หรือ ".join(sorted(matches))
            wrongs = tuple(p for p in IN_WATER if p not in matches) + (
                "ระบุไม่ได้เลย เพราะพลาสติกทุกชนิดจมในน้ำเกลืออิ่มตัว",)
        else:
            right = plastic
            wrongs = tuple(p for p in IN_WATER if p != plastic)
        return _labelled(stem=f"พลาสติกชิ้นหนึ่ง{words[pattern[0]]}ในน้ำ และ{words[pattern[1]]}ในน้ำเกลืออิ่มตัว "
                              "พลาสติกนี้น่าจะเป็นชนิดใด",
                         correct=right, wrongs=wrongs, topic=TOPIC_PLASTIC, hint=hint)


@question_type(
    "chem.plastic_test_application",
    display_name={"th": "ระบุพลาสติกจากผลการทดสอบหลายอย่างและเลือกใช้ผลิตภัณฑ์ยาง"},
    level=UPPER_SIX, subject=CHEMISTRY, topic=TOPIC_PLASTIC,
)
class PlasticTestApplication(QuestionType):
    """Combine tests to pin a plastic down; match a rubber to a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            name, prop, job = rng.choice(RUBBERS)
            others = [r for r in RUBBERS if r[0] != name]
            if job is not None and rng.random() < 0.5:
                return _labelled(stem=f"ควรเลือกยางชนิดใดทำ{job}", correct=name,
                                 wrongs=tuple(r[0] for r in others) + ("ยางที่ผสมน้ำมันจนนิ่มมาก",),
                                 topic=TOPIC_PLASTIC,
                                 hint="เลือกจากสมบัติที่งานต้องการ: ทนร้อนเย็น ยืดหยุ่น หรือทนน้ำมัน")
            return _labelled(stem=f"{name}มีสมบัติตามข้อใด", correct=prop, wrongs=tuple(r[1] for r in others)
                             + ("แข็งมากและไม่ยืดหยุ่นเลย",), topic=TOPIC_PLASTIC,
                             hint="การวัลคาไนซ์เชื่อมสายยางด้วยกำมะถัน ยางจึงทนร้อนเย็นและคืนรูปดีขึ้น")
        plastic = rng.choice((PS, PVC))
        floats = "ลอย" if IN_BRINE[plastic] else "จม"
        return _labelled(stem=f"พลาสติกชิ้นหนึ่งจมในน้ำ {floats}ในน้ำเกลืออิ่มตัว และเมื่อเผา{BURNING[plastic]} "
                              "พลาสติกนี้คือชนิดใด",
                         correct=plastic, wrongs=tuple(p for p in (PS, PVC, PET, PE_OR_PP) if p != plastic),
                         topic=TOPIC_PLASTIC,
                         hint="ใช้ผลทุกการทดสอบร่วมกัน: การลอยจมแยกตามความหนาแน่น การเผาแยกชนิดที่ความหนาแน่นใกล้กัน")
