"""การกินอาหารของไฮดราและพลานาเรีย

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/2

Sets moved here from: science_wave_f59.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f59 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_HYDRA = "การกินอาหารของไฮดราและพลานาเรีย"


HYDRA = ("ใช้หนวดที่มีเซลล์เข็มพิษ (ไนโดไซต์) จับเหยื่อ", "ส่งอาหารเข้าทางปากสู่ช่องแกสโตรวาสคิวลาร์",
         "เซลล์ต่อมหลั่งเอนไซม์ย่อยอาหารในช่องแกสโตรวาสคิวลาร์ก่อน แล้วเซลล์บุช่องจึงนำเข้าไปย่อยต่อภายในเซลล์",
         "กากอาหารถูกขับออกทางปาก")


PLANARIA = ("ยื่นคอหอยออกทางด้านล่างกลางลำตัวเพื่อดูดอาหาร", "ช่องแกสโตรวาสคิวลาร์แตกแขนงไปทั่วลำตัว",
            "ย่อยอาหารนอกเซลล์ก่อน แล้วเซลล์บุทางเดินอาหารนำเข้าไปย่อยต่อภายในเซลล์", "กากอาหารถูกขับออกทางคอหอย")


NEITHER = ("มีทวารหนักแยกจากปาก กากอาหารจึงออกทางด้านท้าย", "มีฟันบดอาหารก่อนส่งเข้าช่องแกสโตรวาสคิวลาร์", "มีกึ๋นบดอาหาร", "ย่อยอาหารในกระเพาะสี่ห้องแบบสัตว์เคี้ยวเอื้อง", "ดูดซึมอาหารด้วยวิลลัสที่บุลำไส้เล็กทั้งลำตัว")


FEED_HINT = ("ไฮดราจับเหยื่อด้วยหนวดที่มีเข็มพิษ พลานาเรียยื่นคอหอยออกจากด้านล่างลำตัว ทั้งคู่มีช่องแกสโตรวาสคิวลาร์ "
             "ย่อยนอกเซลล์แล้วต่อภายในเซลล์ และขับกากออกทางช่องเดิม")


@question_type(
    "biology.hydra_planaria_foundation",
    display_name={"th": "การกินและการย่อยอาหารของไฮดรา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HYDRA,
)
class HydraPlanariaFoundation(QuestionType):
    """How Hydra catches, digests and gets rid of food."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        right = rng.choice(HYDRA)
        wrongs = rng.sample([p for p in PLANARIA[:2]] + list(NEITHER), 3)
        if rng.random() < 0.3:
            order = list(HYDRA)
            shuffled: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(shuffled) < 3:
                o = order[:]
                rng.shuffle(o)
                if o != order:
                    shuffled[" → ".join(x.split(" ")[0] for x in o)] = None
            return _labelled(stem="ข้อใดเรียงขั้นตอนการกินอาหารของไฮดราได้ถูกต้อง", correct=" → ".join(x.split(" ")[0] for x in order),
                             wrongs=tuple(shuffled), topic=TOPIC_HYDRA, hint=FEED_HINT)
        return _labelled(stem="ข้อใดเป็นลักษณะการกินหรือการย่อยอาหารของไฮดรา", correct=right, wrongs=tuple(wrongs), topic=TOPIC_HYDRA,
                         hint=FEED_HINT)


@question_type(
    "biology.hydra_planaria_fluency",
    display_name={"th": "การกินและการย่อยอาหารของพลานาเรีย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HYDRA,
)
class HydraPlanariaFluency(QuestionType):
    """How a planarian feeds through its pharynx."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        right = rng.choice(PLANARIA)
        wrongs = rng.sample([HYDRA[0]] + list(NEITHER), 3)
        return _labelled(stem="ข้อใดเป็นลักษณะการกินหรือการย่อยอาหารของพลานาเรีย", correct=right, wrongs=tuple(wrongs), topic=TOPIC_HYDRA,
                         hint=FEED_HINT)


@question_type(
    "biology.hydra_planaria_application",
    display_name={"th": "เปรียบเทียบการกินอาหารของไฮดราและพลานาเรีย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HYDRA,
)
class HydraPlanariaApplication(QuestionType):
    """Which animal a statement fits: Hydra, planarian, both, or neither."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        groups = {"ไฮดราเท่านั้น": (HYDRA[0], "กินไรน้ำและสัตว์เล็ก ๆ ที่ยังมีชีวิตโดยใช้หนวดจับ"),
                  "พลานาเรียเท่านั้น": (*PLANARIA[:2], "ในห้องปฏิบัติการกินตับหรือไข่แดงต้มสุกชิ้นเล็ก ๆ ได้"),
                  "ทั้งไฮดราและพลานาเรีย": ("มีทางเดินอาหารที่มีช่องเปิดทางเดียว", "ย่อยอาหารทั้งภายนอกและภายในเซลล์",
                                          "ขับกากอาหารออกทางช่องเดียวกับที่รับอาหารเข้า"),
                  "ไม่ใช่ทั้งสองชนิด": NEITHER}
        options = tuple(groups)
        answer = rng.choice(options)
        if rng.random() < 0.5:
            others = [s for k, ss in groups.items() if k != answer for s in ss]
            where = {"ไฮดราเท่านั้น": "พบเฉพาะในไฮดรา", "พลานาเรียเท่านั้น": "พบเฉพาะในพลานาเรีย",
                     "ทั้งไฮดราและพลานาเรีย": "พบทั้งในไฮดราและพลานาเรีย", "ไม่ใช่ทั้งสองชนิด": "ไม่พบทั้งในไฮดราและพลานาเรีย"}[answer]
            return _labelled(stem=f"ข้อใดเป็นลักษณะที่{where}", correct=rng.choice(groups[answer]), wrongs=tuple(others),
                             topic=TOPIC_HYDRA, hint=FEED_HINT)
        statement = rng.choice(groups[answer])
        return _labelled(stem=f"จากการสังเกตการกินอาหาร ลักษณะ \"{statement}\" พบในสัตว์ใด", correct=answer,
                         wrongs=tuple(o for o in options if o != answer), topic=TOPIC_HYDRA, hint=FEED_HINT)
