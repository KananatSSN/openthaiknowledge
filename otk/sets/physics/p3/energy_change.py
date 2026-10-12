"""การเปลี่ยนพลังงานจากรูปหนึ่งไปเป็นอีกรูปหนึ่ง

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.3/1

Sets moved here from: science_wave_d23.
"""

from __future__ import annotations

from itertools import permutations
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


ENERGY_CHANGE_TOPIC = "การเปลี่ยนพลังงานจากรูปหนึ่งไปเป็นอีกรูปหนึ่ง"


DEVICES = (
    ("พัดลม", "พลังงานกล (การเคลื่อนที่)"),
    ("หลอดไฟฟ้า", "พลังงานแสงและพลังงานความร้อน"),
    ("ลำโพง", "พลังงานเสียง"),
    ("เตารีดไฟฟ้า", "พลังงานความร้อน"),
    ("เครื่องปั่นน้ำผลไม้", "พลังงานกล (การเคลื่อนที่)"),
    ("หม้อหุงข้าวไฟฟ้า", "พลังงานความร้อน"),
    ("กาต้มน้ำไฟฟ้า", "พลังงานความร้อน"),
    ("ออดไฟฟ้า", "พลังงานเสียง"),
    ("สว่านไฟฟ้า", "พลังงานกล (การเคลื่อนที่)"),
    ("เครื่องชาร์จที่กำลังชาร์จแบตเตอรี่", "พลังงานเคมี (สะสมไว้ในแบตเตอรี่)"),
    ("วิทยุ", "พลังงานเสียง"),
    ("เครื่องปิ้งขนมปัง", "พลังงานความร้อน"),
)


RESULTS = tuple(dict.fromkeys(r for _, r in DEVICES))


ENERGY_HINT = "สังเกตว่าอุปกรณ์นั้นให้ผลอะไรแก่ผู้ใช้เป็นหลัก เช่น ลม การหมุน แสง เสียง หรือความร้อน"


class EnergyChange(NamedTuple):
    record: str
    before: str
    after: str


ENERGY_CHANGES = (
    EnergyChange("เสียบปลั๊กหลอดไฟฟ้า แล้วหลอดไฟทั้งสว่างและรู้สึกอุ่นเมื่อสัมผัสใกล้ ๆ",
                 "พลังงานไฟฟ้า", "พลังงานแสงและพลังงานความร้อน"),
    EnergyChange("เสียบปลั๊กพัดลม แล้วใบพัดหมุนจนรู้สึกลมพัด",
                 "พลังงานไฟฟ้า", "พลังงานกล (การเคลื่อนที่)"),
    EnergyChange("ใส่ถ่านไฟฉายแล้วไฟฉายสว่างขึ้นทันทีโดยไม่ต้องเสียบปลั๊ก",
                 "พลังงานเคมีในถ่านไฟฉาย", "พลังงานไฟฟ้าและพลังงานแสง"),
    EnergyChange("จุดไฟเผาฟืน แล้วเกิดแสงสว่างและความอบอุ่นโดยรอบ",
                 "พลังงานเคมีในฟืน", "พลังงานแสงและพลังงานความร้อน"),
    EnergyChange("นำแผงโซลาร์เซลล์ไปตากแดด แล้วมิเตอร์วัดไฟฟ้าที่ต่ออยู่แสดงกระแสไฟฟ้าไหล",
                 "พลังงานแสงจากดวงอาทิตย์", "พลังงานไฟฟ้า"),
    EnergyChange("ปั่นจักรยานที่มีไดนาโมติดล้อ แล้วไฟหน้ารถจักรยานสว่างขึ้นเมื่อปั่นเร็ว",
                 "พลังงานกลจากการปั่น", "พลังงานไฟฟ้าและพลังงานแสง"),
    EnergyChange("เสียบปลั๊กหม้อหุงข้าว แล้วน้ำในหม้อร้อนจนข้าวสุก",
                 "พลังงานไฟฟ้า", "พลังงานความร้อน"),
    EnergyChange("ลมพัดใบกังหันลมจนหมุน แล้วหลอดไฟที่ต่อกับกังหันสว่าง",
                 "พลังงานกลของลม", "พลังงานไฟฟ้า"),
    EnergyChange("ใส่ถ่านในวิทยุแล้วเปิดเครื่อง ได้ยินเสียงเพลงดังออกมา",
                 "พลังงานเคมีในถ่านไฟฉาย", "พลังงานไฟฟ้าและพลังงานเสียง"),
    EnergyChange("วางถังน้ำสีดำไว้กลางแดดทั้งวัน แล้วน้ำในถังอุ่นขึ้น",
                 "พลังงานแสงจากดวงอาทิตย์", "พลังงานความร้อน"),
)


ENERGY_CHANGE_SCENARIOS = (
    ("เขื่อนผลิตไฟฟ้าโดยปล่อยน้ำจากที่สูงให้ไหลแรงหมุนกังหัน เป็นการเปลี่ยนพลังงานจากรูปใดไปเป็นรูปใดตามลำดับ",
     "พลังงานศักย์ (จากที่สูง) เป็นพลังงานกล แล้วเป็นพลังงานไฟฟ้า",
     ("พลังงานไฟฟ้าเป็นพลังงานศักย์ แล้วเป็นพลังงานกล", "พลังงานเคมีเป็นพลังงานไฟฟ้าโดยตรง", "พลังงานความร้อนเป็นพลังงานกล แล้วเป็นพลังงานศักย์")),
    ("นักเรียนถูฝ่ามือทั้งสองข้างเข้าด้วยกันอย่างรวดเร็ว จนรู้สึกอุ่นขึ้น เป็นการเปลี่ยนพลังงานจากรูปใดไปเป็นรูปใด",
     "พลังงานกล (การเคลื่อนที่ของมือ) เป็นพลังงานความร้อน",
     ("พลังงานความร้อนเป็นพลังงานกล", "พลังงานไฟฟ้าเป็นพลังงานความร้อน", "พลังงานเคมีเป็นพลังงานกล")),
    ("รถของเล่นที่ใช้ถ่านไฟฉายวิ่งได้เมื่อเปิดสวิตช์ เป็นการเปลี่ยนพลังงานจากรูปใดไปเป็นรูปใดตามลำดับ",
     "พลังงานเคมีในถ่านไฟฉาย เป็นพลังงานไฟฟ้า แล้วเป็นพลังงานกล",
     ("พลังงานไฟฟ้าเป็นพลังงานเคมี แล้วเป็นพลังงานกล", "พลังงานกลเป็นพลังงานเคมีโดยตรง", "พลังงานเคมีเป็นพลังงานกลโดยตรงโดยไม่ผ่านไฟฟ้า")),
)


