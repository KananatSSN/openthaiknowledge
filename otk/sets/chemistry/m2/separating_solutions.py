"""การแยกสารละลาย

เคมี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.2/1, ว 2.1 ม.2/2

Sets moved here from: science_successors, science_wave_a2, substances.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, math, text
from otk.core.distractors import combine, fixed, label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.numeric_scenario import fmt
from otk.sets._support.science_successors import FluencyStage, FoundationStage
from otk.sets._support.science_wave_a2 import CHEMISTRY, MATTER, _question
from otk.sets._support.substances import LEVEL, SUBJECT, TOPIC_SEP
from otk.sets.chemistry.m2.distillation import Distillation
from otk.sets.chemistry.m2.separation import Separation

PROVENANCE = Provenance("original")


SOLUTION_TASKS = (
    ("ต้องการเกลือแกงคืนจากน้ำเกลือ โดยไม่จำเป็นต้องเก็บน้ำไว้ใช้",
     "การระเหยแห้ง เพราะน้ำระเหยไปหมดและเหลือของแข็งที่ละลายอยู่ไว้",
     ("การกลั่นอย่างง่าย เพราะต้องเก็บไอน้ำกลับมาเป็นของเหลว",
      "โครมาโทกราฟีแบบกระดาษ เพราะต้องแยกสารที่มีสีต่างกัน",
      "การสกัดด้วยตัวทำละลาย เพราะเกลือละลายในตัวทำละลายอินทรีย์ได้ดีกว่า")),
    ("ต้องการน้ำบริสุทธิ์คืนจากน้ำเกลือ โดยเก็บน้ำไว้ใช้ด้วย",
     "การกลั่นอย่างง่าย เพราะน้ำกลายเป็นไอแล้วควบแน่นกลับมาเป็นของเหลวที่แยกไว้ได้",
     ("การระเหยแห้ง เพราะได้ทั้งเกลือและน้ำจืดกลับคืนมาพร้อมกันในขั้นตอนเดียว",
      "การกรอง เพราะเกลือที่ละลายอยู่มีขนาดใหญ่กว่ารูกระดาษกรอง จึงค้างบนกระดาษ",
      "การตกผลึก เพราะน้ำจะแยกตัวออกมาเป็นผลึก")),
    ("ต้องการแยกสีผสมอาหารหลายสีที่ปนกันอยู่ในหยดเดียว เพื่อดูว่ามีกี่สี",
     "โครมาโทกราฟีแบบกระดาษ เพราะแต่ละสีเคลื่อนที่ไปกับตัวทำละลายได้ไม่เท่ากัน",
     ("การระเหยแห้ง เพราะสีจะเหลือค้างอยู่ทั้งหมด",
      "การกลั่นอย่างง่าย เพราะแต่ละสีมีจุดเดือดเท่ากันจึงกลั่นออกมาพร้อมกันได้",
      "การกรอง เพราะแต่ละสีมีขนาดอนุภาคต่างกันมาก จึงติดกระดาษกรองคนละชั้น")),
    ("ต้องการสกัดสารสีจากใบไม้ออกมาศึกษา",
     "การสกัดด้วยตัวทำละลาย เพราะสารสีละลายในตัวทำละลายที่เลือกได้ดีกว่าในน้ำ",
     ("การระเหยแห้ง เพราะสารสีจะระเหยออกมาก่อนน้ำ แล้วควบแน่นแยกไว้ได้",
      "การตกผลึก เพราะสารสีจะตกผลึกทันทีที่บดใบไม้",
      "การกรอง เพราะสารสีในใบไม้มีขนาดใหญ่กว่ารูกระดาษกรอง จึงแยกออกจากน้ำได้")),
    ("ต้องการผลึกจุนสีที่บริสุทธิ์ขึ้นจากสารละลายจุนสีที่มีสิ่งเจือปนเล็กน้อย",
     "การตกผลึก เพราะเมื่อสารละลายอิ่มตัวและเย็นลง สารที่ต้องการจะแยกออกมาเป็นผลึกก่อน",
     ("การระเหยแห้ง เพราะสิ่งเจือปนจะระเหยไปพร้อมน้ำ เหลือแต่สารที่ต้องการบริสุทธิ์",
      "โครมาโทกราฟีแบบกระดาษ เพราะผลึกจะเคลื่อนที่ขึ้นไปตามกระดาษ",
      "การกรองสารละลายใส เพราะสิ่งเจือปนที่ละลายอยู่จะติดอยู่บนกระดาษกรอง")),
)


class ChromaSpec(NamedTuple):
    """One drawn chromatogram: how far the solvent ran, and how far each spot did.

    Distances are millimetres measured from the baseline, matching the scale
    drawn down the left of the picture. Spots are listed nearest-first.

    Two constraints keep ``chem.rf_value`` answerable *from the picture* rather
    than from a number printed on it: every distance is a multiple of 5, so it
    lands on a gridline of the drawn scale, and every one divides the solvent
    front into a clean two decimals. That is why the fronts are 50 and 100 —
    at 60 mm a spot at 20 would read off the scale exactly but give Rf 0.333.
    """
    solvent: int                       # ระยะทางที่ตัวทำละลายเคลื่อนที่ (มม.)
    spots: tuple[int, ...]             # ระยะทางของแต่ละสาร, เรียงจากน้อยไปมาก

    @property
    def asset_id(self) -> str:
        return f"chroma_{self.solvent}_{'_'.join(map(str, self.spots))}"

    def label(self, i: int) -> str:
        return chr(ord("A") + i)

    def rf(self, i: int) -> float:
        return self.spots[i] / self.solvent

    @property
    def names(self) -> list[str]:
        return [f"สาร {self.label(i)}" for i in range(len(self.spots))]


CHROMA_SPECS = [ChromaSpec(*t) for t in [
    (50, (10, 25, 40)),
    (50, (5, 20, 35)),
    (50, (15, 30, 45)),
    (50, (10, 35)),
    (50, (5, 20, 30, 45)),
    (100, (20, 50, 80)),
    (100, (25, 55, 90)),
    (100, (15, 45)),
    (100, (30, 60, 85)),
    # Nothing above Rf 0.9: a spot drawn at 0.95 sits on the solvent front line,
    # which reads as a component that ran off the paper rather than a value.
    (100, (10, 40, 65, 90)),
]]


class ChromaType(QuestionType):
    """Base: show a chromatogram from ``CHROMA_SPECS``, ask one thing about it.

    The alt text says only that spots sit at different heights on a strip — it
    never says which is highest, which would answer three of the four asks for a
    screen reader and in a printed worksheet, where an image renders as its alt
    text alone.
    """

    ALT = ("แผนภาพโครมาโทแกรมบนแผ่นกระดาษ แสดงเส้นเริ่มต้น แนวที่ตัวทำละลายเคลื่อนที่ถึง "
           "และจุดสีของสารแต่ละชนิดที่หยุดอยู่ต่างระดับกัน พร้อมสเกลเป็นมิลลิเมตร")

    def _stem(self, spec: ChromaSpec, prompt: str) -> list:
        return [image(spec.asset_id, alt=self.ALT), text(prompt)]


class Apparatus(NamedTuple):
    """One drawn set-up: its asset, the method it performs, and what it separates.

    ``alt`` describes the glassware without naming the method — otherwise
    ``chem.apparatus_id`` answers itself for a screen reader, and in a printed
    worksheet, where an image renders as its alt text alone.
    """
    code: str                          # ascii asset suffix
    method: str                        # ชื่อวิธี — the answer to the "which method" ask
    example: str                       # ของผสมที่ชุดนี้ใช้แยก
    alt: str
    more_examples: tuple[str, ...] = ()  # other mixtures the same set-up separates

    @property
    def examples(self) -> tuple[str, ...]:
        return (self.example, *self.more_examples)

    @property
    def asset_id(self) -> str:
        return f"apparatus_{self.code}"


APPARATUS_SPECS = [
    # "การกลั่นธรรมดา", matching the ``chem.homo_separation`` label: a ม.2 sheet
    # that mixes the two names for the same method teaches a doubt, not a fact.
    Apparatus("distillation", "การกลั่นธรรมดา", "น้ำเกลือที่ต้องการเก็บทั้งน้ำและเกลือ",
              "แผนภาพชุดอุปกรณ์แก้ว มีขวดก้นกลมตั้งบนตะเกียง ต่อกับท่อแก้วที่มีปลอกน้ำ"
              "หล่อเย็นหุ้มอยู่ และมีภาชนะรองรับของเหลวที่ปลายท่อ",
              ("น้ำทะเลที่ต้องการน้ำจืดไว้ดื่ม", "สารละลายจุนสีที่ต้องการเก็บน้ำบริสุทธิ์ไว้ใช้")),
    Apparatus("funnel", "การใช้กรวยแยก", "น้ำผสมกับน้ำมันพืช",
              "แผนภาพอุปกรณ์แก้วทรงลูกแพร์ที่มีก๊อกปิดเปิดอยู่ที่ก้น ภายในมีของเหลว"
              "สองชั้นวางซ้อนกัน และมีภาชนะรองอยู่ด้านล่าง",
              ("น้ำมันก๊าดที่ลอยเป็นชั้นอยู่บนน้ำ", "น้ำกับน้ำมันเครื่องที่แยกเป็นสองชั้น")),
    Apparatus("filtration", "การกรอง", "ทรายที่ปนอยู่ในน้ำ",
              "แผนภาพกรวยที่บุด้วยแผ่นเยื่อรูปกรวย วางอยู่บนปากบีกเกอร์ "
              "โดยมีของเหลวเทลงมาจากภาชนะด้านบน",
              ("กากชาที่ปนอยู่ในน้ำชา", "ผงชอล์กที่ไม่ละลายซึ่งปนอยู่ในน้ำ")),
    Apparatus("evaporation", "การระเหยจนแห้ง", "น้ำเกลือที่ต้องการเก็บเฉพาะเกลือ",
              "แผนภาพภาชนะปากกว้างก้นตื้นวางบนขาตั้งเหนือตะเกียง ภายในมีของเหลว"
              "และมีไอลอยขึ้นจากผิวหน้า",
              ("น้ำทะเลที่ต้องการเก็บเฉพาะเกลือ", "สารละลายจุนสีที่ต้องการเก็บเฉพาะของแข็ง")),
]


# Methods no set-up here performs, offered only as wrong names.
APPARATUS_DECOYS = ("การระเหิด", "โครมาโทกราฟี", "การใช้แม่เหล็กดูด")


APPARATUS_METHODS = [a.method for a in APPARATUS_SPECS]


@question_type(
    "chem.separation_solution_methods",
    display_name={"th": "เลือกวิธีแยกสารละลาย"},
    level={"th": "ม.2"}, subject="เคมี", topic="การแยกสาร",
)
class SeparationSolutionMethods(FoundationStage, Separation):
    """Evaporation, simple distillation, and chromatography at ม.2."""

    source_key = "chem.separation"
    CATEGORIES = [
        Separation.CATEGORIES[1],
        Category(
            "การกลั่นอย่างง่าย (Simple Distillation)",
            ("แยกน้ำจืดออกจากน้ำทะเล",
             "แยกน้ำบริสุทธิ์ออกจากสารละลายจุนสี"),
        ),
        Separation.CATEGORIES[3],
    ]


@question_type("chem.apparatus_id",
               display_name={"th": "อ่านแผนภาพชุดอุปกรณ์แยกสาร"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class ApparatusId(QuestionType):
    """จากภาพชุดอุปกรณ์ บอกว่าเป็นวิธีแยกสารใด และใช้แยกของผสมชนิดใด.

    Recognising the glassware is the step between knowing the method's name and
    doing it, and it is the one a text-only bank cannot ask.
    """

    ASKS = ("method", "use")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        asked = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        spec = rng.choice(APPARATUS_SPECS)
        stem = [image(spec.asset_id, alt=spec.alt)]
        example = rng.choice(spec.examples)
        if asked == "method":
            return GeneratedQuestion(
                stem=stem + [text("ชุดอุปกรณ์ในภาพใช้แยกสารด้วยวิธีใด")],
                correct=[text(spec.method)],
                distractors=label_pool([*APPARATUS_METHODS, *APPARATUS_DECOYS]),
                topic=self.topic,
            )
        return GeneratedQuestion(
            stem=stem + [text("ชุดอุปกรณ์ในภาพเหมาะกับการแยกของผสมในข้อใด")],
            correct=[text(example)],
            distractors=label_pool([example, *(e for a in APPARATUS_SPECS if a is not spec for e in a.examples)]),
            topic=self.topic,
        )


@question_type(
    "chem.distillation_simple",
    display_name={"th": "การกลั่นอย่างง่าย"},
    level={"th": "ม.2"}, subject="เคมี", topic="การแยกสาร",
)
class SimpleDistillation(FluencyStage, Distillation):
    source_key = "chem.distillation"
    ITEMS = [Distillation.ITEMS[index] for index in (0, 1, 2, 3, 6)]


@question_type("chem.crystallization",
               display_name={"th": "การตกผลึก"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class Crystallization(ConceptBankType):
    """การตกผลึกต้องเริ่มจากสารละลายอิ่มตัว — และต่างจากการระเหยจนแห้งอย่างไร."""

    ITEMS = [
        Concept(
            "การตกผลึกจะเกิดขึ้นได้ สารละลายต้องอยู่ในสภาพใดก่อน",
            "เป็นสารละลายอิ่มตัว คือละลายของแข็งไว้จนไม่สามารถละลายเพิ่มได้อีก",
            ("เป็นสารละลายเจือจางที่ละลายของแข็งไว้เพียงเล็กน้อย",
             "เป็นของเหลวบริสุทธิ์ที่ไม่มีของแข็งละลายอยู่เลย",
             "เป็นสารเนื้อผสมที่มองเห็นของแข็งแยกกันชัดเจน",
             "เป็นของเหลวบริสุทธิ์ที่ระเหยจนแห้ง แล้วเหลือของแข็งเป็นผลึกทันที",
             "เป็นสารละลายที่ยังละลายของแข็งเพิ่มได้อีกมาก จึงยังไม่เกิดผลึก")),
        Concept(
            "การตกผลึกกับการระเหยจนแห้งต่างกันที่จุดใดสำคัญที่สุด",
            "การตกผลึกได้ของแข็งที่บริสุทธิ์กว่า เพราะสิ่งเจือปนยังคงละลายค้างอยู่ในสารละลาย",
            ("การตกผลึกทำให้เกิดสารใหม่ ส่วนการระเหยจนแห้งไม่เกิด",
             "การระเหยจนแห้งได้ของแข็งที่บริสุทธิ์กว่าเสมอ",
             "การตกผลึกได้ของแข็งมากกว่า เพราะของแข็งทั้งหมดตกเป็นผลึกไม่มีส่วนใดค้างในสารละลาย",
             "การระเหยจนแห้งได้ของแข็งที่บริสุทธิ์กว่า เพราะสิ่งเจือปนระเหยออกไปพร้อมกับน้ำ",
             "การระเหยจนแห้งเก็บตัวทำละลายกลับคืนได้ทั้งหมด")),
        Concept(
            "การตกผลึกเหมาะกับการแยกองค์ประกอบของสารในลักษณะใด",
            "ของแข็งที่ละลายอยู่ในของเหลวจนได้สารละลายอิ่มตัว",
            ("ของแข็งที่ไม่ละลายในของเหลวเลย",
             "ของเหลวสองชนิดที่ไม่ละลายเข้าด้วยกัน",
             "ของแข็งที่ละลายในของเหลวได้เพียงเล็กน้อยจนเจือจาง",
             "ของแข็งสองชนิดที่หยิบแยกด้วยมือได้",
             "ของแข็งที่ไม่ละลายซึ่งแขวนลอยกระจายอยู่ในของเหลว")),
        Concept(
            "ข้อใดอธิบายตำแหน่งที่ผลึกอาจก่อตัวได้ถูกต้อง",
            "ผลึกอาจก่อตัวที่ก้นหรือผนังภาชนะ หรือบนเมล็ดผลึก",
            ("ผลึกต้องตกอยู่ที่ก้นภาชนะเท่านั้น",
             "ผลึกต้องลอยอยู่บนผิวสารละลายเท่านั้น",
             "ผลึกเกิดได้เฉพาะเหนือระดับสารละลายเท่านั้น",
             "ผลึกเกิดได้เฉพาะเมื่อเขย่าภาชนะแรงๆ เท่านั้น",
             "ผลึกเกิดได้เฉพาะเมื่อสารละลายเดือดอยู่ตลอดเวลาเท่านั้น")),
        Concept(
            "การทำน้ำตาลกรวดจากน้ำเชื่อมเข้มข้นใช้วิธีใด",
            "การตกผลึก",
            ("การกลั่นลำดับส่วน", "การใช้กรวยแยก", "การระเหิด",
             "การกรอง",
             "การใช้แม่เหล็ก")),
    ]


@question_type("chem.chromatography",
               display_name={"th": "หลักการของโครมาโทกราฟี"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class Chromatography(ConceptBankType):
    """ตัวดูดซับ ตัวทำละลาย วิธีทำ และเหตุผลที่สารแต่ละชนิดเคลื่อนที่ได้ไม่เท่ากัน."""

    ITEMS = [
        Concept(
            "คำว่าโครมาโทกราฟีมีความหมายตรงกับข้อใด",
            "การแยกออกมาให้เห็นเป็นสีๆ",
            ("การทำให้สารรวมกันเป็นเนื้อเดียว",
             "การวัดจุดเดือดของสารผสม",
             "การทำให้สารเปลี่ยนสถานะเป็นแก๊ส",
             "การแยกสารด้วยแม่เหล็ก",
             "การตกตะกอนของสารแขวนลอย")),
        Concept(
            "โครมาโทกราฟีประกอบด้วยส่วนสำคัญสองส่วนใด",
            "ตัวดูดซับและตัวทำละลาย",
            ("ตัวดูดซับและตัวเร่งปฏิกิริยา",
             "ตัวทำละลายและแม่เหล็ก",
             "กระดาษกรองและกรวยแยก",
             "ตัวดูดซับและเครื่องหมุนเหวี่ยง",
             "ตัวทำละลายและเครื่องควบแน่น")),
        Concept(
            "ข้อใดเป็นตัวดูดซับที่ใช้ในโครมาโทกราฟี",
            "กระดาษกรองหรือแท่งชอล์ก",
            ("สารละลายเอทานอลในน้ำ", "แอลกอฮอล์", "กรวยแยกหรือหลอดทดลองแก้ว",
             "กรวยแยก",
             "น้ำกลั่น")),
        Concept(
            "ข้อใดทำหน้าที่เป็นตัวทำละลายในโครมาโทกราฟี",
            "แอลกอฮอล์",
            ("แท่งชอล์ก", "กระดาษโครมาโทกราฟี", "กรวยแยก",
             "แม่เหล็ก",
             "ผงเหล็ก")),
        Concept(
            "เมื่อแช่ตัวดูดซับลงในตัวทำละลาย ต้องวางจุดสีของสารไว้อย่างไร",
            "ให้จุดสีอยู่สูงกว่าระดับของตัวทำละลายเล็กน้อย",
            ("ให้จุดสีจมอยู่ใต้ระดับของตัวทำละลาย",
             "ให้จุดสีอยู่ที่ปลายบนสุดของตัวดูดซับ",
             "ให้จุดสีอยู่ที่ระดับเดียวกับตัวทำละลายพอดี",
             "ให้จุดสีแตะก้นภาชนะที่ใส่ตัวทำละลาย",
             "ให้จุดสีอยู่ด้านหลังของตัวดูดซับที่ไม่เปียก")),
        Concept(
            "เพราะเหตุใดจุดสีจึงต้องอยู่สูงกว่าระดับตัวทำละลาย",
            "เพื่อไม่ให้สารสีละลายหลุดออกไปในตัวทำละลายก่อนที่จะถูกพาขึ้นไปบนตัวดูดซับ",
            ("เพื่อให้ตัวทำละลายเดือดได้เร็วขึ้น",
             "เพื่อให้สารสีละลายลงในตัวทำละลายให้หมดก่อน แล้วจึงค่อยซึมขึ้นไปตามแถบ",
             "เพื่อให้ตัวดูดซับไม่เปียกน้ำเลย",
             "เพื่อให้ตัวทำละลายไหลผ่านจุดสารสีได้เร็วขึ้น สารสีจึงแยกกันได้ดีขึ้น",
             "เพื่อให้ตัวดูดซับแยกเป็นสองชั้น")),
        Concept(
            "สารสีที่เคลื่อนที่ไปบนตัวดูดซับได้ไกลที่สุดมีสมบัติอย่างไร",
            "ละลายในตัวทำละลายได้ดีที่สุดและถูกตัวดูดซับยึดไว้น้อยที่สุด",
            ("ละลายในตัวทำละลายได้น้อยที่สุดและถูกตัวดูดซับยึดไว้มากที่สุด",
             "มีมวลมากที่สุดจึงถูกดันขึ้นไปได้ไกลที่สุด",
             "มีสีเข้มที่สุดจึงมองเห็นได้ไกลที่สุด",
             "มีมวลน้อยที่สุด จึงถูกตัวทำละลายพาขึ้นไปได้ไกลที่สุดเสมอ",
             "ไม่ละลายในตัวทำละลายเลย จึงถูกดันขึ้นไปพร้อมกับตัวทำละลาย")),
        Concept(
            "โครมาโทกราฟีเหมาะกับการแยกสารที่มีลักษณะอย่างไร",
            "สารตั้งแต่ 2 ชนิดขึ้นไปที่ละลายอยู่ในของเหลว และเคลื่อนที่บนตัวดูดซับได้ไม่เท่ากัน",
            ("ของแข็งขนาดใหญ่ที่หยิบออกได้ด้วยมือ",
             "ของเหลวสองชนิดที่ไม่ละลายเข้าด้วยกัน",
             "สารตั้งแต่ 2 ชนิดขึ้นไปที่ไม่ละลายในตัวทำละลาย และเคลื่อนที่บนตัวดูดซับได้เท่ากัน",
             "ของแข็งที่ระเหิดได้ซึ่งปนกับของแข็งอื่น",
             "สารเพียงชนิดเดียวที่ละลายอยู่ในของเหลว และเคลื่อนที่บนตัวดูดซับได้ระยะทางเท่าเดิมเสมอ")),
    ]


@question_type("chem.solvent_extraction",
               display_name={"th": "การสกัดด้วยตัวทำละลาย"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class SolventExtraction(ConceptBankType):
    """การสกัดด้วยตัวทำละลาย — ชื่อวิธีที่ใบความรู้เอ่ยถึงแต่ไม่ได้อธิบายไว้."""

    ITEMS = [
        Concept(
            "การสกัดด้วยตัวทำละลายมีหลักการอย่างไร",
            "เลือกตัวทำละลายที่ละลายเฉพาะสารที่ต้องการ แล้วแยกสารละลายนั้นออกมา",
            ("ให้ความร้อนจนสารที่ต้องการระเหิดกลายเป็นไอ",
             "เลือกตัวทำละลายที่ละลายทุกสารในของผสมได้ แล้วระเหยให้แห้งทั้งหมด",
             "หมุนเหวี่ยงจนสารที่ต้องการแยกลงก้นหลอด",
             "กรองของผสมด้วยกระดาษกรองหลายๆ ชั้น",
             "เลือกตัวทำละลายที่ไม่ละลายสารที่ต้องการ แล้วเก็บสารละลายนั้นไว้ใช้")),
        Concept(
            "ตัวทำละลายที่ดีสำหรับการสกัดควรมีสมบัติอย่างไร",
            "ละลายสารที่ต้องการได้ดี แต่ไม่ละลายสารอื่นที่ไม่ต้องการ",
            ("ละลายได้ทุกสารในของผสมอย่างเท่าเทียมกัน",
             "ละลายสารอื่นได้ดีมาก แต่ไม่ละลายสารที่ต้องการเลยแม้แต่น้อย",
             "มีจุดเดือดสูงมากจนระเหยไม่ได้",
             "มีจุดเดือดใกล้เคียงกับสารที่ต้องการมาก จึงกลั่นแยกออกจากกันได้ง่าย",
             "ทำปฏิกิริยากับสารที่ต้องการจนเกิดสารใหม่")),
        Concept(
            "ข้อใดเป็นตัวอย่างของการสกัดด้วยตัวทำละลาย",
            "การแช่กลีบดอกไม้ในตัวทำละลายที่เหมาะสมเพื่อสกัดสารหอม",
            ("การทำนาเกลือจากน้ำทะเล",
             "การแยกผงเหล็กออกจากผงกำมะถัน",
             "การแยกน้ำมันพืชออกจากน้ำด้วยกรวยแยก",
             "การตั้งน้ำโคลนทิ้งไว้ให้ตกตะกอนแล้วรินน้ำใสส่วนบนออก",
             "การต้มน้ำเกลือจนเดือดแล้วเก็บไอน้ำที่กลั่นตัวไว้ใช้ดื่ม")),
        Concept(
            "หลังสกัดสารที่ต้องการลงในตัวทำละลายแล้ว มักใช้วิธีใดแยกตัวทำละลายออก",
            "การกลั่นหรือการระเหยตัวทำละลายออกไป",
            ("การใช้แม่เหล็กดูดตัวทำละลายออก",
             "การตกตะกอนสารที่สกัดได้ลงก้นภาชนะ",
             "การใช้กรวยแยกไขตัวทำละลายออก",
             "การกรองตัวทำละลายออกด้วยกระดาษกรอง",
             "การตกตะกอนตัวทำละลายลงก้นภาชนะ")),
        Concept(
            "เพราะเหตุใดการต้มสมุนไพรในน้ำจึงถือเป็นการสกัดด้วยตัวทำละลายอย่างง่าย",
            "เพราะน้ำทำหน้าที่ละลายสารสำคัญออกจากเนื้อสมุนไพรมาอยู่ในน้ำ",
            ("เพราะความร้อนเปลี่ยนสมุนไพรให้กลายเป็นสารใหม่",
             "เพราะน้ำทำให้สมุนไพรระเหิดกลายเป็นไอ",
             "เพราะน้ำมีความหนาแน่นมากกว่าสมุนไพร สารสำคัญจึงลอยขึ้นมาบนผิวน้ำ",
             "เพราะความร้อนทำให้สมุนไพรระเหิดเป็นไอ แล้วกลั่นตัวกลับลงในน้ำ",
             "เพราะสมุนไพรแยกเป็นชั้นลอยอยู่บนน้ำ")),
    ]


@question_type("chem.chromatogram_read",
               display_name={"th": "อ่านโครมาโทแกรม"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class ChromatogramRead(ChromaType):
    """อ่านแผนภาพโครมาโทแกรม: สารใดไปไกลสุด ละลายดีสุด ถูกยึดไว้มากสุด และมีกี่ชนิด.

    Four asks over one picture. ``far`` is a plain reading; ``soluble`` and
    ``held`` are the same reading turned into the sheet's explanation (ไปไกล =
    ละลายดี = ถูกดูดซับน้อย), which is the step students skip; ``count`` is what
    a chromatogram is actually *for* — how many สาร the sample contained.
    """

    ASKS = ("far", "soluble", "held", "count")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        asked = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        spec = rng.choice(CHROMA_SPECS)
        n = len(spec.spots)
        if asked == "count":
            return GeneratedQuestion(
                stem=self._stem(spec, "ตัวอย่างสารที่นำมาแยกนี้ประกอบด้วยสารอย่างน้อยกี่ชนิด"),
                correct=[math(str(n))],
                distractors=fixed([math(str(n + 1))], [math(str(n - 1))],
                                  [math(str(n + 2))]),
                topic=self.topic,
                hint=[text("จำนวนจุดสีที่แยกออกมาคือจำนวนสารอย่างน้อยที่สุดในตัวอย่าง")],
            )

        # spots are listed nearest-first, so the last has run the farthest
        if asked == "far":
            prompt = "สารใดเคลื่อนที่บนตัวดูดซับได้ไกลที่สุด"
            i, hint = n - 1, "อ่านจากจุดสีที่อยู่สูงที่สุดเหนือเส้นเริ่มต้น"
        elif asked == "soluble":
            prompt = "สารใดละลายในตัวทำละลายได้ดีที่สุด"
            i, hint = n - 1, "สารที่ละลายได้ดีที่สุดจะถูกพาขึ้นไปได้ไกลที่สุด"
        else:
            prompt = "สารใดถูกตัวดูดซับยึดไว้มากที่สุด"
            i, hint = 0, "สารที่ถูกตัวดูดซับยึดไว้มากจะเคลื่อนที่ขึ้นไปได้น้อยที่สุด"

        # Two spots leave only one other name to offer, so the pair of "no spot
        # is special" statements is what carries a two-component picture to a
        # full four choices. Both are false against any drawn chromatogram.
        others = [nm for k, nm in enumerate(spec.names) if k != i]
        return GeneratedQuestion(
            stem=self._stem(spec, prompt),
            correct=[text(spec.names[i])],
            distractors=combine(
                label_pool(others),
                fixed([text("ทุกสารเคลื่อนที่ได้เท่ากัน")],
                      [text("ไม่มีสารใดเคลื่อนที่ขึ้นจากเส้นเริ่มต้น")])),
            topic=self.topic,
            hint=[text(hint)],
        )


@question_type("chem.rf_value",
               display_name={"th": "หาค่า Rf จากโครมาโทแกรม"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class RfValue(ChromaType):
    """วัดระยะจากแผนภาพแล้วหาค่า Rf = ระยะทางของสาร ÷ ระยะทางของตัวทำละลาย.

    Not in the sheets — an extension of the last paragraph of
    ``การแยกสารเนื้อเดียว.md``, which says the colours travel different distances
    but never puts a number on it. The wrong choices are the *other* spots' Rf
    values from the same picture (a real value, read off the wrong row) and the
    inverted ratio, which is the mistake worth catching: Rf can never exceed 1.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(CHROMA_SPECS)
        i = rng.randrange(len(spec.spots))
        d = spec.spots[i]
        correct = fmt(round(spec.rf(i), 2))
        # The inverted ratio goes first so it is *always* offered — on a
        # four-spot picture the sibling values would otherwise fill the quota
        # and drop the one wrong answer worth catching. Dividing by the distance
        # still to go, rather than by the front, comes next; it keeps a
        # two-spot picture at four choices.
        wrong = [fmt(round(spec.solvent / d, 2)),
                 fmt(round(d / (spec.solvent - d), 2))]
        wrong += [fmt(round(spec.rf(k), 2)) for k in range(len(spec.spots)) if k != i]
        return GeneratedQuestion(
            stem=self._stem(spec, f"จงหาค่า Rf ของ{spec.names[i]} จากโครมาโทแกรมนี้"),
            correct=[math(correct)],
            distractors=fixed(*[[math(w)] for w in wrong if w != correct]),
            topic=self.topic,
            hint=[math(r"R_f = \frac{d_{\mathrm{substance}}}{d_{\mathrm{solvent}}}")],
        )


