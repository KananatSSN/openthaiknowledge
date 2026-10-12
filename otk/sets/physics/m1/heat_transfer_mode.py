"""แบบจำลองการถ่ายโอนความร้อนโดยการนำ การพา และการแผ่รังสี

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/6

Sets moved here from: science_wave_d29.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d28 import FIRST_SECONDARY

PROVENANCE = Provenance("original")


HEAT_TRANSFER_MODEL_TOPIC = "แบบจำลองการถ่ายโอนความร้อนโดยการนำ การพา และการแผ่รังสี"


HEAT_EXAMPLES = {
    "การนำความร้อน": ("ด้ามช้อนโลหะร้อนขึ้นเมื่อแช่ในแกงร้อน", "มือรู้สึกเย็นเมื่อจับราวบันไดเหล็กตอนเช้า", "ก้นกระทะร้อนขึ้นเมื่อวางบนเตา",
                      "เตารีดทำให้ผ้าร้อนขึ้นขณะรีด", "น้ำแข็งละลายเมื่อวางบนฝ่ามือ", "แท่งโลหะร้อนไปถึงปลายที่จับเมื่ออีกปลายอยู่ในกองไฟ"),
    "การพาความร้อน": ("อากาศร้อนเหนือกองไฟลอยขึ้นพาควันขึ้นไปด้วย", "น้ำในหม้อหมุนวนขณะต้มจนเดือด", "ลมทะเลพัดเข้าฝั่งในตอนกลางวัน",
                      "เครื่องปรับอากาศติดไว้สูงเพื่อให้อากาศเย็นจมลง", "บอลลูนลมร้อนลอยขึ้นเมื่ออากาศภายในร้อน", "ลมร้อนจากไดร์เป่าผมทำให้ผมแห้ง"),
    "การแผ่รังสีความร้อน": ("รู้สึกร้อนเมื่อยืนกลางแดดแม้อากาศรอบตัวเย็น", "รู้สึกอุ่นเมื่อนั่งหน้ากองไฟโดยไม่ได้สัมผัส", "พลังงานจากดวงอาทิตย์เดินทางผ่านอวกาศมาถึงโลก",
                            "รู้สึกร้อนที่ใบหน้าเมื่อเปิดประตูเตาอบ", "เสื้อสีดำร้อนกว่าเสื้อสีขาวเมื่อตากแดด", "ถนนยางมะตอยแผ่ความร้อนออกมาในตอนเย็น"),
}


HEAT_MODES = tuple(HEAT_EXAMPLES)


HEAT_MODE_FACTS = (
    ("การนำความร้อน (conduction) เกิดขึ้นได้ดีที่สุดในตัวกลางชนิดใด",
     "ของแข็ง โดยเฉพาะโลหะ ซึ่งอนุภาคอยู่ชิดกันและถ่ายโอนพลังงานผ่านการสั่นชนกัน",
     ("สุญญากาศที่ไม่มีอนุภาคใดเลย", "แก๊สที่มีอนุภาคอยู่ห่างกันมาก", "พื้นที่ว่างระหว่างดวงดาวในอวกาศ", "ของเหลวที่หมุนวนอยู่เท่านั้น", "แสงที่เดินทางในอวกาศ")),
    ("การพาความร้อน (convection) เกิดขึ้นได้ในตัวกลางชนิดใด", "ของเหลวและแก๊สที่อนุภาคเคลื่อนที่ไปพร้อมกับความร้อนได้",
     ("ของแข็งเท่านั้น", "สุญญากาศเท่านั้น", "โลหะที่แข็งตัวเท่านั้น", "ไม่ต้องมีตัวกลางใดเลย", "หินและไม้เท่านั้น")),
    ("การถ่ายโอนความร้อนแบบใดไม่ต้องอาศัยตัวกลาง", "การแผ่รังสีความร้อน",
     ("การนำความร้อน", "การพาความร้อน", "การนำและการพาความร้อน", "ทุกแบบต้องอาศัยตัวกลาง", "การระเหย")),
    ("ความร้อนถ่ายโอนจากที่ใดไปที่ใด", "จากบริเวณที่มีอุณหภูมิสูงไปยังบริเวณที่มีอุณหภูมิต่ำ",
     ("จากบริเวณที่มีอุณหภูมิต่ำไปยังบริเวณที่มีอุณหภูมิสูง", "จากวัตถุที่มีมวลน้อยไปวัตถุที่มีมวลมากเสมอ", "ไม่มีทิศทางที่แน่นอน",
      "จากของเหลวไปของแข็งเสมอ", "จากวัตถุสีขาวไปวัตถุสีดำเสมอ")),
    ("พื้นผิวแบบใดดูดกลืนและแผ่รังสีความร้อนได้ดี", "พื้นผิวสีดำและผิวด้าน",
     ("พื้นผิวสีขาวเงา", "พื้นผิวกระจกเงา", "พื้นผิวอะลูมิเนียมขัดมัน", "พื้นผิวสีเงินสะท้อนแสง", "ไม่มีพื้นผิวแบบใดดูดกลืนได้")),
)


HEAT_MODE_HINT = ("การนำ: ส่งต่อผ่านอนุภาคที่อยู่ชิดกันโดยไม่เคลื่อนที่ การพา: ของเหลวหรือแก๊สเคลื่อนที่พาความร้อนไป "
                  "การแผ่รังสี: คลื่นแม่เหล็กไฟฟ้า ไม่ต้องมีตัวกลาง")


CONDUCTORS = (("ทองแดง", 400), ("อะลูมิเนียม", 240), ("เหล็ก", 80), ("แก้ว", 1), ("ไม้", Fraction(15, 100)), ("พลาสติก", Fraction(2, 10)),
              ("โฟม", Fraction(3, 100)), ("ยาง", Fraction(16, 100)))


HEAT_TRANSFER_PARTS = (
    Part("แท่งโลหะปลายหนึ่งอยู่ในกองไฟ อีกปลายหนึ่งที่จับค่อย ๆ ร้อนขึ้นโดยแท่งโลหะไม่เคลื่อนที่",
         "เป็นการนำความร้อน ถ่ายโอนผ่านการสั่นและชนกันของอนุภาคในของแข็ง โดยอนุภาคไม่เคลื่อนที่จากตำแหน่งเดิม",
         "เป็นการพาความร้อน ถ่ายโอนผ่านการเคลื่อนที่ของอนุภาคเป็นกลุ่มก้อนไปทั้งแท่งโลหะ"),
    Part("น้ำในหม้อต้มที่มีสีผสมอาหารหมุนเวียนเป็นวงขณะน้ำเดือด",
         "เป็นการพาความร้อน ถ่ายโอนผ่านการเคลื่อนที่ของของเหลวร้อนที่ลอยขึ้นและของเหลวเย็นที่จมลง",
         "เป็นการนำความร้อน ถ่ายโอนผ่านการสั่นของอนุภาคโดยของเหลวไม่เคลื่อนที่เลย"),
    Part("รู้สึกอุ่นเมื่อยืนใกล้กองไฟ โดยไม่ได้สัมผัสหรืออยู่เหนือกองไฟ",
         "เป็นการแผ่รังสีความร้อน ถ่ายโอนผ่านคลื่นแม่เหล็กไฟฟ้าโดยไม่ต้องอาศัยตัวกลาง",
         "เป็นการนำความร้อนผ่านอากาศที่อยู่ระหว่างกองไฟกับตัวเรา"),
)


HEAT_TRANSFER_PARTS_STEM = ("นักเรียนสังเกตเหตุการณ์สามอย่างพร้อมกัน — " +
                            " / ".join(part.label for part in HEAT_TRANSFER_PARTS) +
                            " จากข้อมูลนี้ ข้อใดอธิบายวิธีการถ่ายโอนความร้อนของแต่ละเหตุการณ์ได้ถูกต้องทั้งหมด")


HEAT_TRANSFER_MODE_SCENARIOS = (
    ("กระติกน้ำร้อนสุญญากาศมีช่องว่างอากาศถูกดูดออกระหว่างผนังสองชั้น และผนังชั้นในฉาบด้วยสารสะท้อนแสงคล้ายกระจก ออกแบบเช่นนี้เพื่อลดการถ่ายโอนความร้อนแบบใด",
     "ลดทั้งการนำและการพาความร้อนด้วยสุญญากาศ และลดการแผ่รังสีความร้อนด้วยผิวสะท้อนแสง",
     ("ลดเฉพาะการนำความร้อนเท่านั้น ไม่เกี่ยวกับการพาหรือการแผ่รังสี", "เพิ่มการพาความร้อนให้เร็วขึ้นเพื่อรักษาอุณหภูมิ", "สุญญากาศและผิวสะท้อนแสงไม่มีผลต่อการถ่ายโอนความร้อนเลย")),
    ("หน้าต่างกระจกสองชั้นที่มีช่องอากาศคั่นกลางช่วยรักษาอุณหภูมิภายในบ้านได้ดีกว่ากระจกชั้นเดียว เพราะเหตุใด",
     "ช่องอากาศเป็นฉนวนที่นำความร้อนได้ไม่ดี จึงลดการนำความร้อนระหว่างภายในและภายนอกบ้าน",
     ("ช่องอากาศช่วยเพิ่มการนำความร้อนให้เร็วขึ้น", "กระจกสองชั้นหนักกว่าจึงกันความร้อนได้ดีกว่า", "ช่องอากาศไม่มีผลต่อการถ่ายโอนความร้อนระหว่างกระจกสองชั้น")),
    ("เครื่องทำความร้อนแบบแผ่รังสี (เช่น ฮีตเตอร์อินฟราเรด) ทำให้รู้สึกอุ่นทันทีที่เปิดใช้งาน แม้อากาศรอบตัวยังไม่ทันร้อนขึ้น เพราะเหตุใด",
     "รังสีความร้อนเดินทางเป็นคลื่นแม่เหล็กไฟฟ้าไปถึงผิวหนังโดยตรงโดยไม่ต้องรอให้อากาศร้อนขึ้นก่อน",
     ("ฮีตเตอร์ทำให้อากาศทั้งห้องร้อนขึ้นทันทีเสมอ", "รังสีความร้อนต้องอาศัยอากาศเป็นตัวกลางเสมอ", "ความรู้สึกอุ่นทันทีไม่เกี่ยวข้องกับการแผ่รังสีความร้อน")),
)


@question_type(
    "phys.heat_transfer_mode_foundation",
    display_name={"th": "บอกตัวกลางที่เหมาะกับการนำความร้อนได้ดี"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_TRANSFER_MODEL_TOPIC,
)
class HeatTransferModeFoundation(QuestionType):
    """Media, direction and surfaces; which everyday example is each mode."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            mode = rng.choice(HEAT_MODES)
            pool = [e for m, es in HEAT_EXAMPLES.items() if m != mode for e in es]
            return _labelled(stem=f"เหตุการณ์ใดเป็นตัวอย่างของ{mode}", correct=rng.choice(HEAT_EXAMPLES[mode]),
                             wrongs=tuple(pool), hint=HEAT_MODE_HINT, topic=HEAT_TRANSFER_MODEL_TOPIC)
        stem, right, wrongs = rng.choice(HEAT_MODE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=HEAT_MODE_HINT, topic=HEAT_TRANSFER_MODEL_TOPIC)


