"""ความหนาแน่นของสาร

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/5

Sets moved here from: science_wave_a3, substances.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.numeric_scenario import fmt
from otk.sets._support.science_wave_a3 import CHEMISTRY, MATTER, _distinct, _question
from otk.sets._support.substances import LEVEL, SUBJECT, TOPIC_SEP

PROVENANCE = Provenance("original")


# (ชื่อสาร, ความหนาแน่นโดยประมาณ g/cm³) — ค่าอ้างอิงที่ใช้ในระดับ ม.1
DENSITY_MATERIALS = (
    ("ไม้ก๊อก", Fraction(1, 4)),
    ("น้ำมันพืช", Fraction(9, 10)),
    ("น้ำ", Fraction(1)),
    ("อะลูมิเนียม", Fraction(27, 10)),
    ("เหล็ก", Fraction(79, 10)),
    ("ทองแดง", Fraction(89, 10)),
    ("ก้อนน้ำแข็ง", Fraction(23, 25)),     # not "น้ำแข็ง": a name must not start with another ("น้ำ")
    ("ตะกั่ว", Fraction(113, 10)),
)


def _fmt(value: Fraction) -> str:
    return f"{float(value):g}"


class Liquid(NamedTuple):
    name: str
    density: float                     # g/cm³


_AQUEOUS = (Liquid("น้ำ", 1.00), Liquid("น้ำเกลือ", 1.10),
            Liquid("น้ำเชื่อม", 1.15))


# คลอโรฟอร์ม and ไดคลอโรมีเทน are the dense ones, so the organic layer is
# sometimes the *lower* one and the rule cannot be guessed from the wording.
# คาร์บอนเตตระคลอไรด์ would be the classic third, but it is no longer used in
# school labs and its nineteen characters were most of a printed cell.
_ORGANIC = (Liquid("น้ำมันพืช", 0.92), Liquid("น้ำมันก๊าด", 0.80),
            Liquid("เฮกเซน", 0.66), Liquid("เบนซิน", 0.88),
            Liquid("คลอโรฟอร์ม", 1.49), Liquid("ไดคลอโรมีเทน", 1.33))


@question_type(
    "chem.density_foundation",
    display_name={"th": "ความหนาแน่นของสาร: ระบุความหมายและการจม-ลอย"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class DensityFoundation(QuestionType):
    """State what density is, or read one float/sink or equal-volume case."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(5)
        if which == 0:
            return _question(
                stem="ความหนาแน่นของสารหมายถึงอะไร",
                correct="มวลของสารต่อหนึ่งหน่วยปริมาตร",
                wrongs=(
                    "ปริมาตรของสารต่อหนึ่งหน่วยมวล",
                    "มวลทั้งหมดของสารโดยไม่เกี่ยวกับปริมาตร",
                    "น้ำหนักของสารเมื่อชั่งในน้ำ",
                    "ปริมาตรทั้งหมดของสารโดยไม่เกี่ยวกับมวล",
                    "มวลของสารคูณด้วยปริมาตรของสาร",
                ),
                hint="ความหนาแน่นเป็นอัตราส่วน ให้ดูว่าปริมาณใดหารด้วยปริมาณใด",
            )
        if which == 1:
            material, density = rng.choice(
                [item for item in DENSITY_MATERIALS if item[0] != "น้ำ"]
            )
            floats = density < 1
            return _question(
                stem=(f"{material}มีความหนาแน่นประมาณ {_fmt(density)} g/cm³ "
                      "เมื่อหย่อนลงในน้ำซึ่งมีความหนาแน่น 1 g/cm³ จะเกิดอะไรขึ้น"),
                correct="ลอยอยู่บนน้ำ" if floats else "จมลงในน้ำ",
                wrongs=(
                    "จมลงในน้ำ" if floats else "ลอยอยู่บนน้ำ",
                    "ละลายหายไปในน้ำทันที",
                    "ลอยหรือจมขึ้นกับขนาดของชิ้นสารเท่านั้น",
                    "ลอยครึ่งจมครึ่งเสมอไม่ว่าจะเป็นสารใด",
                    "เปลี่ยนเป็นของเหลวทันทีที่สัมผัสน้ำ",
                ),
                hint="เทียบความหนาแน่นของสารกับของน้ำ สารที่หนาแน่นน้อยกว่าจะลอย",
            )
        if which == 2:
            return _question(
                stem="หน่วยใดต่อไปนี้เป็นหน่วยของความหนาแน่น",
                correct="กรัมต่อลูกบาศก์เซนติเมตร (g/cm³)",
                wrongs=(
                    "กรัม (g)",
                    "ลูกบาศก์เซนติเมตร (cm³)",
                    "กรัมคูณลูกบาศก์เซนติเมตร (g·cm³)",
                    "ลูกบาศก์เซนติเมตรต่อกรัม (cm³/g)",
                    "นิวตัน (N)",
                ),
                hint="หน่วยของอัตราส่วนคือหน่วยของตัวตั้งหารด้วยหน่วยของตัวหาร",
            )
        if which == 3:
            heavy, light = rng.sample(
                [item for item in DENSITY_MATERIALS if item[0] != "น้ำ"], 2
            )
            if heavy[1] < light[1]:
                heavy, light = light, heavy
            return _question(
                stem=(f"{heavy[0]}มีความหนาแน่น {_fmt(heavy[1])} g/cm³ และ"
                      f"{light[0]}มีความหนาแน่น {_fmt(light[1])} g/cm³ "
                      "ถ้านำทั้งสองมาปริมาตรเท่ากัน ข้อใดถูกต้อง"),
                correct=f"{heavy[0]}มีมวลมากกว่า",
                wrongs=(
                    f"{light[0]}มีมวลมากกว่า",
                    "ทั้งสองมีมวลเท่ากัน เพราะมีปริมาตรเท่ากัน",
                    "บอกไม่ได้ เพราะมวลไม่เกี่ยวกับความหนาแน่น",
                    f"{light[0]}มีมวลมากกว่า เพราะมีความหนาแน่นน้อยกว่า",
                    "มวลขึ้นกับรูปร่างของชิ้นสารเท่านั้น",
                ),
                hint="ที่ปริมาตรเท่ากัน สารที่มีความหนาแน่นมากกว่าย่อมมีมวลมากกว่า",
            )
        return _question(
            stem=("ตัดโลหะชนิดเดียวกันออกเป็นสองชิ้น ชิ้นใหญ่และชิ้นเล็ก "
                  "ความหนาแน่นของทั้งสองชิ้นเป็นอย่างไร"),
            correct="เท่ากัน เพราะความหนาแน่นเป็นสมบัติเฉพาะตัวของสาร ไม่ขึ้นกับขนาดของชิ้น",
            wrongs=(
                "ชิ้นใหญ่มีความหนาแน่นมากกว่า เพราะมีมวลมากกว่า",
                "ชิ้นเล็กมีความหนาแน่นมากกว่า เพราะมีปริมาตรน้อยกว่า",
                "บอกไม่ได้ เพราะความหนาแน่นเปลี่ยนไปตามขนาดของชิ้นเสมอ",
                "ชิ้นเล็กมีความหนาแน่นเป็นศูนย์ เพราะเล็กเกินไป",
                "ชิ้นใหญ่มีความหนาแน่นเป็นสองเท่าของชิ้นเล็กเสมอ",
            ),
            hint="ทั้งมวลและปริมาตรลดลงในสัดส่วนเดียวกัน อัตราส่วนของทั้งสองจึงไม่เปลี่ยน",
        )


