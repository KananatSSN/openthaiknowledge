"""ทักษะกระบวนการทางวิทยาศาสตร์ ม.3

วิทยาศาสตร์ทั่วไป · ม.3 · เสริมทักษะ
Indicators: —

Filed like the ม.1 unit (บทนำ, no ตัวชี้วัด). ม.3 closes lower secondary with
the skills that judge an investigation as well as run it: what a model shows
and where it stops, why trials are repeated and what to do with an odd result,
and whether a conclusion says only what the data can carry.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_g4 import SUBJECT

PROVENANCE = Provenance("original")


SECONDARY_THREE = {"th": "ม.3"}


PROCESS_SKILL_TOPIC = "ทักษะกระบวนการทางวิทยาศาสตร์"


class Model(NamedTuple):
    """A classroom model, what it stands for, one real limit, and three claims that are not limits."""
    model: str
    stands_for: str
    limit: str
    not_limits: tuple[str, str, str]


MODELS = (
    Model("หยิบลูกปัดจากถุงสองใบ ใบละหนึ่งเม็ดโดยไม่มอง แต่ละถุงมีลูกปัดสีแดงและสีขาวอย่างละเท่ากัน",
          "การถ่ายทอดยีนจากพ่อและแม่ไปสู่ลูกและโอกาสเกิดจีโนไทป์แบบต่าง ๆ",
          "แสดงได้เพียงลักษณะที่ควบคุมด้วยยีนคู่เดียว ไม่แสดงลักษณะที่มียีนหลายคู่ร่วมกันควบคุม",
          ("ลูกปัดมีขนาดใหญ่กว่ายีนจริง จึงใช้อธิบายการถ่ายทอดยีนไม่ได้เลย",
           "ผลการหยิบลูกปัดจะเหมือนกันทุกครั้ง จึงไม่ต้องหยิบหลายครั้ง",
           "แบบจำลองนี้แสดงทุกอย่างของการถ่ายทอดลักษณะได้ตรงกับความจริงทุกประการ")),
    Model("ถือลูกโลกที่แกนเอียงเดินรอบโคมไฟกลางห้อง โดยให้แกนชี้ไปทางเดิมตลอด",
          "การเกิดฤดูกาลจากแกนโลกเอียงขณะโลกโคจรรอบดวงอาทิตย์",
          "ขนาดของโคมไฟกับลูกโลกและระยะห่างระหว่างกันไม่เป็นไปตามสัดส่วนจริง",
          ("โคมไฟให้แสงคนละสีกับดวงอาทิตย์ จึงอธิบายเรื่องฤดูกาลไม่ได้เลย",
           "แบบจำลองนี้พิสูจน์ว่าฤดูกาลเกิดจากระยะห่างระหว่างโลกกับดวงอาทิตย์",
           "แบบจำลองนี้แสดงขนาดและระยะทางของโลกกับดวงอาทิตย์ได้ตรงตามจริงทุกประการ")),
    Model("น้ำไหลวนในท่อปิดโดยมีปั๊มดันน้ำ และมีกังหันเล็ก ๆ หมุนอยู่กลางทาง",
          "กระแสไฟฟ้าในวงจรที่มีแหล่งกำเนิดไฟฟ้าและเครื่องใช้ไฟฟ้า",
          "ท่อที่รั่วทำให้น้ำไหลออกมาได้ แต่สายไฟที่ขาดไม่ได้ทำให้อิเล็กตรอนไหลออกมาแบบเดียวกัน",
          ("น้ำมองเห็นได้แต่ไฟฟ้ามองไม่เห็น จึงเปรียบเทียบกันไม่ได้เลย",
           "แบบจำลองนี้แสดงว่ากระแสไฟฟ้าถูกใช้หมดไปที่เครื่องใช้ไฟฟ้า",
           "แบบจำลองนี้อธิบายพฤติกรรมของไฟฟ้าได้ตรงกับความจริงทุกกรณี")),
    Model("เชื่อมบัตรภาพพืช กระต่าย งู และเหยี่ยวด้วยเชือกตามลูกศรว่าใครถูกกินโดยใคร",
          "การถ่ายทอดพลังงานผ่านโซ่อาหารในระบบนิเวศ",
          "ไม่แสดงว่าพลังงานลดลงเท่าใดเมื่อถ่ายทอดไปยังผู้บริโภคลำดับถัดไป",
          ("บัตรภาพมีสีไม่เหมือนสัตว์จริง จึงใช้อธิบายโซ่อาหารไม่ได้",
           "แบบจำลองนี้แสดงว่าพลังงานเพิ่มขึ้นเมื่อส่งต่อไปยังผู้บริโภคลำดับถัดไป",
           "แบบจำลองนี้แสดงจำนวนสิ่งมีชีวิตทุกชนิดในระบบนิเวศได้ครบถ้วน")),
    Model("ต่อลูกบอลพลาสติกสีต่าง ๆ ด้วยแท่งไม้ แทนอะตอมที่ยึดกันในโมเลกุลของน้ำ",
          "การจัดเรียงอะตอมที่สร้างพันธะกันในโมเลกุล",
          "อะตอมจริงไม่มีสี และพันธะเคมีไม่ได้เป็นแท่งแข็งเหมือนแท่งไม้",
          ("ลูกบอลพลาสติกมีมวลมากกว่าอะตอม จึงแสดงการจัดเรียงอะตอมไม่ได้เลย",
           "แบบจำลองนี้แสดงว่าโมเลกุลของน้ำมีอะตอมสามชนิด",
           "แบบจำลองนี้แสดงขนาดของอะตอมและระยะระหว่างอะตอมได้ตรงตามจริงทุกประการ")),
    Model("บิดบันไดที่ทำจากหลอดกาแฟให้เป็นเกลียว โดยขั้นบันไดแต่ละขั้นเป็นหลอดสองสีต่อกัน",
          "โครงสร้างของดีเอ็นเอที่เป็นเกลียวคู่และมีเบสจับคู่กัน",
          "ไม่แสดงจำนวนคู่เบสที่มีมหาศาลในดีเอ็นเอจริงและขนาดที่เล็กมาก",
          ("หลอดกาแฟทำจากพลาสติก จึงอธิบายโครงสร้างดีเอ็นเอไม่ได้เลย",
           "แบบจำลองนี้แสดงว่าดีเอ็นเอเป็นสายเดี่ยวที่ไม่จับคู่กัน",
           "แบบจำลองนี้แสดงลำดับเบสทั้งหมดของมนุษย์ได้ครบถ้วนทุกคู่")),
)


@question_type(
    "sci.process_skill_m3_foundation",
    display_name={"th": "แบบจำลองแทนสิ่งใดและมีข้อจำกัดอย่างไร"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillM3Foundation(QuestionType):
    """What a classroom model stands for, or the one real limit among claims that are not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(MODELS)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"แบบจำลองต่อไปนี้ “{item.model}” ใช้อธิบายสิ่งใด",
                correct=item.stands_for,
                wrongs=tuple(other.stands_for for other in MODELS if other is not item),
                hint="จับคู่แต่ละส่วนของแบบจำลองกับสิ่งที่มันแทน แล้วดูว่าทั้งหมดรวมกันอธิบายเรื่องใด",
                topic=PROCESS_SKILL_TOPIC,
            )
        return _labelled(
            stem=(f"แบบจำลอง “{item.model}” ใช้อธิบาย{item.stands_for} "
                  "ข้อใดเป็นข้อจำกัดของแบบจำลองนี้ที่ถูกต้อง"),
            correct=item.limit,
            wrongs=item.not_limits,
            hint=("ข้อจำกัดคือสิ่งที่แบบจำลองแสดงไม่ได้หรือแสดงต่างจากของจริง "
                  "แต่แบบจำลองยังใช้อธิบายเรื่องหลักได้ ไม่ใช่ใช้ไม่ได้เลย"),
            topic=PROCESS_SKILL_TOPIC,
        )


