"""สมดุลกลและผลรวมของโมเมนต์

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/8

Sets moved here from: science_wave_f1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_f1 import SUBJECT, UPPER_FOUR, _labelled, _num, _numeric

PROVENANCE = Provenance("adapted", sources=('sheet_database/Faii/ข้อสอบแรง.pdf',))


TOPIC_EQUILIBRIUM = "สมดุลกลและผลรวมของโมเมนต์"


# Three-load levers about a central pivot: two weights one side, one the other,
# every value a whole number of newtons and metres.
LEVER_POOL = tuple(
    (w1, d1, w2, d2, d3, (w1 * d1 + w2 * d2) // d3)
    for w1 in (10, 20, 30, 40) for d1 in (1, 2, 3)
    for w2 in (10, 20, 30) for d2 in (1, 2)
    for d3 in (1, 2, 3, 4)
    if (w1 * d1 + w2 * d2) % d3 == 0 and 5 <= (w1 * d1 + w2 * d2) // d3 <= 200
)


# End-pivot levers (wheelbarrow, forearm): load close in, effort far out.
END_PIVOT_POOL = tuple(
    (load, a, length, round(load * a / length, 2))
    for load in (100, 120, 150, 200, 240, 300, 600)
    for a in (0.3, 0.5, 0.6, 1)
    for length in (1.5, 2, 2.4, 3)
    if length > a and abs(load * a / length * 100 - round(load * a / length * 100)) < 1e-6
)


@question_type(
    "phys.mechanical_equilibrium_foundation",
    display_name={"th": "ระบุเงื่อนไขของสมดุลกล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUILIBRIUM,
)
class MechanicalEquilibriumFoundation(QuestionType):
    """The two conditions themselves, stated before any lever is loaded."""

    FACTS = (
        ("วัตถุอยู่ในสมดุลกลเมื่อใด",
         "เมื่อแรงลัพธ์เป็นศูนย์ และผลรวมของโมเมนต์รอบจุดหมุนใด ๆ เป็นศูนย์",
         ("เมื่อแรงลัพธ์เป็นศูนย์เพียงอย่างเดียว",
          "เมื่อผลรวมของโมเมนต์เป็นศูนย์เพียงอย่างเดียว",
          "เมื่อวัตถุหยุดนิ่งอยู่กับที่เท่านั้น"),
         "สมดุลกลต้องสมดุลทั้งต่อการเลื่อนที่และต่อการหมุน"),
        ("ข้อใดคือเงื่อนไขของสมดุลต่อการหมุน",
         "ผลรวมของโมเมนต์ตามเข็มนาฬิกาเท่ากับผลรวมของโมเมนต์ทวนเข็มนาฬิกา",
         ("ผลรวมของแรงตามเข็มนาฬิกาเท่ากับผลรวมของแรงทวนเข็มนาฬิกา",
          "ระยะจากจุดหมุนทั้งสองข้างเท่ากัน",
          "น้ำหนักที่แขวนทั้งสองข้างเท่ากัน"),
         "เทียบโมเมนต์ ไม่ใช่แรงหรือระยะอย่างใดอย่างหนึ่ง"),
        ("โมเมนต์ของแรงรอบจุดหมุนหาได้จากข้อใด",
         "ผลคูณของแรงกับระยะตั้งฉากจากจุดหมุนถึงแนวแรง",
         ("ผลคูณของแรงกับระยะตามแนวแรง",
          "ผลบวกของแรงกับระยะจากจุดหมุน",
          "อัตราส่วนของแรงต่อระยะจากจุดหมุน"),
         "M = F l โดย l ต้องเป็นระยะตั้งฉาก"),
        ("แรงคู่ควบมีผลต่อวัตถุอย่างไร",
         "ทำให้วัตถุหมุนได้ แม้แรงลัพธ์ที่กระทำต่อวัตถุจะเป็นศูนย์",
         ("ทำให้วัตถุเลื่อนที่โดยไม่หมุน เพราะแรงลัพธ์ไม่เป็นศูนย์",
          "ไม่มีผลใด ๆ ต่อวัตถุ เพราะแรงลัพธ์เป็นศูนย์",
          "ทำให้วัตถุทั้งเลื่อนที่และหมุนพร้อมกันเสมอ"),
         "แรงคู่ควบคือแรงขนาดเท่ากันทิศตรงข้ามคนละแนว โมเมนต์รวมจึงไม่เป็นศูนย์"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            forces = rng.sample(range(5, 61, 5), 3)
            up = rng.randrange(10, 121, 5)
            down = sum(forces)
            balanced = rng.random() < 0.4
            if balanced:
                up = down
            thing = rng.choice(("คาน", "แผ่นไม้", "ป้ายที่แขวนไว้", "สะพานไม้จำลอง"))
            answer = ("แรงลัพธ์เป็นศูนย์ จึงสมดุลต่อการเลื่อนที่ (ยังต้องตรวจโมเมนต์ต่อ)" if up == down
                      else f"แรงลัพธ์ {abs(up - down)} นิวตัน {'ขึ้น' if up > down else 'ลง'} จึงไม่สมดุลต่อการเลื่อนที่")
            options = ["แรงลัพธ์เป็นศูนย์ จึงสมดุลต่อการเลื่อนที่ (ยังต้องตรวจโมเมนต์ต่อ)",
                       f"แรงลัพธ์ {abs(up - down) or up} นิวตัน {'ลง' if up >= down else 'ขึ้น'} จึงไม่สมดุลต่อการเลื่อนที่",
                       f"แรงลัพธ์ {up + down} นิวตัน ขึ้น จึงไม่สมดุลต่อการเลื่อนที่",
                       "สมดุลกลแน่นอนทุกกรณี เพราะมีแรงกระทำทั้งขึ้นและลง"]
            return _labelled(
                stem=(f"{thing}มีแรงกดลง {forces[0]}, {forces[1]} และ {forces[2]} นิวตัน และมีแรงดันขึ้นรวม {up} นิวตัน "
                      "ในแนวดิ่ง ข้อใดสรุปเรื่องสมดุลต่อการเลื่อนที่ได้ถูกต้อง"),
                correct=answer, wrongs=tuple(o for o in dict.fromkeys(options) if o != answer)[:3],
                topic=TOPIC_EQUILIBRIUM, hint="สมดุลต่อการเลื่อนที่ต้องมีผลรวมแรงขึ้นเท่ากับผลรวมแรงลง",
            )
        if roll < 0.7:
            f1, l1 = rng.randrange(10, 101, 10), rng.choice((0.5, 1, 1.5, 2))
            f2 = rng.randrange(10, 101, 10)
            l2 = f1 * l1 / f2
            if l2 * 100 != int(l2 * 100) or l2 == l1:
                f2, l2 = f1, l1 * 1
                f1, l1 = f1 * 2, l1 / 2
            m1 = f1 * l1
            return _labelled(
                stem=(f"คานมีแรง {f1} นิวตัน ทำให้หมุนทวนเข็มนาฬิกาที่ระยะ {l1:g} เมตรจากจุดหมุน "
                      f"และแรง {f2} นิวตัน ทำให้หมุนตามเข็มนาฬิกาที่ระยะ {l2:g} เมตร คานสมดุลต่อการหมุนหรือไม่"),
                correct=f"สมดุล เพราะโมเมนต์ทั้งสองทิศเท่ากัน {m1:g} นิวตัน·เมตร",
                wrongs=(f"ไม่สมดุล เพราะแรง {f1} กับ {f2} นิวตันไม่เท่ากัน", f"ไม่สมดุล เพราะระยะ {l1:g} กับ {l2:g} เมตรไม่เท่ากัน",
                        f"สมดุล เพราะผลรวมของแรงทั้งสองทิศเท่ากับ {f1 + f2:g} นิวตัน"),
                topic=TOPIC_EQUILIBRIUM, hint="สมดุลต่อการหมุนดูที่โมเมนต์ F × l ของแต่ละทิศ ไม่ใช่แรงหรือระยะอย่างเดียว",
            )
        stem, correct, wrongs, hint = rng.choice(self.FACTS)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs,
                         topic=TOPIC_EQUILIBRIUM, hint=hint)


@question_type(
    "phys.mechanical_equilibrium_fluency",
    display_name={"th": "คำนวณแรงที่ไม่ทราบค่าจากผลรวมของโมเมนต์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUILIBRIUM,
)
class MechanicalEquilibriumFluency(QuestionType):
    """Two loads one side of the pivot, one unknown the other — the sheet's ข้อ 8 and 13."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        w1, d1, w2, d2, d3, answer = rng.choice(LEVER_POOL)
        total = w1 * d1 + w2 * d2
        return _numeric(
            stem=(f"คานสม่ำเสมอเบามากวางบนจุดหมุนตรงกลาง ทางซ้ายของจุดหมุนแขวนน้ำหนัก "
                  f"{w1} นิวตัน ที่ระยะ {_num(d1)} เมตร และน้ำหนัก {w2} นิวตัน ที่ระยะ {_num(d2)} เมตร "
                  f"ทางขวาแขวนน้ำหนัก X ที่ระยะ {_num(d3)} เมตร ถ้าคานอยู่ในสมดุล X มีค่าเท่าใด"),
            answer=answer, unit="นิวตัน",
            # Forgetting one of the two left-hand loads, and adding the weights
            # without weighting them by distance.
            slips=(w1 * d1 / d3, w2 * d2 / d3, w1 + w2, total),
            fillers=(answer + 10, answer + 20, answer + 5),
            topic=TOPIC_EQUILIBRIUM,
            hint=(f"ผลรวมโมเมนต์ทวนเข็ม = {w1}×{_num(d1)} + {w2}×{_num(d2)} = {_num(total)} นิวตัน·เมตร "
                  f"ให้เท่ากับ X×{_num(d3)}"),
        )


