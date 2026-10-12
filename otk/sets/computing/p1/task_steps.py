"""ลำดับขั้นตอนการทำงาน

วิทยาการคำนวณ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.1/2

Sets moved here from: technology_t1s3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import FIRST_PRIMARY, SUBJECT

PROVENANCE = Provenance("original")


STEPS_TOPIC = "ลำดับขั้นตอนการทำงาน"


#: task -> its four steps in order. Every step is unique across tasks, so a step
#: from another task is always wrong.
TASKS = {
    "แปรงฟัน": ("บีบยาสีฟันลงบนแปรง", "แปรงฟันให้ทั่วทุกซี่", "บ้วนปากด้วยน้ำสะอาด",
                "ล้างแปรงสีฟันแล้วเก็บเข้าที่"),
    "ล้างมือ": ("เปิดน้ำให้มือเปียก", "ถูสบู่ให้ทั่วมือ", "ล้างฟองสบู่ออกด้วยน้ำสะอาด",
                "เช็ดมือให้แห้ง"),
    "ปลูกต้นไม้ในกระถาง": ("ขุดหลุมในดินในกระถาง", "วางต้นกล้าลงในหลุม", "กลบดินรอบโคนต้น",
                          "รดน้ำให้ดินชุ่ม"),
    "ทำขนมปังทาแยม": ("หยิบขนมปังสองแผ่น", "ทาแยมบนขนมปังแผ่นหนึ่ง", "วางขนมปังอีกแผ่นทับ",
                     "ตัดครึ่งแล้ววางใส่จาน"),
    "ข้ามถนน": ("เดินไปที่ทางม้าลาย", "หยุดรอที่ขอบทางเท้า", "มองขวา มองซ้าย และมองขวาอีกครั้ง",
                "เดินข้ามเมื่อไม่มีรถหรือรถหยุดแล้ว"),
    "รดน้ำต้นไม้": ("เติมน้ำลงในบัวรดน้ำ", "ถือบัวรดน้ำไปที่ต้นไม้", "รดน้ำที่โคนต้น",
                    "เก็บบัวรดน้ำเข้าที่"),
    "เปิดคอมพิวเตอร์": ("เปิดสวิตช์ปลั๊กไฟ", "กดปุ่มเปิดเครื่อง", "รอจนหน้าจอพร้อมใช้งาน",
                        "คลิกเปิดโปรแกรมที่ต้องการ"),
    "เก็บที่นอน": ("ลุกจากที่นอน", "สะบัดผ้าห่ม", "พับผ้าห่ม", "วางหมอนและผ้าห่มให้เรียบร้อย"),
}


STEPS_HINT = "นึกภาพว่าลงมือทำจริงทีละขั้น ขั้นตอนใดต้องทำก่อนจึงจะทำขั้นตอนต่อไปได้"


LABELS = ("ก", "ข", "ค", "ง")


def _other_steps(rng: Random, task: str, count: int) -> list[str]:
    pool = [step for other, steps in TASKS.items() if other != task for step in steps]
    return rng.sample(pool, count)


@question_type(
    "comp.task_steps_foundation",
    display_name={"th": "บอกขั้นตอนแรก ขั้นตอนถัดไป และขั้นตอนสุดท้ายของงาน"},
    level=FIRST_PRIMARY, subject=SUBJECT, topic=STEPS_TOPIC,
)
class TaskStepsFoundation(QuestionType):
    """The first, the last, or the next step of an everyday task."""

    def build(self, rng: Random, **params):
        task = rng.choice(list(TASKS))
        steps = TASKS[task]
        kind = rng.randrange(3)
        if kind == 0:
            stem, correct = f"ขั้นตอนแรกของการ{task}คือข้อใด", steps[0]
        elif kind == 1:
            stem, correct = f"ขั้นตอนสุดท้ายของการ{task}คือข้อใด", steps[-1]
        else:
            index = rng.randrange(3)
            stem = f"ในการ{task} ขั้นตอนที่ทำต่อจาก “{steps[index]}” คือข้อใด"
            correct = steps[index + 1]
        wrongs = [s for s in steps if s != correct]
        if kind == 2:
            wrongs = [s for s in wrongs if s != steps[index]] + _other_steps(rng, task, 1)
        return _labelled(stem=stem, correct=correct, wrongs=tuple(wrongs),
                         hint=STEPS_HINT, topic=STEPS_TOPIC)


@question_type(
    "comp.task_steps_fluency",
    display_name={"th": "เรียงลำดับขั้นตอนการทำงาน"},
    level=FIRST_PRIMARY, subject=SUBJECT, topic=STEPS_TOPIC,
)
class TaskStepsFluency(QuestionType):
    """Put four shuffled steps back in order."""

    def build(self, rng: Random, **params):
        task = rng.choice(list(TASKS))
        steps = list(TASKS[task])
        shown = steps[:]
        while shown == steps:
            rng.shuffle(shown)
        label_of = {step: LABELS[i] for i, step in enumerate(shown)}
        listed = " ".join(f"({label_of[s]}) {s}" for s in shown)

        def order(sequence) -> str:
            return " → ".join(label_of[s] for s in sequence)

        correct = order(steps)
        wrongs: list[str] = []
        while len(wrongs) < 3:
            candidate = steps[:]
            rng.shuffle(candidate)
            text = order(candidate)
            if text != correct and text not in wrongs:
                wrongs.append(text)
        return _labelled(
            stem=f"ขั้นตอนการ{task}ต่อไปนี้ถูกสลับลำดับ {listed} ลำดับที่ถูกต้องคือข้อใด",
            correct=correct, wrongs=tuple(wrongs), hint=STEPS_HINT, topic=STEPS_TOPIC,
        )


@question_type(
    "comp.task_steps_application",
    display_name={"th": "หาขั้นตอนที่หายไปจากลำดับการทำงาน"},
    level=FIRST_PRIMARY, subject=SUBJECT, topic=STEPS_TOPIC,
)
class TaskStepsApplication(QuestionType):
    """One step of four is missing; name it."""

    def build(self, rng: Random, **params):
        task = rng.choice(list(TASKS))
        steps = TASKS[task]
        gap = rng.randrange(4)
        shown = " → ".join("____" if i == gap else s for i, s in enumerate(steps))
        present = [s for i, s in enumerate(steps) if i != gap]
        return _labelled(
            stem=f"ขั้นตอนการ{task}คือ {shown} ขั้นตอนที่หายไปคือข้อใด",
            correct=steps[gap],
            wrongs=(rng.choice(present), *_other_steps(rng, task, 2)),
            hint="ดูขั้นตอนก่อนและหลังช่องว่าง แล้วถามว่าต้องทำอะไรจึงจะไปถึงขั้นตอนถัดไปได้",
            topic=STEPS_TOPIC,
        )
