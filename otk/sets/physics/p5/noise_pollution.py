"""การหลีกเลี่ยงและลดมลพิษทางเสียง

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.5/5

Sets moved here from: science_wave_d25.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d24 import FIFTH

PROVENANCE = Provenance("original")


NOISE_POLLUTION_TOPIC = "การหลีกเลี่ยงและลดมลพิษทางเสียง"


NOISE_FACTS = (
    ("มลพิษทางเสียงหมายถึงสิ่งใด", "เสียงที่ดังเกินไปหรือต่อเนื่องนานจนก่อให้เกิดผลเสียต่อสุขภาพหรือการดำเนินชีวิต",
     ("เสียงเพลงทุกชนิดไม่ว่าจะดังเบาเพียงใด", "เสียงที่มีระดับต่ำกว่า 40 เดซิเบลเท่านั้น", "เสียงใด ๆ ก็ตามที่เกิดจากเครื่องจักร",
      "เสียงที่มนุษย์ไม่ได้ยิน", "เสียงสัตว์ร้องในธรรมชาติทุกชนิด")),
    ("มลพิษทางเสียงส่งผลเสียต่อร่างกายอย่างไร", "ทำให้หูอื้อ การได้ยินเสื่อม เครียด และนอนไม่หลับ",
     ("ทำให้สายตาดีขึ้น", "ทำให้หูได้ยินชัดขึ้น", "ไม่มีผลต่อร่างกายเลย", "ทำให้ร่างกายแข็งแรงขึ้น", "ทำให้เลือดไหลเวียนดีขึ้น")),
    ("การลดมลพิษทางเสียงทำได้ที่ใดบ้าง", "ที่แหล่งกำเนิดเสียง ระหว่างทางที่เสียงเดินทาง และที่ตัวผู้ฟัง",
     ("ที่แหล่งกำเนิดเสียงเท่านั้น", "ที่ตัวผู้ฟังเท่านั้น", "ลดไม่ได้เลย", "ด้วยการเพิ่มเสียงดังกลบ", "ด้วยการเปิดหน้าต่างให้เสียงออก")),
)


NOISE_HINT = "เสียงที่ดังเกิน 85 เดซิเบลต่อเนื่องนานเป็นอันตรายต่อการได้ยิน ลดได้ที่แหล่งกำเนิด ระหว่างทาง หรือที่ตัวผู้ฟัง"


class NoiseProblem(NamedTuple):
    case: str
    method: str


NOISE_PROBLEMS = (
    NoiseProblem("บ้านอยู่ใกล้ถนนที่มีเสียงรถบรรทุกดังตลอดวัน", "ติดตั้งวัสดุกันเสียงที่ผนังหรือหน้าต่าง เช่น กระจกสองชั้น"),
    NoiseProblem("ทำงานในโรงงานที่มีเสียงเครื่องจักรดังต่อเนื่อง", "สวมที่ครอบหูหรือปลั๊กอุดหูลดเสียงขณะทำงาน"),
    NoiseProblem("เปิดเพลงเสียงดังผ่านหูฟังเป็นเวลานานทุกวัน", "ลดระดับเสียงหูฟังลงและพักหูเป็นระยะ"),
    NoiseProblem("อาศัยอยู่ใกล้สนามบินที่มีเสียงเครื่องบินขึ้นลงบ่อย", "ติดตั้งฉนวนกันเสียงหรือปลูกแนวต้นไม้กันเสียง"),
    NoiseProblem("ร้านค้าข้างบ้านเปิดลำโพงโฆษณาเสียงดังทั้งวัน", "พูดคุยขอให้ลดเสียงลำโพง หรือแจ้งผู้นำชุมชนช่วยไกล่เกลี่ย"),
    NoiseProblem("รถจักรยานยนต์ในบ้านท่อไอเสียดังมาก", "ซ่อมหรือเปลี่ยนท่อไอเสียให้ได้มาตรฐานเพื่อลดเสียงที่แหล่งกำเนิด"),
    NoiseProblem("ห้องเรียนดนตรีมีเสียงดังรบกวนห้องเรียนข้าง ๆ", "บุผนังห้องดนตรีด้วยวัสดุดูดซับเสียงและปิดประตูขณะซ้อม"),
    NoiseProblem("เครื่องซักผ้าสั่นและมีเสียงดังขณะปั่น", "วางเครื่องบนพื้นเรียบและใช้แผ่นยางรองลดการสั่น"),
)


NOISE_POLLUTION_SCENARIOS = (
    ("โรงเรียนแห่งหนึ่งตั้งอยู่ใกล้ทางด่วนที่มีเสียงรถดังตลอดเวลา ข้อใดเสนอแนวทางลดมลพิษทางเสียงในห้องเรียนได้เหมาะสมที่สุด",
     "ติดตั้งกระจกสองชั้นหรือวัสดุดูดซับเสียงที่ผนังห้องเรียนด้านที่ติดถนน",
     ("เปิดหน้าต่างไว้ตลอดเวลาเพื่อให้เสียงระบายออกไป", "ไม่ต้องทำอะไรเพราะเสียงรถไม่มีผลต่อการเรียน", "ย้ายโรงเรียนไปที่อื่นทุกครั้งที่มีเสียงดัง")),
    ("นักเรียนคนหนึ่งฟังเพลงผ่านหูฟังเสียงดังมากทุกวันจนรู้สึกหูอื้อบ่อยครั้ง ควรทำอย่างไร",
     "ลดระดับเสียงหูฟังลงให้อยู่ในระดับที่ปลอดภัยและพักหูเป็นระยะ",
     ("เพิ่มระดับเสียงให้ดังขึ้นเพื่อให้ชินกับเสียง", "ฟังเพลงผ่านหูฟังต่อไปตามปกติโดยไม่ต้องเปลี่ยนแปลง", "เปลี่ยนไปฟังเพลงประเภทอื่นแทนโดยไม่ลดระดับเสียง")),
    ("ชุมชนที่อยู่ใกล้สนามบินมักปลูกแนวต้นไม้หนาทึบรอบบ้านเรือน มีประโยชน์อย่างไรเกี่ยวกับมลพิษทางเสียง",
     "แนวต้นไม้ช่วยดูดซับและกั้นเสียงเครื่องบินไม่ให้ดังถึงบ้านเรือนมากเกินไป",
     ("แนวต้นไม้ไม่มีผลใด ๆ ต่อระดับเสียงที่ได้ยิน", "แนวต้นไม้ทำให้เสียงเครื่องบินดังขึ้นกว่าเดิม", "แนวต้นไม้ใช้ป้องกันฝุ่นละอองเท่านั้น ไม่เกี่ยวกับเสียง")),
)


WHERE = (
    ("ซ่อมท่อไอเสียรถให้เงียบลง", "ที่แหล่งกำเนิดเสียง"), ("ลดความเร็วเครื่องจักรหรือเปลี่ยนเป็นรุ่นที่เสียงเบา", "ที่แหล่งกำเนิดเสียง"),
    ("หรี่เสียงลำโพง", "ที่แหล่งกำเนิดเสียง"), ("ปลูกแนวต้นไม้ระหว่างถนนกับบ้าน", "ระหว่างทางที่เสียงเดินทาง"),
    ("สร้างกำแพงกันเสียงข้างทางด่วน", "ระหว่างทางที่เสียงเดินทาง"), ("ติดกระจกสองชั้นที่หน้าต่าง", "ระหว่างทางที่เสียงเดินทาง"),
    ("สวมที่ครอบหูขณะทำงาน", "ที่ตัวผู้ฟัง"), ("ใส่ปลั๊กอุดหูขณะนอน", "ที่ตัวผู้ฟัง"), ("ย้ายไปนั่งห่างจากลำโพง", "ที่ตัวผู้ฟัง"),
)


@question_type(
    "phys.noise_pollution_foundation",
    display_name={"th": "บอกความหมายของมลพิษทางเสียง"},
    level=FIFTH, subject=SUBJECT, topic=NOISE_POLLUTION_TOPIC,
)
class NoisePollutionFoundation(QuestionType):
    """What noise pollution is and does, and whether a stated level is harmful."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, right, wrongs = rng.choice(NOISE_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=NOISE_HINT, topic=NOISE_POLLUTION_TOPIC)
        places = rng.sample(("ห้องสมุด", "ห้องเรียน", "ร้านอาหาร", "ถนนในเมือง", "คอนเสิร์ต", "โรงงาน", "สวนสาธารณะ", "สนามบิน"), 4)
        levels = [rng.randrange(90, 131, 5), *rng.sample(range(30, 81, 5), 3)]
        rows = [f"{p} {n} เดซิเบล" for p, n in zip(places, levels)]
        answer, wrongs = rows[0], rows[1:]
        rows = rng.sample(rows, 4)
        table = " / ".join(rows)
        return _labelled(stem=f"ระดับเสียงที่วัดได้: {table} บริเวณใดมีเสียงดังจนอาจเป็นอันตรายต่อการได้ยินหากอยู่นาน (เกณฑ์ 85 เดซิเบล)",
                         correct=answer, wrongs=tuple(wrongs[:3]), hint=NOISE_HINT, topic=NOISE_POLLUTION_TOPIC)


