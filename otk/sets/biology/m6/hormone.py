"""ฮอร์โมนจากต่อมไร้ท่อ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/16

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


TOPIC_HORMONE = "ฮอร์โมนจากต่อมไร้ท่อ"


HORMONES = (
    ("ไฮโพทาลามัส", "ฮอร์โมนกระตุ้นและยับยั้ง", "ควบคุมการหลั่งฮอร์โมนของต่อมใต้สมองส่วนหน้า"),
    ("ต่อมใต้สมองส่วนหน้า", "โกรทฮอร์โมน", "กระตุ้นการเจริญเติบโตของกระดูกและกล้ามเนื้อ"),
    ("ต่อมใต้สมองส่วนหลัง", "ADH", "เพิ่มการดูดน้ำกลับที่ท่อหน่วยไต"),
    ("ต่อมไทรอยด์", "ไทรอกซิน", "ควบคุมอัตราเมแทบอลิซึมของร่างกาย"),
    ("ต่อมพาราไทรอยด์", "พาราทอร์โมน", "เพิ่มระดับแคลเซียมในเลือด"),
    ("ตับอ่อน", "อินซูลิน", "ลดระดับกลูโคสในเลือด"),
    ("ตับอ่อน", "กลูคากอน", "เพิ่มระดับกลูโคสในเลือด"),
    ("ต่อมหมวกไตชั้นใน", "อะดรีนาลีน", "เพิ่มอัตราการเต้นของหัวใจและระดับกลูโคสเมื่อตื่นเต้นหรือตกใจ"),
    ("ต่อมหมวกไตชั้นนอก", "แอลโดสเตอโรน", "เพิ่มการดูดกลับ Na⁺ ที่ท่อหน่วยไต"),
    ("ต่อมไพเนียล", "เมลาโทนิน", "เกี่ยวข้องกับการควบคุมวงจรการนอนหลับ"),
)


DISORDERS = (
    ("โรคคอพอกจากการขาดไอโอดีน", "ต่อมไทรอยด์สร้างไทรอกซินไม่พอจนขยายใหญ่"),
    ("ภาวะร่างกายสูงใหญ่ผิดปกติ (ไจแกนทิซึม)", "โกรทฮอร์โมนมากเกินไปในวัยเด็ก"),
    ("ภาวะเตี้ยแคระ", "โกรทฮอร์โมนน้อยเกินไปในวัยเด็ก"),
    ("เบาหวาน", "ขาดอินซูลินหรือเซลล์ไม่ตอบสนองต่ออินซูลิน"),
    ("เบาจืด", "ขาดฮอร์โมน ADH"),
    ("อะโครเมกาลี", "โกรทฮอร์โมนมากเกินไปในวัยผู้ใหญ่ ทำให้กระดูกมือ เท้า และขากรรไกรใหญ่ขึ้น"),
)


HORMONE_HINT = ("อินซูลินลดกลูโคส กลูคากอนเพิ่มกลูโคส ไทรอกซินคุมเมแทบอลิซึม ADH เพิ่มการดูดน้ำกลับ พาราทอร์โมนเพิ่ม Ca ในเลือด "
                "อะดรีนาลีนเตรียมร่างกายเมื่อตกใจ ร่างกายควบคุมฮอร์โมนด้วยการป้อนกลับแบบยับยั้ง")


@question_type(
    "biology.hormone_foundation",
    display_name={"th": "ต่อมไร้ท่อ ฮอร์โมน และหน้าที่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HORMONE,
)
class HormoneFoundation(QuestionType):
    """Gland, hormone and job, in any direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        gland, hormone, job = rng.choice(HORMONES)
        others = rng.sample([h for h in HORMONES if h[1] != hormone and h[2] != job], 3)
        roll = rng.random()
        if roll < 0.35:
            return _labelled(stem=f"ฮอร์โมนใด{job}", correct=hormone, wrongs=tuple(h[1] for h in others), topic=TOPIC_HORMONE, hint=HORMONE_HINT)
        if roll < 0.7:
            return _labelled(stem=f"{hormone}มีหน้าที่อะไร", correct=job, wrongs=tuple(h[2] for h in others), topic=TOPIC_HORMONE, hint=HORMONE_HINT)
        # ADH is made in the hypothalamus and released from the posterior pituitary, so both are right for it.
        skip = {gland, "ไฮโพทาลามัส"} if hormone == "ADH" else {gland}
        glands = [h[0] for h in others if h[0] not in skip]
        glands = list(dict.fromkeys(glands + [g for g, _, _ in HORMONES if g not in skip]))[:3]
        return _labelled(stem=f"{hormone}สร้างหรือหลั่งจากต่อมใด", correct=gland, wrongs=tuple(glands), topic=TOPIC_HORMONE, hint=HORMONE_HINT)


@question_type(
    "biology.hormone_fluency",
    display_name={"th": "ความผิดปกติที่เกิดจากฮอร์โมน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HORMONE,
)
class HormoneFluency(QuestionType):
    """Goitre, gigantism, dwarfism, diabetes, acromegaly."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, cause = rng.choice(DISORDERS)
        others = rng.sample([d for d in DISORDERS if d[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}เกิดจากอะไร", correct=cause, wrongs=tuple(d[1] for d in others), topic=TOPIC_HORMONE, hint=HORMONE_HINT)
        return _labelled(stem=f"\"{cause}\" ทำให้เกิดความผิดปกติใด", correct=name, wrongs=tuple(d[0] for d in others), topic=TOPIC_HORMONE,
                         hint=HORMONE_HINT)


@question_type(
    "biology.hormone_application",
    display_name={"th": "การควบคุมสมดุลด้วยฮอร์โมนในสถานการณ์ต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HORMONE,
)
class HormoneApplication(QuestionType):
    """Which hormone rises in each situation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cases = (("หลังรับประทานอาหารที่มีแป้งมาก ระดับกลูโคสในเลือดสูงขึ้น", "อินซูลิน"),
                 ("อดอาหารมาหลายชั่วโมง ระดับกลูโคสในเลือดต่ำลง", "กลูคากอน"),
                 ("ออกกำลังกายหนักจนเสียเหงื่อมากและดื่มน้ำน้อย", "ADH"),
                 ("ถูกสุนัขวิ่งไล่ หัวใจเต้นแรงและเร็ว", "อะดรีนาลีน"),
                 ("ระดับแคลเซียมในเลือดต่ำลง", "พาราทอร์โมน"),
                 ("อากาศหนาวเป็นเวลานาน ร่างกายต้องเพิ่มการสร้างความร้อน", "ไทรอกซิน"))
        scene, hormone = rng.choice(cases)
        pool = [h for _, h in cases if h != hormone] + ["เอสโทรเจน"]
        if rng.random() < 0.3:
            return _labelled(stem="เมื่อระดับไทรอกซินในเลือดสูง ต่อมใต้สมองลดการหลั่ง TSH การควบคุมแบบนี้เรียกว่าอะไร",
                             correct="การป้อนกลับแบบยับยั้ง (negative feedback)",
                             wrongs=tuple(("การป้อนกลับแบบกระตุ้น", "รีเฟล็กซ์", "การเรียนรู้แบบมีเงื่อนไข", "การตอบสนองแบบจำเพาะ")),
                             topic=TOPIC_HORMONE, hint=HORMONE_HINT)
        return _labelled(stem=f"เมื่อ{scene} ร่างกายจะหลั่งฮอร์โมนใดเพิ่มขึ้นเป็นหลัก", correct=hormone, wrongs=tuple(pool),
                         topic=TOPIC_HORMONE, hint=HORMONE_HINT)
