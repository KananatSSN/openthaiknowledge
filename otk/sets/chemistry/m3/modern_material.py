"""พอลิเมอร์ เซรามิก และวัสดุผสม

เคมี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.3/1

Sets moved here from: science_wave_d10.
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
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d10 import SECONDARY_THREE

PROVENANCE = Provenance("original")


MATERIALS_TOPIC = "พอลิเมอร์ เซรามิก และวัสดุผสม"


POLYMER, CERAMIC, COMPOSITE = "พอลิเมอร์", "เซรามิก", "วัสดุผสม"


MATERIAL_KINDS = (POLYMER, CERAMIC, COMPOSITE)


class Sample(NamedTuple):
    name: str
    kind: str
    tested: str


SAMPLES = (
    Sample("ถุงพลาสติก", POLYMER, "ยืดได้ น้ำหนักเบา ไม่นำไฟฟ้า เมื่อได้รับความร้อนอ่อนตัวและหลอมเหลว"),
    Sample("ยางยืด", POLYMER, "ยืดหยุ่นสูง น้ำหนักเบา ไม่นำไฟฟ้า"),
    Sample("จานกระเบื้อง", CERAMIC, "แข็ง ทนความร้อนสูง ไม่นำไฟฟ้า แต่เปราะ ตกแล้วแตก"),
    Sample("ลูกถ้วยไฟฟ้า", CERAMIC, "แข็ง ทนความร้อน เป็นฉนวนไฟฟ้า แต่เปราะ"),
    Sample("คอนกรีตเสริมเหล็ก", COMPOSITE, "รับแรงกดได้มากจากคอนกรีต และรับแรงดึงได้จากเหล็กเส้นที่อยู่ภายใน"),
    Sample("ไฟเบอร์กลาส", COMPOSITE, "แข็งแรง น้ำหนักเบา ทนการกัดกร่อน จากใยแก้วที่ฝังในพลาสติก"),
    Sample("ท่อพีวีซี", POLYMER, "น้ำหนักเบา ไม่เป็นสนิม ไม่นำไฟฟ้า อ่อนตัวเมื่อได้รับความร้อน"),
    Sample("ถุงมือยาง", POLYMER, "ยืดหยุ่น ไม่นำไฟฟ้า กันน้ำได้"),
    Sample("กระถางดินเผา", CERAMIC, "แข็ง ทนความร้อน แต่เปราะ ตกแล้วแตก"),
    Sample("อิฐมอญ", CERAMIC, "แข็ง ทนความร้อน รับแรงกดได้ แต่เปราะ"),
    Sample("ไม้เทนนิสคาร์บอนไฟเบอร์", COMPOSITE, "แข็งแรงมากแต่น้ำหนักเบา จากเส้นใยคาร์บอนที่ฝังในพลาสติก"),
    Sample("ไม้อัด", COMPOSITE, "แข็งแรงและบิดงอน้อยกว่าไม้แผ่นเดียว จากไม้บางหลายชั้นที่ติดกาวสลับแนวเสี้ยน"),
)


KIND_PARTS = {
    POLYMER: Part(POLYMER, "น้ำหนักเบา ยืดหยุ่นหรือขึ้นรูปได้ง่าย ไม่นำไฟฟ้า ใช้ทำบรรจุภัณฑ์และฉนวนหุ้มสายไฟ",
                  "แข็ง ทนความร้อนสูงมาก แต่เปราะ ใช้ทำถ้วยชามและเตาเผา"),
    CERAMIC: Part(CERAMIC, "แข็ง ทนความร้อนและเป็นฉนวนไฟฟ้า แต่เปราะ ใช้ทำถ้วยชาม กระเบื้อง และลูกถ้วยไฟฟ้า",
                  "น้ำหนักเบา ยืดหยุ่นและหลอมเหลวที่อุณหภูมิต่ำ ใช้ทำถุงใส่ของ"),
    COMPOSITE: Part(COMPOSITE, "รวมวัสดุตั้งแต่สองชนิดให้ได้สมบัติที่ดีขึ้น เช่น แข็งแรงแต่น้ำหนักเบา ใช้ทำโครงสร้างอาคาร ตัวเรือ และไม้เทนนิส",
                    "เป็นวัสดุชนิดเดียวที่ไม่ได้ผสมกับสิ่งใด จึงมีสมบัติเหมือนวัสดุตั้งต้นทุกประการ"),
}


MATERIALS_SCENARIOS = (
    ("เหตุใดหม้อหุงข้าวจึงใช้ด้ามจับพลาสติกชนิดทนความร้อน แต่ใช้เซรามิกเคลือบผิวในหม้อบางรุ่น",
     "พลาสติกน้ำหนักเบาและไม่นำความร้อนจึงจับได้ ส่วนเซรามิกทนความร้อนสูงและแข็งจึงเหมาะกับผิวที่สัมผัสความร้อน",
     ("พลาสติกทนความร้อนสูงกว่าเซรามิก",
      "เซรามิกยืดหยุ่นจึงไม่แตกเมื่อร้อน",
      "ทั้งสองอย่างนำไฟฟ้าได้ดี",
      "เซรามิกนำความร้อนได้ดีจึงเหมาะกับด้ามจับ",
      "พลาสติกเปราะจึงเหมาะกับผิวในหม้อ")),
    ("เสาไฟฟ้าคอนกรีตมีเหล็กเส้นอยู่ภายใน ข้อใดอธิบายเหตุผลได้ดีที่สุด",
     "คอนกรีตรับแรงกดได้ดีแต่รับแรงดึงได้ไม่ดี เหล็กเส้นช่วยรับแรงดึง วัสดุผสมนี้จึงแข็งแรงกว่าคอนกรีตอย่างเดียว",
     ("เหล็กเส้นช่วยให้คอนกรีตนำไฟฟ้า",
      "เหล็กเส้นทำให้คอนกรีตน้ำหนักเบาลง",
      "คอนกรีตรับแรงดึงได้ดีกว่าเหล็ก",
      "เหล็กเส้นช่วยให้คอนกรีตยืดหยุ่นเหมือนยาง",
      "เหล็กเส้นใส่ไว้เพื่อให้เสามีสีสวย")),
    ("ถ้าต้องเลือกวัสดุทำตัวเรือแคนูที่เบา แข็งแรง และไม่เป็นสนิม ควรเลือกวัสดุใด",
     "ไฟเบอร์กลาส เพราะเป็นวัสดุผสมที่แข็งแรง น้ำหนักเบา และทนการกัดกร่อน",
     ("เซรามิก เพราะแข็งแต่ไม่เปราะ",
      "เหล็กกล้า เพราะเบาที่สุด",
      "ถุงพลาสติกหลายชั้น เพราะแข็งแรงที่สุด",
      "ยางยืด เพราะแข็งแรงที่สุด",
      "กระเบื้องดินเผา เพราะเบาและไม่แตก")),
    ("ลูกถ้วยไฟฟ้าที่ยึดสายไฟบนเสาไฟฟ้าแรงสูงทำจากเซรามิก เพราะเหตุใด",
     "เซรามิกเป็นฉนวนไฟฟ้าที่ดี แข็ง และทนสภาพอากาศได้นาน",
     ("เซรามิกนำไฟฟ้าได้ดีจึงช่วยส่งกระแส",
      "เซรามิกยืดหยุ่นจึงรับแรงดึงของสายได้",
      "เซรามิกหลอมเหลวที่อุณหภูมิต่ำจึงขึ้นรูปได้ง่ายหน้างาน",
      "เซรามิกเบากว่าพลาสติกทุกชนิด",
      "เซรามิกดึงดูดสายไฟไว้ด้วยแรงแม่เหล็ก")),
    ("ฉนวนหุ้มสายไฟในบ้านทำจากพอลิเมอร์ เพราะเหตุใด",
     "พอลิเมอร์ไม่นำไฟฟ้า ยืดหยุ่น และขึ้นรูปหุ้มสายได้ง่าย",
     ("พอลิเมอร์นำไฟฟ้าได้ดีกว่าทองแดง",
      "พอลิเมอร์แข็งและเปราะจึงป้องกันสายหักงอ",
      "พอลิเมอร์ทนความร้อนได้สูงกว่าเซรามิก",
      "พอลิเมอร์ช่วยเพิ่มกระแสไฟฟ้าในสาย",
      "พอลิเมอร์เป็นวัสดุผสมระหว่างโลหะกับแก้ว")),
)


@question_type(
    "chem.modern_material_foundation",
    display_name={"th": "จำแนกวัสดุเป็นพอลิเมอร์ เซรามิก และวัสดุผสม"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=MATERIALS_TOPIC,
)
class ModernMaterialFoundation(QuestionType):
    """One object; which kind of material it is made of."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        sample = rng.choice(SAMPLES)
        return _labelled(
            stem=f"{sample.name}จัดเป็นวัสดุประเภทใด",
            correct=sample.kind,
            wrongs=(*(k for k in MATERIAL_KINDS if k != sample.kind), "โลหะบริสุทธิ์", "โลหะผสม", "ไม้ธรรมชาติ"),
            hint="พอลิเมอร์เช่นพลาสติกและยาง เซรามิกทำจากดินหรือแร่ที่ผ่านการเผา วัสดุผสมรวมวัสดุหลายชนิดเข้าด้วยกัน",
            topic=MATERIALS_TOPIC,
        )


