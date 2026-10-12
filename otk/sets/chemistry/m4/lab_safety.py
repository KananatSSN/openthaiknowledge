"""ความปลอดภัยในการทำปฏิบัติการเคมี

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/1

Sets moved here from: science_wave_f40.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f40 import SUBJECT

PROVENANCE = Provenance("original")


UPPER_FOUR = {"th": "ม.4"}


TOPIC_SAFETY = "ความปลอดภัยในการทำปฏิบัติการเคมี"


HAZARDS = (
    ("สารไวไฟ", "ห้ามวางใกล้เปลวไฟหรือแหล่งความร้อน"), ("สารกัดกร่อน", "สวมถุงมือและแว่นตานิรภัย เพราะทำลายผิวหนังและดวงตา"),
    ("สารพิษ", "ห้ามสัมผัส สูดดม หรือกลืน อาจถึงแก่ชีวิต"), ("สารออกซิไดซ์", "เก็บให้ห่างจากสารไวไฟ เพราะช่วยให้ไฟลุกแรงขึ้น"),
    ("วัตถุระเบิด", "ห้ามกระแทก เสียดสี หรือให้ความร้อน"), ("สารอันตรายต่อสิ่งแวดล้อม", "ห้ามเททิ้งลงท่อหรือแหล่งน้ำ"),
    ("แก๊สภายใต้ความดัน", "ห้ามวางถังใกล้ความร้อน อาจระเบิดได้"),
)


ACCIDENTS = (
    ("กรดเข้มข้นหกรดผิวหนัง", "ล้างด้วยน้ำสะอาดปริมาณมากอย่างต่อเนื่องอย่างน้อย 15 นาที",
     ("ทาด้วยโซเดียมไฮดรอกไซด์เพื่อสะเทิน", "เช็ดด้วยผ้าแห้งแล้วล้างน้ำเพียงเล็กน้อยไม่เกินหนึ่งนาที", "ทาด้วยสารละลายเบสเข้มข้นทันที เพื่อสะเทินกรดบนผิวหนัง")),
    ("สารเคมีกระเด็นเข้าตา", "ล้างตาด้วยน้ำสะอาดที่ที่ล้างตาฉุกเฉินต่อเนื่องอย่างน้อย 15 นาที แล้วพบแพทย์",
     ("ขยี้ตาเบา ๆ เพื่อให้สารออก แล้วล้างด้วยน้ำเพียงเล็กน้อย", "หยอดยาหยอดตาทันที แล้วปิดตาพักไว้สักครู่โดยไม่ต้องล้างด้วยน้ำ", "ล้างตาด้วยสารละลายเบสเจือจางเพื่อสะเทินกรด แล้วรอดูอาการสักครู่ก่อนพบแพทย์")),
    ("ผิวหนังถูกความร้อนจากเครื่องแก้วลวก", "แช่หรือเปิดน้ำเย็นผ่านบริเวณที่ลวกจนหายแสบ",
     ("เอาน้ำแข็งถูบริเวณแผลแรง ๆ จนหายแสบ", "เจาะตุ่มพองทันทีแล้วเช็ดให้แห้ง", "ทาเนยหรือน้ำมันพืชทันทีเพื่อลดความร้อน")),
    ("กรดหกบนโต๊ะปฏิบัติการ", "โรยโซเดียมไฮโดรเจนคาร์บอเนตให้สะเทินแล้วเช็ดล้างด้วยน้ำ",
     ("เช็ดกรดด้วยกระดาษทิชชูแห้งทันที แล้วทิ้งลงถังขยะทั่วไป", "โรยโซเดียมไฮดรอกไซด์ของแข็งให้สะเทิน แล้วปล่อยให้แห้งเอง", "โรยโซเดียมไฮดรอกไซด์ของแข็ง")),
    ("ปรอทจากเทอร์มอมิเตอร์หกบนพื้น", "โรยผงกำมะถันแล้วเก็บรวบรวมใส่ภาชนะปิด",
     ("ใช้เครื่องดูดฝุ่นดูดแล้วทิ้งถุงลงถังขยะ", "เทน้ำตามลงไปแล้วกวาดลงท่อระบายน้ำ", "ใช้ไม้กวาดกวาดรวมแล้วใส่ถุง")),
    ("ตัวทำละลายไวไฟในบีกเกอร์ติดไฟ", "ปิดปากบีกเกอร์ด้วยกระจกนาฬิกาหรือผ้าชุบน้ำ หรือใช้ถังดับเพลิงชนิดที่เหมาะสม",
     ("ยกบีกเกอร์ที่ติดไฟไปเทลงในอ่างล้างที่มีน้ำ แล้วเปิดน้ำตามลงไปมาก ๆ", "เทน้ำลงไปมาก ๆ ให้ไฟดับทันที", "เป่าลมแรง ๆ ใส่เปลวไฟ แล้วใช้กระดาษพัดให้ออกซิเจนหมดจากบีกเกอร์")),
)


PRACTICES = (
    ("การเจือจางกรดเข้มข้นควรทำอย่างไร", "ค่อย ๆ เทกรดลงในน้ำพร้อมคน", ("เทน้ำลงในกรดอย่างรวดเร็ว",
                                                                             "เทกรดและน้ำพร้อมกันในบีกเกอร์เล็ก", "ต้มกรดก่อนเติมน้ำ")),
    ("การดมกลิ่นสารเคมีที่ถูกวิธีคือข้อใด", "ใช้มือโบกไอสารเข้าหาจมูกเล็กน้อย",
     ("ก้มดมที่ปากขวดโดยตรงเพียงสั้น ๆ", "ก้มดมที่ปากขวดโดยตรงอย่างเร็ว", "ก้มดมเหนือปากขวดห่างเล็กน้อย")),
    ("สารที่ระเหยง่ายและเป็นพิษควรทำปฏิบัติการที่ใด", "ในตู้ดูดควัน", ("บนโต๊ะกลางห้องที่ปิดหน้าต่าง",
                                                                     "ในห้องเก็บสารเคมี", "ใกล้เปลวไฟเพื่อให้ระเหยเร็ว")),
    ("สารเคมีที่เหลือจากการทดลองควรทำอย่างไร", "ทิ้งในภาชนะรองรับของเสียตามประเภทที่กำหนด ไม่เทคืนขวดเดิม",
     ("เทคืนขวดเดิมเพื่อประหยัด ถ้าสารยังดูใสและสะอาดอยู่", "เททิ้งลงอ่างล้างทุกชนิด", "ทิ้งรวมในถังขยะทั่วไป ถ้าสารนั้นเหลือเพียงเล็กน้อย")),
    ("ก่อนทำปฏิบัติการควรทำสิ่งใด", "อ่านฉลากและเอกสารข้อมูลความปลอดภัย (SDS) ของสารที่ใช้",
     ("ผสมสารจำนวนน้อยทุกชนิดเพื่อทดลองดูปฏิกิริยาก่อน", "ถอดแว่นตานิรภัยออกชั่วคราวเพื่ออ่านฉลากให้ชัด", "นำอาหารเข้ามารับประทานระหว่างรอ")),
)


@question_type(
    "chem.lab_safety_foundation",
    display_name={"th": "สัญลักษณ์และข้อควรระวังของสารอันตราย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SAFETY,
)
class LabSafetyFoundation(QuestionType):
    """Each hazard class carries its own precaution."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hazard, caution = rng.choice(HAZARDS)
        others = [h for h in HAZARDS if h[0] != hazard]
        if rng.random() < 0.5:
            return _labelled(stem=f"ขวดสารเคมีที่มีสัญลักษณ์\"{hazard}\" ควรระวังอย่างไร", correct=caution,
                             wrongs=tuple(h[1] for h in rng.sample(others, 3)), topic=TOPIC_SAFETY,
                             hint="อ่านสัญลักษณ์บนฉลากก่อนใช้สารทุกครั้ง")
        return _labelled(stem=f"ข้อควรระวัง \"{caution}\" ตรงกับสัญลักษณ์สารอันตรายใด", correct=hazard,
                         wrongs=tuple(h[0] for h in rng.sample(others, 3)), topic=TOPIC_SAFETY,
                         hint="อ่านสัญลักษณ์บนฉลากก่อนใช้สารทุกครั้ง")


