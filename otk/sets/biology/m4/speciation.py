"""การเกิดสปีชีส์ใหม่

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/15

Sets moved here from: science_wave_f52.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f52 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_SPEC = "การเกิดสปีชีส์ใหม่"


ISOLATION = (
    ("การแยกกันทางแหล่งที่อยู่", "ก่อนการปฏิสนธิ", "กบสองชนิดชนิดหนึ่งอาศัยในลำธาร อีกชนิดอาศัยในบ่อน้ำนิ่ง จึงไม่พบกัน"),
    ("การแยกกันทางฤดูผสมพันธุ์", "ก่อนการปฏิสนธิ", "พืชสองชนิดออกดอกในฤดูต่างกัน ละอองเรณูจึงไม่ไปถึงดอกของอีกชนิด"),
    ("การแยกกันทางพฤติกรรม", "ก่อนการปฏิสนธิ", "นกสองชนิดมีเสียงร้องเกี้ยวพาราสีต่างกัน ตัวเมียจึงไม่ตอบสนองตัวผู้อีกชนิด"),
    ("การแยกกันทางโครงสร้างของอวัยวะสืบพันธุ์", "ก่อนการปฏิสนธิ", "แมลงสองชนิดมีอวัยวะสืบพันธุ์รูปร่างไม่เข้ากัน จึงผสมพันธุ์ไม่ได้"),
    ("การแยกกันทางเซลล์สืบพันธุ์", "ก่อนการปฏิสนธิ", "อสุจิของเม่นทะเลชนิดหนึ่งไม่สามารถเจาะเข้าไข่ของอีกชนิดได้"),
    ("ลูกผสมตายก่อนสืบพันธุ์", "หลังการปฏิสนธิ", "ลูกผสมระหว่างแพะกับแกะส่วนใหญ่ตายตั้งแต่ระยะเอ็มบริโอ"),
    ("ลูกผสมเป็นหมัน", "หลังการปฏิสนธิ", "ล่อซึ่งเกิดจากม้ากับลาเจริญเติบโตได้แต่ให้กำเนิดลูกไม่ได้"),
    ("ลูกผสมรุ่นหลังอ่อนแอ", "หลังการปฏิสนธิ", "ลูกผสมรุ่นแรกของฝ้ายสองชนิดแข็งแรง แต่รุ่นต่อมาอ่อนแอและเป็นหมัน"),
)


SPEC_FACTS = (
    ("ตามแนวคิดสปีชีส์ทางชีววิทยา สิ่งมีชีวิตสปีชีส์เดียวกันหมายถึงข้อใด", "ผสมพันธุ์กันได้ในธรรมชาติและได้ลูกที่ไม่เป็นหมัน",
     ("มีรูปร่างหน้าตาเหมือนกันทุกประการ", "อาศัยอยู่ในแหล่งเดียวกันและกินอาหารชนิดเดียวกัน", "กินอาหารชนิดเดียวกัน", "ผสมพันธุ์กันได้แต่ลูกเป็นหมันทุกตัว")),
    ("การเกิดสปีชีส์ใหม่แบบแยกกันทางภูมิศาสตร์ (allopatric) เกิดอย่างไร", "ประชากรถูกแบ่งด้วยสิ่งกีดขวาง เช่น ภูเขาหรือทะเล จนสะสมความแตกต่างและผสมพันธุ์กันไม่ได้",
     ("ประชากรในพื้นที่เดียวกันเกิดพอลิพลอยดีทันที จนผสมพันธุ์กับกลุ่มเดิมไม่ได้", "สมาชิกทุกตัวกลายพันธุ์พร้อมกัน", "ประชากรสองกลุ่มอพยพมารวมกัน",
      "สมาชิกฝึกใช้อวัยวะบ่อยจนลักษณะเปลี่ยน แล้วถ่ายทอดลักษณะนั้นสู่ลูกจนต่างจากประชากรเดิม")),
    ("การเกิดสปีชีส์ใหม่ในพื้นที่เดียวกัน (sympatric) ที่พบบ่อยในพืชเกิดจากอะไร", "พอลิพลอยดี ทำให้ผสมกับพันธุ์เดิมแล้วได้ลูกเป็นหมัน",
     ("ภูเขาเกิดขึ้นกั้นกลางประชากร จนผสมพันธุ์กันไม่ได้", "แม่น้ำเปลี่ยนเส้นทาง", "การอพยพข้ามทวีป", "ทะเลแยกประชากรออกเป็นสองเกาะที่อยู่ห่างกันมาก")),
    ("นกฟินช์ของดาร์วินบนหมู่เกาะกาลาปากอสเป็นตัวอย่างของอะไร", "การแผ่ขยายพันธุ์ของบรรพบุรุษร่วมกันไปเป็นหลายสปีชีส์ตามแหล่งอาหาร",
     ("การที่ทุกเกาะมีนกสปีชีส์เดียวกันเพราะนกบินข้ามเกาะได้", "ลักษณะที่ได้มาใหม่ เช่น จะงอยปากที่ใช้บ่อย ถ่ายทอดสู่ลูกตามแนวคิดลามาร์ก", "ลูกผสมที่เป็นหมัน",
      "การคัดเลือกพันธุ์นกโดยมนุษย์")),
)


ROUTES = {
    "แบบแยกกันทางภูมิศาสตร์ (allopatric)": ("ประชากรกระรอกถูกแบ่งด้วยหุบเขาลึกจนกลายเป็นสองสปีชีส์",
                                             "ปลาในทะเลสาบที่ถูกแยกเป็นสองแอ่งเมื่อระดับน้ำลด จนผสมพันธุ์กันไม่ได้",
                                             "นกที่อพยพไปอยู่คนละเกาะจนมีลักษณะและเสียงร้องต่างกันและผสมพันธุ์กันไม่ได้"),
    "แบบในพื้นที่เดียวกัน (sympatric)": ("พืชที่จำนวนโครโมโซมเพิ่มเป็น 4n ผสมกับต้น 2n เดิมในแปลงเดียวกันแล้วได้ลูกเป็นหมัน",
                                         "แมลงกลุ่มหนึ่งเปลี่ยนไปวางไข่บนพืชอาหารชนิดใหม่ในพื้นที่เดิมจนไม่ผสมกับกลุ่มเดิม",
                                         "ข้าวสาลีที่เกิดจากลูกผสมของหญ้าต่างชนิดแล้วเพิ่มจำนวนชุดโครโมโซม"),
}


NOT_SPECIATION = ("สุนัขพันธุ์ต่าง ๆ ที่มนุษย์คัดเลือกยังผสมพันธุ์กันได้ลูกที่ไม่เป็นหมัน",
                  "ประชากรนกกลุ่มเดียวอพยพไปทางใต้ในฤดูหนาวแล้วกลับมาผสมพันธุ์ในที่เดิม",
                  "ปลาในบ่อเดียวกันมีสีลำตัวต่างกันเล็กน้อยแต่ผสมพันธุ์กันได้ตามปกติ")


SPEC_HINT = ("กลไกก่อนการปฏิสนธิกันไม่ให้ผสมพันธุ์หรือไม่ให้เกิดไซโกต กลไกหลังการปฏิสนธิทำให้ลูกผสมตาย เป็นหมัน หรืออ่อนแอ "
             "สปีชีส์ใหม่เกิดเมื่อประชากรแยกกันทางการสืบพันธุ์")


PLANTS = ("พืชชนิด ก", "พืชชนิด ข", "พืชชนิด ค", "พืชชนิด ง")


@question_type(
    "biology.speciation_foundation",
    display_name={"th": "ความหมายของสปีชีส์และรูปแบบการเกิดสปีชีส์ใหม่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SPEC,
)
class SpeciationFoundation(QuestionType):
    """The biological species, and the routes to a new one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            kind = rng.choice(sorted(ROUTES))
            other = next(k for k in ROUTES if k != kind)
            if rng.random() < 0.5:
                return _labelled(stem=f"ข้อใดเป็นตัวอย่างการเกิดสปีชีส์ใหม่{kind}", correct=rng.choice(ROUTES[kind]),
                                 wrongs=(*rng.sample(ROUTES[other], 2), rng.choice(NOT_SPECIATION)), topic=TOPIC_SPEC, hint=SPEC_HINT)
            return _labelled(stem=f"\"{rng.choice(ROUTES[kind])}\" เป็นการเกิดสปีชีส์ใหม่แบบใด", correct=kind,
                             wrongs=(other, "ไม่ใช่การเกิดสปีชีส์ใหม่", "การคัดเลือกพันธุ์โดยมนุษย์"), topic=TOPIC_SPEC, hint=SPEC_HINT)
        stem, right, wrongs = rng.choice(SPEC_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SPEC, hint=SPEC_HINT)


