"""การเปลี่ยนสถานะของสสาร

เคมี · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.5/1, ว 2.1 ป.5/2, ว 2.1 ป.5/3, ว 2.1 ป.5/4

Sets moved here from: chemistry, science_pilots.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.chemistry import SUBJECT, TOPIC_MATTER

PROVENANCE = Provenance("original")


CHEMISTRY = "เคมี"


MATTER = "สารในชีวิตประจำวัน"


class PhaseChangeExample(NamedTuple):
    event: str
    change: str
    direction: str


PHASE_CHANGE_EXAMPLES = (
    PhaseChangeExample("น้ำแข็งวางไว้ในห้องแล้วกลายเป็นน้ำ", "การหลอมเหลว", "ได้รับความร้อน"),
    PhaseChangeExample("นำน้ำใส่ช่องแช่แข็งแล้วกลายเป็นน้ำแข็ง", "การแข็งตัว", "สูญเสียความร้อน"),
    PhaseChangeExample("น้ำในกาต้มน้ำเดือดและกลายเป็นไอน้ำ", "การกลายเป็นไอ", "ได้รับความร้อน"),
    PhaseChangeExample("ไอน้ำสัมผัสฝาหม้อที่เย็นแล้วเกิดหยดน้ำ", "การควบแน่น", "สูญเสียความร้อน"),
    PhaseChangeExample("หยดน้ำบนจานค่อย ๆ หายไปเมื่อวางกลางแดด", "การกลายเป็นไอ", "ได้รับความร้อน"),
    PhaseChangeExample("ไอน้ำในอากาศเกิดเป็นหยดน้ำบนผิวแก้วเย็น", "การควบแน่น", "สูญเสียความร้อน"),
    PhaseChangeExample("เนยในกระทะร้อนกลายเป็นของเหลว", "การหลอมเหลว", "ได้รับความร้อน"),
    PhaseChangeExample("น้ำเทียนที่หยดลงโต๊ะแข็งตัวเป็นก้อน", "การแข็งตัว", "สูญเสียความร้อน"),
    PhaseChangeExample("ผ้าเปียกที่ตากไว้แห้งในตอนบ่าย", "การกลายเป็นไอ", "ได้รับความร้อน"),
    PhaseChangeExample("กระจกห้องน้ำเป็นฝ้าหลังอาบน้ำอุ่น", "การควบแน่น", "สูญเสียความร้อน"),
)


PHASE_CHANGE_NAMES = ("การหลอมเหลว", "การแข็งตัว", "การกลายเป็นไอ", "การควบแน่น")


# Offered only as wrong names: none of the examples is sublimation.
PHASE_CHANGE_DECOYS = ("การระเหิด", "การละลาย")


def _chem_question(
    *, stem: str, correct: str, wrongs: tuple[str, ...], hint: str,
) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=MATTER,
        hint=[text(hint)],
    )


@question_type("chem.matter_change",
               display_name={"th": "การเปลี่ยนแปลงของสาร"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_MATTER)
class MatterChange(ClassifyType):
    """แยกการเปลี่ยนแปลงทางกายภาพ (ได้สารเดิม) จากทางเคมี (ได้สารใหม่)."""

    CLASSIFY_STEM = "เหตุการณ์ต่อไปนี้เป็นการเปลี่ยนแปลงประเภทใด: “{member}”"
    PICK_STEM = "เหตุการณ์ในข้อใดจัดเป็น{category}"

    CATEGORIES = [
        Category("การเปลี่ยนแปลงทางกายภาพ (Physical Change)",
                 ("น้ำแข็งหลอมเหลวเป็นน้ำ",
                  "การละลายน้ำตาลทรายในน้ำ",
                  "การฉีกกระดาษเป็นชิ้นเล็กๆ",
                  "การทุบแก้วให้แตก",
                  "การระเหยของน้ำหอม")),
        Category("การเปลี่ยนแปลงทางเคมี (Chemical Change)",
                 ("การเกิดสนิมของเหล็ก",
                  "การเผาไหม้ของกระดาษหรือฟืน",
                  "การสุกของผลไม้ เช่น มะม่วงสุก",
                  "การทอดไข่หรือการต้มไข่",
                  "นมบูดหรืออาหารเน่าเสีย")),
    ]


@question_type("chem.phase_change",
               display_name={"th": "การเปลี่ยนสถานะของสาร"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_MATTER)
class PhaseChange(ClassifyType):
    """ระบุกระบวนการเปลี่ยนสถานะ หลอมเหลว/กลายเป็นไอ/ควบแน่น/แข็งตัว/ระเหิด/ระเหิดกลับ."""

    CLASSIFY_STEM = "เหตุการณ์ต่อไปนี้เป็นการเปลี่ยนสถานะแบบใด: “{member}”"
    PICK_STEM = "เหตุการณ์ในข้อใดเป็นตัวอย่างของกระบวนการ{category}"

    CATEGORIES = [
        Category("การหลอมเหลว (Melting)",
                 ("น้ำแข็งเปลี่ยนเป็นน้ำ", "เนยละลายเมื่อโดนความร้อน",
                  "การหลอมทองคำ")),
        Category("การกลายเป็นไอ (Vaporization)",
                 ("น้ำเดือดกลายเป็นไอน้ำ", "น้ำในแหล่งน้ำระเหยสู่อากาศ")),
        Category("การควบแน่น (Condensation)",
                 ("ไอน้ำควบแน่นเป็นหยดน้ำเกาะข้างแก้ว", "การเกิดน้ำค้างในตอนเช้า")),
        Category("การแข็งตัว (Freezing)",
                 ("น้ำในช่องแช่แข็งกลายเป็นน้ำแข็ง",
                  "เทียนไขที่เหลวแข็งตัวเมื่อเย็นลง")),
        Category("การระเหิด (Sublimation)",
                 ("ลูกเหม็นเล็กลงโดยไม่ทิ้งคราบของเหลว",
                  "น้ำแข็งแห้งเปลี่ยนเป็นแก๊สโดยตรง")),
        Category("การระเหิดกลับ (Deposition)",
                 ("ไอน้ำในอากาศเปลี่ยนเป็นหิมะ", "การเกิดแม่คะนิ้ง (น้ำค้างแข็ง)")),
    ]


@question_type(
    "chem.phase_change_foundation",
    display_name={"th": "การเปลี่ยนสถานะ: ระบุการเปลี่ยนแปลง"},
    level={"th": "ป.5"}, subject=CHEMISTRY, topic=MATTER,
)
class PhaseChangeFoundation(QuestionType):
    """Identify the named change and whether matter gains or loses heat."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        example = rng.choice(PHASE_CHANGE_EXAMPLES)
        if rng.randrange(2) == 0:
            wrongs = tuple(name for name in PHASE_CHANGE_NAMES + PHASE_CHANGE_DECOYS if name != example.change)
            return _chem_question(
                stem=f"เหตุการณ์นี้เป็นการเปลี่ยนสถานะแบบใด: {example.event}",
                correct=example.change,
                wrongs=wrongs,
                hint="ดูว่าสสารเริ่มและจบในสถานะใด แล้วจึงเรียกชื่อการเปลี่ยนสถานะ",
            )
        opposite = "สูญเสียความร้อน" if example.direction == "ได้รับความร้อน" else "ได้รับความร้อน"
        return _chem_question(
            stem=f"จากเหตุการณ์ “{example.event}” ข้อใดระบุการถ่ายโอนความร้อนได้ถูกต้อง",
            correct=f"สสาร{example.direction}",
            wrongs=(
                f"สสาร{opposite}",
                "สสารไม่ได้รับหรือสูญเสียความร้อน",
                "สสารสร้างความร้อนขึ้นเองโดยไม่มีการถ่ายโอน",
                "สสารได้รับความเย็นจากสิ่งแวดล้อมแต่ไม่สูญเสียความร้อน",
                "สสารได้รับและสูญเสียความร้อนเท่ากันพอดี",
            ),
            hint="การหลอมเหลวและการกลายเป็นไอต้องรับความร้อน ส่วนการแข็งตัวและการควบแน่นต้องสูญเสียความร้อน",
        )


