"""การสร้างเซลล์สืบพันธุ์และการปฏิสนธิของพืชดอก

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/14

Sets moved here from: science_wave_f57.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f57 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_GAMETE = "การสร้างเซลล์สืบพันธุ์และการปฏิสนธิของพืชดอก"


GAMETE_STEPS = (
    ("ไมโครสปอร์มาเทอร์เซลล์แบ่งแบบไมโอซิส", "ได้ไมโครสปอร์ 4 เซลล์"),
    ("ไมโครสปอร์แบ่งแบบไมโทซิส 1 ครั้ง", "ได้ละอองเรณูที่มีทิวบ์เซลล์และเจเนอเรทิฟเซลล์"),
    ("เจเนอเรทิฟเซลล์แบ่งแบบไมโทซิส", "ได้สเปิร์ม 2 เซลล์"),
    ("เมกะสปอร์มาเทอร์เซลล์แบ่งแบบไมโอซิส", "ได้เมกะสปอร์ 4 เซลล์ ซึ่ง 3 เซลล์สลายไป"),
    ("นิวเคลียสของเมกะสปอร์ที่เหลือแบ่งแบบไมโทซิส 3 ครั้ง", "ได้ถุงเอ็มบริโอที่มี 8 นิวเคลียส 7 เซลล์"),
)


EMBRYO_SAC = (("เซลล์ไข่", 1, "รวมกับสเปิร์มได้ไซโกต"), ("ซินเนอร์จิด", 2, "อยู่ข้างเซลล์ไข่ ช่วยนำทางละอองเรณู"),
              ("แอนติโพดัล", 3, "อยู่ด้านตรงข้ามกับไมโครไพล์"), ("โพลาร์นิวคลีไอ", 2, "รวมกับสเปิร์มได้เอนโดสเปิร์ม (3n)"))


GAMETE_HINT = ("ละอองเรณู 1 เรณูให้สเปิร์ม 2 เซลล์ ถุงเอ็มบริโอมี เซลล์ไข่ 1 ซินเนอร์จิด 2 แอนติโพดัล 3 และเซลล์กลางที่มีโพลาร์นิวคลีไอ 2 "
               "การปฏิสนธิซ้อน: สเปิร์ม + ไข่ = ไซโกต (2n) สเปิร์ม + โพลาร์นิวคลีไอ = เอนโดสเปิร์ม (3n)")


@question_type(
    "biology.plant_gamete_foundation",
    display_name={"th": "ขั้นตอนการสร้างละอองเรณูและถุงเอ็มบริโอ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GAMETE,
)
class PlantGameteFoundation(QuestionType):
    """Each division, and what it gives."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step, result = rng.choice(GAMETE_STEPS)
        others = rng.sample([s for s in GAMETE_STEPS if s[0] != step], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{step} ได้ผลอย่างไร", correct=result, wrongs=tuple(s[1] for s in others), topic=TOPIC_GAMETE,
                             hint=GAMETE_HINT)
        return _labelled(stem=f"ขั้นตอนใด{result}", correct=step, wrongs=tuple(s[0] for s in others), topic=TOPIC_GAMETE, hint=GAMETE_HINT)


