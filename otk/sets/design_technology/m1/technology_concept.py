"""แนวคิดหลักของเทคโนโลยี

การออกแบบและเทคโนโลยี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.1/1

Sets moved here from: technology_t1.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT

PROVENANCE = Provenance("original")


CONCEPT_TOPIC = "แนวคิดหลักของเทคโนโลยี"


INPUT = "ตัวป้อน (input)"


PROCESS = "กระบวนการ (process)"


OUTPUT = "ผลผลิต (output)"


FEEDBACK = "ข้อมูลย้อนกลับ (feedback)"


ROLES = (INPUT, PROCESS, OUTPUT, FEEDBACK)


class System(NamedTuple):
    """One everyday technology read as a system. ``feedback`` is empty when the
    system has no way of checking its own output and adjusting to it."""
    name: str
    input: str
    process: str
    output: str
    feedback: str = ""

    def parts(self) -> dict[str, str]:
        found = {INPUT: self.input, PROCESS: self.process, OUTPUT: self.output}
        if self.feedback:
            found[FEEDBACK] = self.feedback
        return found


SYSTEMS = (
    System("เตารีดไฟฟ้า",
           "พลังงานไฟฟ้าและการตั้งระดับความร้อนตามชนิดผ้า",
           "ขดลวดความร้อนเปลี่ยนพลังงานไฟฟ้าเป็นความร้อน",
           "แผ่นเตารีดที่ร้อนพอจะรีดผ้าให้เรียบ",
           "เทอร์โมสแตตตรวจอุณหภูมิของแผ่นเตารีดแล้วตัดหรือต่อวงจร"),
    System("หม้อหุงข้าวไฟฟ้า",
           "ข้าวสาร น้ำ และพลังงานไฟฟ้า",
           "แผ่นความร้อนต้มน้ำจนข้าวสุก",
           "ข้าวสวยที่สุกพร้อมรับประทาน",
           "เมื่อน้ำงวดและอุณหภูมิที่ก้นหม้อสูงขึ้น ระบบจะตัดไปเป็นโหมดอุ่น"),
    System("เครื่องปรับอากาศ",
           "พลังงานไฟฟ้าและอุณหภูมิที่ผู้ใช้ตั้งไว้",
           "ระบบทำความเย็นดึงความร้อนออกจากอากาศในห้อง",
           "อากาศในห้องที่เย็นลง",
           "เซนเซอร์วัดอุณหภูมิห้องแล้วสั่งให้คอมเพรสเซอร์ทำงานหรือหยุด"),
    System("เครื่องซักผ้าอัตโนมัติ",
           "ผ้าที่สกปรก น้ำ ผงซักฟอก และพลังงานไฟฟ้า",
           "ถังหมุนทำให้ผ้า น้ำ และผงซักฟอกเสียดสีกัน",
           "ผ้าที่สะอาด",
           "เซนเซอร์วัดระดับน้ำแล้วหยุดเติมน้ำเมื่อถึงระดับที่ตั้งไว้"),
    System("พัดลมไฟฟ้า",
           "พลังงานไฟฟ้าและการกดปุ่มเลือกระดับความแรงลม",
           "มอเตอร์เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานกลเพื่อหมุนใบพัด",
           "ลมที่พัดออกจากหน้าพัดลม"),
    System("เครื่องกรองน้ำ",
           "น้ำประปาที่ไหลเข้าเครื่อง",
           "ไส้กรองดักตะกอนและสิ่งปนเปื้อนในน้ำ",
           "น้ำสะอาดสำหรับดื่ม"),
    System("จักรยาน",
           "แรงที่ผู้ขี่ถีบบันได",
           "โซ่และเฟืองส่งแรงไปหมุนล้อหลัง",
           "จักรยานที่เคลื่อนที่ไปข้างหน้า"),
    System("ไฟฉาย",
           "พลังงานไฟฟ้าจากถ่านไฟฉายและการกดสวิตช์",
           "กระแสไฟฟ้าไหลผ่านหลอดไฟจนหลอดเปล่งแสง",
           "แสงสว่างที่ส่องออกจากไฟฉาย"),
)


class Resource(NamedTuple):
    project: str
    item: str
    kind: str


PEOPLE, DATA, MATERIAL, TOOL, ENERGY, CAPITAL, TIME = (
    "คน", "ข้อมูล", "วัสดุ", "เครื่องมือและอุปกรณ์", "พลังงาน", "ทุน", "เวลา")


RESOURCE_KINDS = (PEOPLE, DATA, MATERIAL, TOOL, ENERGY, CAPITAL, TIME)


TABLE = "ทำโต๊ะไม้หนึ่งตัว"


PLANTER = "ทำกระถางรดน้ำอัตโนมัติเป็นโครงงานของห้องเรียน"


RESOURCES = (
    Resource(TABLE, "ช่างไม้ผู้ออกแบบและประกอบโต๊ะ", PEOPLE),
    Resource(TABLE, "แบบร่างและขนาดของโต๊ะ", DATA),
    Resource(TABLE, "แผ่นไม้และตะปู", MATERIAL),
    Resource(TABLE, "เลื่อยและค้อน", TOOL),
    Resource(TABLE, "ไฟฟ้าที่ใช้กับสว่านไฟฟ้า", ENERGY),
    Resource(TABLE, "เงินที่ใช้ซื้อไม้และตะปู", CAPITAL),
    Resource(TABLE, "สองวันที่ใช้ทำโต๊ะจนเสร็จ", TIME),
    Resource(PLANTER, "นักเรียนในกลุ่มที่ช่วยกันออกแบบ", PEOPLE),
    Resource(PLANTER, "ปริมาณน้ำที่ต้นไม้ต้องการในแต่ละวัน", DATA),
    Resource(PLANTER, "ขวดพลาสติกและสายยาง", MATERIAL),
    Resource(PLANTER, "กรรไกรและปืนกาว", TOOL),
    Resource(PLANTER, "ถ่านไฟฉายที่จ่ายไฟให้ปั๊มน้ำขนาดเล็ก", ENERGY),
    Resource(PLANTER, "งบประมาณ 200 บาทที่โรงเรียนให้", CAPITAL),
    Resource(PLANTER, "คาบเรียนสามสัปดาห์ที่ใช้ทำโครงงาน", TIME),
)


SYSTEM_HINT = ("ตัวป้อนคือสิ่งที่ใส่เข้าไป กระบวนการคือสิ่งที่ระบบทำ ผลผลิตคือสิ่งที่ได้ออกมา "
               "ส่วนข้อมูลย้อนกลับคือการตรวจผลผลิตแล้วนำไปปรับการทำงานของระบบ")


NEED = "ปัญหาหรือความต้องการของมนุษย์"


SCIENCE = "ความก้าวหน้าของความรู้ทางวิทยาศาสตร์"


ECONOMY = "การเปลี่ยนแปลงทางเศรษฐกิจ"


ENVIRONMENT = "ปัญหาสิ่งแวดล้อม"


FACTORS = (NEED, SCIENCE, ECONOMY, ENVIRONMENT)


#: (the change, what drove it, the factor). Each reason is stated in the stem,
#: so the question is naming the kind of factor, not guessing history.
CHANGES = (
    ("ร้านค้าหันมาใช้ถุงผ้าและภาชนะที่ย่อยสลายได้แทนถุงพลาสติก",
     "ขยะพลาสติกตกค้างในทะเลและเป็นอันตรายต่อสัตว์ทะเล", ENVIRONMENT),
    ("หน้ากากผ้าที่ซักแล้วใช้ซ้ำได้ได้รับความนิยมมากขึ้น",
     "หน้ากากแบบใช้ครั้งเดียวกลายเป็นขยะจำนวนมาก", ENVIRONMENT),
    ("รถยนต์ไฟฟ้าได้รับความนิยมมากขึ้น",
     "ผู้คนต้องการลดมลพิษทางอากาศจากไอเสียรถยนต์", ENVIRONMENT),
    ("หลอด LED ให้แสงสีขาวได้และเข้ามาแทนหลอดไส้",
     "นักวิทยาศาสตร์ค้นพบวิธีสร้างไดโอดเปล่งแสงสีฟ้าที่สว่างพอ", SCIENCE),
    ("โทรศัพท์มือถือบางและเบาลงแต่ใช้งานได้นานขึ้น",
     "มีการพัฒนาวัสดุทำแบตเตอรี่ที่เก็บพลังงานได้มากขึ้นในขนาดเล็กลง", SCIENCE),
    ("ชุดตรวจโรคแบบรวดเร็วที่ใช้ได้เองที่บ้านถูกพัฒนาขึ้น",
     "ความรู้เรื่องแอนติเจนและแอนติบอดีทางชีววิทยาก้าวหน้าขึ้น", SCIENCE),
    ("ร้านค้าจำนวนมากรับชำระเงินด้วยคิวอาร์โค้ด",
     "ค่าธรรมเนียมต่ำและช่วยลดต้นทุนการจัดการเงินสด", ECONOMY),
    ("บ้านเรือนติดตั้งแผงเซลล์สุริยะบนหลังคามากขึ้น",
     "ราคาแผงเซลล์สุริยะลดลงมากจนคุ้มค่ากว่าการจ่ายค่าไฟฟ้า", ECONOMY),
    ("โรงงานหลายแห่งเปลี่ยนมาใช้หุ่นยนต์ในสายการผลิต",
     "ค่าแรงสูงขึ้นจนการจ้างคนมีต้นทุนมากกว่าการใช้หุ่นยนต์", ECONOMY),
    ("ร่มพับได้ขนาดเล็กถูกพัฒนาขึ้น",
     "ผู้คนต้องการพกร่มใส่กระเป๋าได้สะดวก", NEED),
    ("เครื่องล้างจานถูกพัฒนาขึ้นสำหรับใช้ในบ้าน",
     "ผู้คนต้องการประหยัดเวลาในการทำงานบ้าน", NEED),
    ("โทรศัพท์มือถือมีกล้องถ่ายภาพคุณภาพสูง",
     "ผู้ใช้อยากถ่ายภาพและส่งให้ผู้อื่นทันทีโดยไม่ต้องพกกล้องแยก", NEED),
)


@question_type(
    "tech.technology_concept_foundation",
    display_name={"th": "ระบุองค์ประกอบของระบบทางเทคโนโลยีและทรัพยากร"},
    level={"th": "ม.1"}, subject=SUBJECT, topic=CONCEPT_TOPIC,
)
class TechnologyConceptFoundation(QuestionType):
    """Pick the part that plays a named role, or name the kind of a resource."""

    def build(self, rng: Random, **params):
        if rng.random() < 0.5:
            system = rng.choice(SYSTEMS)
            parts = system.parts()
            role = rng.choice(list(parts))
            wrongs = [text for other, text in parts.items() if other != role]
            # A system without feedback has only two other parts, so the third
            # wrong answer is the same role taken from another system.
            if len(wrongs) < 3:
                other = rng.choice([s for s in SYSTEMS if s.name != system.name])
                wrongs.append(other.parts()[role])
            return _labelled(
                stem=f"เมื่อมอง{system.name}เป็นระบบทางเทคโนโลยี ข้อใดคือ{role}",
                correct=parts[role], wrongs=tuple(wrongs),
                hint=SYSTEM_HINT, topic=CONCEPT_TOPIC,
            )
        item = rng.choice(RESOURCES)
        wrongs = [kind for kind in RESOURCE_KINDS if kind != item.kind]
        return _labelled(
            stem=f"ในการ{item.project} “{item.item}” จัดเป็นทรัพยากรทางเทคโนโลยีประเภทใด",
            correct=item.kind, wrongs=tuple(wrongs),
            hint=("ทรัพยากรทางเทคโนโลยีมีเจ็ดประเภท ได้แก่ คน ข้อมูล วัสดุ "
                  "เครื่องมือและอุปกรณ์ พลังงาน ทุน และเวลา"),
            topic=CONCEPT_TOPIC,
        )


@question_type(
    "tech.technology_concept_fluency",
    display_name={"th": "จำแนกหน้าที่ขององค์ประกอบและข้อมูลย้อนกลับในระบบ"},
    level={"th": "ม.1"}, subject=SUBJECT, topic=CONCEPT_TOPIC,
)
class TechnologyConceptFluency(QuestionType):
    """Name the role of a given part, or tell which system checks its own output."""

    def build(self, rng: Random, **params):
        if rng.random() < 0.5:
            system = rng.choice(SYSTEMS)
            role, part = rng.choice(list(system.parts().items()))
            return _labelled(
                stem=(f"เมื่อมอง{system.name}เป็นระบบทางเทคโนโลยี "
                      f"“{part}” เป็นองค์ประกอบใดของระบบ"),
                correct=role, wrongs=tuple(r for r in ROLES if r != role),
                hint=SYSTEM_HINT, topic=CONCEPT_TOPIC,
            )
        with_feedback = [s.name for s in SYSTEMS if s.feedback]
        without = [s.name for s in SYSTEMS if not s.feedback]
        if rng.random() < 0.5:
            stem = "ระบบใดต่อไปนี้มีข้อมูลย้อนกลับ ที่ตรวจผลการทำงานแล้วปรับการทำงานของตัวเองได้"
            correct, pool = rng.choice(with_feedback), without
        else:
            stem = "ระบบใดต่อไปนี้ไม่มีข้อมูลย้อนกลับ ผลผลิตจึงไม่ได้ถูกนำไปปรับการทำงานของระบบ"
            correct, pool = rng.choice(without), with_feedback
        return _labelled(
            stem=stem, correct=correct, wrongs=tuple(pool),
            hint=("ถามว่าระบบนั้นมีส่วนที่ตรวจผลผลิต เช่น อุณหภูมิหรือระดับน้ำ "
                  "แล้วสั่งให้ระบบเปลี่ยนการทำงานเองหรือไม่"),
            topic=CONCEPT_TOPIC,
        )


@question_type(
    "tech.technology_concept_application",
    display_name={"th": "วิเคราะห์ปัจจัยที่ทำให้เทคโนโลยีเปลี่ยนแปลง"},
    level={"th": "ม.1"}, subject=SUBJECT, topic=CONCEPT_TOPIC,
)
class TechnologyConceptApplication(QuestionType):
    """Name the factor behind a change, or find the change a factor drove."""

    def build(self, rng: Random, **params):
        hint = ("อ่านเหตุผลที่ทำให้เทคโนโลยีเปลี่ยน แล้วถามว่าเกิดจากความต้องการของผู้ใช้ "
                "ความรู้ใหม่ทางวิทยาศาสตร์ เรื่องเงินและต้นทุน หรือปัญหาสิ่งแวดล้อม")
        if rng.random() < 0.5:
            change, reason, factor = rng.choice(CHANGES)
            return _labelled(
                stem=(f"“{change}” เพราะ{reason} "
                      f"การเปลี่ยนแปลงนี้เกิดจากปัจจัยใดเป็นหลัก"),
                correct=factor, wrongs=tuple(f for f in FACTORS if f != factor),
                hint=hint, topic=CONCEPT_TOPIC,
            )
        factor = rng.choice(FACTORS)
        change, reason, _ = rng.choice([c for c in CHANGES if c[2] == factor])
        others = [c for c in CHANGES if c[2] != factor]
        return _labelled(
            stem=f"ข้อใดเป็นการเปลี่ยนแปลงของเทคโนโลยีที่เกิดจาก{factor}เป็นหลัก",
            correct=f"{change} เพราะ{reason}",
            wrongs=tuple(f"{c} เพราะ{r}" for c, r, _ in rng.sample(others, 3)),
            hint=hint, topic=CONCEPT_TOPIC,
        )