@question_type(
    "chem.lab_safety_fluency",
    display_name={"th": "ข้อปฏิบัติที่ปลอดภัยในห้องปฏิบัติการเคมี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SAFETY,
)
class LabSafetyFluency(QuestionType):
    """Acid into water, waft don't sniff, fume hood, waste bins, read the label."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(PRACTICES)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SAFETY,
                         hint="ทำตามข้อปฏิบัติเพื่อความปลอดภัยของตนเอง ผู้อื่น และสิ่งแวดล้อม")


@question_type(
    "chem.lab_safety_application",
    display_name={"th": "การแก้ไขเมื่อเกิดอุบัติเหตุจากสารเคมี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SAFETY,
)
class LabSafetyApplication(QuestionType):
    """First aid and clean-up for common lab accidents."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        accident, right, wrongs = rng.choice(ACCIDENTS)
        # Each accident's own wrong remedies only: borrowing another row's put
        # "pop the blister" under a chemical splash in the eye.
        return _labelled(stem=f"เกิดอุบัติเหตุ: {accident} ควรแก้ไขอย่างไร", correct=right,
                         wrongs=tuple(wrongs), topic=TOPIC_SAFETY,
                         hint="สารบนร่างกายล้างด้วยน้ำปริมาณมาก ไฟจากตัวทำละลายตัดออกซิเจน อย่าใช้สารที่ทำให้เกิดอันตรายซ้ำ")
