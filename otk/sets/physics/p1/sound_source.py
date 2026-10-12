"""การเกิดเสียงและทิศทางการเคลื่อนที่ของเสียง

ฟิสิกส์ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.1/1

Sets moved here from: science_wave_d22.
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
from otk.sets._support.science_wave_d22 import KIDS, _facts

PROVENANCE = Provenance("original")


FIRST = {"th": "ป.1"}


SOUND_TOPIC = "การเกิดเสียงและทิศทางการเคลื่อนที่ของเสียง"


SIDES = ("ด้านหน้า", "ด้านหลัง", "ด้านซ้าย", "ด้านขวา")


class SoundSource(NamedTuple):
    action: str
    seen: str
    part: str


SOUND_SOURCES = (
    SoundSource("ดีดสายยางยืดที่ขึงตึง", "สายสั่นไปมาอย่างรวดเร็ว", "สายยาง"),
    SoundSource("ดีดปลายไม้บรรทัดที่ยื่นออกจากขอบโต๊ะ", "ปลายไม้บรรทัดสั่นขึ้นลง", "ไม้บรรทัด"),
    SoundSource("ตีหน้ากลองที่มีเมล็ดข้าวสารวางอยู่", "เมล็ดข้าวสารกระเด้งขึ้นลง แสดงว่าหน้ากลองสั่น", "หน้ากลอง"),
    SoundSource("ดีดส้อมเสียงแล้วแตะปลายลงบนผิวน้ำ", "ผิวน้ำกระเพื่อมเป็นระลอก แสดงว่าส้อมเสียงสั่น", "ส้อมเสียง"),
    SoundSource("เคาะกระดิ่งแล้วแตะด้วยปลายนิ้ว", "ปลายนิ้วรู้สึกว่ากระดิ่งสั่นเบา ๆ", "กระดิ่ง"),
    SoundSource("ดีดสายกีตาร์", "สายกีตาร์สั่นจนมองเห็นเป็นภาพเบลอ", "สายกีตาร์"),
    SoundSource("เปิดเพลงดังจากลำโพงที่มีเศษกระดาษวางบนแผ่นลำโพง", "เศษกระดาษเต้นอยู่บนแผ่นลำโพง", "แผ่นลำโพง"),
    SoundSource("ตีระนาดแล้วแตะลูกระนาดเบา ๆ", "ลูกระนาดสั่นจนรู้สึกได้ที่ปลายนิ้ว", "ลูกระนาด"),
)


SOUNDING = ("กลองที่กำลังถูกตี", "กระดิ่งที่กำลังถูกเคาะ", "สายกีตาร์ที่กำลังถูกดีด", "นกหวีดที่กำลังถูกเป่า", "ส้อมเสียงที่เพิ่งถูกเคาะ",
            "ระฆังที่กำลังถูกตี", "ลำโพงที่กำลังเปิดเพลง", "ขลุ่ยที่กำลังถูกเป่า")


SILENT = ("กลองที่วางนิ่งอยู่บนโต๊ะ", "สายกีตาร์ที่ไม่มีใครแตะ", "ระฆังที่แขวนนิ่งอยู่", "ลำโพงที่ปิดเครื่องอยู่", "ขลุ่ยที่วางอยู่ในกล่อง",
          "ส้อมเสียงที่ถูกกำไว้แน่น")


SOUND_FACTS = (
    ("เสียงเกิดจากสาเหตุใด", "การสั่นของวัตถุ",
     ("แสงจากแหล่งกำเนิดแสง", "การเคลื่อนที่ของอากาศโดยไม่มีวัตถุใดสั่น", "ความร้อนที่เพิ่มขึ้นของวัตถุ", "สีของวัตถุ", "ขนาดของวัตถุเพียงอย่างเดียว")),
    ("เสียงเคลื่อนที่ออกจากแหล่งกำเนิดเสียงไปทางใด", "ทุกทิศทางรอบแหล่งกำเนิดเสียง",
     ("ไปทางด้านหน้าของแหล่งกำเนิดเท่านั้น", "ขึ้นข้างบนแล้วสะท้อนกลับลงมา", "ลงพื้นเท่านั้น", "ไปหาคนที่อยู่ใกล้ที่สุดเท่านั้น", "ไม่เคลื่อนที่ไปไหน")),
    ("ถ้าต้องการให้เสียงกลองหยุดทันที ควรทำอย่างไร", "ใช้มือแตะหน้ากลองให้หยุดสั่น",
     ("ตีกลองให้แรงขึ้นอีกครั้งหนึ่ง", "ส่องไฟไปที่กลอง", "เดินออกห่างจากกลองหนึ่งก้าว", "ทาสีกลองใหม่", "ยกกลองขึ้นสูงเหนือศีรษะ")),
    ("สิ่งที่ทำให้เกิดเสียงเรียกว่าอะไร", "แหล่งกำเนิดเสียง",
     ("แหล่งกำเนิดแสง", "ตัวรับเสียง", "ตัวกลาง", "ตัวนำไฟฟ้า", "ฉนวน")),
)


SOUND_HINT = "เสียงเกิดจากการสั่นของแหล่งกำเนิดเสียง และเคลื่อนที่ออกไปรอบตัวทุกทิศทาง ไม่ใช่ทิศทางเดียว"


SOUND_WRONG_TEMPLATES = (
    "เสียงเกิดจากการสั่นของ{part} แต่ส่งไปถึงผู้ฟังได้โดยไม่ต้องอาศัยตัวกลางใด",
    "เสียงเกิดจากอากาศที่พัดผ่าน{part} โดย{part}ไม่ได้สั่น",
    "เสียงเกิดจากการสั่นของหูผู้ฟังเอง ไม่เกี่ยวกับสิ่งที่นักเรียนเห็นว่ากำลังสั่นอยู่",
    "เสียงเกิดจากแสงที่ส่องไปที่{part} แล้วกระจายออกไปรอบทิศพร้อมกับแสง",
    "เสียงเกิดจากการสั่นของ{part} แต่ได้ยินเฉพาะคนที่ยืนอยู่ตรงหน้าของสิ่งนั้น",
)


SOUND_SCENARIOS = (
    ("เหตุใดผู้ที่ยืนล้อมรอบระฆังวัดจึงได้ยินเสียงระฆังพร้อมกัน แม้จะยืนอยู่คนละด้าน",
     "เพราะเสียงเคลื่อนที่ออกจากแหล่งกำเนิดไปทุกทิศทางรอบตัว ไม่ใช่ทิศทางเดียว",
     ("เพราะเสียงเคลื่อนที่ไปทางผู้ที่อยู่ใกล้ที่สุดก่อน แล้วจึงส่งต่อไปยังคนอื่น", "เพราะแต่ละคนได้ยินเสียงจากระฆังคนละใบที่บังเอิญตีพร้อมกันพอดี", "เพราะเสียงลอดผ่านพื้นดินไปก่อน แล้วจึงขึ้นมาถึงหูของแต่ละคน")),
    ("นักเรียนแตะสายกีตาร์ที่กำลังดังอยู่ด้วยมือจนเสียงหายไปทันที เหตุใดจึงเป็นเช่นนั้น",
     "การแตะทำให้สายหยุดสั่น เมื่อไม่มีการสั่นจึงไม่มีเสียง",
     ("การแตะทำให้พลังงานเสียงเปลี่ยนเป็นแสงแทน จึงไม่ได้ยิน", "มือดูดเสียงที่เคลื่อนที่มาแล้วไว้ทั้งหมด", "สายกีตาร์ยังสั่นอยู่ แต่ความร้อนจากมือทำให้เสียงเงียบลง")),
    ("เหตุใดเราจึงไม่ได้ยินเสียงจากลำโพงที่ไม่มีไฟฟ้าเข้า แม้ตัวลำโพงยังอยู่ครบ",
     "ไม่มีพลังงานไฟฟ้าทำให้แผ่นลำโพงสั่น จึงไม่เกิดเสียง",
     ("ลำโพงที่ไม่มีไฟฟ้าจะสั่นเร็วขึ้นแต่เบาลงจนหูไม่ได้ยิน", "เสียงยังเกิดอยู่แต่เคลื่อนที่ไปทิศทางเดียว", "ลำโพงต้องการแสงสว่างจึงจะสั่นได้ ในห้องมืดจึงไม่มีเสียง")),
)


RINGERS = ("ครูที่ตีกลอง", "ภารโรงที่ตีระฆัง", "เพื่อนที่เป่านกหวีด", "ครูที่เคาะกระดิ่ง", "เพื่อนที่ดีดกีตาร์")


@question_type(
    "phys.sound_source_foundation",
    display_name={"th": "บอกสาเหตุการเกิดเสียง"},
    level=FIRST, subject=SUBJECT, topic=SOUND_TOPIC,
)
class SoundSourceFoundation(QuestionType):
    """What makes a sound, and which things are sounding right now."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            return _labelled(stem="สิ่งใดกำลังทำให้เกิดเสียง", correct=rng.choice(SOUNDING), wrongs=tuple(SILENT),
                             hint="สิ่งที่กำลังสั่นเท่านั้นจึงทำให้เกิดเสียง", topic=SOUND_TOPIC)
        return _facts(rng, SOUND_FACTS, hint=SOUND_HINT, topic=SOUND_TOPIC)


