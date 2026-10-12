"""การทดลองเรื่องปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมี

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/4

Sets moved here from: science_wave_i1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_i1 import CHEMISTRY, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_RATE = "การทดลองเรื่องปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมี"


# (factor, experiment, independent, dependent, controlled, collision explanation)
RATE_EXPERIMENTS = (
    ("ความเข้มข้น", "ใส่ลวดแมกนีเซียมขนาดเท่ากันลงในกรดไฮโดรคลอริกที่มีความเข้มข้นต่างกัน ปริมาตรเท่ากัน "
     "ที่อุณหภูมิเดียวกัน แล้วจับเวลาจนลวดแมกนีเซียมหมด",
     "ความเข้มข้นของกรดไฮโดรคลอริก", "เวลาที่ลวดแมกนีเซียมหมด", "ขนาดของลวดแมกนีเซียม",
     "จำนวนอนุภาคต่อหน่วยปริมาตรมากขึ้น อนุภาคจึงชนกันบ่อยขึ้น"),
    ("พื้นที่ผิว", "ใส่หินปูนมวลเท่ากัน แบบก้อนและแบบผง ลงในกรดไฮโดรคลอริกความเข้มข้นและปริมาตรเท่ากัน "
     "แล้ววัดปริมาตรแก๊สคาร์บอนไดออกไซด์ใน 1 นาที",
     "ขนาดของชิ้นหินปูน", "ปริมาตรแก๊สคาร์บอนไดออกไซด์ใน 1 นาที", "มวลของหินปูน",
     "อนุภาคที่ผิวสัมผัสกับสารอื่นได้มากขึ้น จึงชนกันบ่อยขึ้น"),
    ("อุณหภูมิ", "ผสมสารละลายโซเดียมไทโอซัลเฟตกับกรดไฮโดรคลอริกในขวดที่วางบนกระดาษมีเครื่องหมาย X "
     "ที่อุณหภูมิต่างกัน แล้วจับเวลาจนมองไม่เห็นเครื่องหมาย X",
     "อุณหภูมิของสารละลาย", "เวลาที่มองไม่เห็นเครื่องหมาย X", "ความเข้มข้นของสารละลายทั้งสอง",
     "อนุภาคมีพลังงานจลน์มากขึ้น การชนที่มีพลังงานถึงพลังงานก่อกัมมันต์จึงมากขึ้น"),
    ("ตัวเร่งปฏิกิริยา", "ใส่สารละลายไฮโดรเจนเปอร์ออกไซด์ปริมาตรและความเข้มข้นเท่ากันลงในหลอดสองหลอด "
     "เติมแมงกานีส(IV)ออกไซด์ลงในหลอดหนึ่ง แล้วสังเกตฟองแก๊สออกซิเจน",
     "การเติมแมงกานีส(IV)ออกไซด์", "ปริมาณฟองแก๊สออกซิเจนที่เกิดขึ้น", "ปริมาตรของไฮโดรเจนเปอร์ออกไซด์",
     "เกิดกลไกใหม่ที่มีพลังงานก่อกัมมันต์ต่ำลง อนุภาคที่ชนกันจึงเกิดปฏิกิริยาได้มากขึ้น"),
)


ROLES = ("ตัวแปรต้น", "ตัวแปรตาม", "ตัวแปรควบคุม")


RATE_MISCONCEPTIONS = (
    "ตัวเร่งปฏิกิริยาให้พลังงานแก่อนุภาค อนุภาคจึงมีพลังงานจลน์มากขึ้นและชนกันแรงขึ้น",
    "อุณหภูมิที่สูงขึ้นทำให้พลังงานก่อกัมมันต์ของปฏิกิริยาลดลง อนุภาคจึงเกิดปฏิกิริยาง่ายขึ้น",
    "ความเข้มข้นที่มากขึ้นทำให้อนุภาคแต่ละตัวมีขนาดใหญ่ขึ้น จึงชนกันได้ง่ายขึ้นกว่าเดิม",
)


@question_type(
    "chem.rate_experiment_foundation",
    display_name={"th": "ตัวแปรในการทดลองเรื่องอัตราการเกิดปฏิกิริยา"},
    level=UPPER_FIVE, subject=CHEMISTRY, topic=TOPIC_RATE,
)
class RateExperimentFoundation(QuestionType):
    """Which variable is changed, which is measured, which is kept the same."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        factor, setup, changed, measured, kept, _ = rng.choice(RATE_EXPERIMENTS)
        role = rng.choice(ROLES)
        right = {"ตัวแปรต้น": changed, "ตัวแปรตาม": measured, "ตัวแปรควบคุม": kept}[role]
        return _labelled(stem=f"การทดลอง: {setup} ข้อใดเป็น{role}ของการทดลองนี้", correct=right,
                         wrongs=tuple(v for v in (changed, measured, kept) if v != right)
                         + ("ชนิดของภาชนะที่ใช้วัด",),
                         topic=TOPIC_RATE,
                         hint="ตัวแปรต้นคือสิ่งที่ตั้งใจเปลี่ยน ตัวแปรตามคือสิ่งที่วัด ตัวแปรควบคุมคือสิ่งที่ต้องคงไว้ให้เท่ากัน")