@question_type(
    "phys.noise_pollution_fluency",
    display_name={"th": "เสนอแนวทางหลีกเลี่ยงและลดมลพิษทางเสียง"},
    level=FIFTH, subject=SUBJECT, topic=NOISE_POLLUTION_TOPIC,
)
class NoisePollutionFluency(QuestionType):
    """A noise-exposure situation; the method from the same table that fixes it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(NOISE_PROBLEMS))
        problem = NOISE_PROBLEMS[index]
        others = [p.method for i, p in enumerate(NOISE_PROBLEMS) if i != index]
        return _labelled(
            stem=f"{problem.case} ควรหลีกเลี่ยงหรือลดมลพิษทางเสียงด้วยวิธีใด",
            correct=problem.method,
            wrongs=tuple(others),
            hint="พิจารณาว่าจะกันเสียงที่แหล่งกำเนิด กันที่ทางผ่าน หรือป้องกันที่ตัวผู้ฟัง",
            topic=NOISE_POLLUTION_TOPIC,
        )


@question_type(
    "phys.noise_pollution_application",
    display_name={"th": "วิเคราะห์สถานการณ์มลพิษทางเสียงและเสนอแนวทางแก้ไข"},
    level=FIFTH, subject=SUBJECT, topic=NOISE_POLLUTION_TOPIC,
)
class NoisePollutionApplication(QuestionType):
    """Authored scenes, and where along the way a fix cuts the noise."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, NOISE_POLLUTION_SCENARIOS,
                                              hint="ลดมลพิษทางเสียงได้ทั้งที่แหล่งกำเนิด ระหว่างทาง หรือที่ตัวผู้ฟังเอง"), NOISE_POLLUTION_TOPIC)
        act, where = rng.choice(WHERE)
        place = rng.choice(("ชุมชนริมถนน", "โรงงานแห่งหนึ่ง", "หอพักนักศึกษา", "ตลาดนัด", "บ้านใกล้สนามบิน"))
        return _labelled(stem=f"ที่{place} มีการ{act} เพื่อลดมลพิษทางเสียง วิธีนี้ลดเสียงที่ตำแหน่งใด", correct=f"ลด{where}",
                         wrongs=tuple(f"ลด{w}" for w in ("ที่แหล่งกำเนิดเสียง", "ระหว่างทางที่เสียงเดินทาง", "ที่ตัวผู้ฟัง") if w != where)
                         + ("ไม่ได้ช่วยลดเสียงเลย",),
                         hint="แหล่งกำเนิด = ทำให้สิ่งที่ส่งเสียงเบาลง ระหว่างทาง = กั้นหรือดูดซับเสียง ตัวผู้ฟัง = ป้องกันหูหรือหลีกเลี่ยง",
                         topic=NOISE_POLLUTION_TOPIC)
