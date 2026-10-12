"""การวางแผนสังเกตดาวบนท้องฟ้า

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/19

Sets moved here from: science_wave_f86.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f86 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_PLAN = "การวางแผนสังเกตดาวบนท้องฟ้า"


PLAN_FACTS = (
    ("สถานที่ใดเหมาะแก่การสังเกตดาวด้วยตาเปล่ามากที่สุด", "ที่โล่งบนที่สูง ห่างไกลแสงไฟจากเมือง",
     ("ลานจอดรถกลางเมืองที่มีไฟสว่าง", "ใต้ต้นไม้ใหญ่ที่มีกิ่งปกคลุม", "ริมถนนที่มีรถผ่านตลอดคืน", "ในห้องที่ปิดหน้าต่างและปิดไฟ")),
    ("ช่วงใดของเดือนเหมาะแก่การสังเกตดาวจาง ๆ และทางช้างเผือก", "ช่วงข้างแรมปลายเดือนถึงข้างขึ้นต้นเดือน ใกล้คืนเดือนมืด",
     ("คืนวันเพ็ญ เพราะดวงจันทร์ช่วยให้มองเห็นดาวชัดขึ้น", "ช่วงข้างขึ้น 14 ค่ำ", "ทุกคืนเหมือนกันหมด เพราะแสงจันทร์ไม่รบกวนการดูดาว", "เฉพาะคืนที่มีเมฆมาก")),
    ("ในประเทศไทย ช่วงเดือนใดท้องฟ้ามักโปร่งเหมาะแก่การดูดาว", "ฤดูหนาว ราวเดือนพฤศจิกายนถึงกุมภาพันธ์",
     ("ฤดูฝน ราวเดือนกรกฎาคมถึงกันยายน", "ฤดูร้อน ราวเดือนมีนาคมถึงพฤษภาคม", "ช่วงที่มีพายุเข้า เพราะอากาศใสขึ้นหลังฝน", "ทุกเดือนเท่ากันหมด")),
    ("เหตุใดจึงควรใช้ไฟฉายสีแดงระหว่างดูดาว", "แสงสีแดงรบกวนการปรับตัวของตาในที่มืดน้อยที่สุด",
     ("แสงสีแดงสว่างที่สุด จึงอ่านแผนที่ดาวได้ชัดเจน", "แสงสีแดงทำให้ดาวมีสีแดง", "แสงสีแดงช่วยให้ตาปรับตัวเข้ากับที่มืดได้เร็วที่สุด", "แสงสีแดงทำให้กล้องขยายมากขึ้น")),
    ("ก่อนเริ่มดูดาวจาง ๆ ควรให้ตาปรับตัวในที่มืดนานประมาณเท่าใด", "ประมาณ 20-30 นาที",
     ("ประมาณ 5 วินาที", "ไม่จำเป็นต้องปรับตัว", "ประมาณ 3 ชั่วโมง", "ประมาณ 1 นาที")),
    ("อุปกรณ์ใดช่วยหาตำแหน่งกลุ่มดาวในคืนที่สังเกต", "แผนที่ดาวหรือแอปพลิเคชันแผนที่ดาวที่ตั้งวันเวลาและสถานที่ถูกต้อง",
     ("แผนที่ถนนของจังหวัดที่ตั้งตำแหน่งสถานที่ดูดาวไว้ถูกต้อง", "เข็มทิศเพียงอย่างเดียวโดยไม่มีแผนที่ดาว", "เข็มทิศและนาฬิกาที่ตั้งเวลาตามเวลามาตรฐานประเทศไทยไว้ถูกต้อง", "เครื่องวัดความชื้น")),
    ("การดูดวงอาทิตย์ผ่านกล้องโทรทรรศน์อย่างปลอดภัยต้องทำอย่างไร", "ใช้แผ่นกรองแสงดวงอาทิตย์ที่ได้มาตรฐานปิดหน้ากล้อง หรือฉายภาพลงฉาก",
     ("มองตรงผ่านกล้องในช่วงเช้าที่แดดอ่อน โดยสวมแว่นกันแดดสองชั้นซ้อนกัน", "ใส่แว่นกันแดดธรรมดาแล้วมองผ่านกล้อง ซึ่งช่วยกรองแสงได้เพียงพอแล้ว", "มองผ่านฟิล์มเอกซเรย์ซ้อนกันหลายแผ่น", "มองผ่านกล้องสองตาโดยไม่ใช้แผ่นกรอง")),
    ("เมื่อต้องการดูวัตถุที่กว้างและจาง เช่น กระจุกดาวลูกไก่ ควรใช้อุปกรณ์ใด", "กล้องสองตาหรือกล้องโทรทรรศน์กำลังขยายต่ำที่มีมุมมองกว้าง",
     ("กล้องโทรทรรศน์กำลังขยายสูงสุดเท่าที่ทำได้", "กล้องโทรทรรศน์กำลังขยายสูงที่มีมุมมองแคบมาก", "แว่นขยายขนาดใหญ่ที่มีกำลังขยายต่ำ", "กล้องส่องทางไกลที่ติดแผ่นกรองแสงดวงอาทิตย์")),
)


PLAN_HINT = ("วางแผนดูดาว: เลือกที่มืดห่างแสงเมือง คืนเดือนมืด ฤดูที่ฟ้าโปร่ง ตรวจพยากรณ์อากาศ ให้ตาปรับตัวในที่มืด 20-30 นาที "
             "ใช้ไฟสีแดง แผนที่ดาว กล้องสองตาหรือกล้องโทรทรรศน์ กำลังขยาย = ความยาวโฟกัสเลนส์ใกล้วัตถุ ÷ ความยาวโฟกัสเลนส์ตา "
             "กลุ่มดาวขึ้นเร็วขึ้นเดือนละประมาณ 2 ชั่วโมง")


TARGETS = (
    ("หลุมอุกกาบาตบนดวงจันทร์", "กล้องโทรทรรศน์กำลังขยายต่ำถึงปานกลาง ดูช่วงดวงจันทร์ข้างขึ้นหรือข้างแรมที่เห็นเงาชัด"),
    ("วงแหวนของดาวเสาร์", "กล้องโทรทรรศน์กำลังขยายตั้งแต่ประมาณ 50 เท่าขึ้นไป"),
    ("ฝนดาวตก", "ตาเปล่า นอนมองท้องฟ้ากว้าง ๆ หลังเที่ยงคืนในที่มืด"),
    ("ทางช้างเผือก", "ตาเปล่าในที่มืดสนิท คืนเดือนมืด"),
    ("จุดมืดบนดวงอาทิตย์", "กล้องโทรทรรศน์ที่ติดแผ่นกรองแสงดวงอาทิตย์ หรือฉายภาพลงฉาก ห้ามมองตรงเด็ดขาด"),
)


@question_type(
    "astro.stargazing_plan_foundation",
    display_name={"th": "หลักการวางแผนกิจกรรมสังเกตดาว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PLAN,
)
class StargazingPlanFoundation(QuestionType):
    """Site, Moon phase, season, red light, dark adaptation, star maps."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(PLAN_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_PLAN, hint=PLAN_HINT)


