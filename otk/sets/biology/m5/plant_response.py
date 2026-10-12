"""สิ่งเร้าภายนอกที่มีผลต่อการเจริญเติบโตของพืช

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/18

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


TOPIC_RESPONSE = "สิ่งเร้าภายนอกที่มีผลต่อการเจริญเติบโตของพืช"


MOVEMENTS = (
    ("โฟโตทรอพิซึม", "ยอดพืชที่ปลูกริมหน้าต่างโค้งเข้าหาแสง"),
    ("กราวิทรอพิซึม", "รากพืชเจริญลงสู่พื้นดินตามแรงโน้มถ่วงแม้วางกระถางตะแคง"),
    ("ทิกโมทรอพิซึม", "มือเกาะของตำลึงพันรอบหลักที่สัมผัส"),
    ("เคโมทรอพิซึม", "หลอดละอองเรณูงอกเข้าหาออวุลตามสารเคมี"),
    ("ทิกโมนาสตี", "ใบไมยราบหุบเมื่อถูกสัมผัส"),
    ("นิคทินาสตี (การเคลื่อนไหวเพื่อการหลับ)", "ใบจามจุรีหุบในตอนเย็นและกางในตอนเช้า"),
    ("โฟโตนาสตี", "ดอกบัวบานเมื่อได้รับแสงตอนเช้าและหุบตอนเย็น"),
)


RESPONSE_HINT = ("ทรอพิซึมมีทิศทางสัมพันธ์กับทิศของสิ่งเร้าและเกิดจากการเจริญ นาสตีไม่ขึ้นกับทิศของสิ่งเร้า "
                 "บางชนิดเกิดจากการเปลี่ยนแรงดันเต่ง เช่น ไมยราบหุบใบ")


RESPONSE_FACTS = (
    ("ลำต้นพืชตอบสนองต่อแรงโน้มถ่วงอย่างไร", "เจริญในทิศตรงข้ามกับแรงโน้มถ่วง (กราวิทรอพิซึมเชิงลบ)",
     ("เจริญตามแรงโน้มถ่วง (กราวิทรอพิซึมเชิงบวก)", "เจริญเข้าหาแสงเท่านั้น (โฟโตทรอพิซึมเชิงบวก) ไม่ตอบสนองต่อแรงโน้มถ่วง", "หุบใบทันทีเมื่อถูกแรงโน้มถ่วง (นาสตีเชิงลบ)")),
    ("รากพืชตอบสนองต่อแรงโน้มถ่วงอย่างไร", "เจริญลงตามแรงโน้มถ่วง (กราวิทรอพิซึมเชิงบวก)",
     ("เจริญขึ้นสวนแรงโน้มถ่วง (กราวิทรอพิซึมเชิงลบ)", "ไม่ตอบสนองต่อแรงโน้มถ่วง แต่เจริญตามทิศทางของน้ำ", "เจริญเข้าหาแสงเท่านั้น")),
    ("การหุบใบของไมยราบเมื่อถูกสัมผัสเกิดจากอะไร", "เซลล์บริเวณโคนก้านใบสูญเสียน้ำ แรงดันเต่งลดลง",
     ("เซลล์แบ่งตัวเพิ่มขึ้นอย่างรวดเร็ว", "ออกซินสะสมที่ปลายใบ ทำให้ใบเจริญโค้งงอลง", "เซลล์บริเวณโคนก้านใบได้รับน้ำมากขึ้น แรงดันเต่งเพิ่มขึ้น")),
    ("ความแตกต่างสำคัญระหว่างทรอพิซึมกับนาสตีคือข้อใด", "ทรอพิซึมมีทิศทางสัมพันธ์กับทิศของสิ่งเร้า นาสตีไม่สัมพันธ์กับทิศของสิ่งเร้า",
     ("ทรอพิซึมเกิดเฉพาะกับราก ส่วนนาสตีเกิดเฉพาะกับใบและดอกของพืช", "นาสตีเกิดจากการเจริญเสมอ ทรอพิซึมไม่เกิดจากการเจริญ",
      "ทรอพิซึมเกิดเฉพาะกับสิ่งเร้าที่เป็นแสง ส่วนนาสตีเกิดกับสิ่งเร้าทุกชนิด")),
    ("พืชวันสั้นออกดอกเมื่อใด", "เมื่อได้รับช่วงมืดต่อเนื่องยาวกว่าช่วงมืดวิกฤต",
     ("เมื่อได้รับช่วงมืดสั้นกว่าช่วงมืดวิกฤต", "เมื่อได้รับช่วงสว่างต่อเนื่องยาวกว่าช่วงมืดวิกฤต", "เมื่อได้รับแสงตลอด 24 ชั่วโมงโดยไม่มีช่วงมืดเลย")),
)


PHOTOPERIOD = {"พืชวันสั้น": ("เบญจมาศ", "คริสต์มาส", "ข้าวบางพันธุ์", "ถั่วเหลือง"),
               "พืชวันยาว": ("ผักกาดหอม", "ข้าวสาลี", "ผักโขม", "แรดิช"),
               "พืชที่ไม่ตอบสนองต่อช่วงแสง": ("มะเขือเทศ", "ทานตะวัน", "ข้าวโพด", "แตงกวา")}


@question_type(
    "biology.plant_response_foundation",
    display_name={"th": "ชนิดการตอบสนองของพืชต่อสิ่งเร้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RESPONSE,
)
class PlantResponseFoundation(QuestionType):
    """Name the movement from an example, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, example = rng.choice(MOVEMENTS)
        others = rng.sample([m for m in MOVEMENTS if m[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{example}\" เป็นการตอบสนองแบบใด", correct=name, wrongs=tuple(m[0] for m in others),
                             topic=TOPIC_RESPONSE, hint=RESPONSE_HINT)
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{name}", correct=example, wrongs=tuple(m[1] for m in others), topic=TOPIC_RESPONSE,
                         hint=RESPONSE_HINT)


@question_type(
    "biology.plant_response_fluency",
    display_name={"th": "ทิศทางการตอบสนองและการตอบสนองต่อช่วงแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RESPONSE,
)
class PlantResponseFluency(QuestionType):
    """Positive or negative tropism, and short-day against long-day plants."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            kind = rng.choice(sorted(PHOTOPERIOD))
            plant = rng.choice(PHOTOPERIOD[kind])
            others = [k for k in PHOTOPERIOD if k != kind]
            if rng.random() < 0.5:
                return _labelled(stem=f"{plant}จัดเป็นพืชประเภทใดตามการตอบสนองต่อช่วงแสง", correct=kind,
                                 wrongs=(*others, "พืชที่ออกดอกเฉพาะในที่มืด"), topic=TOPIC_RESPONSE, hint=RESPONSE_HINT)
            pool = [p for k in others for p in PHOTOPERIOD[k]]
            return _labelled(stem=f"ข้อใดเป็น{kind}", correct=plant, wrongs=tuple(pool), topic=TOPIC_RESPONSE,
                             hint="พืชวันสั้นต้องการช่วงมืดยาว เช่น เบญจมาศ พืชวันยาวต้องการช่วงมืดสั้น เช่น ผักกาดหอม")
        stem, right, wrongs = rng.choice(RESPONSE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_RESPONSE, hint=RESPONSE_HINT)


@question_type(
    "biology.plant_response_application",
    display_name={"th": "ทำนายการออกดอกจากช่วงมืดและช่วงมืดวิกฤต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RESPONSE,
)
class PlantResponseApplication(QuestionType):
    """What counts is the longest unbroken dark span, not the day length."""
    max_choices = 2  # a bare yes/no label: fillers only padded it to four

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(("พืชวันสั้น", "พืชวันยาว"))
        plant = rng.choice(PHOTOPERIOD[kind])
        critical = rng.randint(9, 14)
        night = rng.randint(6, 16)
        while night == critical:
            night = rng.randint(6, 16)
        flash = rng.random() < 0.35 and night >= 8
        longest = night / 2 if flash else night
        long_enough = longest > critical
        flowers = long_enough if kind == "พืชวันสั้น" else not long_enough
        setup = f"ได้รับแสง {24 - night} ชั่วโมงและมืด {night} ชั่วโมงต่อวัน" + (" โดยเปิดไฟสว่างสั้น ๆ ตรงกลางช่วงมืด" if flash else "")
        return _labelled(stem=f"{plant}เป็น{kind}ที่มีช่วงมืดวิกฤต {critical} ชั่วโมง ถ้าปลูกให้{setup} พืชจะออกดอกหรือไม่",
                         correct="ออกดอก" if flowers else "ไม่ออกดอก",
                         wrongs=("ไม่ออกดอก" if flowers else "ออกดอก",),
                         topic=TOPIC_RESPONSE,
                         hint="พืชวันสั้นออกดอกเมื่อช่วงมืดต่อเนื่องยาวกว่าช่วงมืดวิกฤต พืชวันยาวออกดอกเมื่อช่วงมืดสั้นกว่า "
                              "การเปิดไฟกลางช่วงมืดทำให้ช่วงมืดต่อเนื่องสั้นลงครึ่งหนึ่ง")
