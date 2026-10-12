"""ประโยชน์ของสารกัมมันตรังสีและการป้องกันอันตรายจากกัมมันตภาพรังสี

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/25

Sets moved here from: science_wave_e9.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e9 import (
    ALPHA,
    BETA,
    GAMMA,
    ISOTOPES,
    RAYS,
    SUBJECT,
    UPPER_FIVE,
    _labelled,
    _show,
)

PROVENANCE = Provenance("original")


TOPIC_RADIO_USE = "ประโยชน์ของสารกัมมันตรังสีและการป้องกันอันตรายจากกัมมันตภาพรังสี"


MEDICINE, FARMING, INDUSTRY, DATING, ENERGY = (
    "การแพทย์", "การเกษตรและอาหาร", "อุตสาหกรรม", "โบราณคดีและธรณีวิทยา", "การผลิตพลังงาน")


FIELDS = (MEDICINE, FARMING, INDUSTRY, DATING, ENERGY)


RADIO_USES = (
    ("ใช้ไอโอดีน-131 ตรวจและรักษาโรคต่อมไทรอยด์", MEDICINE),
    ("ใช้โคบอลต์-60 ฉายรังสีรักษาโรคมะเร็ง", MEDICINE),
    ("ใช้เทคนีเชียม-99m ถ่ายภาพการทำงานของอวัยวะในร่างกาย", MEDICINE),
    ("ใช้รังสีแกมมาฆ่าเชื้อในเครื่องมือแพทย์ที่ใช้ครั้งเดียวทิ้ง", MEDICINE),
    ("ฉายรังสีแกมมาให้ผลไม้เพื่อกำจัดแมลงและยืดอายุการเก็บรักษา", FARMING),
    ("ใช้ฟอสฟอรัส-32 ศึกษาการดูดซึมปุ๋ยของพืช", FARMING),
    ("ฉายรังสีเมล็ดพันธุ์เพื่อปรับปรุงพันธุ์พืชให้ได้พันธุ์ใหม่", FARMING),
    ("ใช้รังสีตรวจหารอยร้าวในแนวเชื่อมของท่อส่งแก๊ส", INDUSTRY),
    ("ใช้รังสีบีตาวัดและควบคุมความหนาของแผ่นกระดาษในโรงงาน", INDUSTRY),
    ("ใช้อะเมริเซียม-241 ในเครื่องตรวจจับควัน", INDUSTRY),
    ("ใช้คาร์บอน-14 หาอายุของซากสิ่งมีชีวิตโบราณ", DATING),
    ("ใช้ยูเรเนียม-238 หาอายุของหินที่มีอายุหลายล้านปี", DATING),
    ("ใช้ยูเรเนียม-235 เป็นเชื้อเพลิงในโรงไฟฟ้านิวเคลียร์", ENERGY),
    ("ใช้พลูโทเนียม-238 เป็นแหล่งพลังงานไฟฟ้าของยานสำรวจอวกาศ", ENERGY),
)


TIME, DISTANCE, SHIELD, MONITOR = (
    "ลดเวลาที่สัมผัสรังสี", "เพิ่มระยะห่างจากแหล่งกำเนิดรังสี",
    "ใช้วัสดุกำบังรังสี", "ตรวจวัดและแสดงสัญลักษณ์เตือน")


PRINCIPLES = (TIME, DISTANCE, SHIELD, MONITOR)


PROTECTIONS = (
    ("ทำงานใกล้แหล่งกำเนิดรังสีให้เสร็จเร็วที่สุด แล้วออกจากบริเวณนั้นทันที", TIME),
    ("ผลัดเปลี่ยนเจ้าหน้าที่ที่ต้องทำงานในห้องที่มีรังสี", TIME),
    ("ใช้คีมด้ามยาวหยิบจับสารกัมมันตรังสีแทนการใช้มือ", DISTANCE),
    ("ยืนให้ห่างจากเครื่องฉายรังสีขณะเครื่องทำงาน", DISTANCE),
    ("ควบคุมหุ่นยนต์จากระยะไกลให้เคลื่อนย้ายสารกัมมันตรังสี", DISTANCE),
    ("เก็บสารกัมมันตรังสีไว้ในภาชนะตะกั่วหนา", SHIELD),
    ("สร้างห้องฉายรังสีด้วยผนังคอนกรีตหนา", SHIELD),
    ("ติดเครื่องวัดปริมาณรังสีประจำตัวขณะปฏิบัติงาน", MONITOR),
    ("ติดสัญลักษณ์เตือนอันตรายจากรังสีบริเวณที่เก็บสารกัมมันตรังสี", MONITOR),
)


@question_type(
    "chem.radioisotope_use_foundation",
    display_name={"th": "สารกัมมันตรังสีใช้ประโยชน์ในด้านใด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RADIO_USE,
)
class RadioisotopeUseFoundation(QuestionType):
    """Sort one named use, or one protective step, into its kind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            use, field = rng.choice(RADIO_USES)
            return _labelled(
                stem=f"\"{use}\" เป็นการใช้ประโยชน์จากสารกัมมันตรังสีด้านใด",
                correct=field, wrongs=tuple([f for f in FIELDS if f != field]),
                topic=TOPIC_RADIO_USE,
                hint="ดูว่าใครใช้และใช้ทำอะไร: รักษาคน ปลูกพืชหรือถนอมอาหาร ตรวจสอบในโรงงาน หาอายุ หรือผลิตไฟฟ้า",
            )
        step, principle = rng.choice(PROTECTIONS)
        return _labelled(
            stem=f"\"{step}\" เป็นการป้องกันอันตรายจากรังสีโดยหลักการใด",
            correct=principle, wrongs=tuple(p for p in PRINCIPLES if p != principle),
            topic=TOPIC_RADIO_USE,
            hint="การป้องกันอันตรายจากรังสีใช้หลัก: อยู่ใกล้ให้สั้นที่สุด อยู่ให้ห่างที่สุด มีสิ่งกำบัง และตรวจวัดเสมอ",
        )