@question_type(
    "chem.solution_separation_application",
    display_name={"th": "การแยกสารละลาย: เลือกวิธีและตีความหลักฐาน"},
    level={"th": "ม.2"}, subject=CHEMISTRY, topic=MATTER,
)
class SolutionSeparationApplication(QuestionType):
    """Choose a method for a stated goal, or read a chromatogram as evidence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            task, correct, wrongs = rng.choice(SOLUTION_TASKS)
            return _question(
                stem=f"{task} ควรใช้วิธีใด และเพราะเหตุใด",
                correct=correct,
                wrongs=wrongs,
                hint="ถามสองข้อ: ต้องเก็บตัวทำละลายไว้ด้วยหรือไม่ และองค์ประกอบต่างกันที่สมบัติใด",
                topic=MATTER,
            )
        if which == 1:
            solvent = rng.randrange(6, 11)
            near = rng.randrange(2, solvent - 2)
            far = near + rng.randrange(1, solvent - near)
            return _question(
                stem=("ทำโครมาโทกราฟีแบบกระดาษกับหมึกตัวอย่างหนึ่ง "
                      f"ตัวทำละลายเคลื่อนที่ได้ {solvent} cm "
                      f"จุดสีแดงเคลื่อนที่ได้ {near} cm และจุดสีน้ำเงินเคลื่อนที่ได้ {far} cm "
                      "ข้อสรุปใดใช้หลักฐานได้ถูกต้อง"),
                correct=("หมึกนี้มีสารมากกว่าหนึ่งชนิด และสีน้ำเงินละลายในตัวทำละลายได้ดีกว่าสีแดง"),
                wrongs=(
                    "หมึกนี้มีสารมากกว่าหนึ่งชนิด และสีแดงละลายในตัวทำละลายได้ดีกว่าสีน้ำเงิน",
                    "หมึกนี้เป็นสารบริสุทธิ์ เพราะทั้งสองจุดเคลื่อนที่ขึ้นไปพร้อมกัน",
                    "หมึกนี้มีสารชนิดเดียว แต่ตัวทำละลายทำให้เกิดสีใหม่ขึ้นสองสี",
                ),
                hint="จำนวนจุดบอกจำนวนสาร ส่วนระยะที่เคลื่อนที่ได้บอกว่าสารใดไปกับตัวทำละลายได้ดีกว่า",
                topic=MATTER,
            )
        return _question(
            stem=("นักเรียนกลั่นน้ำเกลืออย่างง่ายและเก็บของเหลวที่ได้ไว้ "
                  "ต้องการตรวจว่าของเหลวนั้นเป็นน้ำที่แยกออกมาได้จริงหรือไม่ "
                  "หลักฐานใดยืนยันได้ดีที่สุด"),
            correct="ของเหลวที่เก็บได้เดือดที่อุณหภูมิคงที่ประมาณ 100 °C และไม่เหลือของแข็งเมื่อระเหยแห้ง",
            wrongs=(
                "ของเหลวที่เก็บได้ใสไม่มีสี จึงเป็นน้ำบริสุทธิ์แน่นอน",
                "ของเหลวที่เก็บได้มีปริมาตรน้อยกว่าน้ำเกลือเดิม",
                "ของเหลวที่เก็บได้มีรสจืด จึงไม่มีเกลือปนอยู่เลย",
            ),
            hint="เลือกหลักฐานที่วัดสมบัติเฉพาะตัวของสารได้ ไม่ใช่ลักษณะที่สังเกตด้วยตาอย่างเดียว",
            topic=MATTER,
        )


# More items: each set drew from five, so a learner met them all in a few
# tries. Every added item asks something the others do not.
Crystallization.ITEMS = [*Crystallization.ITEMS,
    Concept('ถ้าทำให้สารละลายอิ่มตัวที่ร้อนเย็นลงช้า ๆ ผลึกที่ได้จะเป็นอย่างไรเมื่อเทียบกับการทำให้เย็นลงเร็ว',
            'ผลึกมีขนาดใหญ่กว่า',
            ('ผลึกมีขนาดเล็กกว่าเสมอ', 'ไม่เกิดผลึกเลย', 'ผลึกละลายกลับหมด', 'ได้ผลึกเท่ากันทุกกรณี', 'ได้แก๊สแทนผลึก')),
    Concept('การทำเกลือสมุทรจากน้ำทะเลในนาเกลืออาศัยหลักการใด',
            'ให้น้ำระเหยจนสารละลายเกลืออิ่มตัวแล้วเกลือตกผลึกออกมา',
            ('กรองเกลือออกจากน้ำทะเลด้วยผ้า', 'ใช้แม่เหล็กดูดเกลือ', 'กลั่นน้ำทะเลแล้วเก็บไอน้ำเป็นเกลือ', 'ตั้งทิ้งไว้ให้เกลือลอยขึ้นมาเอง', 'ใช้ตัวทำละลายสกัดเกลือออก')),
    Concept('เพราะเหตุใดจึงต้องกรองสารละลายร้อนก่อนปล่อยให้ตกผลึก',
            'เพื่อกำจัดสิ่งเจือปนที่ไม่ละลายออกก่อน ผลึกที่ได้จึงบริสุทธิ์ขึ้น',
            ('เพื่อให้สารละลายเย็นลงเร็วขึ้น', 'เพื่อเพิ่มสิ่งเจือปนให้ผลึก', 'เพื่อเปลี่ยนสารละลายเป็นแก๊ส', 'เพื่อทำให้ผลึกมีสีสวย', 'ไม่จำเป็นต้องกรองเลย')),
    Concept('เติมผลึกเล็ก ๆ ลงในสารละลายอิ่มตัวยิ่งยวด จะเกิดอะไรขึ้น',
            'ผลึกเล็กเป็นจุดเริ่มต้นให้ตัวละลายตกผลึกออกมาเกาะเพิ่ม',
            ('ผลึกเล็กละลายหายไปทันที', 'สารละลายกลายเป็นแก๊ส', 'ไม่มีการเปลี่ยนแปลงใด ๆ', 'สารละลายเดือดทันที', 'ผลึกเล็กเปลี่ยนเป็นน้ำ')),
]

SolventExtraction.ITEMS = [*SolventExtraction.ITEMS,
    Concept('การชงชาด้วยน้ำร้อนจนได้น้ำชาสีน้ำตาลเป็นการแยกสารแบบใด',
            'การสกัดด้วยตัวทำละลาย โดยน้ำร้อนละลายสารในใบชาออกมา',
            ('การกลั่นลำดับส่วน', 'การตกผลึก', 'การใช้แม่เหล็ก', 'การระเหิด', 'การตกตะกอน')),
    Concept('การสกัดน้ำมันจากเมล็ดพืชด้วยตัวทำละลาย ควรเลือกตัวทำละลายแบบใด',
            'ตัวทำละลายที่ละลายน้ำมันได้ดีและระเหยแยกออกได้ง่าย',
            ('น้ำ เพราะละลายน้ำมันได้ดีที่สุด', 'ตัวทำละลายที่ไม่ละลายน้ำมันเลย', 'ตัวทำละลายที่ระเหยยากที่สุด', 'ทรายแห้ง', 'ตัวทำละลายที่ทำปฏิกิริยากับน้ำมันจนเป็นสารใหม่')),
    Concept('เพราะเหตุใดการสกัดด้วยตัวทำละลายที่ติดไฟง่ายจึงต้องทำในที่อากาศถ่ายเทและห่างเปลวไฟ',
            'ไอของตัวทำละลายติดไฟได้และอาจเป็นอันตรายต่อการหายใจ',
            ('ตัวทำละลายจะกลายเป็นน้ำแข็ง', 'เปลวไฟทำให้สารที่สกัดได้มากขึ้น', 'ไม่จำเป็นต้องระวังเลย', 'อากาศถ่ายเททำให้สารละลายไม่ละลาย', 'ตัวทำละลายทุกชนิดไม่ติดไฟ')),
    Concept('สกัดสารสีจากใบเตยด้วยการคั้นกับน้ำ แล้วกรองเอากากออก ขั้นตอนการกรองมีไว้เพื่ออะไร',
            'แยกกากใบเตยที่ไม่ละลายออกจากน้ำที่มีสารสีละลายอยู่',
            ('เปลี่ยนน้ำใบเตยให้เป็นของแข็ง', 'ทำให้สารสีระเหยออกไป', 'เพิ่มกากใบเตยลงในน้ำ', 'ทำให้น้ำใบเตยเดือด', 'แยกสีออกจากน้ำจนน้ำใส')),
]

# More items: these tables held six or fewer, so a learner met them all in
# a few tries. Each added item has wrong readings of its own.
SimpleDistillation.ITEMS = [*SimpleDistillation.ITEMS,
    Concept('น้ำกลั่นที่ใช้เติมแบตเตอรี่รถยนต์ได้มาจากกระบวนการใด',
            'การกลั่นน้ำ ให้ระเหยแล้วควบแน่นกลับเป็นน้ำบริสุทธิ์',
            ('การกรองน้ำประปาด้วยกระดาษกรองเพียงครั้งเดียว', 'การต้มน้ำจนเดือดแล้วเก็บน้ำที่เหลือในหม้อ', 'การเติมสารส้มให้ตะกอนตกแล้วรินน้ำใสออก', 'การแช่แข็งน้ำแล้วปล่อยให้ละลายตามเดิม', 'การใช้แม่เหล็กดูดสิ่งเจือปนออกจากน้ำ')),
    Concept('ในชุดกลั่น ควรต่อน้ำหล่อเย็นให้ไหลเข้าเครื่องควบแน่นทางด้านใด',
            'เข้าทางด้านล่าง แล้วไหลออกทางด้านบน เพื่อให้มีน้ำเย็นเต็มเครื่องควบแน่น',
            ('เข้าทางด้านบน แล้วไหลออกทางด้านล่าง เพื่อให้น้ำไหลลงเร็วที่สุด', 'ไม่ต้องต่อน้ำหล่อเย็นเลย เพราะไอจะเย็นลงเองในอากาศ', 'ต่อน้ำร้อนเข้าเครื่องควบแน่นเพื่อให้ไอร้อนขึ้นอีก', 'เทน้ำเย็นลงในขวดกลั่นโดยตรงแทนเครื่องควบแน่น', 'ปิดทางน้ำออกไว้ให้น้ำค้างอยู่ในเครื่องควบแน่นตลอด')),
    Concept('เหตุใดจึงต้องใส่เศษกระเบื้องพรุนลงในขวดกลั่นก่อนให้ความร้อน',
            'ช่วยให้ของเหลวเดือดสม่ำเสมอ ไม่เดือดพลุ่งกระเด็น',
            ('ช่วยดูดซับสารที่ต้องการแยกไว้ในเนื้อกระเบื้อง', 'ช่วยเพิ่มจุดเดือดของของเหลวให้สูงขึ้นมาก', 'ช่วยเปลี่ยนสีของของเหลวให้สังเกตได้ง่าย', 'ช่วยทำให้ไอเย็นลงก่อนออกจากขวดกลั่น', 'ช่วยกรองของแข็งออกจากของเหลวในขวดกลั่น')),
]