@question_type(
    "phys.sound_source_fluency",
    display_name={"th": "บรรยายการเกิดเสียงและทิศทางการเคลื่อนที่ของเสียงจากหลักฐานเชิงประจักษ์"},
    level=FIRST, subject=SUBJECT, topic=SOUND_TOPIC,
)
class SoundSourceFluency(QuestionType):
    """A vibrating source seen and heard equally from every side."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        source = rng.choice(SOUND_SOURCES)
        sides = rng.sample(SIDES, rng.randint(3, 4))
        return _labelled(
            stem=(f"นักเรียน{source.action} สังเกตเห็น{source.seen} และได้ยินเสียงพร้อมกันทั้งจาก{' '.join(sides)} "
                  "จากหลักฐานนี้ ข้อใดบรรยายการเกิดเสียงและทิศทางการเคลื่อนที่ของเสียงได้ถูกต้อง"),
            correct=f"เสียงเกิดจากการสั่นของ{source.part} และเคลื่อนที่ออกจากแหล่งกำเนิดเสียงไปทุกทิศทางรอบตัว",
            wrongs=tuple(t.format(part=source.part) for t in rng.sample(SOUND_WRONG_TEMPLATES, 3)),
            hint=SOUND_HINT,
            topic=SOUND_TOPIC,
        )


@question_type(
    "phys.sound_source_application",
    display_name={"th": "ใช้ความรู้เรื่องการเกิดเสียงอธิบายสถานการณ์"},
    level=FIRST, subject=SUBJECT, topic=SOUND_TOPIC,
)
class SoundSourceApplication(QuestionType):
    """Authored cases, and children standing round a sound on every side."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, SOUND_SCENARIOS, hint=SOUND_HINT), SOUND_TOPIC)
        count = rng.randint(3, 4)
        kids = rng.sample(KIDS, count)
        sides = rng.sample(SIDES, count)
        who = rng.choice(RINGERS)
        where = " ".join(f"{k}ยืนอยู่{s}" for k, s in zip(kids, sides))
        one, two = rng.sample(kids, 2)
        return _labelled(stem=f"เด็ก ๆ ยืนล้อมรอบ{who} {where} ใครได้ยินเสียงบ้าง",
                         correct="ได้ยินทุกคน เพราะเสียงเคลื่อนที่ออกไปทุกทิศทาง",
                         wrongs=(f"ได้ยินเฉพาะ{one} เพราะเสียงเคลื่อนที่ไปทางเดียว", "ไม่มีใครได้ยิน เพราะเสียงลอยขึ้นข้างบน",
                                 f"ได้ยินเฉพาะ{two} เพราะยืนอยู่ใกล้ที่สุด"),
                         hint=SOUND_HINT, topic=SOUND_TOPIC)
