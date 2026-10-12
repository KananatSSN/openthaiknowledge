"""วัฏจักรไนโตรเจน กำมะถัน และฟอสฟอรัส

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/3

Sets moved here from: science_wave_f71.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f71 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_CYCLE = "วัฏจักรไนโตรเจน กำมะถัน และฟอสฟอรัส"


NITROGEN = (
    ("การตรึงไนโตรเจน", "เปลี่ยน N₂ ในอากาศเป็นแอมโมเนีย", "ไรโซเบียมในปมรากพืชตระกูลถั่วและไซยาโนแบคทีเรีย"),
    ("แอมโมนิฟิเคชัน", "เปลี่ยนสารอินทรีย์ในซากเป็นแอมโมเนียม", "ผู้ย่อยสลาย เช่น แบคทีเรียและรา"),
    ("ไนตริฟิเคชัน", "เปลี่ยนแอมโมเนียมเป็นไนไทรต์แล้วเป็นไนเตรต", "ไนโตรโซโมแนสและไนโตรแบคเตอร์"),
    ("ดีไนตริฟิเคชัน", "เปลี่ยนไนเตรตกลับเป็นแก๊สไนโตรเจน", "แบคทีเรียในดินที่ขาดออกซิเจน"),
    ("การดูดซึมของพืช", "นำไนเตรตหรือแอมโมเนียมจากดินไปสร้างโปรตีนและกรดนิวคลีอิก", "รากพืช"),
)


CYCLE_FACTS = (
    ("วัฏจักรใดไม่มีแก๊สในบรรยากาศเป็นแหล่งสะสมหลัก", "วัฏจักรฟอสฟอรัส", ("วัฏจักรไนโตรเจน", "วัฏจักรกำมะถัน", "วัฏจักรคาร์บอน", "วัฏจักรน้ำ")),
    ("แก๊สซัลเฟอร์ไดออกไซด์จากการเผาถ่านหินทำให้เกิดปัญหาใด", "ฝนกรด (acid rain)",
     ("ยูโทรฟิเคชัน", "ไบโอแมกนิฟิเคชันของปรอท", "การตรึงไนโตรเจนเพิ่มขึ้น", "ดินมีฟอสเฟตมากขึ้น")),
    ("ฟอสฟอรัสเข้าสู่ระบบนิเวศบนบกจากแหล่งใดเป็นหลัก", "การผุพังของหินที่มีฟอสเฟต", ("แก๊สฟอสฟอรัสในอากาศ", "ฟ้าผ่า", "การหายใจของสัตว์และพืช", "ภูเขาไฟระเบิดเท่านั้น")),
    ("กำมะถันเข้าสู่บรรยากาศจากแหล่งใด", "ภูเขาไฟระเบิด และการเผาเชื้อเพลิงฟอสซิลที่มีกำมะถัน",
     ("การตรึงโดยไรโซเบียมในปมรากพืชตระกูลถั่ว", "การผุพังของหินฟอสเฟตและการชะล้างลงสู่แหล่งน้ำ", "การสังเคราะห์ด้วยแสงและการหายใจของพืชและสัตว์", "การดูดซึมของราก")),
    ("พืชนำกำมะถันไปใช้ในรูปใด", "ซัลเฟต (SO₄²⁻) ในดิน", ("แก๊สไฮโดรเจนซัลไฟด์", "กำมะถันผงบริสุทธิ์", "แก๊สซัลเฟอร์ไดออกไซด์เท่านั้น", "ฟอสเฟต")),
    ("การใช้ปุ๋ยฟอสเฟตมากเกินจนไหลลงแหล่งน้ำทำให้เกิดอะไร", "เกิดยูโทรฟิเคชัน สาหร่ายเพิ่มมากจนน้ำขาดออกซิเจน",
     ("น้ำใสขึ้นและมีปลามากขึ้นเพราะมีอาหารมากขึ้น", "ฝนกรด (acid rain)", "ปรอทสะสมในปลาและถ่ายทอดสู่ผู้บริโภค", "แหล่งน้ำเย็นลงจนสาหร่ายและปลาตายหมด")),
    ("การปลูกพืชตระกูลถั่วหมุนเวียนช่วยบำรุงดินเพราะเหตุใด", "แบคทีเรียในปมรากตรึงไนโตรเจนเพิ่มสารประกอบไนโตรเจนในดิน",
     ("รากถั่วดูดฟอสเฟตออกจากดินจนดินเหลือแต่ไนโตรเจน", "ถั่วปล่อยกำมะถันลงดิน", "ถั่วปล่อยกรดออกจากรากจนดินเป็นกรดจัด พืชอื่นจึงโตดีขึ้น", "ถั่วดูดไนเตรตออกหมด")),
)


CYCLE_HINT = ("ไนโตรเจน: ตรึง → ดูดซึม → แอมโมนิฟิเคชัน → ไนตริฟิเคชัน → ดีไนตริฟิเคชัน กำมะถันมีทั้งแก๊สและซัลเฟตในดิน "
              "ฟอสฟอรัสไม่มีแก๊ส หมุนเวียนระหว่างหิน ดิน น้ำ และสิ่งมีชีวิต")


NITRO_ORDER = ("N₂ ในอากาศ", "แอมโมเนีย", "ไนไทรต์", "ไนเตรต")


@question_type(
    "biology.nutrient_cycle_foundation",
    display_name={"th": "ขั้นตอนของวัฏจักรไนโตรเจน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CYCLE,
)
class NutrientCycleFoundation(QuestionType):
    """Each step, what it does, and who does it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step, does, who = rng.choice(NITROGEN)
        others = rng.sample([n for n in NITROGEN if n[0] != step], 3)
        roll = rng.random()
        if roll < 0.35:
            return _labelled(stem=f"ขั้น{step}ในวัฏจักรไนโตรเจนคือข้อใด", correct=does, wrongs=tuple(n[1] for n in others), topic=TOPIC_CYCLE,
                             hint=CYCLE_HINT)
        if roll < 0.7:
            return _labelled(stem=f"การ{does}เรียกว่าอะไร", correct=step, wrongs=tuple(n[0] for n in others), topic=TOPIC_CYCLE, hint=CYCLE_HINT)
        return _labelled(stem=f"สิ่งมีชีวิตใดเกี่ยวข้องกับขั้น{step}", correct=who, wrongs=tuple(n[2] for n in others), topic=TOPIC_CYCLE,
                         hint=CYCLE_HINT)


