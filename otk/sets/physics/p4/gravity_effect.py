"""แรงโน้มถ่วงของโลก

ฟิสิกส์ · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.4/1

Sets moved here from: science_wave_d15.
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
from otk.sets._support.science_wave_d15 import FOURTH

PROVENANCE = Provenance("original")


GRAVITY_TOPIC = "แรงโน้มถ่วงของโลก"


FALLS = "แรงโน้มถ่วงดึงวัตถุเข้าหาโลก วัตถุจึงตกลงสู่พื้น"


WEIGHS = "แรงโน้มถ่วงดึงวัตถุเข้าหาโลก วัตถุจึงมีน้ำหนัก"


class Sighting(NamedTuple):
    record: str
    effect: str


SIGHTINGS = (
    Sighting("โยนลูกบอลขึ้นไปตรง ๆ ลูกบอลขึ้นไปได้ระยะหนึ่งแล้วตกกลับลงมาที่พื้น", FALLS),
    Sighting("ปล่อยก้อนดินน้ำมันจากมือ ก้อนดินน้ำมันตกลงสู่พื้นทุกครั้ง ไม่ว่าจะปล่อยจากที่สูงเท่าใด", FALLS),
    Sighting("ใบไม้ที่หลุดจากกิ่งร่วงลงสู่พื้นดิน", FALLS),
    Sighting("แขวนถุงทรายไว้กับสปริง สปริงยืดออก และเมื่อเพิ่มทรายลงในถุง สปริงยืดออกมากขึ้น", WEIGHS),
    Sighting("วางกล่องบนตาชั่ง เข็มของตาชั่งเลื่อนไปจากศูนย์ เมื่อยกกล่องออก เข็มกลับที่ศูนย์", WEIGHS),
    Sighting("ถือกระเป๋าหนังสือไว้ รู้สึกว่ากระเป๋าดึงมือลงตลอดเวลา", WEIGHS),
    Sighting("ผลมะม่วงสุกหลุดจากขั้วแล้วหล่นลงพื้น", FALLS),
    Sighting("หยดน้ำฝนตกจากก้อนเมฆลงมาถึงพื้นดิน", FALLS),
    Sighting("ลูกบอลกลิ้งตกจากขอบโต๊ะลงไปที่พื้น", FALLS),
    Sighting("ปล่อยกระดาษที่ขยำเป็นก้อนจากชั้นสอง ก้อนกระดาษตกลงสู่พื้นล่าง", FALLS),
    Sighting("เด็กที่นั่งบนชิงช้าสูงสุดแล้วแกว่งกลับลงมาทุกครั้ง", FALLS),
    Sighting("แขวนตุ้มกับยางวง ยางวงยืดออก เมื่อแขวนตุ้มเพิ่ม ยางวงยืดยาวขึ้นอีก", WEIGHS),
    Sighting("ยืนบนเครื่องชั่งน้ำหนักในห้องพยาบาล เข็มหรือตัวเลขแสดงค่าน้ำหนักของตัวเรา", WEIGHS),
    Sighting("หิ้วถังน้ำเต็มถัง รู้สึกว่าถังดึงแขนลงมากกว่าตอนถังเปล่า", WEIGHS),
    Sighting("วางหนังสือหนาหลายเล่มบนไม้บรรทัดที่พาดระหว่างโต๊ะสองตัว ไม้บรรทัดโค้งลง", WEIGHS),
)


GRAVITY_TRUE = (
    "แรงโน้มถ่วงของโลกดึงวัตถุทุกชนิดเข้าหาศูนย์กลางของโลก",
    "แรงโน้มถ่วงเป็นแรงไม่สัมผัส ดึงวัตถุได้โดยไม่ต้องแตะ",
    "น้ำหนักของวัตถุคือแรงที่โลกดึงดูดวัตถุนั้น",
    "แรงโน้มถ่วงดึงทั้งวัตถุที่อยู่นิ่งและวัตถุที่กำลังเคลื่อนที่",
    "วัตถุที่ถูกโยนขึ้นตกกลับลงมาเพราะแรงโน้มถ่วงของโลก",
)


GRAVITY_ITEMS = ("ลูกบอล", "ขนนก", "ก้อนหิน", "ลูกโป่งที่มีลมธรรมดา", "แก้วน้ำ", "ดินสอ", "ผลส้ม", "รองเท้า")


NOT_GRAVITY = (
    "แรงโน้มถ่วงผลักวัตถุออกห่างจากโลก วัตถุจึงลอยขึ้น",
    "แรงโน้มถ่วงทำให้วัตถุเปลี่ยนสี",
    "แรงโน้มถ่วงกระทำเฉพาะวัตถุที่กำลังเคลื่อนที่ วัตถุที่อยู่นิ่งจึงไม่มีน้ำหนัก",
    "แรงโน้มถ่วงทำให้วัตถุมีขนาดใหญ่ขึ้น",
    "แรงโน้มถ่วงดึงเฉพาะวัตถุที่ทำจากเหล็ก",
    "แรงโน้มถ่วงต้องสัมผัสวัตถุจึงจะดึงได้",
)


GRAVITY_EVENTS = ("น้ำตกไหลจากหน้าผาลงสู่แอ่งน้ำด้านล่าง", "ลูกมะพร้าวหล่นจากต้น", "เด็กไถลลงจากกระดานลื่น",
                  "ลูกบอลที่เตะขึ้นฟ้าตกกลับลงมา", "นักกระโดดร่มลอยลงสู่พื้น", "ทรายในนาฬิกาทรายไหลลงข้างล่าง",
                  "หยดน้ำจากก๊อกหยดลงอ่าง")


OTHER_FORCE_EVENTS = ("คลิปเหล็กถูกแม่เหล็กดูดขึ้นจากโต๊ะ", "ลมพัดว่าวให้ลอยสูงขึ้น", "ลูกโป่งที่ถูกับผมดูดเศษกระดาษ",
                      "เข็มทิศชี้ไปทางทิศเหนือ", "ผลักประตูให้เปิดออก", "ขั้วเหนือของแม่เหล็กสองแท่งผลักกัน")


GRAVITY_SCENARIOS = (
    ("นักบินอวกาศที่อยู่บนดวงจันทร์กระโดดได้สูงกว่าตอนอยู่บนโลก เพราะเหตุใด",
     "แรงโน้มถ่วงของดวงจันทร์น้อยกว่าของโลก จึงดึงนักบินอวกาศกลับลงมาได้น้อยกว่า",
     ("ดวงจันทร์ไม่มีแรงโน้มถ่วงเลย",
      "นักบินอวกาศมีมวลเพิ่มขึ้นบนดวงจันทร์",
      "แรงโน้มถ่วงของดวงจันทร์มากกว่าของโลก")),
    ("น้ำในแม่น้ำไหลจากภูเขาลงสู่ทะเลเสมอ เกี่ยวข้องกับแรงโน้มถ่วงอย่างไร",
     "แรงโน้มถ่วงดึงน้ำให้ไหลจากที่สูงลงสู่ที่ต่ำ",
     ("แรงโน้มถ่วงดึงน้ำจากทะเลขึ้นไปบนภูเขา",
      "น้ำไหลเพราะไม่มีแรงใดกระทำ",
      "แรงโน้มถ่วงทำให้น้ำระเหย")),
    ("เหตุใดช่างก่อสร้างจึงใช้ลูกดิ่ง (ตุ้มน้ำหนักผูกเชือก) ตรวจว่าเสาตั้งตรง",
     "แรงโน้มถ่วงดึงตุ้มลงในแนวดิ่งตรงเข้าหาโลก เชือกจึงแสดงแนวตั้งตรงได้",
     ("ตุ้มน้ำหนักถูกดึงไปทางทิศเหนือเสมอ",
      "เชือกแข็งจึงตั้งตรงเอง",
      "ลมพัดตุ้มให้อยู่ในแนวตรง")),
    ("ลูกโป่งที่เติมแก๊สฮีเลียมลอยขึ้น แต่ลูกโป่งที่เป่าด้วยปากตกลงพื้น ข้อใดถูกต้อง",
     "แรงโน้มถ่วงดึงลูกโป่งทั้งสองลง แต่ลูกโป่งฮีเลียมเบากว่าอากาศ อากาศจึงดันให้ลอยขึ้น",
     ("ลูกโป่งฮีเลียมไม่มีแรงโน้มถ่วงกระทำ", "แรงโน้มถ่วงผลักลูกโป่งฮีเลียมขึ้น", "ลูกโป่งที่เป่าด้วยปากไม่มีน้ำหนัก")),
    ("ในสถานีอวกาศ นักบินอวกาศต้องมัดตัวไว้ขณะนอน แต่บนโลกไม่ต้อง เพราะเหตุใด",
     "บนโลกแรงโน้มถ่วงดึงร่างกายให้แนบกับที่นอน ส่วนในสถานีอวกาศทุกสิ่งลอยตัวเสมือนไร้น้ำหนัก",
     ("บนโลกไม่มีแรงโน้มถ่วง", "ในสถานีอวกาศมีแรงโน้มถ่วงมากกว่าบนโลก", "นักบินอวกาศมีมวลเป็นศูนย์")),
)


@question_type(
    "phys.gravity_effect_foundation",
    display_name={"th": "บอกทิศทางของแรงโน้มถ่วงของโลก"},
    level=FOURTH, subject=SUBJECT, topic=GRAVITY_TOPIC,
)
class GravityEffectFoundation(QuestionType):
    """Which statement about gravity's pull is true, or which way a dropped thing goes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            thing = rng.choice(GRAVITY_ITEMS)
            where = rng.choice(("บนยอดเขา", "บนดาดฟ้าตึก", "บนเรือกลางทะเล", "ที่ประเทศไทย", "ที่ขั้วโลกใต้", "ในห้องเรียน"))
            return _labelled(
                stem=f"ปล่อย{thing}จากมือ{where} {thing}จะเคลื่อนที่ไปทางใด",
                correct="ตกลงสู่พื้น เข้าหาศูนย์กลางของโลก",
                wrongs=("ลอยขึ้นสู่ท้องฟ้า", "ลอยนิ่งอยู่กับที่", f"ตกลงเฉพาะเมื่อ{thing}ทำจากเหล็ก"),
                hint="แรงโน้มถ่วงดึงวัตถุเข้าหาศูนย์กลางของโลกเสมอ ไม่ว่าจะอยู่ที่ใดบนโลก",
                topic=GRAVITY_TOPIC,
            )
        return _labelled(
            stem="ข้อใดกล่าวถึงแรงโน้มถ่วงของโลกได้ถูกต้อง",
            correct=rng.choice(GRAVITY_TRUE),
            wrongs=tuple(NOT_GRAVITY),
            hint="แรงโน้มถ่วงดึงวัตถุเข้าหาโลกเสมอ ทั้งวัตถุที่อยู่นิ่งและกำลังเคลื่อนที่",
            topic=GRAVITY_TOPIC,
        )


