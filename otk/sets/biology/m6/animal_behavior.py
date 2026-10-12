"""พฤติกรรมที่เป็นมาแต่กำเนิดและที่เกิดจากการเรียนรู้

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/17

Sets moved here from: science_wave_f69.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f69 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_BEHAVIOUR = "พฤติกรรมที่เป็นมาแต่กำเนิดและที่เกิดจากการเรียนรู้"


BEHAVIOURS = {
    "ไคนีซิส": ("ตัวกะปิเคลื่อนที่เร็วและเปลี่ยนทิศบ่อยในที่แห้ง แต่ช้าลงในที่ชื้น", "พารามีเซียมเคลื่อนที่เร็วขึ้นแบบไม่มีทิศทางเมื่ออยู่ในน้ำที่ร้อน"),
    "แทกซิส": ("แมลงเม่าบินเข้าหาแสงไฟ", "ยูกลีนาว่ายเข้าหาแสง"),
    "รีเฟล็กซ์": ("กระตุกมือออกเมื่อสัมผัสของร้อน", "กระพริบตาเมื่อมีวัตถุพุ่งเข้าหา"),
    "รีเฟล็กซ์ต่อเนื่อง (สัญชาตญาณ)": ("แมงมุมชักใยได้เองโดยไม่ต้องเรียนรู้", "นกสร้างรังได้ตามแบบของชนิดตนเองตั้งแต่ครั้งแรก"),
    "แฮบิชูเอชัน": ("นกไม่บินหนีหุ่นไล่กาเมื่อเห็นบ่อย ๆ", "หอยทากเลิกหดตัวเมื่อถูกแตะเบา ๆ ซ้ำหลายครั้ง"),
    "การฝังใจ": ("ลูกเป็ดที่เพิ่งฟักเดินตามสิ่งแรกที่เคลื่อนไหว", "ลูกห่านเดินตามคนที่มันเห็นเป็นคนแรกหลังฟัก"),
    "การมีเงื่อนไข": ("สุนัขน้ำลายไหลเมื่อได้ยินเสียงกระดิ่งที่เคยดังพร้อมอาหาร", "หนูกดคานเมื่อเรียนรู้ว่าจะได้อาหาร"),
    "การใช้เหตุผล": ("ลิงชิมแปนซีต่อกล่องซ้อนกันเพื่อหยิบกล้วยบนที่สูงตั้งแต่ครั้งแรก", "นักเรียนแก้โจทย์ใหม่ด้วยการคิดวางแผนก่อนลงมือ"),
}


INNATE = {"ไคนีซิส", "แทกซิส", "รีเฟล็กซ์", "รีเฟล็กซ์ต่อเนื่อง (สัญชาตญาณ)"}


BEHAVIOUR_HINT = ("พฤติกรรมแต่กำเนิด: ไคนีซิส แทกซิส รีเฟล็กซ์ สัญชาตญาณ พฤติกรรมเรียนรู้: แฮบิชูเอชัน การฝังใจ การมีเงื่อนไข การใช้เหตุผล "
                  "ไคนีซิสเปลี่ยนความเร็วแบบไม่มีทิศทาง แทกซิสเคลื่อนที่เข้าหาหรือหนีสิ่งเร้าอย่างมีทิศทาง")


@question_type(
    "biology.animal_behavior_foundation",
    display_name={"th": "พฤติกรรมที่เป็นมาแต่กำเนิดและพฤติกรรมที่เกิดจากการเรียนรู้"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BEHAVIOUR,
)
class AnimalBehaviorFoundation(QuestionType):
    """Innate or learned."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        innate = rng.random() < 0.5
        same = [e for k, es in BEHAVIOURS.items() if (k in INNATE) == innate for e in es]
        other = [e for k, es in BEHAVIOURS.items() if (k in INNATE) != innate for e in es]
        kind = "พฤติกรรมที่เป็นมาแต่กำเนิด" if innate else "พฤติกรรมที่เกิดจากการเรียนรู้"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็น{kind}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_BEHAVIOUR,
                             hint=BEHAVIOUR_HINT)
        return _labelled(stem=f"\"{rng.choice(same)}\" เป็นพฤติกรรมประเภทใด", correct=kind,
                         wrongs=("พฤติกรรมที่เกิดจากการเรียนรู้" if innate else "พฤติกรรมที่เป็นมาแต่กำเนิด", "การสื่อสารด้วยสารเคมี",
                                 "การตอบสนองของพืช"), topic=TOPIC_BEHAVIOUR, hint=BEHAVIOUR_HINT)


