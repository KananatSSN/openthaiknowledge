"""วัฏจักรชีวิตแบบสลับของพืชดอก

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/13

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


TOPIC_CYCLE = "วัฏจักรชีวิตแบบสลับของพืชดอก"


STAGES = (
    ("สปอโรไฟต์", "2n", "ต้นพืชดอกที่เราเห็นทั่วไป"),
    ("สปอร์ (n)", "n", "ไมโครสปอร์และเมกะสปอร์"),
    ("แกมีโทไฟต์", "n", "ละอองเรณูที่งอกแล้วและถุงเอ็มบริโอ"),
    ("แกมีต (n)", "n", "สเปิร์มนิวเคลียสและเซลล์ไข่"),
    ("ไซโกต", "2n", "เซลล์ที่ได้จากการปฏิสนธิระหว่างสเปิร์มกับเซลล์ไข่"),
)


TRANSITIONS = (
    ("สปอโรไฟต์", "สปอร์ (n)", "ไมโอซิส"), ("สปอร์ (n)", "แกมีโทไฟต์", "ไมโทซิส"), ("แกมีโทไฟต์", "แกมีต (n)", "ไมโทซิส"),
    ("แกมีต (n)", "ไซโกต", "การปฏิสนธิ"), ("ไซโกต", "สปอโรไฟต์", "ไมโทซิส"),
)


CYCLE_HINT = ("สปอโรไฟต์ (2n) แบ่งแบบไมโอซิสได้สปอร์ (n) สปอร์แบ่งแบบไมโทซิสเป็นแกมีโทไฟต์ (n) ซึ่งสร้างแกมีต (n) "
              "แกมีตปฏิสนธิได้ไซโกต (2n) เจริญเป็นสปอโรไฟต์ พืชดอกมีสปอโรไฟต์เด่น")


CYCLE_FACTS = (
    ("ในพืชดอก ระยะใดเด่นและมีอายุยาวนานกว่า", "สปอโรไฟต์", ("แกมีโทไฟต์", "สปอร์ (n)", "แกมีต (n)")),
    ("ในมอส ระยะใดเป็นต้นที่เห็นเด่นชัด", "แกมีโทไฟต์", ("สปอโรไฟต์", "ไซโกต", "เอ็มบริโอ")),
    ("แกมีโทไฟต์เพศผู้ของพืชดอกคืออะไร", "ละอองเรณูที่มีทิวบ์นิวเคลียสและเจเนอเรทิฟเซลล์หรือสเปิร์ม",
     ("อับเรณูทั้งอันที่มีไมโครสปอร์มาเทอร์เซลล์อยู่ภายใน", "ไมโครสปอร์มาเทอร์เซลล์", "ไมโครสปอร์มาเทอร์เซลล์ที่ยังไม่แบ่งตัวแบบไมโอซิส")),
    ("แกมีโทไฟต์เพศเมียของพืชดอกคืออะไร", "ถุงเอ็มบริโอ", ("ออวุลทั้งหมด", "รังไข่", "เมกะสปอร์มาเทอร์เซลล์")),
    ("เหตุใดจึงเรียกว่าวัฏจักรชีวิตแบบสลับ", "มีระยะสปอโรไฟต์ (2n) และแกมีโทไฟต์ (n) สลับกันในวัฏจักร",
     ("พืชสลับออกดอกปีเว้นปี", "พืชสลับกันออกดอกเพศผู้และเพศเมียในแต่ละฤดู", "มีระยะแกมีโทไฟต์ (2n) และสปอโรไฟต์ (n) สลับกันในวัฏจักร")),
    ('ในเฟิร์น ต้นที่มีใบขนาดใหญ่ที่เราเห็นทั่วไปเป็นระยะใด', 'สปอโรไฟต์',
     ('แกมีโทไฟต์', 'ไซโกต', 'สปอร์ (n)')),
    ('โพรแทลลัสของเฟิร์นที่มีรูปร่างคล้ายหัวใจเป็นระยะใด', 'แกมีโทไฟต์',
     ('สปอโรไฟต์', 'เอ็มบริโอ', 'ไซโกต')),
    ('สปอร์ของพืชเกิดจากการแบ่งเซลล์แบบใด', 'ไมโอซิสของเซลล์ในสปอโรไฟต์',
     ('ไมโทซิสของเซลล์ในแกมีโทไฟต์', 'การปฏิสนธิระหว่างแกมีตสองเซลล์', 'ไมโทซิสของไซโกตในออวุล')),
    ('แกมีตของพืชเกิดจากการแบ่งเซลล์แบบใด', 'ไมโทซิสของเซลล์ในแกมีโทไฟต์',
     ('ไมโอซิสของเซลล์ในสปอโรไฟต์', 'ไมโอซิสของเซลล์ในแกมีโทไฟต์', 'การปฏิสนธิระหว่างสปอร์สองเซลล์')),
)


STRUCTURE_PLOIDY = (("เซลล์ใบ", 2), ("ไมโครสปอร์มาเทอร์เซลล์", 2), ("ไมโครสปอร์", 1), ("ทิวบ์นิวเคลียสของละอองเรณู", 1),
                    ("สเปิร์มนิวเคลียส", 1), ("เมกะสปอร์", 1), ("เซลล์ไข่", 1), ("แอนติโพดัล", 1), ("ไซโกต", 2),
                    ("เอนโดสเปิร์ม", 3), ("เปลือกเมล็ด", 2), ("เอ็มบริโอในเมล็ด", 2))


@question_type(
    "biology.plant_life_cycle_foundation",
    display_name={"th": "ระยะต่าง ๆ ในวัฏจักรชีวิตแบบสลับ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CYCLE,
)
class PlantLifeCycleFoundation(QuestionType):
    """Each stage's ploidy and the step that makes the next."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            src, dst, how = rng.choice(TRANSITIONS)
            return _labelled(stem=f"ในวัฏจักรชีวิตแบบสลับ {src}เปลี่ยนเป็น{dst}ด้วยกระบวนการใด", correct=how,
                             wrongs=tuple(x for x in ("ไมโอซิส", "ไมโทซิส", "การปฏิสนธิ", "การแตกหน่อ") if x != how)[:3],
                             topic=TOPIC_CYCLE, hint=CYCLE_HINT)
        name, ploidy, example = rng.choice(STAGES)
        if roll < 0.7:
            return _labelled(stem=f"{name}ในวัฏจักรชีวิตของพืชดอกมีชุดโครโมโซมแบบใด", correct=ploidy,
                             wrongs=tuple(x for x in ("n", "2n", "3n", "4n") if x != ploidy), topic=TOPIC_CYCLE, hint=CYCLE_HINT)
        others = rng.sample([s for s in STAGES if s[0] != name], 3)
        return _labelled(stem=f"ในพืชดอก ข้อใดเป็น{name}", correct=example, wrongs=tuple(s[2] for s in others), topic=TOPIC_CYCLE,
                         hint=CYCLE_HINT)


