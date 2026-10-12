"""แผนภาพและการต่อชิ้นส่วนอิเล็กทรอนิกส์อย่างง่าย

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/7

Sets moved here from: science_wave_d33.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d32 import THIRD_SECONDARY

PROVENANCE = Provenance("original")


ELECTRONIC_DIAGRAM_TOPIC = "แผนภาพและการต่อชิ้นส่วนอิเล็กทรอนิกส์อย่างง่าย"


SYMBOLS = (
    ("รูปสามเหลี่ยมชี้ไปที่ขีดตั้งฉาก", "ไดโอด"),
    ("รูปสามเหลี่ยมชี้ไปที่ขีดตั้งฉาก และมีลูกศรเล็กสองอันชี้ออกไปด้านนอก", "หลอด LED"),
    ("เส้นขนานสั้นสองเส้นเว้นช่องห่างกันเล็กน้อย", "ตัวเก็บประจุ"),
    ("รูปสี่เหลี่ยมผืนผ้าเล็ก ๆ หรือเส้นหยักฟันเลื่อย", "ตัวต้านทาน"),
    ("รูปสี่เหลี่ยมผืนผ้าที่มีลูกศรลากทแยงผ่าน", "ตัวต้านทานปรับค่าได้"),
    ("รูปสี่เหลี่ยมผืนผ้าที่มีลูกศรเล็กสองอันชี้เข้าหา", "ตัวต้านทานไวแสง"),
    ("วงกลมที่มีขาสามขา และมีลูกศรที่ขาหนึ่ง", "ทรานซิสเตอร์"),
)


LED_CASES = (
    (True, True, "LED สว่างตามปกติ เพราะต่อถูกทิศทางและมีตัวต้านทานจำกัดกระแส"),
    (True, False, "LED สว่างจ้าชั่วครู่แล้วอาจเสีย เพราะไม่มีตัวต้านทานจำกัดกระแส"),
    (False, True, "LED ไม่สว่าง เพราะต่อกลับทิศทางที่ยอมให้กระแสไหล"),
    (False, False, "LED ไม่สว่าง เพราะต่อกลับทิศทางที่ยอมให้กระแสไหล แม้ไม่มีตัวต้านทาน"),
)


DIAGRAM_HINT = "LED และไดโอดยอมให้กระแสไหลทิศทางเดียว (ขายาวของ LED ต่อด้านขั้วบวก) และควรต่ออนุกรมกับตัวต้านทานเพื่อจำกัดกระแส"


ELECTRONIC_DIAGRAM_SCENARIOS = (
    ("เพื่อนวาดแผนภาพวงจรที่มีไดโอดโดยลากลูกศรของสัญลักษณ์ไดโอดสวนทางกับทิศทางที่ต้องการให้กระแสไหล ข้อใดแก้ไขได้ถูกต้อง",
     "ต้องกลับสัญลักษณ์ไดโอดให้ลูกศรชี้ไปในทิศทางเดียวกับที่ต้องการให้กระแสไฟฟ้าไหล",
     ("ถูกต้องแล้ว ทิศทางของสัญลักษณ์ไดโอดไม่มีผลต่อวงจร", "ควรลบไดโอดออกจากวงจรไปเลย", "ควรเพิ่มไดโอดอีกตัวในทิศทางตรงข้ามแทน")),
    ("วงจรไฟกระพริบที่ใช้ตัวเก็บประจุและ LED ทำงานได้เพราะเหตุใด",
     "ตัวเก็บประจุสะสมและปลดปล่อยประจุไฟฟ้าสลับกันเป็นจังหวะ ทำให้ LED สว่างและดับเป็นช่วง ๆ",
     ("LED สร้างกระแสไฟฟ้าขึ้นมาเองเป็นจังหวะ", "ตัวเก็บประจุทำให้กระแสไฟฟ้าไหลคงที่ตลอดเวลาโดยไม่กระพริบ", "การกระพริบไม่เกี่ยวข้องกับตัวเก็บประจุเลย")),
    ("ช่างซ่อมเครื่องใช้ไฟฟ้าตรวจพบว่า LED บนแผงวงจรไม่ติด แต่วัดแรงดันไฟฟ้าที่จ่ายให้ถูกต้อง ข้อใดเป็นสาเหตุที่เป็นไปได้มากที่สุด",
     "LED อาจต่อกลับขั้ว หรือ LED เสียหายจนไม่สามารถนำไฟฟ้าได้ตามปกติ",
     ("แรงดันไฟฟ้าที่ถูกต้องหมายความว่า LED ต้องติดสว่างเสมอ", "LED ไม่จำเป็นต้องต่อขั้วให้ถูกทิศทาง", "ปัญหานี้เกิดจากตัวต้านทานเท่านั้น ไม่เกี่ยวกับ LED")),
)


TWO_DIODES = (
    ("หลอดไฟต่ออนุกรมกับไดโอดที่ต่อตามทิศกระแส", "หลอดไฟสว่าง"),
    ("หลอดไฟต่ออนุกรมกับไดโอดที่ต่อกลับทิศกระแส", "หลอดไฟไม่สว่าง"),
    ("หลอดไฟต่ออนุกรมกับไดโอดสองตัวที่ต่อตามทิศกระแสทั้งคู่", "หลอดไฟสว่าง"),
    ("หลอดไฟต่ออนุกรมกับไดโอดสองตัว ตัวหนึ่งตามทิศ อีกตัวกลับทิศ", "หลอดไฟไม่สว่าง"),
    ("หลอดไฟต่ออนุกรมกับตัวต้านทานไวแสงที่อยู่ในที่มืดสนิท", "หลอดไฟสว่างน้อยมากหรือไม่สว่าง"),
    ("หลอดไฟต่ออนุกรมกับตัวต้านทานไวแสงที่ถูกแสงแดดส่อง", "หลอดไฟสว่าง"),
)


@question_type(
    "elec.electronic_diagram_foundation",
    display_name={"th": "บอกความหมายของสัญลักษณ์ไดโอดในแผนภาพวงจร"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=ELECTRONIC_DIAGRAM_TOPIC,
)
class ElectronicDiagramFoundation(QuestionType):
    """Circuit symbols both ways, and what the diode symbol's arrow means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.2:
            return _labelled(
                stem="สัญลักษณ์ของไดโอดในแผนภาพวงจรอิเล็กทรอนิกส์บอกอะไร",
                correct="ทิศทางที่กระแสไฟฟ้าไหลผ่านได้ โดยลูกศรชี้ไปทางขีดกั้นแสดงทิศทางที่ยอมให้ไหล",
                wrongs=("ขนาดของกระแสไฟฟ้าสูงสุดที่ไหลผ่านได้", "จำนวนรอบที่กระแสไฟฟ้าไหลผ่านได้ในหนึ่งวินาที", "สีของแสงที่ไดโอดจะเปล่งออกมา"),
                hint="สัญลักษณ์ไดโอดแสดงทิศทางเดียวที่ยอมให้กระแสไหลผ่าน ไม่ใช่ขนาดหรือสีของกระแส",
                topic=ELECTRONIC_DIAGRAM_TOPIC,
            )
        shape, name = rng.choice(SYMBOLS)
        picked = rng.sample([s for s in SYMBOLS if s[1] != name], 3)
        if roll < 0.6:
            return _labelled(stem=f"ในแผนภาพวงจร สัญลักษณ์ \"{shape}\" แทนชิ้นส่วนใด", correct=name, wrongs=tuple(p[1] for p in picked),
                             hint="จำสัญลักษณ์ของแต่ละชิ้นส่วน ลูกศรชี้ออกแทนการเปล่งแสง ลูกศรชี้เข้าแทนการรับแสง", topic=ELECTRONIC_DIAGRAM_TOPIC)
        return _labelled(stem=f"ในแผนภาพวงจร {name}เขียนแทนด้วยสัญลักษณ์ใด", correct=shape, wrongs=tuple(p[0] for p in picked),
                         hint="จำสัญลักษณ์ของแต่ละชิ้นส่วน ลูกศรชี้ออกแทนการเปล่งแสง ลูกศรชี้เข้าแทนการรับแสง", topic=ELECTRONIC_DIAGRAM_TOPIC)


