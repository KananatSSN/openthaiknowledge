"""การจัดความสว่างของแสงให้เหมาะสมกับกิจกรรม

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/21

Sets moved here from: science_wave_d34.
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
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d32 import THIRD_SECONDARY

PROVENANCE = Provenance("original")


BRIGHTNESS_ARRANGEMENT_TOPIC = "การจัดความสว่างของแสงให้เหมาะสมกับกิจกรรม"


class LightProblem(NamedTuple):
    case: str
    method: str


LIGHT_ARRANGEMENT_PROBLEMS = (
    LightProblem("อ่านหนังสือใต้แสงไฟที่สลัวเกินไปในตอนกลางคืน",
                 "เพิ่มความสว่างของไฟอ่านหนังสือให้เพียงพอ หรือย้ายไปอ่านในบริเวณที่มีแสงสว่างเหมาะสม"),
    LightProblem("ทำงานหน้าจอคอมพิวเตอร์ในห้องที่มีแสงจ้าสะท้อนจอจนแสบตา",
                 "ปรับความสว่างของจอให้เหมาะสมกับแสงในห้อง หรือลดแสงจ้าที่สะท้อนหน้าจอ"),
    LightProblem("นักเรียนวาดภาพในห้องที่มีแสงไม่สม่ำเสมอ มืดบางมุมสว่างบางมุม",
                 "จัดโต๊ะทำงานให้อยู่ในบริเวณที่มีแสงสว่างสม่ำเสมอเพียงพอทั่วพื้นที่ทำงาน"),
    LightProblem("ห้องนอนเปิดไฟสว่างจ้าทั้งคืนขณะนอนหลับ",
                 "ปิดไฟหรือลดความสว่างลงให้เหมาะสมกับการนอนหลับ เพื่อไม่รบกวนการพักผ่อนของดวงตา"),
    LightProblem("นักเรียนถนัดขวาเขียนหนังสือโดยวางโคมไฟไว้ทางขวามือ ทำให้เงามือบังตัวหนังสือ",
                 "ย้ายโคมไฟไปไว้ทางซ้ายมือ เพื่อไม่ให้เงาของมือที่เขียนบังพื้นที่เขียน"),
    LightProblem("เล่นโทรศัพท์มือถือในห้องมืดสนิทก่อนนอนจนแสบตา",
                 "เปิดไฟในห้องให้สว่างพอประมาณและลดความสว่างของหน้าจอ เพื่อลดความต่างระหว่างจอกับห้อง"),
    LightProblem("โรงงานเย็บผ้ามีคนงานเย็บตะเข็บละเอียดใต้หลอดไฟดวงเดียวที่อยู่สูงมาก",
                 "ติดโคมไฟเฉพาะจุดที่ส่องลงบนงานเย็บ เพื่อให้ความสว่างเพียงพอกับงานละเอียด"),
    LightProblem("ทางเดินในหอพักมืดมากตอนกลางคืนจนผู้พักสะดุดขั้นบันได",
                 "ติดไฟส่องทางเดินและบันไดให้สว่างพอมองเห็นขั้นบันไดชัดเจน"),
    LightProblem("ห้องเรียนเปิดไฟทุกดวงตอนกลางวัน ทั้งที่มีแสงแดดส่องเข้ามาเพียงพอแล้ว",
                 "ปิดไฟแถวที่อยู่ติดหน้าต่างซึ่งได้แสงธรรมชาติเพียงพอ เพื่อประหยัดพลังงานโดยยังสว่างพอ"),
    LightProblem("กระดานไวท์บอร์ดสะท้อนแสงไฟจ้าจนนักเรียนแถวข้างมองไม่เห็นตัวหนังสือ",
                 "ปรับตำแหน่งหรือมุมของหลอดไฟ หรือใช้โคมที่มีแผ่นกระจายแสง เพื่อลดแสงสะท้อนบนกระดาน"),
    LightProblem("ผู้สูงอายุอ่านฉลากยาในห้องที่เปิดไฟสลัวเพียงดวงเดียว",
                 "เพิ่มไฟส่องเฉพาะจุดบริเวณที่อ่านฉลาก เพื่อให้มองเห็นตัวหนังสือเล็กได้ชัด"),
    LightProblem("นักเรียนดูโทรทัศน์ในห้องที่มีหน้าต่างอยู่ด้านหลังจอ แสงจ้าจากหน้าต่างทำให้มองจอลำบาก",
                 "ปิดม่านหน้าต่างหรือย้ายจอไม่ให้หันเข้าหาแสงจ้าจากหน้าต่าง"),
)


BRIGHTNESS_HINT = "งานละเอียดต้องการแสงมาก งานพักผ่อนต้องการแสงน้อย และแสงควรสม่ำเสมอโดยไม่จ้าหรือสะท้อนเข้าตา"


# From the most to the least light an activity usually needs.
ACTIVITY_NEEDS = ("การผ่าตัดในห้องผ่าตัด", "การประกอบวงจรขนาดเล็ก", "การปักผ้าลายละเอียด",
                  "การอ่านหนังสือเรียน", "การเดินในทางเดินอาคาร", "การนอนหลับในห้องนอน")


BRIGHTNESS_FACTS = (
    ("แสงจ้าที่สะท้อนจากพื้นผิวมันเข้าตาเรียกว่าอะไร และมีผลอย่างไร", "แสงบาดตา ทำให้มองเห็นไม่ชัดและล้าตา",
     ("แสงสลัว ทำให้มองชัดขึ้น", "แสงธรรมชาติ ไม่มีผลต่อดวงตา", "แสงสม่ำเสมอ ช่วยพักสายตา", "แสงเงา ทำให้ตาแข็งแรงขึ้น",
      "แสงอัลตราไวโอเลต ทำให้มองเห็นสีดีขึ้น")),
    ("การอ่านหนังสือในที่สลัวเป็นเวลานานมีผลอย่างไร", "ตาต้องเพ่งมาก ทำให้ปวดตาและล้าตา",
     ("ทำให้สายตาดีขึ้นเพราะได้ฝึกเพ่ง", "ไม่มีผลใด ๆ", "ช่วยให้อ่านเร็วขึ้นเพราะตาต้องตั้งใจ", "ทำให้มองเห็นสีชัดขึ้น", "ทำให้ตาปรับจนไม่ต้องใช้แว่น")),
    ("เหตุใดจึงควรใช้แสงธรรมชาติในห้องเรียนเมื่อเหมาะสม", "ให้แสงสว่างเพียงพอและช่วยประหยัดพลังงานไฟฟ้า",
     ("แสงธรรมชาติไม่มีความสว่าง", "แสงธรรมชาติทำให้ห้องมืดลง", "เพื่อเพิ่มการใช้ไฟฟ้า", "แสงธรรมชาติไม่เปลี่ยนตามเวลา",
      "เพื่อให้เกิดแสงบาดตามากขึ้น")),
    ("การจัดแสงที่ดีสำหรับการทำงานควรมีลักษณะใด", "สว่างเพียงพอกับงาน สม่ำเสมอ และไม่จ้าเข้าตา",
     ("สว่างจ้าที่สุดเท่าที่ทำได้เสมอ", "สลัวเพื่อถนอมสายตา", "มีแสงสะท้อนเข้าตามาก ๆ", "สว่างเฉพาะมุมห้อง",
      "เปิดปิดสลับไปมาตลอด")),
)


BRIGHTNESS_ARRANGEMENT_SCENARIOS = (
    ("ห้องเรียนแห่งหนึ่งมีแสงแดดจ้าส่องเข้ามาโดยตรงบริเวณที่นั่งบางแถวในช่วงบ่าย ขณะที่แถวอื่นแสงสลัว ข้อใดแนะนำได้เหมาะสมที่สุด",
     "ติดตั้งผ้าม่านหรือมูลี่กรองแสงจ้าบริเวณที่มีแสงแดดจ้า และเพิ่มไฟส่องสว่างในบริเวณที่แสงสลัว เพื่อให้แสงสม่ำเสมอทั่วห้อง",
     ("ปล่อยไว้ตามเดิมเพราะแสงแดดธรรมชาติดีต่อสุขภาพเสมอ", "ปิดไฟทั้งหมดในห้องเพื่อให้สม่ำเสมอกับแสงแดด", "ให้นักเรียนทุกคนย้ายไปนั่งแถวที่มีแสงจ้าเท่านั้น")),
    ("ผู้สูงอายุที่มีปัญหาสายตามักต้องการความสว่างมากกว่าคนหนุ่มสาวในการอ่านหนังสือ เหตุใดจึงควรจัดแสงต่างกันตามกลุ่มผู้ใช้",
     "ความต้องการความสว่างที่เหมาะสมแตกต่างกันตามสภาพดวงตาของแต่ละบุคคล จึงควรปรับแสงให้เหมาะกับผู้ใช้งานจริง",
     ("ทุกคนต้องการความสว่างเท่ากันไม่ว่าอายุหรือสภาพดวงตาจะเป็นอย่างไร", "ผู้สูงอายุควรอ่านหนังสือในที่แสงสลัวเพื่อถนอมสายตา", "อายุและสภาพดวงตาไม่มีผลต่อความต้องการความสว่างเลย")),
    ("โรงพยาบาลจัดแสงในห้องพักผู้ป่วยให้สลัวกว่าห้องตรวจรักษา เหตุใดจึงจัดความสว่างต่างกันในแต่ละพื้นที่",
     "แต่ละพื้นที่มีกิจกรรมต่างกัน ห้องพักต้องการแสงสลัวเพื่อการพักผ่อน ส่วนห้องตรวจต้องการแสงจ้าเพื่อความละเอียดในการตรวจ",
     ("ทุกห้องในโรงพยาบาลควรมีความสว่างเท่ากันเสมอ", "ห้องพักผู้ป่วยควรมีแสงจ้าที่สุดเพื่อกระตุ้นให้ตื่นตัว", "ความสว่างของห้องไม่มีผลต่อกิจกรรมที่ทำในห้องนั้น")),
)


@question_type(
    "phys.brightness_arrangement_foundation",
    display_name={"th": "บอกผลของแสงสว่างที่ไม่เหมาะสมต่อดวงตา"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
)
class BrightnessArrangementFoundation(QuestionType):
    """Unsuitable light and the eyes, facts about arranging it, and which activity needs more light."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            stem, right, wrongs = rng.choice(BRIGHTNESS_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=BRIGHTNESS_HINT,
                             topic=BRIGHTNESS_ARRANGEMENT_TOPIC)
        if roll < 0.85:
            i, j = sorted(rng.sample(range(len(ACTIVITY_NEEDS)), 2))
            more = rng.random() < 0.5
            first, second = rng.sample((ACTIVITY_NEEDS[i], ACTIVITY_NEEDS[j]), 2)
            pick = ACTIVITY_NEEDS[i] if more else ACTIVITY_NEEDS[j]
            other = ACTIVITY_NEEDS[j] if more else ACTIVITY_NEEDS[i]
            return _labelled(
                stem=f"ระหว่าง{first}กับ{second} กิจกรรมใดต้องการความสว่าง{'มาก' if more else 'น้อย'}กว่า",
                correct=f"{pick} เพราะ{'เป็นงานที่ต้องมองรายละเอียดมากกว่า' if more else 'ต้องการมองรายละเอียดน้อยกว่า'}",
                wrongs=(f"{other} เพราะ{'เป็นงานที่ต้องมองรายละเอียดมากกว่า' if more else 'ต้องการมองรายละเอียดน้อยกว่า'}",
                        "ต้องการความสว่างเท่ากัน เพราะใช้ดวงตาเหมือนกัน",
                        f"{other} เพราะยิ่งทำนานยิ่งต้องการแสงน้อยลงเพื่อพักสายตา"),
                hint=BRIGHTNESS_HINT, topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
            )
        return _labelled(
            stem="แสงสว่างที่ไม่เหมาะสมกับกิจกรรม (จ้าเกินไปหรือสลัวเกินไป) อาจส่งผลอย่างไรต่อดวงตา",
            correct="ทำให้ดวงตาทำงานหนักเกินไป อาจปวดตา มองไม่ชัด หรือเสียต่อการมองเห็นในระยะยาว",
            wrongs=("ทำให้ดวงตามองเห็นสีสันได้ชัดเจนขึ้นเสมอ",
                    "ไม่มีผลใด ๆ ต่อดวงตาตราบใดที่ยังมองเห็นได้",
                    "ทำให้ดวงตาปรับตัวจนแข็งแรงขึ้นเมื่อใช้งานเป็นเวลานาน และมองเห็นในที่มืดได้ดี"),
            hint="แสงจ้าเกินไปหรือสลัวเกินไปทั้งสองแบบทำให้ดวงตาต้องทำงานหนักผิดปกติ",
            topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
        )


