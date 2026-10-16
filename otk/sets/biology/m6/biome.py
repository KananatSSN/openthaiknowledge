"""ไบโอม

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/4

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


TOPIC_BIOME = "ไบโอม"


# (name, rain mm/year range, mean temperature °C range, description)
BIOMES = (
    ("ป่าดิบชื้น", (2000, 4000), (24, 28), "ฝนตกชุกเกือบตลอดปี อากาศร้อนชื้น มีความหลากหลายของสิ่งมีชีวิตสูงที่สุด"),
    ("สะวันนา", (500, 1200), (22, 28), "ทุ่งหญ้าที่มีต้นไม้ขึ้นกระจาย มีฤดูแล้งยาวนาน"),
    ("ทะเลทราย", (20, 200), (15, 30), "ฝนตกน้อยมาก พืชมีใบลดรูปเก็บน้ำได้ เช่น กระบองเพชร"),
    ("ป่าผลัดใบในเขตอบอุ่น", (750, 1500), (6, 14), "มีสี่ฤดูชัดเจน ต้นไม้ทิ้งใบในฤดูหนาว"),
    ("ป่าสน (ไทกา)", (300, 800), (-5, 3), "ฤดูหนาวยาวนานและหนาวจัด ต้นไม้ส่วนใหญ่เป็นสนใบเข็ม"),
    ("ทุนดรา", (100, 250), (-15, -8), "ดินชั้นล่างเป็นน้ำแข็งตลอดปี พืชเป็นมอส ไลเคน และไม้พุ่มเตี้ย"),
)


BIOME_HINT = ("ป่าดิบชื้นร้อนและฝนชุก สะวันนาเป็นทุ่งหญ้ามีฤดูแล้ง ทะเลทรายฝนน้อยมาก ป่าผลัดใบเขตอบอุ่นมีสี่ฤดู "
              "ไทกาเป็นป่าสนเขตหนาว ทุนดรามีดินเยือกแข็งตลอดปี")


ADAPT = (
    ("กระบองเพชรมีใบลดรูปเป็นหนามและลำต้นอวบน้ำ", "ทะเลทราย"), ("ต้นสนมีใบเป็นเข็มเคลือบคิวทินหนา", "ป่าสน (ไทกา)"),
    ("ต้นไม้ทิ้งใบก่อนฤดูหนาวแล้วแตกใบใหม่ในฤดูใบไม้ผลิ", "ป่าผลัดใบในเขตอบอุ่น"), ("ไลเคนและมอสขึ้นบนดินที่เยือกแข็งใต้ผิวดิน", "ทุนดรา"),
    ("ต้นไม้เรียงเป็นหลายชั้นเรือนยอดและมีพืชอิงอาศัยมาก", "ป่าดิบชื้น"), ("ยีราฟและม้าลายกินหญ้าในทุ่งกว้างที่มีต้นไม้ห่าง ๆ", "สะวันนา"),
)


@question_type(
    "biology.biome_foundation",
    display_name={"th": "ลักษณะของไบโอมต่าง ๆ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BIOME,
)
class BiomeFoundation(QuestionType):
    """Name the biome from its description, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, _, _, desc = rng.choice(BIOMES)
        others = rng.sample([b for b in BIOMES if b[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ไบโอมที่ \"{desc}\" คือไบโอมใด", correct=name, wrongs=tuple(b[0] for b in others), topic=TOPIC_BIOME,
                             hint=BIOME_HINT)
        return _labelled(stem=f"ข้อใดเป็นลักษณะของไบโอม{name}", correct=desc, wrongs=tuple(b[3] for b in others), topic=TOPIC_BIOME,
                         hint=BIOME_HINT)


@question_type(
    "biology.biome_fluency",
    display_name={"th": "การปรับตัวของสิ่งมีชีวิตในแต่ละไบโอม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BIOME,
)
class BiomeFluency(QuestionType):
    """Where each adaptation belongs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait, biome = rng.choice(ADAPT)
        others = rng.sample([b[0] for b in BIOMES if b[0] != biome], 3)
        return _labelled(stem=f"\"{trait}\" เป็นลักษณะที่พบในไบโอมใด", correct=biome, wrongs=tuple(others), topic=TOPIC_BIOME, hint=BIOME_HINT)


@question_type(
    "biology.biome_application",
    display_name={"th": "ระบุไบโอมจากข้อมูลภูมิอากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BIOME,
)
class BiomeApplication(QuestionType):
    """Rainfall and temperature drawn inside one biome's band."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, (r_lo, r_hi), (t_lo, t_hi), _ = rng.choice(BIOMES)
        rain = rng.randrange(r_lo, r_hi + 1, 10)
        temp = rng.randint(t_lo, t_hi)
        others = rng.sample([b[0] for b in BIOMES if b[0] != name], 3)
        return _labelled(stem=f"พื้นที่หนึ่งมีปริมาณน้ำฝนเฉลี่ย {rain:,} mm ต่อปี และอุณหภูมิเฉลี่ยทั้งปี {temp} °C น่าจะเป็นไบโอมใด", correct=name,
                         wrongs=tuple(others), topic=TOPIC_BIOME,
                         hint="ปริมาณน้ำฝนบอกความชื้น อุณหภูมิบอกเขตภูมิอากาศ ร้อนและฝนชุกเป็นป่าดิบชื้น หนาวจัดและฝนน้อยเป็นทุนดรา")


# One more adaptation for each biome.
ADAPT = (*ADAPT,
    ("กวางเรนเดียร์อพยพมากินไลเคนในช่วงฤดูร้อนสั้น ๆ บนพื้นที่ที่ดินชั้นล่างเยือกแข็งตลอดปี", "ทุนดรา"),
    ("หนูจิงโจ้ได้น้ำจากเมล็ดพืชที่กินและแทบไม่ต้องดื่มน้ำเลย", "ทะเลทราย"),
    ("เถาวัลย์ไต่ขึ้นลำต้นไม้สูงเพื่อรับแสงเหนือเรือนยอดที่หนาทึบ", "ป่าดิบชื้น"),
    ("หญ้างอกใหม่จากโคนต้นได้เร็วหลังไฟไหม้ทุ่งในฤดูแล้ง", "สะวันนา"),
    ("กระรอกสะสมลูกโอ๊กที่ร่วงในฤดูใบไม้ร่วงไว้กินในฤดูหนาว", "ป่าผลัดใบในเขตอบอุ่น"),
    ("ต้นไม้มีทรงพุ่มเป็นรูปกรวยและกิ่งลู่ลง ให้หิมะไถลตกจากกิ่งได้ง่าย", "ป่าสน (ไทกา)"),
)