@question_type(
    "biology.nutrient_cycle_fluency",
    display_name={"th": "วัฏจักรกำมะถันและฟอสฟอรัส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CYCLE,
)
class NutrientCycleFluency(QuestionType):
    """Where sulfur and phosphorus come from and go."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(CYCLE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_CYCLE, hint=CYCLE_HINT)


@question_type(
    "biology.nutrient_cycle_application",
    display_name={"th": "ลำดับการเปลี่ยนแปลงของสารในวัฏจักรไนโตรเจน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CYCLE,
)
class NutrientCycleApplication(QuestionType):
    """Follow a nitrogen atom through the forms it takes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            i = rng.randrange(len(NITRO_ORDER) - 1)
            pool = [n for n in NITRO_ORDER if n not in (NITRO_ORDER[i], NITRO_ORDER[i + 1])] + ["ซัลเฟต", "ฟอสเฟต"]
            return _labelled(stem=f"ในวัฏจักรไนโตรเจน {NITRO_ORDER[i]}จะถูกเปลี่ยนไปเป็นสารใดในขั้นถัดไป", correct=NITRO_ORDER[i + 1],
                             wrongs=tuple(pool), topic=TOPIC_CYCLE, hint=CYCLE_HINT)
        cases = (("ถ้าแบคทีเรียไนตริฟายอิงในดินถูกทำลายหมด จะเกิดอะไรขึ้น", "แอมโมเนียมสะสม แต่ไนเตรตในดินลดลง"),
                 ("ถ้าไม่มีผู้ย่อยสลายในระบบนิเวศ จะเกิดอะไรขึ้นกับวัฏจักรไนโตรเจน", "ไนโตรเจนค้างอยู่ในซากสิ่งมีชีวิต ไม่กลับคืนสู่ดิน"),
                 ("ในนาที่มีน้ำขังจนดินขาดออกซิเจน กระบวนการใดเกิดมากขึ้น", "ดีไนตริฟิเคชัน ทำให้ไนโตรเจนหายไปสู่อากาศ"),
                 ("ถ้าปลูกถั่วที่ไม่มีปมราก พืชจะได้ไนโตรเจนจากแหล่งใด", "ไนเตรตและแอมโมเนียมที่มีอยู่ในดินเท่านั้น"))
        stem, right = rng.choice(cases)
        pool = [r for s, r in cases if s != stem] + ["ไนเตรตในดินเพิ่มขึ้นมากทันที", "ฟอสเฟตกลายเป็นแก๊สในอากาศ",
                                                   "พืชตรึงไนโตรเจนจากอากาศได้เองทุกชนิด"]
        return _labelled(stem=stem, correct=right, wrongs=tuple(pool), topic=TOPIC_CYCLE, hint=CYCLE_HINT)