@question_type(
    "biology.animal_behavior_fluency",
    display_name={"th": "ระบุชนิดของพฤติกรรมจากตัวอย่าง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BEHAVIOUR,
)
class AnimalBehaviorFluency(QuestionType):
    """Name the behaviour from an example, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(BEHAVIOURS))
        example = rng.choice(BEHAVIOURS[kind])
        others = [k for k in BEHAVIOURS if k != kind]
        if rng.random() < 0.55:
            return _labelled(stem=f"\"{example}\" เป็นพฤติกรรมแบบใด", correct=kind, wrongs=tuple(others), topic=TOPIC_BEHAVIOUR,
                             hint=BEHAVIOUR_HINT)
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{kind}", correct=example,
                         wrongs=tuple(rng.choice(BEHAVIOURS[k]) for k in rng.sample(others, 3)), topic=TOPIC_BEHAVIOUR, hint=BEHAVIOUR_HINT)


@question_type(
    "biology.animal_behavior_application",
    display_name={"th": "วิเคราะห์การทดลองเกี่ยวกับพฤติกรรมสัตว์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BEHAVIOUR,
)
class AnimalBehaviorApplication(QuestionType):
    """Read what an experiment shows about behaviour."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cases = (
            ("ปล่อยตัวกะปิในกล่องที่ด้านหนึ่งชื้น อีกด้านแห้ง ผ่านไปสักพักพบตัวกะปิส่วนใหญ่อยู่ด้านชื้น สาเหตุคืออะไร",
             "ตัวกะปิเคลื่อนที่ช้าลงในที่ชื้นจึงไปรวมกันอยู่ที่นั่น (ไคนีซิส)",
             ("ตัวกะปิเคลื่อนที่ตรงเข้าหาความชื้น (แทกซิส)", "ตัวกะปิเรียนรู้ว่าที่ชื้นมีอาหาร", "ตัวกะปิใช้เหตุผลเลือกที่อยู่", "ตัวกะปิฝังใจกับความชื้น")),
            ("ลูกเป็ดที่ฟักในตู้อบแล้วเห็นคนเป็นสิ่งแรก จะเดินตามคน การทดลองนี้แสดงว่าการฝังใจมีลักษณะใด",
             "เกิดในช่วงเวลาจำกัดหลังฟักและเกิดกับสิ่งที่เห็นเป็นครั้งแรก",
             ("เกิดได้ทุกช่วงอายุ", "เกิดเฉพาะกับแม่เป็ดเท่านั้น", "เป็นรีเฟล็กซ์ที่ไม่เกี่ยวกับการเรียนรู้", "ต้องมีรางวัลเป็นอาหารทุกครั้ง")),
            ("สั่นกระดิ่งก่อนให้อาหารสุนัขทุกวัน ต่อมาเพียงได้ยินกระดิ่งสุนัขก็น้ำลายไหล กระดิ่งในการทดลองนี้เรียกว่าอะไร",
             "สิ่งเร้าที่มีเงื่อนไข", ("สิ่งเร้าที่ไม่มีเงื่อนไข", "การตอบสนองที่ไม่มีเงื่อนไข", "สิ่งเร้าที่ทำให้เกิดแฮบิชูเอชัน", "ฟีโรโมน")),
            ("หนูในกล่องกดคานโดยบังเอิญแล้วได้อาหาร ต่อมากดคานบ่อยขึ้น เป็นการเรียนรู้แบบใด", "การมีเงื่อนไขแบบลองผิดลองถูก",
             ("การฝังใจ", "แฮบิชูเอชัน", "รีเฟล็กซ์", "แทกซิส", "ไคนีซิส")),
            ("เคาะตู้ปลาเบา ๆ ซ้ำหลายวัน ปลาที่เคยตกใจว่ายหนี ต่อมาไม่สนใจเสียงเคาะ เป็นพฤติกรรมแบบใด", "แฮบิชูเอชัน",
             ("การฝังใจ", "แทกซิส", "การใช้เหตุผล", "รีเฟล็กซ์ต่อเนื่อง", "การมีเงื่อนไข")),
            ("ปล่อยยูกลีนาในจานที่ด้านหนึ่งสว่าง อีกด้านมืด ยูกลีนาว่ายไปรวมที่ด้านสว่างอย่างมีทิศทาง เป็นพฤติกรรมแบบใด", "แทกซิส",
             ("ไคนีซิส", "แฮบิชูเอชัน", "การมีเงื่อนไข", "การฝังใจ", "การใช้เหตุผล")),
        )
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_BEHAVIOUR, hint=BEHAVIOUR_HINT)