@question_type(
    "biology.plant_gamete_fluency",
    display_name={"th": "เซลล์ในถุงเอ็มบริโอและการปฏิสนธิซ้อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GAMETE,
)
class PlantGameteFluency(QuestionType):
    """The seven cells of the embryo sac, and the two fusions."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, count, role = rng.choice(EMBRYO_SAC)
        others = [e for e in EMBRYO_SAC if e[0] != name]
        roll = rng.random()
        if roll < 0.35:
            return numeric(stem=f"ถุงเอ็มบริโอของพืชดอก 1 ถุงมี{name}กี่{'นิวเคลียส' if name == 'โพลาร์นิวคลีไอ' else 'เซลล์'}", answer=count,
                           wrongs=[e[1] for e in others if e[1] != count] + [8, 4], unit="นิวเคลียส" if name == "โพลาร์นิวคลีไอ" else "เซลล์",
                           topic=TOPIC_GAMETE, hint=GAMETE_HINT)
        if roll < 0.55:
            roles = [e[2] for e in others] + ["งอกเป็นหลอดละอองเรณู", "แบ่งตัวเป็นเปลือกเมล็ด"]
            return _labelled(stem=f"{name}ในถุงเอ็มบริโอมีลักษณะหรือบทบาทใด", correct=role, wrongs=tuple(roles),
                             topic=TOPIC_GAMETE, hint=GAMETE_HINT)
        if roll < 0.75:
            names = [e[0] for e in others] + ["ทิวบ์นิวเคลียส", "ไมโครไพล์"]
            return _labelled(stem=f"ส่วนใดในถุงเอ็มบริโอ{role}", correct=name, wrongs=tuple(names), topic=TOPIC_GAMETE,
                             hint=GAMETE_HINT)
        facts = (("การปฏิสนธิซ้อนของพืชดอกหมายถึงข้อใด", "สเปิร์มหนึ่งรวมกับเซลล์ไข่ อีกสเปิร์มรวมกับโพลาร์นิวคลีไอ",
                  ("สเปิร์มสองเซลล์รวมกับเซลล์ไข่เซลล์เดียว", "เซลล์ไข่สองเซลล์รวมกับสเปิร์มเซลล์เดียว", "ละอองเรณูสองเรณูงอกพร้อมกัน",
                   "ทิวบ์นิวเคลียสรวมกับแอนติโพดัล")),
                 ("เอนโดสเปิร์มของพืชดอกมีชุดโครโมโซมแบบใดและเกิดจากอะไร", "3n เกิดจากสเปิร์มรวมกับโพลาร์นิวคลีไอ 2 นิวเคลียส",
                  ("2n เกิดจากสเปิร์มรวมกับเซลล์ไข่", "n เกิดจากเมกะสปอร์", "3n เกิดจากสเปิร์มสองเซลล์รวมกับเซลล์ไข่", "2n เกิดจากเปลือกออวุล")),
                 ("ทิวบ์นิวเคลียสของละอองเรณูมีหน้าที่อะไร", "ควบคุมการงอกของหลอดละอองเรณูไปยังออวุล",
                  ("รวมกับเซลล์ไข่", "รวมกับโพลาร์นิวคลีไอ", "สร้างเอนโดสเปิร์ม", "สร้างเปลือกเมล็ด")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_GAMETE, hint=GAMETE_HINT)


@question_type(
    "biology.plant_gamete_application",
    display_name={"th": "คำนวณจำนวนละอองเรณู สเปิร์ม และเมล็ด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GAMETE,
)
class PlantGameteApplication(QuestionType):
    """Four pollen per mother cell, two sperm per pollen, one seed per ovule, one pollen per seed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        k = rng.randrange(5, 201)
        cases = (
            (f"ไมโครสปอร์มาเทอร์เซลล์ {k} เซลล์ สร้างละอองเรณูได้กี่เรณู", 4 * k, [k, 2 * k, 8 * k], "เรณู"),
            (f"ไมโครสปอร์มาเทอร์เซลล์ {k} เซลล์ สร้างสเปิร์มได้ทั้งหมดกี่เซลล์", 8 * k, [4 * k, 2 * k, k], "เซลล์"),
            (f"เมกะสปอร์มาเทอร์เซลล์ {k} เซลล์ ได้ถุงเอ็มบริโอกี่ถุง", k, [4 * k, 3 * k, 8 * k], "ถุง"),
            (f"ฝักถั่วฝักหนึ่งมีเมล็ด {k % 12 + 3} เมล็ด ต้องมีละอองเรณูเข้าผสมอย่างน้อยกี่เรณู", k % 12 + 3,
             [2 * (k % 12 + 3), (k % 12 + 3) // 2 or 1, 4 * (k % 12 + 3)], "เรณู"),
            (f"ผลแตงโมผลหนึ่งมีเมล็ด {k} เมล็ด ใช้สเปิร์มในการปฏิสนธิซ้อนทั้งหมดกี่เซลล์", 2 * k, [k, 4 * k, 3 * k], "เซลล์"),
            (f"ต้องการให้เกิดเมล็ด {k} เมล็ด ต้องมีออวุลที่ได้รับการปฏิสนธิอย่างน้อยกี่ออวุล", k, [2 * k, k // 2 or 1, 4 * k], "ออวุล"),
        )
        stem, answer, wrongs, unit = rng.choice(cases)
        return numeric(stem=stem, answer=answer, wrongs=wrongs, unit=unit, topic=TOPIC_GAMETE, hint=GAMETE_HINT)