@question_type(
    "biology.plant_life_cycle_fluency",
    display_name={"th": "แกมีโทไฟต์และสปอโรไฟต์ในพืชดอกและพืชอื่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CYCLE,
)
class PlantLifeCycleFluency(QuestionType):
    """Which generation dominates, and where each hides in a flower."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(CYCLE_FACTS)
        pool = [w for _, r, ws in CYCLE_FACTS for w in (r, *ws) if w != right and w not in wrongs]
        return _labelled(stem=stem, correct=right, wrongs=(*rng.sample(wrongs, 2), rng.choice(pool)), topic=TOPIC_CYCLE, hint=CYCLE_HINT)


@question_type(
    "biology.plant_life_cycle_application",
    display_name={"th": "จำนวนโครโมโซมในโครงสร้างต่าง ๆ ของพืชดอก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CYCLE,
)
class PlantLifeCycleApplication(QuestionType):
    """n, 2n or 3n, times the haploid number."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        plant, diploid = rng.choice((("ข้าว", 24), ("ข้าวโพด", 20), ("ถั่วลันเตา", 14), ("มะเขือเทศ", 24), ("หอมหัวใหญ่", 16),
                                     ("พืชชนิดหนึ่ง", rng.randrange(8, 41, 2))))
        name, sets = rng.choice(STRUCTURE_PLOIDY)
        n = diploid // 2
        return numeric(stem=f"{plant}มีโครโมโซม 2n = {diploid} {name}มีโครโมโซมกี่แท่ง", answer=n * sets,
                       wrongs=[n * s for s in (1, 2, 3) if s != sets] + [diploid * 2], unit="แท่ง", topic=TOPIC_CYCLE,
                       hint="สปอโรไฟต์และไซโกตเป็น 2n สปอร์ แกมีโทไฟต์ และแกมีตเป็น n เอนโดสเปิร์มเป็น 3n เปลือกเมล็ดมาจากต้นแม่ (2n)")
