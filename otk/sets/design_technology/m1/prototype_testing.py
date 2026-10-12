"""การทดสอบและปรับปรุงชิ้นงาน

การออกแบบและเทคโนโลยี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.1/4

Sets moved here from: technology_t2s1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t2s1 import LABELS, M1

PROVENANCE = Provenance("original")


TEST_TOPIC = "การทดสอบและปรับปรุงชิ้นงาน"


FIXES = (
    ("ที่วางโทรศัพท์ล้มเมื่อวางโทรศัพท์", "ขยายฐานให้กว้างขึ้นเพื่อให้ตั้งได้มั่นคง"),
    ("สะพานกระดาษยุบตรงกลางเมื่อวางเหรียญ", "พับกระดาษเป็นคานรูปตัวยูหรือสามเหลี่ยมเพื่อเพิ่มความแข็งแรง"),
    ("น้ำจากขวดรดน้ำหยดเร็วจนหมดภายในวันเดียว", "ทำรูที่ฝาขวดให้เล็กลง"),
    ("ป้ายบอกประเภทขยะมองไม่เห็นจากระยะไกล", "ใช้ตัวอักษรขนาดใหญ่และสีที่ต่างกันชัดเจน"),
    ("กล่องแยกยาเปิดฝายากสำหรับคุณยาย", "เปลี่ยนเป็นฝาแบบเลื่อนหรือเพิ่มที่จับให้ใหญ่ขึ้น"),
    ("ชั้นวางรองเท้าโยกเมื่อวางรองเท้าหลายคู่", "เพิ่มไม้ค้ำยันแนวทแยงที่ด้านหลัง"),
    ("รถของเล่นวิ่งได้ระยะสั้นเพราะล้อเสียดสีกับตัวรถ", "เว้นระยะระหว่างล้อกับตัวรถให้ล้อหมุนได้คล่อง"),
    ("ที่ม้วนสายชาร์จทำให้สายหักงอตรงหัวชาร์จ", "ออกแบบให้ม้วนสายเป็นวงกว้างขึ้นและไม่พับสายตรงหัวชาร์จ"),
)


@question_type(
    "tech.prototype_testing_foundation",
    display_name={"th": "อ่านผลการทดสอบชิ้นงานเทียบกับเกณฑ์"},
    level=M1, subject=SUBJECT, topic=TEST_TOPIC,
)
class PrototypeTestingFoundation(QuestionType):
    """Four paper bridges, coins held, one pass mark: which pass or which is best."""

    def build(self, rng: Random, **params):
        need = rng.randint(15, 40)
        held = rng.sample(range(need - 12, need + 13), 4)
        passing = [h for h in held if h >= need]
        if not passing:
            held[rng.randrange(4)] = need + rng.randint(0, 8)
            passing = [h for h in held if h >= need]
        listed = " ".join(f"แบบ {ell} รับได้ {h} เหรียญ" for ell, h in zip(LABELS, held))
        hint = "เทียบผลของแต่ละแบบกับเกณฑ์ ค่าที่เท่ากับเกณฑ์ถือว่าผ่าน"
        if rng.random() < 0.5 or len(passing) != 1:
            best = LABELS[held.index(max(held))]
            return _labelled(
                stem=f"ผลการทดสอบสะพานกระดาษ {listed} แบบใดรับเหรียญได้มากที่สุด",
                correct=f"แบบ {best}", wrongs=tuple(f"แบบ {ell}" for ell in LABELS if ell != best),
                hint="เปรียบเทียบจำนวนเหรียญของทุกแบบ", topic=TEST_TOPIC,
            )
        answer = LABELS[held.index(passing[0])]
        return _labelled(
            stem=(f"เกณฑ์คือสะพานกระดาษต้องรับได้อย่างน้อย {need} เหรียญ ผลการทดสอบ {listed} "
                  f"แบบใดผ่านเกณฑ์"),
            correct=f"แบบ {answer}", wrongs=tuple(f"แบบ {ell}" for ell in LABELS if ell != answer),
            hint=hint, topic=TEST_TOPIC,
        )


@question_type(
    "tech.prototype_testing_fluency",
    display_name={"th": "ระบุแนวทางปรับปรุงข้อบกพร่องของชิ้นงาน"},
    level=M1, subject=SUBJECT, topic=TEST_TOPIC,
)
class PrototypeTestingFluency(QuestionType):
    def build(self, rng: Random, **params):
        index = rng.randrange(len(FIXES))
        flaw, fix = FIXES[index]
        others = rng.sample([row for i, row in enumerate(FIXES) if i != index], 3)
        hint = "แนวทางปรับปรุงที่ดีแก้ที่สาเหตุของข้อบกพร่องนั้นโดยตรง"
        if rng.random() < 0.5:
            return _labelled(stem=f"ผลการทดสอบพบว่า{flaw} ควรปรับปรุงอย่างไร",
                             correct=fix, wrongs=tuple(f for _, f in others),
                             hint=hint, topic=TEST_TOPIC)
        return _labelled(stem=f"การปรับปรุงโดย “{fix}” แก้ข้อบกพร่องใด",
                         correct=flaw, wrongs=tuple(f for f, _ in others),
                         hint=hint, topic=TEST_TOPIC)


@question_type(
    "tech.prototype_testing_application",
    display_name={"th": "ประเมินผลการทดสอบซ้ำด้วยค่าเฉลี่ย"},
    level=M1, subject=SUBJECT, topic=TEST_TOPIC,
)
class PrototypeTestingApplication(QuestionType):
    """Three runs of a toy car, their mean against a requirement."""

    def build(self, rng: Random, **params):
        mean = rng.randint(80, 200)
        a = rng.randint(3, 15) * rng.choice((-1, 1))   # never three equal runs
        b = rng.randint(-15, 15)
        runs = [mean + a, mean + b, mean - a - b]
        rng.shuffle(runs)
        need = mean + rng.choice((-10, -5, 0, 5, 10))
        passes = mean >= need

        def verdict(value: int, ok: bool) -> str:
            return f"ค่าเฉลี่ย {value} ซม. {'ผ่านเกณฑ์' if ok else 'ไม่ผ่านเกณฑ์'}"

        correct = verdict(mean, passes)
        wrongs = {verdict(mean, not passes), verdict(max(runs), max(runs) >= need),
                  verdict(sum(runs), True), verdict(min(runs), min(runs) >= need)} - {correct}
        return _labelled(
            stem=(f"ทดสอบรถของเล่น 3 ครั้ง วิ่งได้ {runs[0]} ซม. {runs[1]} ซม. และ {runs[2]} ซม. "
                  f"เกณฑ์คือค่าเฉลี่ยต้องไม่น้อยกว่า {need} ซม. ข้อใดถูกต้อง"),
            correct=correct, wrongs=tuple(sorted(wrongs)),
            hint="ค่าเฉลี่ยคือผลรวมของทุกครั้งหารด้วยจำนวนครั้ง แล้วจึงเทียบกับเกณฑ์",
            topic=TEST_TOPIC,
        )
