"""การแก้ปัญหาอย่างง่าย

วิทยาการคำนวณ · ป.1 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.1/1

Sets moved here from: technology_t1s3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import FIRST_PRIMARY, SUBJECT

PROVENANCE = Provenance("original")


SOLVE_TOPIC = "การแก้ปัญหาอย่างง่าย"


TRIAL = "ลองผิดลองถูก"


COMPARE = "การเปรียบเทียบ"


METHOD_CHOICES = (TRIAL, COMPARE, "การเดาโดยไม่ลงมือทำ", "การรอให้ผู้อื่นแก้ให้")


STORIES = {
    TRIAL: (
        "แพรลองกดปุ่มบนรีโมตทีละปุ่ม จนพบปุ่มที่เปิดโทรทัศน์ได้",
        "ต้นลองใช้กุญแจทีละดอก จนเปิดกล่องได้",
        "มิ้นลองวางชิ้นจิ๊กซอว์ทีละชิ้น จนพบชิ้นที่ลงล็อก",
        "บอยลองเสียบสายชาร์จทีละด้าน จนพบด้านที่เสียบเข้าได้",
        "น้ำลองเปิดสวิตช์ทีละตัว จนพบสวิตช์ที่เปิดไฟห้องน้ำ",
        "ภูมิลองเดินในเขาวงกตทีละทาง ถ้าเจอทางตันก็ย้อนกลับไปลองทางใหม่",
    ),
    COMPARE: (
        "แพรดูภาพสองภาพ แล้วหาจุดที่แตกต่างกัน",
        "ต้นวางดินสอสองแท่งเทียบกัน เพื่อดูว่าแท่งใดยาวกว่า",
        "มิ้นดูรองเท้าทีละข้าง เพื่อหาข้างที่มีสีและขนาดเหมือนกันมาเป็นคู่",
        "บอยดูรูปร่างของตัวต่อกับรูปร่างของช่อง แล้วเลือกช่องที่มีรูปร่างเหมือนกัน",
        "น้ำวางผลไม้สองผลบนตาชั่งสองแขน เพื่อดูว่าผลใดหนักกว่า",
        "ภูมิดูป้ายราคาขนมสองห่อ เพื่อเลือกห่อที่ราคาถูกกว่า",
    ),
}


NOT_SOLVING = (
    "ฝนเห็นของเล่นพังแล้ววางทิ้งไว้โดยไม่ทำอะไรเลย",
    "โอ๊ตตอบทันทีโดยไม่ได้ดูหรือลองทำอะไรเลย",
)


SOLVE_HINT = ("ลองผิดลองถูกคือการลองทำทีละวิธีจนพบวิธีที่ได้ผล "
              "การเปรียบเทียบคือการดูว่าสิ่งของเหมือนหรือต่างกันอย่างไร")


#: (what is being tried, what opens or works, the thing each one is).
TRIAL_SETTINGS = (
    ("กุญแจ", "ดอก", "ไขกล่องของเล่นได้"),
    ("สวิตช์", "ตัว", "เปิดไฟห้องครัวได้"),
    ("ปุ่มบนรีโมต", "ปุ่ม", "เปิดพัดลมได้"),
)


SHAPES = ("วงกลม", "สามเหลี่ยม", "สี่เหลี่ยม", "รูปดาว")


COLOURS = ("สีแดง", "สีเหลือง", "สีฟ้า", "สีเขียว")


FRUITS = ("แอปเปิล", "ส้ม", "กล้วย", "มะม่วง", "สับปะรด", "แตงโม", "มังคุด")


@question_type(
    "comp.simple_problem_foundation",
    display_name={"th": "บอกวิธีแก้ปัญหาแบบลองผิดลองถูกและการเปรียบเทียบ"},
    level=FIRST_PRIMARY, subject=SUBJECT, topic=SOLVE_TOPIC,
)
class SimpleProblemFoundation(QuestionType):
    """Name the method a child used, or pick the story that uses a method."""

    def build(self, rng: Random, **params):
        method = rng.choice((TRIAL, COMPARE))
        if rng.random() < 0.5:
            story = rng.choice(STORIES[method])
            return _labelled(
                stem=f"“{story}” เป็นการแก้ปัญหาด้วยวิธีใด",
                correct=method, wrongs=tuple(m for m in METHOD_CHOICES if m != method),
                hint=SOLVE_HINT, topic=SOLVE_TOPIC,
            )
        other = COMPARE if method == TRIAL else TRIAL
        return _labelled(
            stem=f"ข้อใดเป็นการแก้ปัญหาด้วยวิธี{method}",
            correct=rng.choice(STORIES[method]),
            wrongs=tuple((*STORIES[other], *NOT_SOLVING)),
            hint=SOLVE_HINT, topic=SOLVE_TOPIC,
        )


@question_type(
    "comp.simple_problem_fluency",
    display_name={"th": "แก้ปัญหาด้วยการลองผิดลองถูกทีละขั้น"},
    level=FIRST_PRIMARY, subject=SUBJECT, topic=SOLVE_TOPIC,
)
class SimpleProblemFluency(QuestionType):
    """Keys tried one at a time: which one is left, and how many tries it takes."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        thing, unit, works = rng.choice(TRIAL_SETTINGS)
        count = rng.randint(4, 6)
        if rng.random() < 0.6:
            answer = rng.randint(1, count)
            failed = [n for n in range(1, count + 1) if n != answer]
            tried = " ".join(f"{unit}ที่ {n}" for n in failed)
            return _labelled(
                stem=(f"มี{thing} {count} {unit} ติดหมายเลข 1 ถึง {count} "
                      f"มีเพียง{unit}เดียวที่{works} เมื่อลองแล้วพบว่า {tried} ใช้ไม่ได้ "
                      f"{unit}ใดใช้ได้"),
                correct=f"{unit}ที่ {answer}",
                wrongs=tuple(f"{unit}ที่ {n}" for n in rng.sample(failed, 3)),
                hint="ตัดตัวที่ลองแล้วใช้ไม่ได้ออกไปทีละตัว ตัวที่เหลืออยู่คือคำตอบ",
                topic=SOLVE_TOPIC,
            )
        return _labelled(
            stem=(f"มี{thing} {count} {unit} มีเพียง{unit}เดียวที่{works} "
                  f"ถ้าลองทีละ{unit}โดยไม่ลองซ้ำ ต้องลองอย่างมากกี่ครั้งจึงรู้แน่ว่า{unit}ใดใช้ได้"),
            correct=f"{count - 1} ครั้ง",
            wrongs=(f"{count} ครั้ง", f"{count - 2} ครั้ง", f"{count + 1} ครั้ง"),
            hint=(f"ถ้าลองไปแล้ว {count - 1} {unit}และใช้ไม่ได้ทั้งหมด "
                  f"{unit}ที่เหลือต้องเป็น{unit}ที่ใช้ได้ โดยไม่ต้องลองอีก"),
            topic=SOLVE_TOPIC,
        )