@question_type("chem.density_layers",
               display_name={"th": "ความหนาแน่นกับชั้นของเหลวในกรวยแยก"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_SEP)
class DensityLayers(QuestionType):
    """จากความหนาแน่น บอกว่าของเหลวใดอยู่ชั้นบน–ชั้นล่าง และไขออกมาก่อน.

    Three asks: name the lower layer, name the upper layer, and name what comes
    out of the tap first. The third is the one that matters in the lab — and the
    answer is the *same* liquid as the second question's wrong choice, so a
    student who has only memorised "หนาแน่นมากอยู่ล่าง" still has to think.
    """

    ASKS = ("bottom", "top", "drain")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        asked = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        a, b = rng.choice(_AQUEOUS), rng.choice(_ORGANIC)
        lower, upper = (a, b) if a.density > b.density else (b, a)
        first, second = rng.sample([a, b], 2)          # order shown in the stem

        # A table head rather than a sentence, and the unit as a symbol: the PDF
        # renderer neither wraps nor clips, so a stem long enough to overrun its
        # cell is simply painted past it. คาร์บอนเตตระคลอไรด์ alone is 19
        # characters, so the scaffold around the numbers has to stay lean.
        scenario = (f"ความหนาแน่น (g/cm³) {first.name} = {fmt(first.density)}, "
                    f"{second.name} = {fmt(second.density)} ไม่ละลายกัน ")
        # The two padding choices are worded per ask: "ไหลออกมาพร้อมกัน" is not an
        # answer to "ของเหลวใดอยู่ชั้นบน".
        if asked == "top":
            question, correct, near = "ของเหลวใดอยู่ชั้นบน", upper, lower
            why = "ของเหลวที่มีความหนาแน่นน้อยกว่าจะลอยอยู่ชั้นบน"
            padding = "อยู่ชั้นเดียวกันทั้งสองชนิด"
        elif asked == "bottom":
            question, correct, near = "ของเหลวใดอยู่ชั้นล่าง", lower, upper
            why = "ของเหลวที่มีความหนาแน่นมากกว่าจะจมอยู่ชั้นล่าง"
            padding = "อยู่ชั้นเดียวกันทั้งสองชนิด"
        else:
            question = "ไขก๊อกแล้วของเหลวใดออกก่อน"
            correct, near = lower, upper
            why = "ก๊อกอยู่ก้นกรวย ของเหลวชั้นล่างจึงไหลออกมาก่อน"
            padding = "ไหลออกมาพร้อมกันทั้งสองชนิด"

        return GeneratedQuestion(
            stem=[text(scenario + question)],
            correct=[text(correct.name)],
            distractors=fixed([text(near.name)], [text(padding)],
                              [text("รวมเป็นเนื้อเดียวกัน จึงแยกชั้นไม่ได้")]),
            topic=self.topic,
            hint=[text(why)],
        )


@question_type(
    "chem.density_application",
    display_name={"th": "ความหนาแน่นของสาร: คำนวณและเปรียบเทียบจากข้อมูล"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class DensityApplication(QuestionType):
    """Compute a density from measurements, or identify a sample by it."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            volume = rng.choice((2, 4, 5, 10, 20))
            density = rng.choice((2, 3, 5, 8))
            mass = density * volume
            correct = f"{density} g/cm³"
            wrongs = _distinct(correct, [
                f"{mass} g/cm³",
                f"{volume} g/cm³",
                f"{mass + volume} g/cm³",
                f"{Fraction(volume, mass)} g/cm³",
            ])
            assert wrongs is not None
            return _question(
                stem=(f"วัตถุชิ้นหนึ่งมีมวล {mass} g และมีปริมาตร {volume} cm³ "
                      "ความหนาแน่นของวัตถุนี้เป็นเท่าใด"),
                correct=correct,
                wrongs=wrongs,
                hint="ความหนาแน่นคือมวลหารด้วยปริมาตร ตรวจหน่วยของคำตอบด้วย",
            )
        if which == 1:
            material, density = rng.choice(DENSITY_MATERIALS)
            volume = rng.choice((10, 20, 50))
            mass = density * volume
            others = [m for m, d in DENSITY_MATERIALS if m != material]
            return _question(
                stem=(f"ตัวอย่างสารบริสุทธิ์ชิ้นหนึ่งมีปริมาตร {volume} cm³ "
                      f"และมีมวล {_fmt(mass)} g เมื่อเทียบกับตารางความหนาแน่น "
                      f"({', '.join(f'{m} {_fmt(d)}' for m, d in DENSITY_MATERIALS)} g/cm³) "
                      "ตัวอย่างนี้น่าจะเป็นสารใด"),
                correct=material,
                wrongs=tuple(rng.sample(others, 3)),
                hint="หาความหนาแน่นของตัวอย่างจากมวลและปริมาตรก่อน แล้วจึงเทียบกับตาราง",
            )
        return _question(
            stem=("เทน้ำมันพืช น้ำ และน้ำเชื่อมเข้มข้นลงในกระบอกเดียวกัน "
                  "แล้วตั้งทิ้งไว้จนแยกชั้น พบว่าน้ำเชื่อมอยู่ล่างสุดและน้ำมันพืชอยู่บนสุด "
                  "ข้อสรุปใดใช้หลักฐานได้ถูกต้อง"),
            correct="น้ำเชื่อมมีความหนาแน่นมากที่สุด และน้ำมันพืชมีความหนาแน่นน้อยที่สุด",
            wrongs=(
                "น้ำมันพืชมีความหนาแน่นมากที่สุด และน้ำเชื่อมมีความหนาแน่นน้อยที่สุด",
                "ของเหลวทั้งสามมีความหนาแน่นเท่ากัน จึงแยกชั้นกันได้พอดี",
                "ลำดับชั้นขึ้นกับปริมาตรที่เทลงไป ไม่ได้ขึ้นกับความหนาแน่น",
            ),
            hint="ของเหลวที่หนาแน่นมากกว่าจะจมลงอยู่ชั้นล่าง เรียงลำดับชั้นจากล่างขึ้นบน",
        )