@question_type(
    "astro.stargazing_plan_fluency",
    display_name={"th": "เลือกอุปกรณ์และช่วงเวลาให้เหมาะกับเป้าหมายการสังเกต"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PLAN,
)
class StargazingPlanFluency(QuestionType):
    """Match the target to the method; pick the best night."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            target, how = rng.choice(TARGETS)
            picked = rng.sample([t for t in TARGETS if t[0] != target], 3)
            return _labelled(stem=f"ถ้าต้องการสังเกต{target} ควรวางแผนอย่างไรเหมาะสมที่สุด", correct=how, wrongs=tuple(p[1] for p in picked),
                             topic=TOPIC_PLAN, hint=PLAN_HINT)
        nights = (("ขึ้น 15 ค่ำ", False), ("ขึ้น 12 ค่ำ", False), ("ขึ้น 10 ค่ำ", False), ("แรม 14 ค่ำ", True), ("แรม 13 ค่ำ", True),
                  ("ขึ้น 1 ค่ำ", True), ("ขึ้น 14 ค่ำ", False), ("แรม 1 ค่ำ", False))
        dark = rng.choice([n for n, d in nights if d])
        bright = rng.sample([n for n, d in nights if not d], 3)
        return _labelled(stem="ชมรมดาราศาสตร์ต้องการถ่ายภาพทางช้างเผือก ควรเลือกคืนใด", correct=f"คืน{dark}",
                         wrongs=tuple(f"คืน{b}" for b in bright), topic=TOPIC_PLAN, hint=PLAN_HINT + " คืนใกล้แรม 15 ค่ำ (เดือนมืด) ฟ้ามืดที่สุด")


@question_type(
    "astro.stargazing_plan_application",
    display_name={"th": "คำนวณกำลังขยายและเวลาที่กลุ่มดาวปรากฏ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PLAN,
)
class StargazingPlanApplication(QuestionType):
    """Magnification; the useful limit 2 × aperture in mm; two hours earlier each month."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            focal = rng.choice((600, 700, 900, 1000, 1200, 1500, 2000))
            eye = rng.choice((5, 10, 20, 25))
            if rng.random() < 0.5:
                return numeric(stem=f"กล้องโทรทรรศน์มีความยาวโฟกัสเลนส์ใกล้วัตถุ {show(focal)} mm ใช้เลนส์ตาความยาวโฟกัส {eye} mm ได้กำลังขยายกี่เท่า",
                               answer=Fraction(focal, eye), wrongs=[focal * eye, focal - eye, Fraction(focal, eye) * 2], unit="เท่า", topic=TOPIC_PLAN,
                               hint="กำลังขยาย = f เลนส์ใกล้วัตถุ ÷ f เลนส์ตา")
            mag = Fraction(focal, eye)
            return numeric(stem=f"กล้องโทรทรรศน์ความยาวโฟกัส {show(focal)} mm ต้องการกำลังขยาย {show(mag)} เท่า ควรใช้เลนส์ตาความยาวโฟกัสกี่ mm",
                           answer=eye, wrongs=[eye * 2, Fraction(focal, 100), eye + 5], unit="mm", topic=TOPIC_PLAN, hint="f เลนส์ตา = f เลนส์ใกล้วัตถุ ÷ กำลังขยาย")
        if roll < 0.65:
            aperture = rng.choice((50, 60, 70, 80, 90, 100, 114, 127, 150, 200))
            return numeric(stem=f"กล้องโทรทรรศน์หน้ากล้องกว้าง {aperture} mm (กำลังขยายสูงสุดที่ใช้ได้ดี ≈ 2 เท่าของเส้นผ่านศูนย์กลางหน้ากล้องเป็น mm) "
                                f"ควรใช้กำลังขยายไม่เกินกี่เท่า", answer=2 * aperture, wrongs=[aperture, 4 * aperture, aperture + 2], unit="เท่า",
                           topic=TOPIC_PLAN, hint="กำลังขยายสูงสุด ≈ 2 × D (mm)")
        start = rng.randrange(20 * 60, 24 * 60 + 1, 30)
        months = rng.randint(1, 3)
        new = start - 120 * months
        clock = lambda m: f"{(m // 60) % 24:02d}:{m % 60:02d} น."
        const = rng.choice(("กลุ่มดาวนายพราน", "กลุ่มดาวแมงป่อง", "กลุ่มดาวสิงโต", "กลุ่มดาวหมีใหญ่", "กลุ่มดาวค้างคาว"))
        return _labelled(stem=f"คืนนี้{const}ผ่านเมริเดียนเวลาประมาณ {clock(start)} ถ้าดาวขึ้นเร็วขึ้นเดือนละประมาณ 2 ชั่วโมง อีก {months} เดือน "
                              f"กลุ่มดาวนี้จะผ่านเมริเดียนเวลาประมาณเท่าใด", correct=clock(new),
                         wrongs=(clock(start + 120 * months), clock(start - 60 * months), clock(start - 240 * months)), topic=TOPIC_PLAN,
                         hint="เวลาใหม่ = เวลาเดิม − 2 ชั่วโมง × จำนวนเดือน")