@question_type(
    "chem.phase_change_fluency",
    display_name={"th": "การเปลี่ยนสถานะ: อธิบายจากหลักฐาน"},
    level={"th": "ป.5"}, subject=CHEMISTRY, topic=MATTER,
)
class PhaseChangeFluency(QuestionType):
    """Use one observation as evidence for a change of state and heat flow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(4)
        if which == 0:
            minutes = rng.randrange(3, 9)
            return _chem_question(
                stem=(f"วางน้ำแข็งมวลเท่ากันไว้สองจาน {minutes} นาที จาน ก อยู่ในห้อง "
                      "จาน ข อยู่กลางแดด พบว่าจาน ข มีน้ำเหลวมากกว่า ข้อสรุปใดเหมาะสมที่สุด"),
                correct="จาน ข ได้รับความร้อนมากกว่า จึงเกิดการหลอมเหลวมากกว่า",
                wrongs=(
                    "จาน ข สูญเสียความร้อนมากกว่า จึงเกิดการแข็งตัวมากกว่า",
                    "แสงแดดเปลี่ยนน้ำแข็งเป็นสารชนิดใหม่",
                    "ปริมาณน้ำเหลวไม่เกี่ยวข้องกับความร้อนที่ได้รับ",
                ),
                hint="ใช้ปริมาณน้ำเหลวเป็นหลักฐาน แล้วเชื่อมกับการรับความร้อนและการหลอมเหลว",
            )
        if which == 1:
            return _chem_question(
                stem=("ใส่น้ำอุณหภูมิห้องในแก้วโลหะ แล้ววางแก้วในอ่างน้ำแข็ง "
                      "ต่อมาพบน้ำบางส่วนกลายเป็นน้ำแข็ง ข้อใดอธิบายหลักฐานนี้ได้ถูกต้อง"),
                correct="น้ำถ่ายโอนความร้อนสู่อ่างน้ำแข็ง จึงแข็งตัวเป็นของแข็ง",
                wrongs=(
                    "น้ำรับความร้อนจากอ่างน้ำแข็ง จึงหลอมเหลว",
                    "น้ำกลายเป็นสารใหม่เพราะอุณหภูมิลดลง",
                    "น้ำแข็งเกิดจากอากาศเข้าไปแทนที่น้ำ",
                ),
                hint="พิจารณาทิศทางการถ่ายโอนความร้อนจากสิ่งที่อุ่นกว่าไปยังสิ่งที่เย็นกว่า",
            )
        if which == 2:
            return _chem_question(
                stem=("ต้มน้ำในภาชนะและถือฝาโลหะเย็นไว้เหนือปากภาชนะ "
                      "พบหยดน้ำใต้ฝา ข้อใดเรียงการเปลี่ยนสถานะได้ถูกต้อง"),
                correct="น้ำเหลวได้รับความร้อนกลายเป็นไอ แล้วไอสูญเสียความร้อนและควบแน่น",
                wrongs=(
                    "น้ำเหลวสูญเสียความร้อนกลายเป็นไอ แล้วไอได้รับความร้อนและแข็งตัว",
                    "น้ำเหลวหลอมเหลว แล้วไอแข็งตัวเป็นหยดน้ำ",
                    "น้ำเกิดปฏิกิริยาเคมีเป็นสารใหม่ แล้วเปลี่ยนกลับเป็นน้ำ",
                ),
                hint="ติดตามน้ำสองช่วง: จากภาชนะสู่อากาศ และจากไอเมื่อสัมผัสฝาเย็น",
            )
        start = rng.randrange(40, 71, 5)
        end = start - rng.randrange(15, 31, 5)
        return _chem_question(
            stem=(f"ปิดฝาภาชนะที่มีไอน้ำไว้ เมื่ออุณหภูมิลดจาก {start} °C เป็น {end} °C "
                  "พบหยดน้ำบนผนังภาชนะ หลักฐานสนับสนุนข้อใด"),
            correct="ไอน้ำสูญเสียความร้อนและควบแน่นเป็นน้ำเหลว",
            wrongs=(
                "ไอน้ำได้รับความร้อนและกลายเป็นไอเพิ่มขึ้น",
                "น้ำเหลวสูญเสียความร้อนและหลอมเหลว",
                "หยดน้ำเป็นสารใหม่ที่เกิดจากปฏิกิริยาเคมี",
            ),
            hint="เชื่อมอุณหภูมิที่ลดลงกับสถานะเริ่มต้นและสถานะที่สังเกตพบ",
        )


@question_type(
    "chem.phase_change_application",
    display_name={"th": "การเปลี่ยนสถานะ: วิเคราะห์การทดลอง"},
    level={"th": "ป.5"}, subject=CHEMISTRY, topic=MATTER,
)
class PhaseChangeApplication(QuestionType):
    """Interpret experimental evidence and control variables in unfamiliar contexts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(4)
        mass = rng.randrange(40, 101, 5)
        interval = rng.randrange(2, 7)
        if which == 0:
            remaining = mass - rng.randrange(5, min(26, mass), 5)
            return _chem_question(
                stem=(f"ทดลองให้ความร้อนแก่น้ำแข็ง {mass} g และบันทึกทุก {interval} นาที "
                      f"ช่วงหนึ่งอุณหภูมิคงที่ที่ 0 °C แต่มวลน้ำแข็งลดเหลือ {remaining} g "
                      "ข้อสรุปใดใช้หลักฐานได้ดีที่สุด"),
                correct="น้ำแข็งได้รับความร้อนและกำลังหลอมเหลว แม้อุณหภูมิช่วงนั้นคงที่",
                wrongs=(
                    "น้ำแข็งไม่ได้รับความร้อนเลย เพราะอุณหภูมิไม่เพิ่มขึ้นตลอดช่วงนั้น",
                    "น้ำแข็งกำลังแข็งตัวมากขึ้น เพราะมวลของแข็งลดลงระหว่างการทดลอง",
                    "น้ำแข็งเปลี่ยนเป็นสารชนิดใหม่ เพราะมวลของแข็งเปลี่ยนไปจากเดิม",
                ),
                hint="ใช้ทั้งอุณหภูมิและมวลน้ำแข็งเป็นหลักฐาน; อุณหภูมิคงที่ไม่ได้แปลว่าไม่มีการรับความร้อน",
            )
        if which == 1:
            formed = rng.randrange(5, min(31, mass), 5)
            return _chem_question(
                stem=(f"นำน้ำ {mass} g ไปทำให้เย็นและบันทึกทุก {interval} นาที "
                      f"ช่วงหนึ่งอุณหภูมิคงที่ที่ 0 °C และมีน้ำแข็งเกิดขึ้น {formed} g "
                      "คำอธิบายใดสอดคล้องกับข้อมูล"),
                correct="น้ำสูญเสียความร้อนและกำลังแข็งตัว แม้อุณหภูมิช่วงนั้นคงที่",
                wrongs=(
                    "น้ำได้รับความร้อนและกำลังหลอมเหลว แม้อุณหภูมิช่วงนั้นคงที่",
                    "น้ำไม่ได้ถ่ายโอนความร้อนเลย เพราะอุณหภูมิคงที่ตลอดช่วงนั้น",
                    "น้ำแข็งเกิดจากน้ำเปลี่ยนเป็นสารชนิดใหม่เมื่ออุณหภูมิถึง 0 °C",
                ),
                hint="พิจารณาว่าสถานะของน้ำเปลี่ยนไปทางใดขณะที่ระบบถูกทำให้เย็น",
            )
        if which == 2:
            cool_loss = rng.randrange(2, 7)
            warm_loss = cool_loss + rng.randrange(4, 11)
            return _chem_question(
                stem=(f"ใส่น้ำจานละ {mass} g ในจานเหมือนกันนาน {interval} ชั่วโมง "
                      f"จาน ก อยู่ที่ 25 °C มวลลด {cool_loss} g; จาน ข อยู่ที่ 40 °C มวลลด {warm_loss} g "
                      "ถ้าต้องการทดสอบผลของอุณหภูมิต่อการกลายเป็นไอ การจัดทดลองนี้ดีเพราะเหตุใด"),
                correct="เปลี่ยนเฉพาะอุณหภูมิ โดยควบคุมมวลเริ่มต้น ภาชนะ และเวลาให้เหมือนกัน",
                wrongs=(
                    "เปลี่ยนทั้งอุณหภูมิและชนิดภาชนะพร้อมกัน เพื่อให้เห็นผลต่างของมวลชัดขึ้น",
                    "มวลที่ลดลงต่างกันพิสูจน์ว่าน้ำในจานที่ร้อนกว่าเปลี่ยนเป็นสารชนิดใหม่",
                    "ไม่ต้องควบคุมเวลา เพราะการกลายเป็นไอไม่ขึ้นกับระยะเวลาที่วางจานไว้",
                ),
                hint="หาตัวแปรต้นหนึ่งตัว และตรวจว่าปัจจัยอื่นที่มีผลต่อการระเหยถูกควบคุมหรือไม่",
            )
        dyed = rng.choice(("สีฟ้า", "สีแดง", "สีเขียว", "สีม่วง"))
        drops = rng.randrange(3, 13)
        return _chem_question(
            stem=(f"อุ่นน้ำผสมสี{dyed}ในบีกเกอร์และวางแผ่นแก้วเย็นด้านบน "
                  f"หลัง {interval} นาทีพบหยดน้ำใส {drops} หยดใต้แผ่นแก้ว แต่สีคงอยู่ในบีกเกอร์ "
                  "แบบจำลองใดอธิบายผลได้ครบที่สุด"),
            correct="น้ำกลายเป็นไอขึ้นไป แล้วไอน้ำสูญเสียความร้อนและควบแน่นบนแผ่นแก้ว",
            wrongs=(
                "สีระเหยขึ้นไปก่อน แล้วเปลี่ยนเป็นน้ำใสเมื่อสัมผัสแผ่นแก้วที่เย็น",
                "น้ำกระโดดขึ้นไปเป็นหยดโดยตรง โดยไม่ผ่านสถานะแก๊สก่อนถึงแผ่นแก้ว",
                "น้ำและสีเกิดปฏิกิริยาเคมี แล้วได้สารใหม่เป็นหยดใสบนแผ่นแก้ว",
            ),
            hint="อธิบายทั้งการหายไปของน้ำจากบีกเกอร์และการเกิดหยดบนพื้นผิวเย็น โดยติดตามสารเดิม",
        )
