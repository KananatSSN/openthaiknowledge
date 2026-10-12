"""สารบริสุทธิ์และสารผสม

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/4

Sets moved here from: science_wave_a, substances.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.science_wave_a import CHEMISTRY, MATTER, _question
from otk.sets._support.substances import LEVEL, SUBJECT, TOPIC_PURE

PROVENANCE = Provenance("original")


PURE_EXAMPLES = (
    ("น้ำกลั่น", "สารบริสุทธิ์"),
    ("ทองคำบริสุทธิ์", "สารบริสุทธิ์"),
    ("แก๊สออกซิเจนที่แยกได้", "สารบริสุทธิ์"),
    ("น้ำเกลือ", "สารผสม"),
    ("น้ำเชื่อม", "สารผสม"),
    ("อากาศ", "สารผสม"),
    ("นมสด", "สารผสม"),
    ("เงินบริสุทธิ์", "สารบริสุทธิ์"),
    ("แก๊สไนโตรเจนที่แยกได้", "สารบริสุทธิ์"),
    ("น้ำตาลทรายบริสุทธิ์", "สารบริสุทธิ์"),
    ("น้ำแข็งที่ทำจากน้ำกลั่น", "สารบริสุทธิ์"),
    ("น้ำโคลน", "สารผสม"),
    ("น้ำส้มคั้น", "สารผสม"),
    ("ทองเหลือง", "สารผสม"),
    ("น้ำอัดลม", "สารผสม"),
)


_LABELS = ("ก", "ข", "ค", "ง")


_FIXED_BP = (65, 78, 80, 100, 118, 132)          # °C, จุดเดือดคงที่


_RANGE_BP = ((70, 85), (88, 96), (95, 103),      # °C, ช่วงที่อุณหภูมิค่อยๆ สูงขึ้น
             (105, 120), (60, 78), (125, 140))


@question_type(
    "chem.pure_mixture_foundation",
    display_name={"th": "สารบริสุทธิ์และสารผสม: จำแนกจากตัวอย่าง"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class PureMixtureFoundation(QuestionType):
    """Classify one named material, or state what a fixed boiling point means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.randrange(2) == 0:
            material, kind = rng.choice(PURE_EXAMPLES)
            other = "สารผสม" if kind == "สารบริสุทธิ์" else "สารบริสุทธิ์"
            return _question(
                stem=f"{material}จัดเป็นสารประเภทใด",
                correct=kind,
                wrongs=(
                    other,
                    "ธาตุ",
                    "สารประกอบ",
                    "สารละลายกรด",
                ),
                hint="ถามว่าสารนี้มีองค์ประกอบชนิดเดียวหรือมีหลายชนิดปนกัน",
                topic=MATTER,
            )
        if rng.randrange(2) == 0:
            return _question(
                stem="ขณะที่สารผสมกำลังเดือด อุณหภูมิของสารมีลักษณะอย่างไร",
                correct="ค่อย ๆ เปลี่ยนไปเป็นช่วงอุณหภูมิ ไม่คงที่ที่ค่าเดียว",
                wrongs=(
                    "คงที่ตลอดช่วงที่เดือด เช่นเดียวกับสารบริสุทธิ์",
                    "ลดลงเรื่อย ๆ จนสารผสมกลับเป็นของแข็งทั้งหมด",
                    "เท่ากับ 100 °C ทุกครั้ง ไม่ว่าจะเป็นสารผสมใด",
                    "คงที่ที่ค่าเดียว ซึ่งสูงกว่าจุดเดือดของน้ำเสมอ",
                ),
                hint="สารบริสุทธิ์มีจุดเดือดคงที่ ส่วนสารผสมมีช่วงอุณหภูมิที่เปลี่ยนไปขณะเดือด",
                topic=MATTER,
            )
        return _question(
            stem="ขณะที่สารบริสุทธิ์กำลังเดือด อุณหภูมิของสารมีลักษณะอย่างไร",
            correct="คงที่ตลอดช่วงที่เดือด",
            wrongs=(
                "เพิ่มขึ้นตลอดช่วงที่เดือด",
                "ลดลงตลอดช่วงที่เดือด",
                "เท่ากับ 100 °C ทุกครั้ง",
                "เปลี่ยนตามปริมาณที่ต้ม",
            ),
            hint="สารบริสุทธิ์มีจุดเดือดคงที่ ส่วนสารผสมมีช่วงอุณหภูมิที่เปลี่ยนไปขณะเดือด",
            topic=MATTER,
        )