@question_type(
    "biology.speciation_fluency",
    display_name={"th": "กลไกการแยกกันทางการสืบพันธุ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SPEC,
)
class SpeciationFluency(QuestionType):
    """Name the barrier, or say which side of fertilisation it acts on."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, when, case = rng.choice(ISOLATION)
        if rng.random() < 0.3:
            return _labelled(stem=f"\"{case}\" เป็นกลไกแยกกันทางการสืบพันธุ์ระยะใด", correct=f"กลไก{when}",
                             wrongs=(f"กลไก{'หลังการปฏิสนธิ' if when == 'ก่อนการปฏิสนธิ' else 'ก่อนการปฏิสนธิ'}",
                                     "ไม่ใช่กลไกแยกกันทางการสืบพันธุ์", "เป็นการคัดเลือกโดยมนุษย์"), topic=TOPIC_SPEC, hint=SPEC_HINT)
        others = rng.sample([i for i in ISOLATION if i[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{case}\" เป็นกลไกแยกกันทางการสืบพันธุ์แบบใด", correct=name,
                             wrongs=tuple(i[0] for i in others), topic=TOPIC_SPEC, hint=SPEC_HINT)
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{name}", correct=case, wrongs=tuple(i[2] for i in others), topic=TOPIC_SPEC,
                         hint=SPEC_HINT)


@question_type(
    "biology.speciation_application",
    display_name={"th": "จำนวนโครโมโซมในการเกิดสปีชีส์ใหม่ด้วยพอลิพลอยดี"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SPEC,
)
class SpeciationApplication(QuestionType):
    """A hybrid gets n from each parent; doubling it makes a fertile new species."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.sample(range(4, 31, 2), 2)
        x, y = rng.sample(PLANTS, 2)
        hybrid = a // 2 + b // 2
        intro = f"{x} มีโครโมโซม 2n = {a} ผสมกับ{y} ซึ่งมี 2n = {b}"
        kind = rng.randrange(4)
        hint = "ลูกผสมได้ n จากแต่ละพ่อแม่ ลูกผสมเป็นหมันเพราะโครโมโซมไม่มีคู่ เมื่อจำนวนโครโมโซมเพิ่มเป็น 2 เท่าจะมีคู่และสืบพันธุ์ได้"
        if kind == 0:
            return numeric(stem=f"{intro} ลูกผสมมีโครโมโซมในเซลล์ร่างกายกี่แท่ง", answer=hybrid, wrongs=[a + b, hybrid * 2, abs(a - b) or 2],
                           unit="แท่ง", topic=TOPIC_SPEC, hint=hint)
        if kind == 1:
            return numeric(stem=f"{intro} ได้ลูกผสมที่เป็นหมัน ต่อมาจำนวนโครโมโซมของลูกผสมเพิ่มเป็น 2 เท่าจนสืบพันธุ์ได้ "
                                f"พืชสปีชีส์ใหม่นี้มีโครโมโซมในเซลล์ร่างกายกี่แท่ง", answer=hybrid * 2, wrongs=[hybrid, hybrid * 4, a * 2],
                           unit="แท่ง", topic=TOPIC_SPEC, hint=hint)
        if kind == 2:
            return numeric(stem=f"{intro} ลูกผสมที่เพิ่มจำนวนโครโมโซมเป็น 2 เท่าแล้ว สร้างเซลล์สืบพันธุ์ที่มีโครโมโซมกี่แท่ง",
                           answer=hybrid, wrongs=[hybrid // 2 or hybrid + 1, hybrid * 2, a // 2], unit="แท่ง", topic=TOPIC_SPEC, hint=hint)
        return _labelled(stem=f"{intro} ได้ลูกผสมที่มีโครโมโซม {hybrid} แท่ง เหตุใดลูกผสมนี้จึงเป็นหมัน",
                         correct="โครโมโซมจากพ่อและแม่ไม่เป็นคู่เหมือนกัน จึงเข้าคู่กันไม่ได้ในไมโอซิส",
                         wrongs=("ลูกผสมไม่มีโครโมโซมเลย", "ลูกผสมมีจำนวนโครโมโซมมากเกินไป 2 เท่า", "ลูกผสมได้รับโครโมโซมจากแม่เท่านั้น"),
                         topic=TOPIC_SPEC, hint=hint)