@question_type(
    "chem.radioisotope_use_fluency",
    display_name={"th": "ยกตัวอย่างประโยชน์ของสารกัมมันตรังสีและการป้องกันอันตราย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RADIO_USE,
)
class RadioisotopeUseFluency(QuestionType):
    """The indicator's นำเสนอตัวอย่าง: pick the example that fits."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            field = rng.choice(FIELDS)
            mine = [u for u, f in RADIO_USES if f == field]
            others = [u for u, f in RADIO_USES if f != field]
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างการใช้ประโยชน์จากสารกัมมันตรังสีด้าน{field}",
                correct=rng.choice(mine), wrongs=tuple(others),
                topic=TOPIC_RADIO_USE,
                hint="ดูว่าผู้ใช้ในแต่ละข้อเป็นแพทย์ เกษตรกร โรงงาน นักโบราณคดี หรือโรงไฟฟ้า",
            )
        principle = rng.choice(PRINCIPLES)
        mine = [s for s, p in PROTECTIONS if p == principle]
        others = [s for s, p in PROTECTIONS if p != principle]
        return _labelled(
            stem=f"ข้อใดเป็นการป้องกันอันตรายจากรังสีโดยหลักการ \"{principle}\"",
            correct=rng.choice(mine), wrongs=tuple(others),
            topic=TOPIC_RADIO_USE,
            hint="แต่ละข้อป้องกันรังสีคนละแบบ: ลดเวลา เพิ่มระยะห่าง มีสิ่งกำบัง หรือตรวจวัดและเตือน",
        )


@question_type(
    "chem.radioisotope_use_application",
    display_name={"th": "เลือกไอโซโทปและวิธีป้องกันรังสีให้เหมาะกับสถานการณ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RADIO_USE,
)
class RadioisotopeUseApplication(QuestionType):
    """Reason from the ray and the half-life: why a job uses the isotope it does,
    and which protection a given ray needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.3:
            # Imaging inside the body: gamma escapes, and a short half-life fades fast.
            best = next(i for i in ISOTOPES if i.name == "เทคนีเชียม-99m")
            # Clearly unsuitable only: an alpha or pure-beta source, or one that
            # lingers for years. Iodine-131 and gold-198 also give gamma and have
            # been used for scans, so they are not offered as wrong.
            wrong = [i for i in ISOTOPES
                     if i.name not in ("เทคนีเชียม-99m", "ไอโอดีน-131", "ทอง-198")
                     and (i.ray != GAMMA or i.unit == "ปี")]
            picks = rng.sample(wrong, 3)
            return _labelled(
                stem=("แพทย์ต้องการฉีดสารกัมมันตรังสีเข้าร่างกายผู้ป่วย เพื่อถ่ายภาพอวัยวะจากเครื่องตรวจภายนอกร่างกาย "
                      "ควรเลือกไอโซโทปใดเหมาะสมที่สุด"),
                correct=f"{best.name} (ให้{best.ray} ครึ่งชีวิต {_show(best.half_life)} {best.unit})",
                wrongs=tuple(f"{i.name} (ให้{i.ray} ครึ่งชีวิต {_show(i.half_life)} {i.unit})" for i in picks),
                topic=TOPIC_RADIO_USE,
                hint="รังสีต้องทะลุออกมานอกร่างกายได้ และสารควรสลายตัวหมดไปเร็วเพื่อไม่ให้ผู้ป่วยได้รับรังสีนาน",
            )
        if shape < 0.5:
            return _labelled(
                stem=("โรงงานใช้รังสีวัดความหนาของแผ่นกระดาษ โดยวางแหล่งกำเนิดรังสีไว้ด้านหนึ่งและเครื่องวัดไว้อีกด้าน "
                      "เหตุใดจึงเลือกใช้รังสีบีตา"),
                correct="รังสีบีตาทะลุกระดาษได้บางส่วน ปริมาณที่ทะลุผ่านจึงเปลี่ยนไปตามความหนาของกระดาษ",
                wrongs=("รังสีบีตาทะลุผ่านได้มากที่สุด จึงวัดได้ทุกความหนา",
                        "รังสีบีตาถูกกระดาษกั้นไว้ทั้งหมด จึงวัดได้แม่นยำ",
                        "รังสีบีตาไม่มีประจุ จึงไม่ถูกรบกวนจากเครื่องจักร"),
                topic=TOPIC_RADIO_USE,
                hint="แอลฟาถูกกระดาษกั้นหมด แกมมาทะลุผ่านเกือบหมด ต้องเลือกรังสีที่ปริมาณที่ทะลุผ่านเปลี่ยนตามความหนา",
            )
        if shape < 0.75:
            ray = rng.choice(RAYS)
            answers = {
                ALPHA: "ระวังไม่ให้สารเข้าสู่ร่างกายทางการหายใจหรือการกิน เพราะภายนอกผิวหนังและกระดาษก็กั้นได้",
                BETA: "ใช้แผ่นอะลูมิเนียมหรือพลาสติกหนากั้น และใช้คีมด้ามยาวหยิบจับ",
                GAMMA: "เก็บในภาชนะตะกั่วหนาหรือหลังผนังคอนกรีต และอยู่ห่างให้มากที่สุด",
            }
            return _labelled(
                stem=f"สารที่แผ่{ray}เป็นหลัก ควรป้องกันอันตรายด้วยวิธีใดเหมาะสมที่สุด",
                correct=answers[ray],
                wrongs=(*[v for k, v in answers.items() if k != ray],
                        "ไม่ต้องป้องกัน เพราะรังสีทุกชนิดกั้นได้ด้วยเสื้อผ้าธรรมดา"),
                topic=TOPIC_RADIO_USE,
                hint="เลือกวิธีกำบังตามอำนาจทะลุผ่านของรังสีชนิดนั้น แอลฟาน้อยที่สุด แกมมามากที่สุด",
            )
        use, field = rng.choice(RADIO_USES)
        step, principle = rng.choice(PROTECTIONS)
        return _labelled(
            stem=(f"เจ้าหน้าที่ในงาน\"{use}\" ต้องการลดอันตรายจากรังสีโดยหลักการ \"{principle}\" "
                  "ควรปฏิบัติตามข้อใด"),
            correct=step,
            wrongs=tuple([s for s, p in PROTECTIONS if p != principle]),
            topic=TOPIC_RADIO_USE,
            hint="จับคู่วิธีปฏิบัติกับหลักการ: ลดเวลา เพิ่มระยะห่าง มีสิ่งกำบัง หรือตรวจวัดและเตือน",
        )
