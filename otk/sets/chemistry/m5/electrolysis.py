"""การชุบโลหะ การแยกสารด้วยไฟฟ้า และการป้องกันการกัดกร่อน

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/31

Sets moved here from: science_wave_f40.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f40 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_ELECTROLYSIS = "การชุบโลหะ การแยกสารด้วยไฟฟ้า และการป้องกันการกัดกร่อน"


PLATING = ("Cu", "Ag", "Ni", "Cr", "Au", "Zn", "Sn")


PLATING_SALT = {"Cu": "CuSO₄", "Ag": "AgNO₃", "Ni": "NiSO₄", "Cr": "Cr₂(SO₄)₃", "Au": "AuCl₃", "Zn": "ZnSO₄",
                "Sn": "SnSO₄"}


OBJECTS = ("ช้อนเหล็ก", "กุญแจทองเหลือง", "ต่างหูทองแดง", "น็อตเหล็ก", "ถาดเหล็ก", "เหรียญทองแดง")


# (what is electrolysed, product at the cathode, product at the anode)
ELECTROLYSES = (
    ("NaCl หลอมเหลว", "โลหะ Na", "แก๊ส Cl₂"), ("สารละลาย NaCl เข้มข้น", "แก๊ส H₂ (และได้ NaOH ในสารละลาย)", "แก๊ส Cl₂"),
    ("น้ำที่เติม H₂SO₄ เจือจาง", "แก๊ส H₂", "แก๊ส O₂"), ("สารละลาย CuSO₄ ด้วยขั้วแกรไฟต์", "โลหะ Cu", "แก๊ส O₂"),
    ("Al₂O₃ หลอมเหลวในไครโอไลต์", "โลหะ Al", "แก๊ส O₂ (ทำปฏิกิริยากับขั้วคาร์บอนเป็น CO₂)"),
    ("MgCl₂ หลอมเหลว", "โลหะ Mg", "แก๊ส Cl₂"),
)


PROTECTIONS = (
    ("ทาสีหรือเคลือบพลาสติกบนเหล็ก", "กันไม่ให้เหล็กสัมผัสน้ำและออกซิเจน"),
    ("ชุบสังกะสีบนแผ่นเหล็ก (เหล็กอาบสังกะสี)", "สังกะสีเป็นตัวรีดิวซ์ที่ดีกว่า จึงถูกกัดกร่อนแทนเหล็กแม้ผิวเป็นรอย"),
    ("ต่อแท่ง Mg เข้ากับท่อเหล็กใต้ดิน", "Mg เป็นแอโนดสังเวยที่ถูกออกซิไดส์แทนเหล็ก"),
    ("ต่อท่อเหล็กเข้ากับขั้วลบของแหล่งจ่ายไฟฟ้า", "เหล็กเป็นแคโทด จึงไม่ถูกออกซิไดส์"),
    ("ทาน้ำมันหรือจาระบีบนเครื่องจักร", "กันไม่ให้โลหะสัมผัสน้ำและอากาศ"),
)


@question_type(
    "chem.electrolysis_foundation",
    display_name={"th": "การชุบโลหะด้วยไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ELECTROLYSIS,
)
class ElectrolysisFoundation(QuestionType):
    """The object is the cathode; the plating metal is the anode; its ions are in the solution."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal, thing = rng.choice(PLATING), rng.choice(OBJECTS)
        salt = PLATING_SALT[metal]
        right = f"{thing}ต่อขั้วลบเป็นแคโทด แท่ง {metal} ต่อขั้วบวกเป็นแอโนด ใช้สารละลาย {salt}"
        wrongs = (f"{thing}ต่อขั้วบวกเป็นแอโนด แท่ง {metal} ต่อขั้วลบเป็นแคโทด ใช้สารละลาย {salt}",
                  f"{thing}ต่อขั้วลบเป็นแคโทด แท่ง {metal} ต่อขั้วบวกเป็นแอโนด ใช้สารละลาย NaCl",
                  f"{thing}และแท่ง {metal} ต่อขั้วบวกทั้งคู่ ใช้น้ำกลั่น",
                  # Poles swapped and the wrong solution: wrong twice over.
                  f"{thing}ต่อขั้วบวกเป็นแอโนด แท่ง {metal} ต่อขั้วลบเป็นแคโทด ใช้สารละลาย NaCl",
                  f"{thing}ต่อขั้วบวกเป็นแอโนด แท่ง {metal} ต่อขั้วลบเป็นแคโทด ใช้น้ำกลั่น")
        return _labelled(stem=f"ต้องการชุบ{thing}ด้วย {metal} ควรจัดเซลล์อย่างไร", correct=right, wrongs=wrongs,
                         topic=TOPIC_ELECTROLYSIS,
                         hint="ไอออนโลหะถูกรีดิวซ์มาเกาะที่แคโทด (ชิ้นงาน) แอโนดเป็นโลหะที่ใช้ชุบซึ่งละลายเติมไอออนให้สารละลาย")