class Repeat(NamedTuple):
    """A measurement taken four times; ``spread`` is how far a sound trial strays."""
    what: str
    unit: str
    centre: tuple[int, int]
    spread: int
    off_by: tuple[int, int]


REPEATS = (
    Repeat("ระยะที่รถของเล่นเคลื่อนที่ได้หลังลงจากพื้นเอียง", "เซนติเมตร", (80, 120), 2, (25, 40)),
    Repeat("เวลาที่เม็ดฟู่ละลายหมดในน้ำ", "วินาที", (40, 70), 2, (15, 25)),
    Repeat("ความสูงที่ลูกบอลกระดอนขึ้น", "เซนติเมตร", (50, 70), 2, (15, 25)),
    Repeat("จำนวนคลิปที่แม่เหล็กไฟฟ้าดูดได้", "ตัว", (12, 20), 1, (6, 9)),
)


def repeated_trials(rng: Random, repeat: Repeat) -> tuple[list[int], int]:
    """Four trials, one of them odd; the three sound ones average to a whole number."""
    centre = rng.randint(*repeat.centre)
    while True:
        sound = [centre + rng.randint(-repeat.spread, repeat.spread) for _ in range(3)]
        if sum(sound) % 3 == 0 and len(set(sound)) > 1:
            break
    odd = centre + rng.choice((-1, 1)) * rng.randint(*repeat.off_by)
    position = rng.randrange(4)
    trials = sound[:position] + [odd] + sound[position:]
    return trials, position