@question_type(
    "phys.mechanical_equilibrium_application",
    display_name={"th": "ใช้สมดุลของโมเมนต์กับคานที่มีจุดหมุนอยู่ปลายข้างหนึ่ง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_EQUILIBRIUM,
)
class MechanicalEquilibriumApplication(QuestionType):
    """The wheelbarrow/forearm lever: pivot at one end, effort at the other."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    TOOLS = (
        ("รถเข็นล้อเดียว", "ล้อ", "มือที่ยกด้าม"),
        ("ไม้คานงัดก้อนหิน", "จุดหมุนที่รองไว้", "มือที่กดปลายคาน"),
        ("ที่เปิดฝาขวดแบบก้านยาว", "ขอบขวดที่เป็นจุดหมุน", "มือที่ยกก้าน"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        load, a, length, answer = rng.choice(END_PIVOT_POOL)
        tool, pivot, effort = rng.choice(self.TOOLS)
        return _numeric(
            stem=(f"{tool}มีจุดหมุนอยู่ที่{pivot} ของหนัก {load} นิวตัน วางห่างจุดหมุน {_num(a)} เมตร "
                  f"และ{effort}อยู่ห่างจุดหมุน {_num(length)} เมตร ต้องออกแรงในแนวดิ่งเท่าใด "
                  f"จึงจะยกของขึ้นได้พอดี (คานเบามาก)"),
            answer=answer, unit="นิวตัน",
            # Inverting the lever arms, and forgetting that the load's own
            # distance is measured from the pivot rather than from the hand.
            slips=(load * length / a, load, load * a, load / length),
            fillers=(answer + 10, answer + 25, answer + 50),
            topic=TOPIC_EQUILIBRIUM,
            hint=(f"สมดุลต่อการหมุนรอบจุดหมุน: {load}×{_num(a)} = F×{_num(length)} "
                  f"ยิ่งแขนของแรงพยายามยาว ยิ่งใช้แรงน้อย"),
        )