@question_type(
    "chem.electrolysis_fluency",
    display_name={"th": "ผลิตภัณฑ์จากการแยกสารด้วยไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ELECTROLYSIS,
)
class ElectrolysisFluency(QuestionType):
    """Reduction at the cathode, oxidation at the anode."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        what, cathode, anode = rng.choice(ELECTROLYSES)
        where = rng.choice(("แคโทด", "แอโนด"))
        right = cathode if where == "แคโทด" else anode
        other = anode if where == "แคโทด" else cathode
        pool = sorted(({e[1] for e in ELECTROLYSES} | {e[2] for e in ELECTROLYSES}) - {right, other})
        return _labelled(stem=f"แยก{what}ด้วยไฟฟ้า ที่{where}ได้ผลิตภัณฑ์ใด", correct=right,
                         wrongs=(other, *rng.sample(pool, 2)), topic=TOPIC_ELECTROLYSIS,
                         hint="แคโทดเกิดรีดักชัน (ได้โลหะหรือ H₂) แอโนดเกิดออกซิเดชัน (ได้ Cl₂ หรือ O₂)")


@question_type(
    "chem.electrolysis_application",
    display_name={"th": "การทำโลหะให้บริสุทธิ์และการป้องกันการกัดกร่อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_ELECTROLYSIS,
)
class ElectrolysisApplication(QuestionType):
    """Refining puts impure copper at the anode; protection keeps iron from being oxidised."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            facts = (
                ("การทำทองแดงให้บริสุทธิ์ด้วยไฟฟ้าจัดขั้วอย่างไร", "ทองแดงไม่บริสุทธิ์เป็นแอโนด ทองแดงบริสุทธิ์เป็นแคโทด ในสารละลาย CuSO₄",
                 ("ทองแดงบริสุทธิ์เป็นแอโนด ทองแดงไม่บริสุทธิ์เป็นแคโทด", "ใช้แกรไฟต์ทั้งสองขั้ว ในสารละลาย CuSO₄ เข้มข้น",
                  "ทองแดงไม่บริสุทธิ์เป็นแคโทด ในสารละลาย NaCl")),
                ("ในการทำทองแดงให้บริสุทธิ์ เงินและทองที่ปนอยู่ไปอยู่ที่ใด", "ตกลงใต้แอโนดเป็นกากแอโนด เพราะถูกออกซิไดส์ยากกว่าทองแดง",
                 ("ไปเกาะที่แคโทดพร้อมทองแดง เพราะถูกรีดิวซ์ได้ง่ายกว่าทองแดง", "ละลายเป็นไอออนอยู่ในสารละลาย เพราะถูกออกซิไดส์ง่ายกว่าทองแดง", "กลายเป็นแก๊สออกจากเซลล์ที่แอโนด")),
                ("ในการทำทองแดงให้บริสุทธิ์ สังกะสีและเหล็กที่ปนอยู่ไปอยู่ที่ใด", "ละลายเป็นไอออนอยู่ในสารละลาย แต่ไม่ไปเกาะที่แคโทด",
                 ("ตกลงใต้แอโนดเป็นกากแอโนด เพราะถูกออกซิไดส์ยากกว่าทองแดง", "ไปเกาะที่แคโทดพร้อมทองแดง ทำให้ทองแดงที่ได้ไม่บริสุทธิ์", "กลายเป็นแก๊สออกจากเซลล์")),
            )
            stem, right, wrongs = rng.choice(facts)
            wrongs = tuple(wrongs)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_ELECTROLYSIS,
                             hint="โลหะที่ถูกออกซิไดส์ง่ายกว่า Cu ละลายไปในสารละลาย โลหะที่ยากกว่าตกเป็นกากแอโนด")
        method, why = rng.choice(PROTECTIONS)
        others = [p[1] for p in PROTECTIONS if p[1] != why]
        return _labelled(stem=f"\"{method}\" ป้องกันการกัดกร่อนของเหล็กได้เพราะเหตุใด", correct=why,
                         wrongs=tuple(others), topic=TOPIC_ELECTROLYSIS,
                         hint="กันสัมผัสน้ำและอากาศ หรือให้โลหะที่เป็นตัวรีดิวซ์ดีกว่าถูกกัดกร่อนแทน หรือทำให้เหล็กเป็นแคโทด")