@question_type(
    "phys.heat_transfer_mode_fluency",
    display_name={"th": "สร้างแบบจำลองที่อธิบายการนำ การพา และการแผ่รังสีความร้อน"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_TRANSFER_MODEL_TOPIC,
)
class HeatTransferModeFluency(QuestionType):
    """The three-observation model, or one observation named by its mode."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return parts_item(
                rng, HEAT_TRANSFER_PARTS, stem=HEAT_TRANSFER_PARTS_STEM,
                hint="แยกพิจารณาแต่ละเหตุการณ์: มีการเคลื่อนที่ของอนุภาคเป็นกลุ่มก้อนหรือไม่ และต้องอาศัยตัวกลางหรือไม่",
                topic=HEAT_TRANSFER_MODEL_TOPIC,
            )
        if rng.random() < 0.45:
            m1, m2 = rng.sample(HEAT_MODES, 2)
            e1, e2 = rng.choice(HEAT_EXAMPLES[m1]), rng.choice(HEAT_EXAMPLES[m2])
            m3 = next(m for m in HEAT_MODES if m not in (m1, m2))
            line = lambda a, b: f"เหตุการณ์ที่ 1 เป็น{a} / เหตุการณ์ที่ 2 เป็น{b}"
            return _labelled(stem=f"เหตุการณ์ที่ 1: {e1} เหตุการณ์ที่ 2: {e2} ข้อใดระบุวิธีการถ่ายโอนความร้อนได้ถูกต้องทั้งสองเหตุการณ์",
                             correct=line(m1, m2), wrongs=(line(m2, m1), line(m1, m3), line(m3, m2)), hint=HEAT_MODE_HINT,
                             topic=HEAT_TRANSFER_MODEL_TOPIC)
        mode = rng.choice(HEAT_MODES)
        example = rng.choice(HEAT_EXAMPLES[mode])
        return _labelled(stem=f"\"{example}\" เป็นการถ่ายโอนความร้อนแบบใด", correct=mode,
                         wrongs=(*(m for m in HEAT_MODES if m != mode), "ไม่มีการถ่ายโอนความร้อน"), hint=HEAT_MODE_HINT,
                         topic=HEAT_TRANSFER_MODEL_TOPIC)


@question_type(
    "phys.heat_transfer_mode_application",
    display_name={"th": "ใช้ความรู้เรื่องการนำ การพา และการแผ่รังสีอธิบายอุปกรณ์จริง"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=HEAT_TRANSFER_MODEL_TOPIC,
)
class HeatTransferModeApplication(QuestionType):
    """Authored devices, and picking materials by how well they conduct."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _retopic(scenario_question(
                rng, HEAT_TRANSFER_MODE_SCENARIOS,
                hint="พิจารณาว่าอุปกรณ์นั้นลดหรือใช้ประโยชน์จากการนำ การพา หรือการแผ่รังสีความร้อน",
            ), HEAT_TRANSFER_MODEL_TOPIC)
        picked = rng.sample(CONDUCTORS, 4)
        good = rng.random() < 0.5
        right = (max if good else min)(picked, key=lambda c: c[1])[0]
        task = rng.choice(("ก้นหม้อหุงต้ม", "แผ่นระบายความร้อนของคอมพิวเตอร์", "ก้นกระทะ")) if good else \
            rng.choice(("ด้ามจับกระทะ", "ที่จับหม้อ", "ผนังกล่องเก็บความเย็น", "ถุงมือจับของร้อน"))
        table = " ".join(f"{n} {show(k)}" for n, k in picked)
        return _labelled(stem=f"ค่าการนำความร้อน (W/m·K) ของวัสดุ: {table} ควรเลือกวัสดุใดทำ{task}", correct=right,
                         wrongs=tuple(n for n, _ in picked if n != right),
                         hint="งานที่ต้องการให้ความร้อนผ่านเร็วใช้วัสดุนำความร้อนดี งานที่ต้องการกันความร้อนใช้วัสดุนำความร้อนไม่ดี (ฉนวน)",
                         topic=HEAT_TRANSFER_MODEL_TOPIC)