@question_type("chem.pure_or_mixture",
               display_name={"th": "สารบริสุทธิ์ สารละลาย และสารเนื้อผสม"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_PURE)
class PureOrMixture(ClassifyType):
    """จำแนกสารเป็นสารบริสุทธิ์ / สารเนื้อเดียวที่ไม่บริสุทธิ์ / สารเนื้อผสม.

    The three-way split both sheets open with. The middle category is the one
    students collapse into the first: น้ำเกลือ *is* เนื้อเดียว — you cannot see
    the salt — but it is not บริสุทธิ์, because its จุดเดือด is not คงที่.
    """

    # "ตรงกับ" / "เป็นตัวอย่างหรือลักษณะของ" rather than "จัดเป็น", because the
    # members are a mix of substances and properties: "ข้อใดจัดเป็นสารเนื้อผสม"
    # does not read as a question about "สมบัติของสารแต่ละส่วนไม่เหมือนกัน…".
    CLASSIFY_STEM = "“{member}” ตรงกับสารประเภทใด"
    PICK_STEM = "ข้อใดเป็นตัวอย่างหรือลักษณะของ{category}"

    CATEGORIES = [
        Category("สารบริสุทธิ์ (สารเนื้อเดียว จุดเดือดคงที่)",
                 ("น้ำกลั่น", "แอลกอฮอล์บริสุทธิ์", "เกลือแกง", "น้ำตาลทราย",
                  "ทองคำบริสุทธิ์", "แก๊สออกซิเจน",
                  "มีจุดเดือดและจุดหลอมเหลวคงที่",
                  "ประกอบด้วยสารเพียงชนิดเดียว")),
        Category("สารเนื้อเดียวที่ไม่บริสุทธิ์ (สารละลาย)",
                 ("น้ำเกลือ", "น้ำเชื่อม", "อากาศ", "น้ำส้มสายชู", "ทองเหลือง",
                  "มองไม่เห็นเนื้อสารแยกกัน แต่จุดเดือดไม่คงที่",
                  "เกิดจากสารตั้งแต่ 2 ชนิดผสมกันจนกลมกลืนเป็นเนื้อเดียว")),
        Category("สารเนื้อผสม",
                 ("น้ำโคลน", "ข้าวสารที่มีข้าวเปลือกปน", "พริกกับเกลือที่ตำรวมกัน",
                  "น้ำกับน้ำมันพืช", "ผงเหล็กผสมผงกำมะถัน",
                  "มองเห็นเนื้อสารแต่ละส่วนแยกกันไม่กลมกลืน",
                  "สมบัติของสารแต่ละส่วนไม่เหมือนกันทุกตำแหน่ง")),
    ]


@question_type(
    "chem.pure_mixture_fluency",
    display_name={"th": "สารบริสุทธิ์และสารผสม: อ่านกราฟและตารางอุณหภูมิ"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class PureMixtureFluency(QuestionType):
    """Read one heating record and decide pure or mixture."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(2)
        if which == 0:
            plateau = rng.choice((56, 65, 78, 80, 100, 118))
            return _question(
                stem=("ให้ความร้อนแก่ของเหลวชนิดหนึ่งและบันทึกอุณหภูมิทุกนาที "
                      f"พบว่าอุณหภูมิคงที่ที่ {plateau} °C ตลอดช่วงที่ของเหลวเดือด "
                      "ข้อสรุปใดเหมาะสมที่สุด"),
                correct=f"เป็นสารบริสุทธิ์ เพราะมีจุดเดือดคงที่ที่ {plateau} °C",
                wrongs=(
                    f"เป็นสารผสม เพราะอุณหภูมิคงที่ที่ {plateau} °C",
                    "เป็นสารผสม เพราะของเหลวทุกชนิดที่เดือดได้เป็นสารผสม",
                    "บอกไม่ได้ เพราะจุดเดือดไม่เกี่ยวกับความบริสุทธิ์ของสาร",
                    "เป็นสารผสม เพราะจุดเดือดไม่ใช่ 100 °C" if plateau != 100 else "เป็นสารผสม เพราะน้ำทุกชนิดเป็นสารผสม",
                    "เป็นสารบริสุทธิ์ เพราะของเหลวมีสีใส",
                ),
                hint="ดูว่าอุณหภูมิขณะเดือดคงที่หรือค่อย ๆ เปลี่ยน แล้วจึงสรุปความบริสุทธิ์",
                topic=MATTER,
            )
        start = rng.choice((92, 95, 98))
        end = start + rng.randrange(4, 9)
        return _question(
            stem=("ให้ความร้อนแก่ของเหลวอีกชนิดหนึ่ง พบว่าขณะเดือดอุณหภูมิ "
                  f"ค่อย ๆ เพิ่มจาก {start} °C เป็น {end} °C ข้อสรุปใดเหมาะสมที่สุด"),
            correct="เป็นสารผสม เพราะขณะเดือดอุณหภูมิไม่คงที่แต่เปลี่ยนเป็นช่วง",
            wrongs=(
                "เป็นสารบริสุทธิ์ เพราะอุณหภูมิเพิ่มขึ้นอย่างสม่ำเสมอ",
                f"เป็นสารบริสุทธิ์ ที่มีจุดเดือด {end} °C ซึ่งเป็นค่าสุดท้ายที่วัดได้",
                "เป็นสารบริสุทธิ์ เพราะสารผสมไม่สามารถเดือดได้เลยไม่ว่าจะให้ความร้อนเท่าใด",
                f"เป็นสารบริสุทธิ์ ที่มีจุดเดือด {start} °C ซึ่งเป็นค่าแรกที่เริ่มเดือด",
                "บอกไม่ได้ เพราะของเหลวทุกชนิดเดือดเป็นช่วงอุณหภูมิ",
            ),
            hint="สารบริสุทธิ์เดือดที่อุณหภูมิคงที่ค่าเดียว ส่วนสารผสมเดือดเป็นช่วงอุณหภูมิ",
            topic=MATTER,
        )


@question_type("chem.purity_from_boiling",
               display_name={"th": "อ่านจุดเดือดเพื่อบอกความบริสุทธิ์ของสาร"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC_PURE)
class PurityFromBoiling(QuestionType):
    """ตัดสินว่าสารบริสุทธิ์หรือไม่ จากพฤติกรรมของอุณหภูมิขณะเดือด.

    Two asks. ``1`` shows two substances and asks which is บริสุทธิ์ — the
    comparison the sheet's definition rests on. ``2`` shows one and asks what it
    is, so the rule has to be applied without a foil to lean on.
    """

    ASKS = ("compare", "single")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        asked = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        fixed_bp = rng.choice(_FIXED_BP)
        lo, hi = rng.choice(_RANGE_BP)
        if asked == "compare":
            return self._compare(rng, fixed_bp, lo, hi)
        return self._single(rng, fixed_bp, lo, hi)

    def _compare(self, rng: Random, bp: int, lo: int, hi: int) -> GeneratedQuestion:
        pure, mixed = rng.sample(_LABELS, 2)
        # The unit is stated once up front rather than after each number: the PDF
        # renderer neither wraps nor clips, and in a two-column sheet a cell is
        # half as wide, so every repeated word is one that runs off the page.
        return GeneratedQuestion(
            stem=[text(f"หน่วยเป็นองศาเซลเซียส สาร {pure} เดือดคงที่ที่ {bp} "
                       f"ส่วนสาร {mixed} เดือดในช่วง {lo}–{hi} "
                       f"สารใดเป็นสารบริสุทธิ์")],
            correct=[text(f"สาร {pure}")],
            distractors=fixed([text(f"สาร {mixed}")],
                              [text("เป็นสารบริสุทธิ์ทั้งสองชนิด")],
                              [text("ไม่เป็นสารบริสุทธิ์ทั้งสองชนิด")]),
            topic=self.topic,
            hint=[text("สารบริสุทธิ์มีจุดเดือดคงที่ สารผสมเดือดในช่วงอุณหภูมิหนึ่ง")],
        )

    def _single(self, rng: Random, bp: int, lo: int, hi: int) -> GeneratedQuestion:
        label = rng.choice(_LABELS)
        if rng.random() < 0.5:
            stem = (f"ขณะที่สาร {label} เดือด วัดอุณหภูมิได้ {bp} องศาเซลเซียส "
                    f"คงที่ตลอด สาร {label} จัดเป็นสารประเภทใด")
            correct = "สารบริสุทธิ์ เพราะมีจุดเดือดคงที่"
            wrong = "สารผสม เพราะมีจุดเดือดคงที่"
        else:
            stem = (f"ขณะที่สาร {label} เดือด อุณหภูมิสูงขึ้นเรื่อยๆ จาก {lo} ถึง "
                    f"{hi} องศาเซลเซียส สาร {label} จัดเป็นสารประเภทใด")
            correct = "สารผสม เพราะจุดเดือดไม่คงที่"
            wrong = "สารบริสุทธิ์ เพราะจุดเดือดไม่คงที่"
        return GeneratedQuestion(
            stem=[text(stem)],
            correct=[text(correct)],
            distractors=fixed([text(wrong)],
                              [text("ธาตุ เพราะแยกด้วยวิธีทางเคมีไม่ได้")],
                              [text("สารเนื้อผสม เพราะมองเห็นเนื้อสารแยกกัน")]),
            topic=self.topic,
            hint=[text("สารบริสุทธิ์มีจุดเดือดคงที่ สารผสมเดือดในช่วงอุณหภูมิหนึ่ง")],
        )


@question_type(
    "chem.pure_mixture_application",
    display_name={"th": "สารบริสุทธิ์และสารผสม: วิเคราะห์ข้อมูลการทดลอง"},
    level={"th": "ม.1"}, subject=CHEMISTRY, topic=MATTER,
)
class PureMixtureApplication(QuestionType):
    """Compare two samples, or judge an experimental claim from a record."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            fixed = rng.choice((100, 80, 78))
            low = fixed - rng.randrange(3, 7)
            high = fixed + rng.randrange(3, 7)
            return _question(
                stem=("ให้ความร้อนแก่ของเหลวสองตัวอย่างและบันทึกอุณหภูมิขณะเดือด\n"
                      f"ตัวอย่าง ก: คงที่ที่ {fixed} °C\n"
                      f"ตัวอย่าง ข: เพิ่มจาก {low} °C เป็น {high} °C\n"
                      "ข้อสรุปใดใช้หลักฐานได้ถูกต้อง"),
                correct="ก เป็นสารบริสุทธิ์ และ ข เป็นสารผสม",
                wrongs=(
                    "ก เป็นสารผสม และ ข เป็นสารบริสุทธิ์",
                    "ทั้งสองเป็นสารบริสุทธิ์ เพราะทั้งคู่เดือดได้",
                    "ทั้งสองเป็นสารผสม เพราะอุณหภูมิของทั้งคู่เปลี่ยนแปลงระหว่างการทดลอง",
                ),
                hint="เทียบว่าอุณหภูมิขณะเดือดของแต่ละตัวอย่างคงที่หรือเป็นช่วง",
                topic=MATTER,
            )
        if which == 1:
            pure = rng.choice((100, 80))
            added = rng.randrange(2, 6)
            return _question(
                stem=(f"น้ำกลั่นเดือดที่ {pure} °C เมื่อละลายเกลือลงไปแล้ววัดใหม่ "
                      f"พบว่าเดือดที่ประมาณ {pure + added} °C นักเรียนสรุปว่า "
                      "“น้ำเกลือเป็นสารบริสุทธิ์ชนิดใหม่” ข้อใดประเมินข้อสรุปนี้ได้ถูกต้อง"),
                correct=("ไม่ถูกต้อง เพราะน้ำเกลือเป็นสารผสม การที่จุดเดือดเปลี่ยนไป "
                         "เป็นผลจากตัวละลายที่ปนอยู่ ไม่ใช่การเกิดสารบริสุทธิ์ใหม่"),
                wrongs=(
                    "ถูกต้อง เพราะสารที่มีจุดเดือดต่างจากเดิมย่อมเป็นสารบริสุทธิ์ชนิดใหม่",
                    "ไม่ถูกต้อง เพราะการเติมเกลือไม่มีผลต่อจุดเดือดของน้ำเลย ค่าที่วัดได้จึงมาจากเทอร์มอมิเตอร์ที่คลาดเคลื่อน",
                    "ถูกต้อง เพราะน้ำและเกลือรวมตัวกันเป็นสารประกอบชนิดใหม่ ซึ่งมีจุดเดือดคงที่ค่าใหม่ของตนเอง",
                    "ไม่ถูกต้อง เพราะน้ำเกลือเป็นธาตุ การที่จุดเดือดสูงขึ้นแสดงว่าเกลือเปลี่ยนน้ำให้เป็นธาตุชนิดใหม่",
                ),
                hint="ถามว่าองค์ประกอบยังแยกกันอยู่หรือไม่ และจุดเดือดที่เปลี่ยนไปบอกอะไรเกี่ยวกับความบริสุทธิ์",
                topic=MATTER,
            )
        return _question(
            stem=("ต้องการตรวจว่าของเหลวที่ได้จากการกลั่นเป็นสารบริสุทธิ์หรือไม่ "
                  "วิธีการใดให้หลักฐานที่ดีที่สุด"),
            correct=("วัดอุณหภูมิขณะเดือดอย่างต่อเนื่อง แล้วดูว่าอุณหภูมิคงที่ที่ค่าเดียว "
                     "หรือเปลี่ยนเป็นช่วง"),
            wrongs=(
                "ดูว่าของเหลวใสและไม่มีสี เพราะของเหลวที่ใสไม่มีสีย่อมเป็นสารบริสุทธิ์ทุกชนิด",
                "ดมกลิ่นของเหลว เพราะสารบริสุทธิ์ไม่มีกลิ่น ส่วนสารผสมมีกลิ่นของสารที่ปนอยู่",
                "วัดปริมาตรของเหลวก่อนและหลังการกลั่น ถ้าปริมาตรเท่าเดิมแสดงว่าเป็นสารบริสุทธิ์",
            ),
            hint="เลือกวิธีที่วัดสมบัติเฉพาะตัวของสาร ไม่ใช่ลักษณะที่มองเห็นได้เพียงอย่างเดียว",
            topic=MATTER,
        )