@question_type(
    "phys.gravity_effect_fluency",
    display_name={"th": "ระบุผลของแรงโน้มถ่วงที่มีต่อวัตถุจากหลักฐาน"},
    level=FOURTH, subject=SUBJECT, topic=GRAVITY_TOPIC,
)
class GravityEffectFluency(QuestionType):
    """An observation; the effect of gravity it shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        sighting = rng.choice(SIGHTINGS)
        # The other effect is also true of every object, so it is never offered as wrong.
        return _labelled(
            stem=f"นักเรียนสังเกตได้ว่า {sighting.record} จากหลักฐานนี้ ข้อใดระบุผลของแรงโน้มถ่วงได้ถูกต้องที่สุด",
            correct=sighting.effect,
            wrongs=tuple(NOT_GRAVITY),
            hint="ถ้าเห็นวัตถุตกลงมา แรงโน้มถ่วงทำให้ตก ถ้าเห็นวัตถุดึงสปริงหรือตาชั่ง แรงโน้มถ่วงทำให้มีน้ำหนัก",
            topic=GRAVITY_TOPIC,
        )


@question_type(
    "phys.gravity_effect_application",
    display_name={"th": "ใช้ผลของแรงโน้มถ่วงอธิบายปรากฏการณ์"},
    level=FOURTH, subject=SUBJECT, topic=GRAVITY_TOPIC,
)
class GravityEffectApplication(QuestionType):
    """Authored cases, and whether an everyday event is caused by gravity."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            yes = rng.random() < 0.6
            right_pool, wrong_pool = (GRAVITY_EVENTS, OTHER_FORCE_EVENTS) if yes else (OTHER_FORCE_EVENTS, GRAVITY_EVENTS)
            return _labelled(
                stem=("เหตุการณ์ใดเกิดจากแรงโน้มถ่วงของโลก" if yes else "เหตุการณ์ใดไม่ได้เกิดจากแรงโน้มถ่วงของโลกเป็นหลัก"),
                correct=rng.choice(right_pool), wrongs=tuple(wrong_pool),
                hint="แรงโน้มถ่วงดึงวัตถุลงสู่พื้นและทำให้มีน้ำหนัก ส่วนแม่เหล็กและลมเป็นแรงคนละชนิด",
                topic=GRAVITY_TOPIC,
            )
        return _retopic(scenario_question(
            rng, GRAVITY_SCENARIOS,
            hint="แรงโน้มถ่วงดึงวัตถุเข้าหาศูนย์กลางของดาว และดาวต่างดวงมีแรงโน้มถ่วงไม่เท่ากัน",
        ), GRAVITY_TOPIC)