@question_type(
    "elec.electronic_diagram_fluency",
    display_name={"th": "บอกผลของการต่อ LED กลับขั้วในวงจร"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=ELECTRONIC_DIAGRAM_TOPIC,
)
class ElectronicDiagramFluency(QuestionType):
    """An LED wired either way, with or without its resistor."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        forward, resistor, right = rng.choice(LED_CASES)
        cells = rng.choice((2, 3, 4))
        colour = rng.choice(("สีแดง", "สีเขียว", "สีน้ำเงิน", "สีเหลือง", "สีขาว"))
        legs = "ขายาวต่อด้านขั้วบวกของถ่าน" if forward else "ขาสั้นต่อด้านขั้วบวกของถ่าน (กลับขั้ว)"
        wrongs = [c[2] for c in LED_CASES if c[2] != right and c[2].split(" เพราะ")[0] != right.split(" เพราะ")[0]]
        wrongs += ["LED สว่างสลับกับดับเป็นจังหวะ เพราะกระแสไหลไปกลับ"]
        return _labelled(stem=f"นักเรียนต่อหลอด LED {colour}กับถ่านไฟฉาย {cells} ก้อน โดย{legs} "
                              f"{'และต่ออนุกรมกับตัวต้านทาน' if resistor else 'โดยไม่มีตัวต้านทาน'} ผลจะเป็นอย่างไร",
                         correct=right, wrongs=tuple(wrongs[:3]) if len(wrongs) >= 3 else (*wrongs, "LED สว่างจ้ากว่าปกติเพราะกระแสไฟฟ้าไหลย้อนกลับ"),
                         hint=DIAGRAM_HINT, topic=ELECTRONIC_DIAGRAM_TOPIC)


@question_type(
    "elec.electronic_diagram_application",
    display_name={"th": "ตรวจสอบและแก้ไขแผนภาพวงจรที่มีชิ้นส่วนอิเล็กทรอนิกส์"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=ELECTRONIC_DIAGRAM_TOPIC,
)
class ElectronicDiagramApplication(QuestionType):
    """Authored corrections, and predicting a bulb from the parts drawn with it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(
                rng, ELECTRONIC_DIAGRAM_SCENARIOS,
                hint="ไดโอดและ LED ยอมให้กระแสไหลทิศทางเดียว ตัวเก็บประจุสะสมและปลดปล่อยพลังงานได้",
            ), ELECTRONIC_DIAGRAM_TOPIC)
        case, right = rng.choice(TWO_DIODES)
        cells = rng.choice((2, 3, 4))
        pools = {
            # Short readings beside short answers, so the answer is not the one brief choice.
            "หลอดไฟสว่าง": ("หลอดไฟไม่สว่าง", "หลอดไฟกะพริบ", "ไดโอดสว่างแทน", "หลอดไฟขาดทันที", "ถ่านชาร์จเต็ม"),
            "หลอดไฟไม่สว่าง": ("หลอดไฟสว่าง", "หลอดไฟสว่างจ้า", "หลอดไฟกะพริบ", "สว่างครึ่งดวง", "ไดโอดสว่างแทน"),
            "หลอดไฟสว่างน้อยมากหรือไม่สว่าง": ("หลอดไฟสว่างจ้ามากกว่าปกติทุกครั้ง", "หลอดไฟสว่างสลับดับเป็นจังหวะ",
                                               "หลอดไฟสว่างตามปกติเหมือนไม่มี LDR", "หลอดไฟขาดทันทีเมื่อต่อวงจร",
                                               "ตัวต้านทานไวแสงเปล่งแสงแทนหลอดไฟ"),
        }
        wrongs = tuple(rng.sample(pools[right], 3))
        return _labelled(stem=f"แผนภาพวงจรแสดงถ่านไฟฉาย {cells} ก้อนต่อกับ{case} หลอดไฟจะเป็นอย่างไร", correct=right, wrongs=wrongs,
                         hint="ไดโอดที่กลับทิศตัวใดตัวหนึ่งจะกั้นกระแสทั้งวงจรอนุกรม ตัวต้านทานไวแสงมีความต้านทานสูงในที่มืด", topic=ELECTRONIC_DIAGRAM_TOPIC)