@question_type(
    "chem.modern_material_fluency",
    display_name={"th": "ระบุสมบัติทางกายภาพและการใช้ประโยชน์ของพอลิเมอร์ เซรามิก และวัสดุผสมจากหลักฐาน"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=MATERIALS_TOPIC,
)
class ModernMaterialFluency(QuestionType):
    """A record of one sample per kind; properties and uses of all three kinds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = [rng.choice([s for s in SAMPLES if s.kind == kind]) for kind in MATERIAL_KINDS]
        rng.shuffle(chosen)
        record = " / ".join(f"{s.name} ({s.kind}): {s.tested}" for s in chosen)
        return parts_item(
            rng, tuple(KIND_PARTS[kind] for kind in MATERIAL_KINDS),
            stem=(f"ผลการทดสอบและข้อมูลวัสดุ — {record} "
                  "จากหลักฐานและสารสนเทศนี้ ข้อใดระบุสมบัติทางกายภาพและการใช้ประโยชน์ของวัสดุแต่ละประเภทได้ถูกต้องทั้งหมด"),
            hint="จับคู่ผลการทดสอบของตัวอย่างแต่ละชิ้นกับประเภทของมัน ข้อที่ผิดจะผิดอย่างน้อยหนึ่งประเภท",
            topic=MATERIALS_TOPIC,
        )


@question_type(
    "chem.modern_material_application",
    display_name={"th": "เลือกใช้พอลิเมอร์ เซรามิก และวัสดุผสมตามสมบัติ"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=MATERIALS_TOPIC,
)
class ModernMaterialApplication(QuestionType):
    """A rice cooker, reinforced concrete poles, and a canoe hull."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, MATERIALS_SCENARIOS,
            hint="ระบุสมบัติที่งานต้องการ แล้วเลือกประเภทวัสดุที่มีสมบัตินั้น",
        ), MATERIALS_TOPIC)