@question_type(
    "phys.brightness_arrangement_fluency",
    display_name={"th": "วิเคราะห์สถานการณ์และเสนอแนะการจัดความสว่างให้เหมาะสมกับกิจกรรม"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
)
class BrightnessArrangementFluency(QuestionType):
    """An activity with poor lighting; the method from the same table that fixes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(LIGHT_ARRANGEMENT_PROBLEMS))
        problem = LIGHT_ARRANGEMENT_PROBLEMS[index]
        others = [p.method for i, p in enumerate(LIGHT_ARRANGEMENT_PROBLEMS) if i != index]
        return _labelled(
            stem=f"{problem.case} ควรจัดความสว่างให้เหมาะสมด้วยวิธีใด",
            correct=problem.method,
            wrongs=tuple(others),
            hint="พิจารณาว่าแสงในสถานการณ์นั้นจ้าเกินไป สลัวเกินไป หรือไม่สม่ำเสมอ แล้วเลือกวิธีที่ปรับแสงให้เหมาะสม",
            topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
        )


@question_type(
    "phys.brightness_arrangement_application",
    display_name={"th": "ประเมินการจัดความสว่างให้เหมาะสมกับผู้ใช้และกิจกรรมจริง"},
    level=THIRD_SECONDARY, subject=SUBJECT, topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
)
class BrightnessArrangementApplication(QuestionType):
    """Authored cases, and a reading against a recommended range."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            place, low, high = rng.choice((("โต๊ะอ่านหนังสือ", 300, 750), ("ห้องเรียน", 300, 500), ("ห้องนั่งเล่น", 100, 300),
                                           ("โต๊ะวาดภาพ", 500, 1000), ("ห้องครัว", 200, 500), ("ห้องทำงาน", 300, 750)))
            reading = rng.choice((rng.randrange(25, low, 25), rng.randrange(low, high + 1, 25), rng.randrange(high + 50, high * 3, 50)))
            if reading < low:
                answer = "สลัวเกินไป ควรเพิ่มแสงสว่าง"
            elif reading > high:
                answer = "จ้าเกินไป ควรลดแสงหรือกรองแสง"
            else:
                answer = "อยู่ในช่วงที่เหมาะสม คงการจัดแสงไว้ได้"
            return _labelled(
                stem=(f"ค่าความสว่างที่เหมาะสมสำหรับ{place}อยู่ระหว่าง {low}-{high} ลักซ์ วัดได้ {reading} ลักซ์ "
                      "ควรจัดความสว่างอย่างไร"),
                correct=answer,
                wrongs=tuple(w for w in ("สลัวเกินไป ควรเพิ่มแสงสว่าง", "จ้าเกินไป ควรลดแสงหรือกรองแสง",
                                         "อยู่ในช่วงที่เหมาะสม คงการจัดแสงไว้ได้", "ควรปิดไฟทั้งหมดแล้วใช้แสงจากหน้าจอแทน")
                             if w != answer),
                hint="เทียบค่าที่วัดได้กับช่วงที่เหมาะสม ต่ำกว่าช่วงต้องเพิ่มแสง สูงกว่าช่วงต้องลดหรือกรองแสง",
                topic=BRIGHTNESS_ARRANGEMENT_TOPIC,
            )
        return _retopic(scenario_question(
            rng, BRIGHTNESS_ARRANGEMENT_SCENARIOS,
            hint="จัดความสว่างให้เหมาะกับกิจกรรมและผู้ใช้งาน ไม่ใช่ยึดค่าความสว่างเดียวสำหรับทุกสถานการณ์",
        ), BRIGHTNESS_ARRANGEMENT_TOPIC)
