"""ความสัมพันธ์ระหว่างสิ่งมีชีวิต

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.3/2

Sets moved here from: biology, science_wave_b.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.biology import SUBJECT, TOPIC_ECOLOGY
from otk.sets._support.science_wave_b import (
    BOTH_GAIN,
    BOTH_LOSE,
    LEVEL,
    ONE_GAIN_ONE_LOSE,
    ONE_GAIN_ONE_NEUTRAL,
    RELATIONSHIP_SURVEYS,
    RELATIONSHIPS,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


SIGN_PAIRS = (BOTH_GAIN, ONE_GAIN_ONE_LOSE, ONE_GAIN_ONE_NEUTRAL, BOTH_LOSE)


@question_type("ecology.symbiosis",
               display_name={"th": "รูปแบบความสัมพันธ์ของสิ่งมีชีวิต"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_ECOLOGY)
class Symbiosis(ClassifyType):
    """รูปแบบความสัมพันธ์ของสิ่งมีชีวิตที่อยู่ร่วมกัน — ระบุจากตัวอย่างจริง.

    เครื่องหมายในวงเล็บบอกว่าแต่ละฝ่ายได้ (+) เสีย (−) หรือไม่ได้ไม่เสีย (0)
    ประโยชน์ ล่าเหยื่อและปรสิตต่างก็เป็น (+, −) แต่เป็นคนละรูปแบบ — เป็นคู่ที่
    ผู้เรียนต้องแยกให้ออก จึงถูกใช้เป็นตัวลวงของกันและกันได้.
    """

    CLASSIFY_STEM = "ความสัมพันธ์ต่อไปนี้จัดเป็นรูปแบบใด: “{member}”"
    PICK_STEM = "ข้อใดเป็นตัวอย่างของ{category}"

    CATEGORIES = [
        Category("ภาวะพึ่งพากัน (+, +)",
                 ("ไลเคน (ราและสาหร่ายที่อยู่ร่วมกัน)",
                  "แบคทีเรียไรโซเบียมในปมรากพืชตระกูลถั่ว",
                  "โพรโทซัวในลำไส้ปลวก",
                  "ราไมคอร์ไรซากับรากของพืช")),
        Category("ภาวะได้ประโยชน์ร่วมกันแบบไม่จำเป็นต่อการอยู่รอด (+, +)",
                 ("นกเอี้ยงจิกกินเห็บบนตัวควาย ทำให้นกได้อาหารและควายมีปรสิตลดลง",
                  "ปูเสฉวนกับดอกไม้ทะเล",
                  "ผึ้งกินน้ำหวานจากดอกไม้และช่วยถ่ายเรณูให้พืช")),
        Category("ภาวะอิงอาศัย (Commensalism +, 0)",
                 ("กล้วยไม้ที่เกาะอยู่บนต้นไม้ใหญ่",
                  "เพรียงที่เกาะบนผิวหนังของปลาวาฬ",
                  "ปลาเหาฉลามที่เกาะติดกับปลาฉลาม",
                  "เฟินที่เกาะอาศัยอยู่บนต้นไม้ใหญ่")),
        Category("ภาวะปรสิต (Parasitism +, −)",
                 ("พยาธิตัวตืดในลำไส้ของคน",
                  "เห็บดูดเลือดบนตัวสุนัข",
                  "กาฝากที่เกาะเบียนบนต้นไม้ใหญ่",
                  "ต้นฝอยทองที่เลื้อยเกาะต้นไม้อื่น")),
        Category("ภาวะล่าเหยื่อ (Predation +, −)",
                 ("เสือล่ากวางเป็นอาหาร",
                  "งูจับหนูกิน",
                  "นกจับหนอนกิน",
                  "สิงโตล่าม้าลาย")),
        Category("ภาวะแข่งขัน (Competition −, −)",
                 ("วัชพืชกับต้นข้าวแย่งน้ำและแร่ธาตุในดิน",
                  "สิงโตกับไฮยีนาแย่งชิงเหยื่อในบริเวณเดียวกัน",
                  "ต้นไม้ในป่าที่แย่งกันรับแสงอาทิตย์")),
    ]


@question_type(
    "ecology.relationship_signs_fluency",
    display_name={"th": "การได้และเสียประโยชน์ของความสัมพันธ์แต่ละรูปแบบ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RelationshipSignsFluency(QuestionType):
    """Say who gains and who loses, and separate the two (+, −) relationships.

    `ecology.symbiosis` asks for the name of the pattern. The name is the easy
    half: ภาวะล่าเหยื่อ and ภาวะปรสิต are both (+, −), so a learner who has only
    memorised labels cannot say what either one costs whom, which is what ม.3/2
    asks for.
    """

    # The pair a learner is most likely to confuse, and what actually separates
    # them. Kept as one item rather than generated, because there is exactly one
    # distinction to draw.
    PREDATION_VS_PARASITISM = (
        "ภาวะล่าเหยื่อกับภาวะปรสิตต่างก็เป็นความสัมพันธ์แบบ (+, −) "
        "ข้อใดคือความแตกต่างที่สำคัญของสองรูปแบบนี้",
        "ผู้ล่าฆ่าเหยื่อเพื่อกินเป็นอาหารในเวลาอันสั้น ส่วนปรสิตอาศัยอยู่กับผู้ถูกอาศัย "
        "เป็นเวลานานโดยทั่วไปไม่ทำให้ตายทันที",
        ("ผู้ล่ามีขนาดเล็กกว่าเหยื่อเสมอ ส่วนปรสิตมีขนาดใหญ่กว่าผู้ถูกอาศัยเสมอ",
         "ภาวะล่าเหยื่อเกิดกับสัตว์เท่านั้น ส่วนภาวะปรสิตเกิดกับพืชเท่านั้น",
         "ผู้ล่าได้ประโยชน์ฝ่ายเดียว ส่วนปรสิตทำให้ทั้งสองฝ่ายเสียประโยชน์"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            name, signs, examples = rng.choice(RELATIONSHIPS)
            return _labelled(
                stem=f"“{name}” เป็นความสัมพันธ์ที่แต่ละฝ่ายได้หรือเสียประโยชน์อย่างไร",
                correct=signs,
                wrongs=tuple(pair for pair in SIGN_PAIRS if pair != signs),
                hint="ถามทีละฝ่ายว่าฝ่ายนั้นได้ เสีย หรือไม่ได้ไม่เสียประโยชน์ "
                     "แล้วจึงเขียนเป็นคู่",
            )
        if which == 1:
            name, signs, examples = rng.choice(RELATIONSHIPS)
            example = rng.choice(examples)
            return _labelled(
                stem=f"จากการสำรวจพบความสัมพันธ์ต่อไปนี้ในแหล่งที่อยู่เดียวกัน: "
                     f"“{example}” ทั้งสองฝ่ายได้หรือเสียประโยชน์อย่างไร",
                correct=signs,
                wrongs=tuple(pair for pair in SIGN_PAIRS if pair != signs),
                hint="พิจารณาว่าฝ่ายที่ถูกอาศัยหรือถูกแย่งนั้นเสียอะไรไปหรือไม่ "
                     "ถ้าไม่เสียอะไรเลยให้ถือเป็น 0",
            )
        stem, correct, wrongs = self.PREDATION_VS_PARASITISM
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint="ทั้งสองรูปแบบผู้ได้ประโยชน์คือฝ่ายที่กิน ต่างกันที่ระยะเวลาและ"
                 "ผลที่เกิดกับอีกฝ่าย",
        )


@question_type(
    "ecology.relationship_survey_application",
    display_name={"th": "สรุปรูปแบบความสัมพันธ์และผลที่ตามมาจากผลการสำรวจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class RelationshipSurveyApplication(QuestionType):
    """Name the pattern a survey shows *and* say what follows from it.

    Naming alone is Foundation work and `ecology.symbiosis` already covers it.
    Each item here needs the pattern identified before the consequence can be
    predicted, so a learner who picks the right label for the wrong reason still
    lands on a wrong choice.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, RELATIONSHIP_SURVEYS,
            hint="ระบุก่อนว่าแต่ละฝ่ายได้หรือเสียประโยชน์ แล้วจึงคาดการณ์ว่าถ้าฝ่ายหนึ่ง"
                 "หายไป อีกฝ่ายจะเป็นอย่างไร",
            topic=TOPIC,
        )
