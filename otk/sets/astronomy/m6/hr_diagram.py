"""วิวัฒนาการของดาวฤกษ์และแผนภาพเฮิร์ตซ์สปรุง-รัสเซลล์

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/9

Sets moved here from: science_wave_f83.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f83 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_HR = "วิวัฒนาการของดาวฤกษ์และแผนภาพเฮิร์ตซ์สปรุง-รัสเซลล์"


HR_REGIONS = (
    ("แถบลำดับหลัก", "แนวทแยงจากมุมบนซ้าย (ร้อน สว่างมาก) ไปมุมล่างขวา (เย็น สว่างน้อย)"),
    ("ดาวยักษ์แดง", "ด้านขวาบน อุณหภูมิผิวต่ำแต่ส่องสว่างมากเพราะมีขนาดใหญ่"),
    ("ดาวยักษ์ใหญ่", "ด้านบนสุดของแผนภาพ ส่องสว่างมากที่สุด"),
    ("ดาวแคระขาว", "ด้านซ้ายล่าง อุณหภูมิผิวสูงแต่ส่องสว่างน้อยเพราะมีขนาดเล็ก"),
)


LOW_PATH = ("ดาวฤกษ์ในลำดับหลัก", "ดาวยักษ์แดง", "เนบิวลาดาวเคราะห์", "ดาวแคระขาว")


HIGH_PATH = ("ดาวฤกษ์ในลำดับหลัก", "ดาวยักษ์ใหญ่แดง", "ซูเปอร์โนวา", "ดาวนิวตรอนหรือหลุมดำ")


HR_HINT = ("แผนภาพ H-R: แกนนอนอุณหภูมิผิว (ร้อนทางซ้าย) แกนตั้งความส่องสว่าง ลำดับหลักพาดแนวทแยง ดาวยักษ์อยู่ขวาบน ดาวแคระขาวอยู่ซ้ายล่าง "
           "ดาวมวลน้อย: ลำดับหลัก → ดาวยักษ์แดง → เนบิวลาดาวเคราะห์ → ดาวแคระขาว "
           "ดาวมวลมาก: ลำดับหลัก → ดาวยักษ์ใหญ่แดง → ซูเปอร์โนวา → ดาวนิวตรอนหรือหลุมดำ")


END_STATES = ("ดาวแคระขาว", "ดาวนิวตรอน", "หลุมดำ")


@question_type(
    "astro.hr_diagram_foundation",
    display_name={"th": "บริเวณต่าง ๆ บนแผนภาพเฮิร์ตซ์สปรุง-รัสเซลล์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HR,
)
class HrDiagramFoundation(QuestionType):
    """Main sequence, giants, supergiants and white dwarfs on the diagram."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        name, where = rng.choice(HR_REGIONS)
        if roll < 0.35:
            return _labelled(stem=f"บนแผนภาพ H-R {name}อยู่บริเวณใด", correct=where, wrongs=tuple(w for n, w in HR_REGIONS if n != name),
                             topic=TOPIC_HR, hint=HR_HINT)
        if roll < 0.7:
            return _labelled(stem=f"บนแผนภาพ H-R ดาวที่อยู่{where}คือดาวกลุ่มใด", correct=name, wrongs=tuple(n for n, _ in HR_REGIONS if n != name),
                             topic=TOPIC_HR, hint=HR_HINT)
        facts = (("แกนนอนของแผนภาพ H-R แสดงปริมาณใด และเรียงอย่างไร", "อุณหภูมิผิว โดยร้อนอยู่ทางซ้าย เย็นอยู่ทางขวา",
                  ("อุณหภูมิผิว โดยเย็นอยู่ทางซ้าย ร้อนอยู่ทางขวา", "ระยะทางจากโลก", "อายุของดาว", "มวลของดาวเรียงจากมากไปน้อย")),
                 ("ดาวฤกษ์ส่วนใหญ่ที่สังเกตพบอยู่ในบริเวณใดของแผนภาพ H-R", "แถบลำดับหลัก",
                  ("บริเวณดาวแคระขาว", "บริเวณดาวยักษ์ใหญ่", "มุมขวาล่าง", "นอกแผนภาพ")),
                 ("ดาวฤกษ์ในแถบลำดับหลักสร้างพลังงานจากปฏิกิริยาใด", "ฟิวชันไฮโดรเจนเป็นฮีเลียมที่แกน",
                  ("ฟิวชันเหล็ก", "ฟิชชันยูเรเนียม", "การเผาไหม้ไฮโดรเจนกับออกซิเจน", "การยุบตัวเพียงอย่างเดียว")),
                 ("แกนตั้งของแผนภาพ H-R แสดงปริมาณใด", "ความส่องสว่างหรือโชติมาตรสัมบูรณ์ของดาว",
                  ("ระยะทางจากโลก", "อายุของดาว", "จำนวนดาวเคราะห์", "ความเร็วในการหมุนรอบตัวเอง")),
                 ("ในแถบลำดับหลัก ดาวที่อยู่ด้านบนซ้ายต่างจากดาวด้านล่างขวาอย่างไร", "มีมวลมากกว่า ร้อนกว่า และส่องสว่างมากกว่า",
                  ("มีมวลน้อยกว่า เย็นกว่า และส่องสว่างน้อยกว่า", "มีอายุในลำดับหลักยาวกว่า", "อยู่ใกล้โลกมากกว่าเสมอ", "เป็นดาวแคระขาวทั้งหมด")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_HR, hint=HR_HINT)


@question_type(
    "astro.hr_diagram_fluency",
    display_name={"th": "ลำดับวิวัฒนาการของดาวฤกษ์ตามมวลตั้งต้น"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HR,
)
class HrDiagramFluency(QuestionType):
    """End state by starting mass; order of stages; what changes on the way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            mass = Fraction(rng.choice([n for n in range(3, 600) if not 70 <= n <= 90 and not 230 <= n <= 270]), 10)
            right = END_STATES[0] if mass < 8 else END_STATES[1] if mass < 25 else END_STATES[2]
            return _labelled(stem=f"ดาวฤกษ์มวลตั้งต้น {show(mass)} เท่าของดวงอาทิตย์ ในบั้นปลายจะกลายเป็นวัตถุใด "
                                  f"(น้อยกว่า 8 เท่า → ดาวแคระขาว, 8-25 เท่า → ดาวนิวตรอน, มากกว่า 25 เท่า → หลุมดำ)",
                             correct=right, wrongs=(*(e for e in END_STATES if e != right), "ดาวเคราะห์แก๊สยักษ์"), topic=TOPIC_HR, hint=HR_HINT)
        if roll < 0.7:
            path = rng.choice((LOW_PATH, HIGH_PATH))
            perms = [p for p in permutations(path) if p != path and p[0] == path[0]]
            label = "มวลน้อยอย่างดวงอาทิตย์" if path is LOW_PATH else "มวลมากกว่าดวงอาทิตย์หลายสิบเท่า"
            return _labelled(stem=f"ข้อใดเรียงลำดับวิวัฒนาการของดาวฤกษ์{label}ได้ถูกต้อง", correct=" → ".join(path),
                             wrongs=tuple(" → ".join(p) for p in rng.sample(perms, 3)), topic=TOPIC_HR, hint=HR_HINT)
        changes = (("เมื่อดาวฤกษ์ออกจากลำดับหลักกลายเป็นดาวยักษ์แดง ขนาดและอุณหภูมิผิวเปลี่ยนอย่างไร", "ขนาดใหญ่ขึ้นมาก อุณหภูมิผิวลดลง",
                    ("ขนาดเล็กลง อุณหภูมิผิวสูงขึ้น", "ขนาดเล็กลง อุณหภูมิผิวลดลง", "ขนาดและอุณหภูมิผิวคงเดิม")),
                   ("เมื่อดาวยักษ์แดงกลายเป็นดาวแคระขาว ตำแหน่งบนแผนภาพ H-R เปลี่ยนอย่างไร", "เลื่อนจากขวาบนไปซ้ายล่าง",
                    ("เลื่อนจากซ้ายล่างไปขวาบน", "เลื่อนจากซ้ายบนไปขวาล่างตามแถบลำดับหลัก", "ไม่เปลี่ยนตำแหน่ง")),
                   ("ดาวแคระขาวมีขนาดและอุณหภูมิผิวอย่างไรเมื่อเทียบกับดวงอาทิตย์", "ขนาดเล็กกว่ามาก แต่อุณหภูมิผิวสูงกว่าหรือใกล้เคียง",
                    ("ขนาดใหญ่กว่ามาก อุณหภูมิผิวต่ำกว่า", "ขนาดเท่ากัน อุณหภูมิผิวเท่ากัน", "ขนาดใหญ่กว่ามาก อุณหภูมิผิวสูงกว่ามาก")),
                   ("ดาวฤกษ์มวลมากอยู่ในลำดับหลักได้นานกว่าหรือสั้นกว่าดาวมวลน้อย", "สั้นกว่า เพราะใช้เชื้อเพลิงเร็วกว่ามาก",
                    ("นานกว่า เพราะมีเชื้อเพลิงมากกว่า", "นานเท่ากันทุกดวง", "นานกว่า เพราะอุณหภูมิต่ำกว่า")))
        stem, right, wrongs = rng.choice(changes)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_HR, hint=HR_HINT)


@question_type(
    "astro.hr_diagram_application",
    display_name={"th": "คำนวณความส่องสว่างและอายุในลำดับหลักจากมวล"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HR,
)
class HrDiagramApplication(QuestionType):
    """L ∝ M⁴ and life = 10,000 million years × M / L; place a star on the diagram."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        mass = rng.choice((2, 3, 4, 5, 10, 20))
        if roll < 0.3:
            return numeric(stem=f"ดาวฤกษ์ในลำดับหลักมวล {mass} เท่าของดวงอาทิตย์ (L ∝ M⁴) มีความส่องสว่างกี่เท่าของดวงอาทิตย์",
                           answer=mass ** 4, wrongs=[mass ** 2, mass * 4, mass ** 3], unit="เท่า", topic=TOPIC_HR, hint="L = M⁴ เมื่อเทียบกับดวงอาทิตย์")
        if roll < 0.6:
            mass = rng.choice((2, 4, 5, 10, 20))
            life = Fraction(10000, mass ** 3)
            return numeric(stem=f"ดาวฤกษ์มวล {mass} เท่าของดวงอาทิตย์ (L ∝ M⁴ และอายุในลำดับหลัก = 10,000 ล้านปี × M ÷ L) "
                                f"จะอยู่ในลำดับหลักได้ประมาณกี่ล้านปี", answer=life,
                           wrongs=[Fraction(10000, mass ** 4), Fraction(10000, mass), 10000 * mass], unit="ล้านปี", topic=TOPIC_HR,
                           hint="อายุ = 10,000 × M ÷ M⁴ = 10,000 ÷ M³ ล้านปี")
        protos = (("แถบลำดับหลัก", (5000, 6500), (1, 3)), ("ดาวยักษ์แดง", (3200, 4500), (100, 1000)),
                  ("ดาวยักษ์ใหญ่", (3500, 20000), (50000, 300000)), ("ดาวแคระขาว", (8000, 25000), (0, 0)))
        name, (tlo, thi), (llo, lhi) = rng.choice(protos)
        temp = rng.randrange(tlo, thi + 1, 100)
        lum = f"{show(rng.randint(llo, lhi))}" if name != "ดาวแคระขาว" else rng.choice(("0.001", "0.005", "0.01", "0.002"))
        return _labelled(stem=f"ดาวฤกษ์ดวงหนึ่งมีอุณหภูมิผิว {show(temp)} K และส่องสว่าง {lum} เท่าของดวงอาทิตย์ น่าจะเป็นดาวกลุ่มใดบนแผนภาพ H-R",
                         correct=name, wrongs=tuple(p[0] for p in protos if p[0] != name), topic=TOPIC_HR, hint=HR_HINT)
