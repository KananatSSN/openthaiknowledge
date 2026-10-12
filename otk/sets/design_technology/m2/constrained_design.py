"""การออกแบบภายใต้เงื่อนไขและทรัพยากร

การออกแบบและเทคโนโลยี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.2/3

Sets moved here from: technology_t2s2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s2 import M2

PROVENANCE = Provenance("original")


BUDGET_TOPIC = "การออกแบบภายใต้เงื่อนไขและทรัพยากร"


LABELS = ("ก", "ข", "ค", "ง")


PRICES = (("แผ่นไม้อัด", "แผ่น", 45, 120), ("ตะปู", "กล่อง", 20, 45), ("สีทาไม้", "กระป๋อง", 60, 150),
          ("บานพับ", "คู่", 15, 40), ("กาวลาเท็กซ์", "ขวด", 25, 60), ("ล้อเลื่อน", "ล้อ", 20, 50))


BUILD_STEPS = ("ร่างแบบ", "ตัดชิ้นส่วน", "ประกอบ", "ทาสีและรอให้แห้ง", "ทดสอบ")


def _clock(minutes: int) -> str:
    return f"{minutes // 60:02d}:{minutes % 60:02d} น."


CRITERIA = (("ราคาถูก", 3), ("ความแข็งแรง", 2), ("ความสวยงาม", 1))


def weighted(scores) -> int:
    return sum(score * weight for score, (_, weight) in zip(scores, CRITERIA))


@question_type(
    "tech.constrained_design_foundation",
    display_name={"th": "คำนวณค่าใช้จ่ายของวัสดุเทียบกับงบประมาณ"},
    level=M2, subject=SUBJECT, topic=BUDGET_TOPIC,
)
class ConstrainedDesignFoundation(QuestionType):
    def build(self, rng: Random, **params):
        items = rng.sample(PRICES, 3)
        lines = []
        total = 0
        for name, unit, low, high in items:
            price = rng.randrange(low, high + 1, 5)
            count = rng.randint(1, 4)
            total += price * count
            lines.append(f"{name} {count} {unit} {unit}ละ {price} บาท")
        budget = (total // 50 + rng.choice((-1, 1, 2, 3))) * 50
        listed = " ".join(lines)
        if budget >= total:
            left = budget - total
            return _labelled(
                stem=f"งบประมาณ {budget} บาท ต้องซื้อ {listed} จะเหลือเงินกี่บาท",
                correct=f"{left} บาท",
                wrongs=tuple(f"{w} บาท" for w in rng.sample(_near(left, (total, left + 50, abs(left - 45), budget)), 3)),
                hint="คูณราคาต่อหน่วยกับจำนวนของวัสดุแต่ละรายการ รวมกันเป็นค่าใช้จ่าย แล้วหักออกจากงบประมาณ",
                topic=BUDGET_TOPIC,
            )
        over = total - budget
        return _labelled(
            stem=f"งบประมาณ {budget} บาท ต้องซื้อ {listed} ค่าใช้จ่ายเกินงบประมาณกี่บาท",
            correct=f"{over} บาท",
            wrongs=tuple(f"{w} บาท" for w in rng.sample(_near(over, (total, over + 50, budget, over + 5)), 3)),
            hint="คูณราคาต่อหน่วยกับจำนวนของวัสดุแต่ละรายการ รวมกันเป็นค่าใช้จ่าย แล้วเทียบกับงบประมาณ",
            topic=BUDGET_TOPIC,
        )


@question_type(
    "tech.constrained_design_fluency",
    display_name={"th": "วางแผนเวลาในการสร้างชิ้นงาน"},
    level=M2, subject=SUBJECT, topic=BUDGET_TOPIC,
)
class ConstrainedDesignFluency(QuestionType):
    def build(self, rng: Random, **params):
        durations = [rng.randrange(10, 65, 5) for _ in BUILD_STEPS]
        start = rng.randrange(8 * 60, 14 * 60 + 1, 15)
        total = sum(durations)
        listed = " ".join(f"{s} {d} นาที" for s, d in zip(BUILD_STEPS, durations))
        finish = start + total
        wrongs = _near(finish, (finish - durations[-1], finish + 30, start + total // 2, finish - 60))
        return _labelled(
            stem=(f"แผนการสร้างชิ้นงานมีขั้นตอนต่อเนื่องกันดังนี้ {listed} "
                  f"ถ้าเริ่มงานเวลา {_clock(start)} และทำต่อเนื่องไม่หยุดพัก จะเสร็จเวลาใด"),
            correct=_clock(finish), wrongs=tuple(_clock(w) for w in rng.sample(wrongs, 3)),
            hint="รวมเวลาของทุกขั้นตอน แล้วนับต่อจากเวลาเริ่ม 60 นาทีเท่ากับ 1 ชั่วโมง",
            topic=BUDGET_TOPIC,
        )


@question_type(
    "tech.constrained_design_application",
    display_name={"th": "ตัดสินใจเลือกแนวทางด้วยตารางให้คะแนนแบบถ่วงน้ำหนัก"},
    level=M2, subject=SUBJECT, topic=BUDGET_TOPIC,
)
class ConstrainedDesignApplication(QuestionType):
    def build(self, rng: Random, **params):
        while True:
            options = [[rng.randint(1, 5) for _ in CRITERIA] for _ in range(3)]
            totals = [weighted(o) for o in options]
            if len(set(totals)) == 3:
                break
        weights = " ".join(f"{name} น้ำหนัก {w}" for name, w in CRITERIA)
        table = " ".join(
            f"แบบ {LABELS[i]} ได้ " + " ".join(f"{name} {s}" for (name, _), s in zip(CRITERIA, o)) + " คะแนน"
            for i, o in enumerate(options))
        best = LABELS[totals.index(max(totals))]
        return _labelled(
            stem=(f"ตารางตัดสินใจให้คะแนนแต่ละเกณฑ์เต็ม 5 และถ่วงน้ำหนักดังนี้ {weights} "
                  f"ผลการให้คะแนน {table} เมื่อคูณคะแนนกับน้ำหนักแล้วรวมกัน ควรเลือกแบบใด"),
            correct=f"แบบ {best}",
            wrongs=(*[f"แบบ {ell}" for ell in LABELS[:3] if ell != best], "ทุกแบบได้คะแนนรวมเท่ากัน"),
            hint="คูณคะแนนของแต่ละเกณฑ์กับน้ำหนัก รวมทุกเกณฑ์ของแต่ละแบบ แล้วเลือกแบบที่ได้ผลรวมมากที่สุด",
            topic=BUDGET_TOPIC,
        )