# More rows: the set drew from five, so a learner met them all in a few
# tries. Each added row is a situation no other row describes, since every
# row's answer is a distractor for the others, and has five wrong readings.
MATERIALS_SCENARIOS += (
    ('เหตุใดไม้แบดมินตันและไม้เทนนิสรุ่นใหม่จึงทำจากวัสดุผสมเส้นใยคาร์บอน',
     'เส้นใยคาร์บอนเบา แข็งแรง และไม่บิดงอง่าย',
     ('เส้นใยคาร์บอนหนักที่สุดในบรรดาวัสดุ', 'เส้นใยคาร์บอนนิ่มเหมือนยาง', 'เส้นใยคาร์บอนละลายน้ำได้', 'เส้นใยคาร์บอนเป็นสนิมเร็ว', 'เส้นใยคาร์บอนนำความร้อนจนจับไม่ได้')),
    ('กระเบื้องที่ใช้ปูพื้นห้องน้ำมักทำจากเซรามิก เพราะเหตุใด',
     'เซรามิกแข็ง ไม่ดูดซับน้ำมาก ทำความสะอาดง่าย',
     ('เซรามิกยืดหยุ่นเหมือนยาง', 'เซรามิกดูดซับน้ำได้หมด', 'เซรามิกเป็นโลหะนำไฟฟ้า', 'เซรามิกละลายในน้ำสบู่', 'เซรามิกนิ่มเหมือนผ้า')),
    ('เหตุใดขวดน้ำดื่มพลาสติกจึงควรนำไปรีไซเคิลแทนการทิ้ง',
     'พอลิเมอร์ส่วนใหญ่ย่อยสลายช้ามาก การรีไซเคิลช่วยลดขยะและลดการใช้วัตถุดิบใหม่',
     ('พลาสติกย่อยสลายได้ในหนึ่งวัน', 'พลาสติกกลายเป็นปุ๋ยเองในดิน', 'พลาสติกไม่ใช้วัตถุดิบในการผลิต', 'พลาสติกละลายในฝนหมด', 'การรีไซเคิลทำให้พลาสติกมีพิษมากขึ้น')),
    ('ภาชนะแก้วเซรามิกที่ใช้อบอาหารในเตาอบทนความร้อนสูงได้ เพราะเหตุใด',
     'เซรามิกทนความร้อนสูงและไม่หลอมเหลวที่อุณหภูมิเตาอบ',
     ('เซรามิกหลอมเหลวที่อุณหภูมิห้อง', 'เซรามิกนำไฟฟ้าดีที่สุด', 'เซรามิกเป็นพลาสติกชนิดหนึ่ง', 'เซรามิกระเหยเมื่อร้อน', 'เซรามิกนิ่มลงเมื่อได้รับความร้อน')),
)
