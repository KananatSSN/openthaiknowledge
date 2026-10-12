"""ภูมิศาสตร์กับความหลากหลายของไบโอม

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.4/1

Sets moved here from: science_wave_b32.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC
from otk.sets._support.science_wave_b32 import BIOME_SCENARIOS

PROVENANCE = Provenance("original")


class Biome(NamedTuple):
    """A biome, where one is found, what grows there, and why."""
    name: str
    where: str
    vegetation: str
    reason: str


BIOMES = (
    Biome("ป่าดิบชื้น", "ภาคใต้ของประเทศไทยและลุ่มน้ำแอมะซอน",
          "ต้นไม้ใหญ่ไม่ผลัดใบขึ้นหนาแน่นเป็นเรือนยอดหลายชั้น",
          "อยู่ใกล้เส้นศูนย์สูตร ได้รับแสงมากและฝนตกชุกเกือบตลอดปี "
          "พืชจึงเจริญเติบโตได้ตลอดทั้งปี"),
    Biome("ป่าผลัดใบเขตอบอุ่น", "ยุโรปตะวันตกและภาคตะวันออกของสหรัฐอเมริกา",
          "ต้นไม้ใบกว้างที่ทิ้งใบทั้งหมดก่อนเข้าฤดูหนาว",
          "อยู่ละติจูดกลาง มีสี่ฤดูชัดเจน ต้นไม้ทิ้งใบเพื่อลดการสูญเสียน้ำ"
          "ในฤดูหนาวที่น้ำในดินเย็นจัดจนดูดขึ้นไปใช้ได้ยาก"),
    Biome("ป่าสน", "ตอนกลางของแคนาดาและคาบสมุทรสแกนดิเนเวีย",
          "ต้นสนที่มีใบเล็กเรียวคล้ายเข็มและไม่ผลัดใบ",
          "อยู่ละติจูดสูง ฤดูหนาวยาวนานและมีหิมะมาก ใบรูปเข็มเสียน้ำน้อย "
          "และทรงพุ่มรูปกรวยช่วยให้หิมะไหลลงไม่หักกิ่ง"),
    Biome("ทุนดรา", "ชายฝั่งมหาสมุทรอาร์กติกของอะแลสกาและกรีนแลนด์",
          "มอส ไลเคน และไม้พุ่มเตี้ย โดยไม่มีต้นไม้ใหญ่",
          "อยู่ใกล้ขั้วโลก หนาวจัดเกือบตลอดปีและดินชั้นล่างเป็นน้ำแข็งถาวร "
          "รากของต้นไม้ใหญ่จึงหยั่งลึกลงไปไม่ได้"),
    Biome("ทะเลทราย", "ตอนกลางของทวีปออสเตรเลียและตอนเหนือของทวีปแอฟริกา",
          "พืชอวบน้ำ เช่น กระบองเพชร ขึ้นกระจายอยู่ห่าง ๆ",
          "ฝนตกน้อยมากตลอดปี มีเพียงพืชที่เก็บน้ำหรือลดการคายน้ำได้ดีเท่านั้น"
          "ที่อยู่รอด"),
    Biome("ทุ่งหญ้าเขตร้อน", "แอฟริกาตะวันออก เช่น ประเทศเคนยาและแทนซาเนีย",
          "หญ้าเป็นพืชหลัก มีต้นไม้ขึ้นกระจายอยู่ห่าง ๆ",
          "อากาศร้อนแต่ฝนตกเป็นฤดูและมีฤดูแล้งยาว น้ำไม่พอให้ป่าหนาแน่นเจริญได้ "
          "แต่หญ้าที่ฟื้นตัวเร็วหลังฝนมาอยู่ได้"),
)


GEOGRAPHY_FACTS = (
    Fact("เหตุใดเมื่อเดินทางจากเส้นศูนย์สูตรไปทางขั้วโลก จึงพบไบโอมบนบกเปลี่ยนไปเป็นลำดับ",
         "อุณหภูมิลดลงเมื่อละติจูดสูงขึ้น และปริมาณฝนก็เปลี่ยนไป "
         "พืชที่อยู่รอดได้ในแต่ละช่วงจึงต่างกัน"),
    Fact("เหตุใดเมื่อขึ้นไปบนภูเขาสูง จึงพบพืชพรรณเปลี่ยนไปคล้ายการเดินทางไปทางขั้วโลก",
         "อุณหภูมิลดลงเมื่อความสูงจากระดับทะเลเพิ่มขึ้น"),
    Fact("ปัจจัยทางกายภาพหลักที่กำหนดชนิดของไบโอมบนบกคืออะไร",
         "อุณหภูมิและปริมาณน้ำฝนตลอดปี"),
    Fact("เหตุใดบริเวณที่อยู่ละติจูดใกล้เคียงกันจึงอาจเป็นไบโอมต่างชนิดกันได้",
         "เพราะได้รับฝนต่างกัน เช่น ด้านหนึ่งอยู่ติดทะเล "
         "อีกด้านหนึ่งอยู่หลังแนวเขาที่บังฝนไว้"),
    Fact("เหตุใดไบโอมเขตร้อนชื้นจึงมีพืชหลายชนิดมากกว่าไบโอมเขตหนาว",
         "เพราะได้รับพลังงานแสงมากและอุณหภูมิเหมาะสมตลอดปี "
         "พืชจึงเจริญได้ต่อเนื่องและมีช่องทางดำรงชีวิตหลายแบบ"),
    Fact("เหตุใดทะเลทรายใหญ่หลายแห่งของโลกจึงอยู่ใกล้ละติจูด 30 องศา",
         "เพราะอากาศที่แห้งจมตัวลงบริเวณนั้นเป็นประจำ ฝนจึงตกน้อยมาก"),
)


@question_type(
    "ecology.biome_foundation",
    display_name={"th": "ตัวอย่างไบโอมชนิดต่าง ๆ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class BiomeFoundation(QuestionType):
    """Give an example of each biome — by what grows there, or where one is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BIOMES)
        others = [other for other in BIOMES if other.name != item.name]
        rng.shuffle(others)
        hint = "นึกถึงภูมิอากาศของบริเวณนั้นก่อน แล้วค่อยนึกถึงพืชพรรณที่อยู่รอดได้"
        branch = rng.random()
        if branch < 0.4:
            return _labelled(
                stem=f"ไบโอมที่มีพืชพรรณเด่นเป็น{item.vegetation} คือไบโอมใด",
                correct=item.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint=hint, topic=ECOLOGY_TOPIC,
            )
        if branch < 0.7:
            return _labelled(
                stem=f"บริเวณ{item.where} เป็นตัวอย่างของไบโอมใด",
                correct=item.name,
                wrongs=tuple(other.name for other in others[:3]),
                hint=hint, topic=ECOLOGY_TOPIC,
            )
        return _labelled(
            stem=f"ข้อใดเป็นตัวอย่างบริเวณที่พบไบโอม{item.name}",
            correct=item.where,
            wrongs=tuple(other.where for other in others[:3]),
            hint=hint, topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.biome_fluency",
    display_name={"th": "อธิบายภูมิศาสตร์กับความหลากหลายของไบโอม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class BiomeFluency(QuestionType):
    """Explain a biome by the geography and climate that produce it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return _fact_question(
                rng, GEOGRAPHY_FACTS, topic=ECOLOGY_TOPIC,
                hint="ไล่จากตำแหน่งบนโลก ไปสู่อุณหภูมิและฝน แล้วจึงไปสู่พืชพรรณ",
            )
        item = rng.choice(BIOMES)
        others = [other.reason for other in BIOMES if other.name != item.name]
        rng.shuffle(others)
        return _labelled(
            stem=f"เหตุใดไบโอม{item.name}จึงมีพืชพรรณเด่นเป็น{item.vegetation}",
            correct=item.reason, wrongs=tuple(others[:3]),
            hint="ไล่จากตำแหน่งบนโลก ไปสู่อุณหภูมิและฝน แล้วจึงไปสู่พืชพรรณ",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.biome_application",
    display_name={"th": "วิเคราะห์ไบโอมจากข้อมูลภูมิอากาศ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class BiomeApplication(QuestionType):
    """Reason from climate data, altitude or a rain shadow to the biome."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, BIOME_SCENARIOS,
            hint="หาว่าปัจจัยใดจำกัดการเจริญของพืชมากที่สุดในบริเวณนั้น",
        ), ECOLOGY_TOPIC)