@question_type(
    "comp.simple_problem_application",
    display_name={"th": "แก้ปัญหาด้วยการเปรียบเทียบความเหมือนและความต่าง"},
    level=FIRST_PRIMARY, subject=SUBJECT, topic=SOLVE_TOPIC,
)
class SimpleProblemApplication(QuestionType):
    """Find the odd one out, or the item missing from a second row."""

    def build(self, rng: Random, **params):
        if rng.random() < 0.5:
            shape, colour = rng.choice(SHAPES), rng.choice(COLOURS)
            odd = rng.randint(1, 4)
            if rng.random() < 0.5:
                other = f"{rng.choice([s for s in SHAPES if s != shape])}{colour}"
            else:
                other = f"{shape}{rng.choice([c for c in COLOURS if c != colour])}"
            items = [other if n == odd else f"{shape}{colour}" for n in range(1, 5)]
            listed = " ".join(f"รูปที่ {n} เป็น{item}" for n, item in enumerate(items, 1))
            return _labelled(
                stem=f"{listed} รูปใดแตกต่างจากรูปอื่น",
                correct=f"รูปที่ {odd}",
                wrongs=tuple(f"รูปที่ {n}" for n in range(1, 5) if n != odd),
                hint="เปรียบเทียบทั้งรูปร่างและสีของทุกรูป รูปที่ต่างคือรูปที่ไม่เหมือนรูปอื่นแม้เพียงอย่างเดียว",
                topic=SOLVE_TOPIC,
            )
        top = rng.sample(FRUITS, 4)
        missing = rng.choice(top)
        bottom = [f for f in top if f != missing]
        rng.shuffle(bottom)
        return _labelled(
            stem=(f"แถวบนมี {' '.join(top)} แถวล่างมี {' '.join(bottom)} "
                  f"ผลไม้ใดหายไปจากแถวล่าง"),
            correct=missing, wrongs=tuple(bottom),
            hint="เปรียบเทียบผลไม้ในแถวบนทีละผลว่ามีอยู่ในแถวล่างหรือไม่",
            topic=SOLVE_TOPIC,
        )