@question_type(
    "sci.process_skill_m3_fluency",
    display_name={"th": "ทดลองซ้ำ หาค่าที่ผิดปกติและค่าเฉลี่ย"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillM3Fluency(QuestionType):
    """Four repeats with one odd result: find it, or average the sound ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        repeat = rng.choice(REPEATS)
        trials, position = repeated_trials(rng, repeat)
        table = " / ".join(f"ครั้งที่ {i + 1}: {v} {repeat.unit}" for i, v in enumerate(trials))
        stem = f"นักเรียนวัด{repeat.what}ซ้ำ 4 ครั้ง ได้ผลดังนี้ {table} "
        if rng.random() < 0.5:
            return _labelled(
                stem=stem + "ผลของครั้งใดน่าจะผิดปกติและควรตรวจสอบหรือทำซ้ำใหม่",
                correct=f"ครั้งที่ {position + 1}",
                wrongs=tuple(f"ครั้งที่ {i + 1}" for i in range(4) if i != position),
                hint="ผลที่ดีของการทดลองซ้ำควรใกล้เคียงกัน หาค่าที่ห่างจากค่าอื่นมากที่สุด",
                topic=PROCESS_SKILL_TOPIC,
            )
        sound = [v for i, v in enumerate(trials) if i != position]
        return numeric(
            stem=stem + "ถ้าตัดผลที่ผิดปกติออก ค่าเฉลี่ยของผลที่เหลือเป็นเท่าใด",
            answer=sum(sound) // 3,
            # Averaging all four, and taking the odd result itself.
            wrongs=(Fraction(sum(trials), 4), trials[position]),
            unit=repeat.unit,
            hint="หาค่าที่ห่างจากค่าอื่นมากที่สุดแล้วตัดออก จากนั้นรวมค่าที่เหลือแล้วหารด้วยจำนวนครั้งที่เหลือ",
            topic=PROCESS_SKILL_TOPIC,
        )


SUPPORTED = "ข้อสรุปนี้สอดคล้องกับข้อมูล เพราะเป็นการทดสอบที่ยุติธรรมและทำซ้ำหลายครั้ง"
TOO_FEW = "ยังสรุปไม่ได้ เพราะทดลองครั้งเดียวหรือใช้ตัวอย่างน้อยเกินไป"
UNCONTROLLED = "ยังสรุปไม่ได้ เพราะมีตัวแปรอื่นที่แตกต่างกันโดยไม่ได้ควบคุม"
BEYOND = "สรุปเกินกว่าข้อมูล เพราะข้อมูลที่ได้ไม่ครอบคลุมสิ่งที่นำไปสรุป"
VERDICTS = (SUPPORTED, TOO_FEW, UNCONTROLLED, BEYOND)


#: (an investigation and its conclusion, the one verdict that fits). Each case
#: has exactly one fault, or none, so only one verdict is defensible.
CASES = (
    ("นักเรียนปลูกต้นถั่วในดินร่วน 10 ต้นและในดินทราย 10 ต้น ให้น้ำและแสงเท่ากัน ทำซ้ำ 3 รอบ "
     "พบว่าต้นในดินร่วนสูงกว่าทุกรอบ จึงสรุปว่าต้นถั่วในการทดลองนี้เติบโตในดินร่วนได้ดีกว่าดินทราย",
     SUPPORTED),
    ("นักเรียนจับเวลาน้ำตาลละลายในน้ำ 30 และ 60 องศาเซลเซียส ใช้น้ำตาลและน้ำปริมาณเท่ากัน ทำซ้ำชุดละ 5 ครั้ง "
     "พบว่าน้ำ 60 องศาเซลเซียสใช้เวลาน้อยกว่าทุกครั้ง จึงสรุปว่าในช่วงนี้น้ำตาลละลายเร็วขึ้นเมื่อน้ำร้อนขึ้น",
     SUPPORTED),
    ("นักเรียนโยนเหรียญเพียง 3 ครั้งได้หัวทั้ง 3 ครั้ง จึงสรุปว่าเหรียญนี้ออกหัวได้บ่อยกว่าออกก้อย",
     TOO_FEW),
    ("นักเรียนปลูกถั่วกระถางละต้นเพียง 2 กระถาง ใส่ปุ๋ยกระถางหนึ่ง พบว่าต้นที่ใส่ปุ๋ยสูงกว่า 1 เซนติเมตร "
     "จึงสรุปว่าปุ๋ยชนิดนี้ทำให้ต้นถั่วสูงขึ้น",
     TOO_FEW),
    ("นักเรียนเทียบผงซักฟอกสองยี่ห้อ โดยซักยี่ห้อ ก ด้วยน้ำอุ่นและซักยี่ห้อ ข ด้วยน้ำเย็น "
     "พบว่ายี่ห้อ ก ขจัดคราบได้ดีกว่า จึงสรุปว่ายี่ห้อ ก ขจัดคราบได้ดีกว่ายี่ห้อ ข",
     UNCONTROLLED),
    ("นักเรียนห่อน้ำแข็งก้อนหนึ่งด้วยผ้าฝ้ายวางในห้องปรับอากาศ อีกก้อนห่อผ้าขนสัตว์วางกลางแดด "
     "พบว่าก้อนที่ห่อผ้าขนสัตว์ละลายเร็วกว่า จึงสรุปว่าผ้าขนสัตว์ทำให้น้ำแข็งละลายเร็วขึ้น",
     UNCONTROLLED),
    ("นักเรียนทดลองละลายน้ำตาลในน้ำ 20 ถึง 60 องศาเซลเซียส ทำซ้ำหลายครั้ง พบว่าน้ำตาลละลายเร็วขึ้นเมื่อน้ำร้อนขึ้น "
     "จึงสรุปว่าสารทุกชนิดละลายน้ำได้เร็วขึ้นเมื่อน้ำร้อนขึ้น",
     BEYOND),
    ("นักเรียนแขวนมวล 100 ถึง 400 กรัมกับสปริงตัวหนึ่ง ทำซ้ำหลายครั้ง พบว่าสปริงยืดเป็นสัดส่วนกับมวล "
     "จึงสรุปว่าสปริงนี้จะยืดเป็นสัดส่วนกับมวลเสมอ แม้แขวนมวลถึง 50 กิโลกรัม",
     BEYOND),
)


@question_type(
    "sci.process_skill_m3_application",
    display_name={"th": "ประเมินว่าข้อสรุปสอดคล้องกับข้อมูลหรือไม่"},
    level=SECONDARY_THREE, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillM3Application(QuestionType):
    """Judge one investigation's conclusion; the four verdicts are always the choices."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case, verdict = rng.choice(CASES)
        return _labelled(
            stem=f"{case} ข้อใดประเมินข้อสรุปนี้ได้เหมาะสมที่สุด",
            correct=verdict,
            wrongs=tuple(v for v in VERDICTS if v != verdict),
            hint=("ตรวจทีละเรื่อง: ทดสอบยุติธรรมหรือไม่ ทำซ้ำพอหรือไม่ "
                  "และข้อสรุปพูดเกินกว่าสิ่งที่ทดลองจริงหรือไม่"),
            topic=PROCESS_SKILL_TOPIC,
        )