@question_type(
    "chem.rate_experiment_fluency",
    display_name={"th": "อ่านผลการทดลองเรื่องอัตราการเกิดปฏิกิริยา"},
    level=UPPER_FIVE, subject=CHEMISTRY, topic=TOPIC_RATE,
)
class RateExperimentFluency(QuestionType):
    """Shorter time to the end point means a faster reaction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        temps = sorted(rng.sample(range(20, 61, 10), 3))
        first = rng.randrange(60, 161, 20)
        times = [first // (2 ** i) for i in range(3)]  # roughly halves per 10 °C
        runs = list(zip("ABC", temps, times))
        rng.shuffle(runs)
        table = " ".join(f"การทดลอง {name}: {t} °C ใช้เวลา {s} s" for name, t, s in runs)
        stem = (f"ผสมสารละลายโซเดียมไทโอซัลเฟตกับกรดไฮโดรคลอริกที่อุณหภูมิต่างกัน แล้วจับเวลาจนมองไม่เห็น"
                f"เครื่องหมาย X ใต้ขวด ได้ผลดังนี้ {table}")
        hint = "เวลาที่ใช้น้อย แปลว่าปฏิกิริยาเกิดเร็ว อัตราการเกิดปฏิกิริยาสูง"
        if rng.random() < 0.5:
            fastest = min(runs, key=lambda r: r[2])[0]
            return _labelled(stem=f"{stem} การทดลองใดมีอัตราการเกิดปฏิกิริยาสูงที่สุด",
                             correct=f"การทดลอง {fastest}",
                             wrongs=tuple(f"การทดลอง {r[0]}" for r in runs if r[0] != fastest)
                             + ("ทุกการทดลองมีอัตราเท่ากัน",),
                             topic=TOPIC_RATE, hint=hint)
        return _labelled(stem=f"{stem} สรุปผลการทดลองได้ตามข้อใด",
                         correct="อุณหภูมิสูงขึ้น อัตราการเกิดปฏิกิริยาเพิ่มขึ้น",
                         wrongs=("อุณหภูมิสูงขึ้น อัตราการเกิดปฏิกิริยาลดลง เพราะใช้เวลานานขึ้น",
                                 "อุณหภูมิไม่มีผลต่ออัตราการเกิดปฏิกิริยา",
                                 "อุณหภูมิสูงขึ้น ได้ผลิตภัณฑ์มากขึ้นแต่อัตราเท่าเดิม"),
                         topic=TOPIC_RATE, hint=hint)


@question_type(
    "chem.rate_experiment_application",
    display_name={"th": "อธิบายผลการทดลองด้วยทฤษฎีการชนและตรวจการออกแบบการทดลอง"},
    level=UPPER_FIVE, subject=CHEMISTRY, topic=TOPIC_RATE,
)
class RateExperimentApplication(QuestionType):
    """Explain a factor's effect by collisions; spot a test that changed two things."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        factor, setup, changed, measured, kept, why = rng.choice(RATE_EXPERIMENTS)
        if rng.random() < 0.6:
            others = tuple(e[5] for e in RATE_EXPERIMENTS if e[0] != factor)
            return _labelled(stem=f"การทดลองเรื่องผลของ{factor}พบว่าปฏิกิริยาเกิดเร็วขึ้น อธิบายด้วยทฤษฎีการชนได้ตามข้อใด",
                             correct=why, wrongs=others + RATE_MISCONCEPTIONS, topic=TOPIC_RATE,
                             hint="ความเข้มข้นและพื้นที่ผิวเพิ่มความถี่ของการชน อุณหภูมิเพิ่มพลังงานของการชน "
                                  "ตัวเร่งลดพลังงานก่อกัมมันต์")
        return _labelled(stem=f"นักเรียนต้องการศึกษาผลของ{factor} แต่ในการทดลองได้เปลี่ยน{kept}ไปด้วย "
                              "ผลการทดลองนี้สรุปได้หรือไม่ เพราะเหตุใด",
                         correct="สรุปไม่ได้ เพราะเปลี่ยนตัวแปรมากกว่าหนึ่งตัว",
                         wrongs=(f"สรุปได้ เพราะยังวัด{measured} ได้ครบทุกการทดลอง",
                                 "สรุปได้ เพราะยิ่งเปลี่ยนตัวแปรหลายตัวพร้อมกัน ผลก็ยิ่งเห็นชัดเจนขึ้น",
                                 "สรุปไม่ได้ เพราะการทดลองเรื่องอัตราต้องทำที่อุณหภูมิห้องเท่านั้น"),
                         topic=TOPIC_RATE, hint="การทดลองที่ยุติธรรมเปลี่ยนตัวแปรต้นเพียงตัวเดียว และคงตัวแปรอื่นไว้")