CHAINS = (
    ("โรงไฟฟ้าพลังน้ำจ่ายไฟให้พัดลมในบ้าน", ("พลังงานศักย์ของน้ำ", "พลังงานไฟฟ้า", "พลังงานกลของใบพัด")),
    ("ถ่านไฟฉายในรถของเล่นทำให้รถวิ่ง", ("พลังงานเคมี", "พลังงานไฟฟ้า", "พลังงานกล")),
    ("แผงโซลาร์เซลล์ชาร์จแบตเตอรี่ของโคมไฟสนามที่สว่างตอนกลางคืน", ("พลังงานแสงอาทิตย์", "พลังงานไฟฟ้า", "พลังงานเคมีในแบตเตอรี่", "พลังงานแสงของหลอดไฟ")),
    ("กังหันลมผลิตไฟฟ้าให้ลำโพงเปิดเพลง", ("พลังงานกลของลม", "พลังงานไฟฟ้า", "พลังงานเสียง")),
    ("ไดนาโมจักรยานทำให้ไฟหน้าสว่างเมื่อปั่น", ("พลังงานกล", "พลังงานไฟฟ้า", "พลังงานแสง")),
    ("ร่างกายกินอาหารแล้วนำไปวิ่ง", ("พลังงานเคมีในอาหาร", "พลังงานกลของกล้ามเนื้อ", "พลังงานความร้อนที่ทำให้ร่างกายอุ่น")),
)


@question_type(
    "phys.energy_change_foundation",
    display_name={"th": "บอกพลังงานที่อุปกรณ์ไฟฟ้าเปลี่ยนพลังงานไฟฟ้าไปเป็น"},
    level=THIRD, subject=SUBJECT, topic=ENERGY_CHANGE_TOPIC,
)
class EnergyChangeFoundation(QuestionType):
    """A device; the energy it mainly turns electricity into."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        device, result = rng.choice(DEVICES)
        # A result inside another ("heat" within "light and heat") would be half right.
        others = [r for r in RESULTS if r != result and r not in result and result not in r]
        return _labelled(
            stem=f"เมื่อเสียบปลั๊ก{device} อุปกรณ์นี้เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานใดเป็นหลัก",
            correct=result,
            wrongs=tuple(others),
            hint=ENERGY_HINT,
            topic=ENERGY_CHANGE_TOPIC,
        )


@question_type(
    "phys.energy_change_fluency",
    display_name={"th": "ยกตัวอย่างการเปลี่ยนพลังงานจากหลักฐานเชิงประจักษ์"},
    level=THIRD, subject=SUBJECT, topic=ENERGY_CHANGE_TOPIC,
)
class EnergyChangeFluency(QuestionType):
    """An observed device; the energy form it started and ended as."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(ENERGY_CHANGES))
        change = ENERGY_CHANGES[index]
        right = f"เปลี่ยนจาก{change.before}เป็น{change.after}"
        others = list(dict.fromkeys(f"เปลี่ยนจาก{c.before}เป็น{c.after}" for i, c in enumerate(ENERGY_CHANGES) if i != index))
        others = [o for o in others if o != right] + [f"เปลี่ยนจาก{change.after}เป็น{change.before}"]
        return _labelled(
            stem=f"{change.record} จากหลักฐานนี้ เป็นการเปลี่ยนพลังงานจากรูปใดไปเป็นรูปใด",
            correct=right,
            wrongs=tuple(others),
            hint="สังเกตว่าพลังงานที่ป้อนเข้าไปคือรูปใด และผลที่สังเกตได้แสดงพลังงานรูปใหม่รูปใด",
            topic=ENERGY_CHANGE_TOPIC,
        )


@question_type(
    "phys.energy_change_application",
    display_name={"th": "ใช้ความรู้เรื่องการเปลี่ยนพลังงานอธิบายสถานการณ์"},
    level=THIRD, subject=SUBJECT, topic=ENERGY_CHANGE_TOPIC,
)
class EnergyChangeApplication(QuestionType):
    """Authored chains, and a chain of changes put in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(rng, ENERGY_CHANGE_SCENARIOS, hint="ตามพลังงานทีละขั้นจากจุดเริ่มต้นไปจนถึงผลที่สังเกตได้ในที่สุด"),
                            ENERGY_CHANGE_TOPIC)
        case, chain = rng.choice(CHAINS)
        orders = [" → ".join(p) for p in permutations(chain) if p != chain]
        return _labelled(stem=f"{case} ข้อใดเรียงลำดับการเปลี่ยนพลังงานได้ถูกต้อง", correct=" → ".join(chain),
                         wrongs=tuple(orders), hint="ตามพลังงานทีละขั้นจากจุดเริ่มต้นไปจนถึงผลที่สังเกตได้ในที่สุด",
                         topic=ENERGY_CHANGE_TOPIC)
