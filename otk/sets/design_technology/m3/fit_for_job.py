"""การเลือกวัสดุ อุปกรณ์ และวงจรให้เหมาะกับงาน

การออกแบบและเทคโนโลยี · ม.3 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.3/5

Sets moved here from: technology_t2s3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s3 import M3, _bank, _pair_either_way

PROVENANCE = Provenance("original")


FIT_TOPIC = "การเลือกวัสดุ อุปกรณ์ และวงจรให้เหมาะกับงาน"


JOINS = (
    ("ไม้กับไม้ในงานโครงชั้นวาง", "ตะปูหรือสกรูร่วมกับกาวลาเท็กซ์"),
    ("ขาอุปกรณ์อิเล็กทรอนิกส์กับแผ่นวงจร", "การบัดกรีด้วยตะกั่วบัดกรี"),
    ("ผ้ากับผ้าในงานกระเป๋า", "การเย็บด้วยด้าย"),
    ("ท่อพีวีซีกับข้อต่อพีวีซี", "กาวทาท่อพีวีซี"),
    ("แผ่นโลหะสองแผ่นที่ต้องการรอยต่อถาวรและแข็งแรง", "การเชื่อมโลหะหรือหมุดย้ำ"),
    ("กระดาษแข็งกับกระดาษแข็งในแบบจำลอง", "กาวร้อนหรือเทปกาวสองหน้า"),
)


def _volts(value: float) -> str:
    return f"{round(value, 2):g} โวลต์"


#: (cell, its voltage): ordinary, rechargeable nickel-metal-hydride, lithium-ion.
CELLS = (("ถ่านไฟฉาย", 1.5), ("ถ่านชาร์จนิกเกิลเมทัลไฮไดรด์", 1.2), ("เซลล์ลิเทียมไอออน", 3.7))


#: Every choice names a component, what it is wired to, and what for, so the
#: answer is picked by whether the parts do the job.
CIRCUITS = (
    ("ไฟหน้าบ้านที่เปิดเองเมื่อมืด",
     "ตัวต้านทานไวแสงทำงานร่วมกับทรานซิสเตอร์เพื่อควบคุมหลอด LED",
     ("สวิตช์กดติดปล่อยดับต่อกับหลอด LED ให้คนในบ้านกดเปิดเมื่อมืด",
      "ตัวต้านทานค่าคงที่ต่อกับหลอด LED โดยไม่มีตัวรับแสงในวงจร",
      "สวิตช์แม่เหล็กติดที่ประตูบ้านต่อกับหลอด LED ให้ติดเมื่อเปิดประตู",
      "ตัวเก็บประจุต่อกับหลอด LED เพื่อเก็บแสงแดดไว้ใช้ตอนกลางคืน",
      "ออดต่อกับแผงเซลล์สุริยะ ให้ส่งเสียงเตือนเมื่อแสงแดดหมดตอนเย็น")),
    ("สัญญาณเตือนเมื่อมีคนเปิดประตู",
     "สวิตช์แม่เหล็กที่ติดกับประตูต่อกับออด",
     ("ตัวต้านทานไวแสงที่ติดกับประตูต่อกับมอเตอร์",
      "หลอด LED ที่ติดกับประตูต่อกับตัวต้านทานเท่านั้น",
      "ไดโอดที่ติดกับประตูต่อกับแผงเซลล์สุริยะ",
      "ตัวเก็บประจุที่ติดกับประตูต่อกับหลอด LED",
      "มอเตอร์ที่ติดกับประตูต่อกับถ่านไฟฉายโดยตรง")),
    ("พัดลมตั้งโต๊ะขนาดเล็กที่ปรับความเร็วได้",
     "ตัวต้านทานปรับค่าได้ต่อกับมอเตอร์",
     ("ตัวต้านทานไวแสงต่อกับออดของพัดลม",
      "ไดโอดต่อกลับทิศกับมอเตอร์ของพัดลม",
      "สวิตช์แม่เหล็กต่อกับหลอด LED ของพัดลม",
      "ตัวเก็บประจุต่อกับถ่านไฟฉายโดยตรง",
      "ตัวต้านทานไวแสงต่อกับมอเตอร์พัดลม")),
    ("หลอด LED ที่ต่อกับแบตเตอรี่ 9 โวลต์โดยไม่ให้หลอดขาด",
     "ต่อตัวต้านทานที่มีค่าเหมาะสมอนุกรมกับหลอด LED",
     ("ต่อหลอด LED กับแบตเตอรี่ 9 โวลต์โดยตรงไม่ผ่านอุปกรณ์อื่น",
      "ต่อตัวเก็บประจุอนุกรมกับหลอด LED แทนตัวต้านทาน",
      "ต่อแบตเตอรี่เพิ่มอีกก้อนแบบอนุกรมกับหลอด LED",
      "ต่อหลอด LED กลับขั้ว เพื่อลดกระแสที่ไหลผ่านหลอด",
      "ต่อตัวต้านทานขนานกับหลอด LED โดยไม่ผ่านอนุกรม")),
    ("ไฟฉายฉุกเฉินที่ป้องกันกระแสไหลย้อนกลับเข้าแผงเซลล์สุริยะในเวลากลางคืน",
     "ต่อไดโอดระหว่างแผงเซลล์สุริยะกับแบตเตอรี่",
     ("ต่อแผงเซลล์สุริยะกับแบตเตอรี่โดยตรงไม่ผ่านอุปกรณ์ใด",
      "ต่อมอเตอร์คั่นระหว่างแผงเซลล์สุริยะกับแบตเตอรี่",
      "ต่อตัวเก็บประจุกลับขั้วระหว่างแผงกับแบตเตอรี่",
      "ต่อตัวต้านทานไวแสงระหว่างแผงเซลล์สุริยะกับออด",
      "ต่อไดโอดกลับทิศระหว่างแผงกับแบตเตอรี่")),
    ("กล่องดนตรีที่ส่งเสียงเมื่อเปิดฝากล่อง",
     "สวิตช์ที่ต่อวงจรเมื่อเปิดฝา ต่อกับออดหรือโมดูลเสียง",
     ("ตัวต้านทานไวแสงในกล่อง ต่อกับมอเตอร์ให้หมุนเมื่อสว่าง",
      "ออดต่อกับถ่านไฟฉายโดยตรง ให้ดังตลอดเวลาโดยไม่มีสวิตช์",
      "ตัวต้านทานปรับค่าได้ ต่อกับแผงเซลล์สุริยะที่ติดบนฝากล่อง",
      "หลอด LED ต่อกับตัวเก็บประจุ ให้กระพริบเมื่อปิดฝากล่อง",
      "สวิตช์ที่ตัดวงจรเมื่อเปิดฝา ต่อกับออดหรือโมดูลเสียง")),
)


@question_type(
    "tech.fit_for_job_foundation",
    display_name={"th": "เลือกวิธียึดติดให้เหมาะกับวัสดุ"},
    level=M3, subject=SUBJECT, topic=FIT_TOPIC,
)
class FitForJobFoundation(QuestionType):
    def build(self, rng: Random, **params):
        return _pair_either_way(rng, JOINS,
                                forward="ต้องการยึดติด{} ควรใช้วิธีใด",
                                backward="{}เหมาะสำหรับยึดติดวัสดุคู่ใด",
                                hint="วิธียึดติดต้องเหมาะกับชนิดของวัสดุ ความแข็งแรงที่ต้องการ และต้องถอดได้หรือเป็นรอยต่อถาวร",
                                topic=FIT_TOPIC)


@question_type(
    "tech.fit_for_job_fluency",
    display_name={"th": "ต่อเซลล์ไฟฟ้าแบบอนุกรมและขนานให้ได้แรงดันตามต้องการ"},
    level=M3, subject=SUBJECT, topic=FIT_TOPIC,
)
class FitForJobFluency(QuestionType):
    """Identical cells: series adds voltage, parallel keeps it."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        name, cell = rng.choice(CELLS)
        count = rng.randint(2, 6)
        kind = rng.randrange(3)
        hint = "ต่ออนุกรมแรงดันรวมเท่ากับผลบวกของแรงดันแต่ละก้อน ต่อขนานแรงดันรวมเท่ากับแรงดันของหนึ่งก้อน"
        if kind == 0:
            value = cell * count
            pool = {round(v, 2) for v in (cell, cell * (count + 1), cell * (count - 1), value + 1)}
            pool.discard(round(value, 2))
            return _labelled(
                stem=f"ต่อ{name}ขนาด {cell:g} โวลต์ จำนวน {count} ก้อนแบบอนุกรม จะได้แรงดันรวมกี่โวลต์",
                correct=_volts(value), wrongs=tuple(_volts(w) for w in rng.sample(sorted(pool), 3)),
                hint=hint, topic=FIT_TOPIC,
            )
        if kind == 1:
            pool = {round(v, 2) for v in (cell * count, cell * (count - 1), cell / 2, cell + 1)}
            pool.discard(round(cell, 2))
            return _labelled(
                stem=f"ต่อ{name}ขนาด {cell:g} โวลต์ จำนวน {count} ก้อนแบบขนาน จะได้แรงดันรวมกี่โวลต์",
                correct=_volts(cell), wrongs=tuple(_volts(w) for w in rng.sample(sorted(pool), 3)),
                hint=hint, topic=FIT_TOPIC,
            )
        return _labelled(
            stem=f"ต้องการแรงดัน {round(cell * count, 2):g} โวลต์ จาก{name}ขนาด {cell:g} โวลต์ ต้องต่อแบบอนุกรมกี่ก้อน",
            correct=f"{count} ก้อน",
            wrongs=tuple(f"{w} ก้อน" for w in rng.sample(_near(count, (count + 1, count - 1, count * 2)), 3)),
            hint=hint, topic=FIT_TOPIC,
        )


@question_type(
    "tech.fit_for_job_application",
    display_name={"th": "เลือกวงจรไฟฟ้าและอิเล็กทรอนิกส์ให้เหมาะกับงาน"},
    level=M3, subject=SUBJECT, topic=FIT_TOPIC,
)
class FitForJobApplication(QuestionType):
    def build(self, rng: Random, **params):
        return _bank(rng, CIRCUITS, "ต้องการสร้าง{} ควรใช้วงจรใด",
                     hint="ระบุว่างานต้องรับรู้อะไร เช่น แสงหรือการเปิดประตู และต้องให้ผลอะไร เช่น แสง เสียง หรือการหมุน",
                     topic=FIT_TOPIC)
