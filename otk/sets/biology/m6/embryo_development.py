"""การเจริญเติบโตของสัตว์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/15

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


TOPIC_EMBRYO = "การเจริญเติบโตของสัตว์"


GERM_LAYERS = {
    "เอกโทเดิร์ม": ("ผิวหนังชั้นนอก", "สมองและไขสันหลัง", "เลนส์ตา"),
    "มีโซเดิร์ม": ("กล้ามเนื้อ", "กระดูก", "หัวใจและหลอดเลือด", "ไต"),
    "เอนโดเดิร์ม": ("เยื่อบุทางเดินอาหาร", "ปอด", "ตับ", "ตับอ่อน"),
}


STAGES = ("ไซโกต", "คลีเวจ", "มอรูลา", "บลาสทูลา", "แกสทรูลา", "ออร์แกโนเจเนซิส")


MEMBRANES = (("แอมเนียน", "ล้อมรอบเอ็มบริโอด้วยของเหลว ป้องกันการกระทบกระเทือนและการสูญเสียน้ำ"),
             ("ถุงไข่แดง", "เก็บอาหารสำหรับเอ็มบริโอของไก่"),
             ("แอลแลนทอยส์", "เก็บของเสียและช่วยแลกเปลี่ยนแก๊สในไข่ไก่"),
             ("คอเรียน", "หุ้มชั้นนอกสุดและเป็นส่วนหนึ่งของรกในมนุษย์"),
             ("รก", "แลกเปลี่ยนอาหาร แก๊ส และของเสียระหว่างแม่กับลูกในครรภ์"))


EMBRYO_HINT = ("ไซโกต → คลีเวจ → มอรูลา → บลาสทูลา → แกสทรูลา → ออร์แกโนเจเนซิส เอกโทเดิร์มเป็นผิวหนังและระบบประสาท "
               "มีโซเดิร์มเป็นกล้ามเนื้อ กระดูก เลือด เอนโดเดิร์มเป็นเยื่อบุทางเดินอาหารและทางเดินหายใจ")


POST_EMBRYO = (
    ("ลูกอ๊อดเปลี่ยนเป็นกบ มีการสลายหาง สร้างขา และเปลี่ยนจากเหงือกเป็นปอด เรียกว่าอะไร", "เมทามอร์โฟซิส",
     ("คลีเวจ", "แกสทรูเลชัน", "การงอกใหม่", "การแตกหน่อ")),
    ("ฮอร์โมนใดควบคุมการเปลี่ยนแปลงรูปร่างของลูกอ๊อดเป็นกบ", "ไทรอกซิน", ("อินซูลิน", "ออกซิน", "อะดรีนาลีน", "เอสโทรเจน")),
    ("ในไข่ไก่ เอ็มบริโอได้อาหารจากที่ใดเป็นหลัก", "ไข่แดงในถุงไข่แดง", ("รกของแม่ไก่", "อากาศผ่านเปลือกไข่", "แอลแลนทอยส์เท่านั้น", "เปลือกไข่")),
    ("ทารกในครรภ์มนุษย์ได้รับอาหารและออกซิเจนทางใด", "รกและสายสะดือ", ("ถุงไข่แดง", "การหายใจด้วยปอดในครรภ์", "การดื่มน้ำคร่ำ", "ผิวหนังโดยตรง")),
    ("ในระยะคลีเวจ เซลล์ของเอ็มบริโอเปลี่ยนแปลงอย่างไร", "แบ่งเซลล์แบบไมโทซิสหลายครั้ง จำนวนเซลล์เพิ่มแต่ขนาดโดยรวมแทบไม่เปลี่ยน",
     ("เซลล์ขยายขนาดขึ้นมากโดยไม่แบ่ง ทำให้เอ็มบริโอมีขนาดใหญ่ขึ้นอย่างรวดเร็ว", "แบ่งเซลล์แบบไมโอซิส", "เซลล์ลดจำนวนลง", "สร้างอวัยวะครบทุกระบบ และเนื้อเยื่อชั้นต่าง ๆ ภายในระยะนี้")),
    ("ไข่ไก่ที่ไม่ได้รับการผสม เมื่อนำไปฟักจะเป็นอย่างไร", "ไม่เจริญเป็นลูกไก่ เพราะไม่มีไซโกต",
     ("เจริญเป็นลูกไก่เพศผู้", "เจริญเป็นลูกไก่เพศเมีย", "เจริญเป็นลูกไก่ที่เป็นหมัน เพราะไม่มีพ่อ", "เจริญช้ากว่าไข่ที่ผสมแล้ว")),
    ("การเจริญเติบโตของคนหลังคลอดวัดได้จากอะไร", "การเพิ่มขนาดและจำนวนเซลล์ ทำให้ส่วนสูงและน้ำหนักเพิ่มขึ้น",
     ("การเปลี่ยนรูปร่างแบบเมทามอร์โฟซิส จากตัวอ่อนเป็นตัวเต็มวัย", "การลดจำนวนเซลล์", "การแบ่งเซลล์แบบไมโอซิสทั่วร่างกาย ทำให้เซลล์มีจำนวนมากขึ้น", "การลอกคราบ")),
)


@question_type(
    "biology.embryo_development_foundation",
    display_name={"th": "ระยะการเจริญของเอ็มบริโอและเนื้อเยื่อชั้นต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_EMBRYO,
)
class EmbryoDevelopmentFoundation(QuestionType):
    """The order of stages, and what each germ layer becomes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.35:
            i = rng.randrange(len(STAGES) - 1)
            pool = [s for s in STAGES if s not in (STAGES[i], STAGES[i + 1])] + ["เมทามอร์โฟซิส"]
            return _labelled(stem=f"ระยะการเจริญของเอ็มบริโอที่ต่อจาก{STAGES[i]}คือระยะใด", correct=STAGES[i + 1],
                             wrongs=tuple(pool), topic=TOPIC_EMBRYO, hint=EMBRYO_HINT)
        layer = rng.choice(sorted(GERM_LAYERS))
        organ = rng.choice(GERM_LAYERS[layer])
        others = [ell for ell in GERM_LAYERS if ell != layer]
        if rng.random() < 0.5:
            return _labelled(stem=f"{organ}เจริญมาจากเนื้อเยื่อชั้นใด", correct=layer, wrongs=(*others, "ชั้นแอมเนียน"), topic=TOPIC_EMBRYO,
                             hint=EMBRYO_HINT)
        pool = [o for ell in others for o in GERM_LAYERS[ell]]
        return _labelled(stem=f"อวัยวะใดเจริญมาจาก{layer}", correct=organ, wrongs=tuple(pool), topic=TOPIC_EMBRYO, hint=EMBRYO_HINT)


@question_type(
    "biology.embryo_development_fluency",
    display_name={"th": "เยื่อหุ้มเอ็มบริโอและรก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_EMBRYO,
)
class EmbryoDevelopmentFluency(QuestionType):
    """Amnion, yolk sac, allantois, chorion and placenta."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role = rng.choice(MEMBRANES)
        others = rng.sample([m for m in MEMBRANES if m[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}ทำหน้าที่อะไร", correct=role, wrongs=tuple(m[1] for m in others), topic=TOPIC_EMBRYO, hint=EMBRYO_HINT)
        return _labelled(stem=f"โครงสร้างใด{role}", correct=name, wrongs=tuple(m[0] for m in others), topic=TOPIC_EMBRYO, hint=EMBRYO_HINT)


@question_type(
    "biology.embryo_development_application",
    display_name={"th": "การเจริญหลังระยะเอ็มบริโอของกบ ไก่ และมนุษย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_EMBRYO,
)
class EmbryoDevelopmentApplication(QuestionType):
    """Metamorphosis, the egg and the placenta."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(POST_EMBRYO)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_EMBRYO, hint=EMBRYO_HINT)
