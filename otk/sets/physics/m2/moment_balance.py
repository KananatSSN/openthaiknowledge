"""โมเมนต์ของแรง

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/10

Sets moved here from: science_wave_d20.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


MOMENT_TOPIC = "โมเมนต์ของแรง"


MOMENT_SCENARIOS = (
    ("เหตุใดการเปิดประตูโดยผลักที่ขอบประตูด้านไกลบานพับจึงง่ายกว่าผลักใกล้บานพับ",
     "ระยะจากจุดหมุนมากกว่า จึงใช้แรงน้อยกว่าเพื่อให้ได้โมเมนต์เท่ากัน",
     ("ขอบประตูเบากว่าบริเวณใกล้บานพับ", "แรงเสียดทานที่ขอบประตูมากกว่า", "ระยะจากจุดหมุนไม่มีผลต่อการหมุน")),
    ("ประแจด้ามยาวช่วยคลายน็อตที่แน่นได้ง่ายกว่าประแจด้ามสั้น เพราะเหตุใด",
     "ด้ามยาวเพิ่มระยะจากจุดหมุน โมเมนต์จึงมากขึ้นแม้ออกแรงเท่าเดิม",
     ("ด้ามยาวทำให้น็อตหลวมเอง", "ด้ามยาวมีน้ำหนักมากจึงหมุนเอง", "ด้ามยาวลดโมเมนต์ของแรง")),
    ("ถ้าออกแรง 50 นิวตันที่ปลายประแจยาว 0.3 เมตร จะได้โมเมนต์เท่าใด",
     "15 นิวตัน·เมตร", ("50.3 นิวตัน·เมตร", "166.7 นิวตัน·เมตร", "150 นิวตัน·เมตร")),
)


@question_type(
    "phys.moment_balance_foundation",
    display_name={"th": "อธิบายโมเมนต์ของแรงเมื่อคานสมดุลจากผลการทดลอง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=MOMENT_TOPIC,
)
class MomentBalanceFoundation(QuestionType):
    """A balanced ruler's loads and distances, or an unbalanced one and which way it tips."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            while True:
                lf, rf = rng.randint(1, 8), rng.randint(1, 8)
                ld, rd = rng.choice((10, 15, 20, 25, 30, 40)), rng.choice((10, 15, 20, 25, 30, 40))
                if lf * ld != rf * rd:
                    break
            m_left, m_right = lf * ld, rf * rd
            down, up = ("ซ้าย", "ขวา") if m_left > m_right else ("ขวา", "ซ้าย")
            big, small = max(m_left, m_right), min(m_left, m_right)
            return _labelled(
                stem=(f"คานไม้เมตรมีจุดหมุนตรงกลาง แขวนตุ้มหนัก {lf} นิวตัน ห่างจุดหมุนไปทางซ้าย {ld} เซนติเมตร "
                      f"และตุ้มหนัก {rf} นิวตัน ห่างไปทางขวา {rd} เซนติเมตร เมื่อปล่อยมือ คานจะเป็นอย่างไร"),
                correct=f"เอียงลงทาง{down} เพราะโมเมนต์ด้าน{down} {big} นิวตัน·เซนติเมตร มากกว่าด้าน{up} {small} นิวตัน·เซนติเมตร",
                wrongs=(f"เอียงลงทาง{up} เพราะโมเมนต์ด้าน{up} {big} นิวตัน·เซนติเมตร มากกว่าด้าน{down} {small} นิวตัน·เซนติเมตร",
                        "อยู่ในแนวระดับ เพราะโมเมนต์สองข้างเท่ากัน",
                        f"เอียงลงทาง{up} เพราะผลรวมแรงกับระยะด้าน{up}มากกว่า"),
                hint="โมเมนต์ = แรง × ระยะจากจุดหมุน คานเอียงลงทางด้านที่มีโมเมนต์มากกว่า",
                topic=MOMENT_TOPIC,
            )
        # Every loading that balances with whole-newton weights on a metre rule.
        options = [(lf, ld, lf * ld // rd, rd)
                   for lf in (2, 3, 4, 5, 6) for ld in (10, 15, 20, 30) for rd in (10, 15, 20, 30, 40)
                   if rd != ld and (lf * ld) % rd == 0 and lf * ld // rd not in (0, lf)]
        left_f, left_d, right_f, right_d = rng.choice(options)
        moment = left_f * left_d
        return _labelled(
            stem=(f"คานไม้เมตรสมดุลที่จุดหมุนตรงกลาง แขวนตุ้มหนัก {left_f} นิวตัน ห่างจุดหมุนไปทางซ้าย {left_d} เซนติเมตร "
                  f"และตุ้มหนัก {right_f} นิวตัน ห่างไปทางขวา {right_d} เซนติเมตร จากผลการทดลอง ข้อใดอธิบายได้ถูกต้อง"),
            correct=(f"โมเมนต์ทวนเข็มนาฬิกา {left_f} × {left_d} = {moment} เท่ากับโมเมนต์ตามเข็มนาฬิกา "
                     f"{right_f} × {right_d} = {moment} นิวตัน·เซนติเมตร คานจึงสมดุล"),
            wrongs=(f"น้ำหนักทางซ้าย {left_f} นิวตัน เท่ากับทางขวา {right_f} นิวตัน โดยระยะไม่มีผล คานจึงสมดุล",
                    f"ระยะทางซ้าย {left_d} เซนติเมตร เท่ากับระยะทางขวา {right_d} เซนติเมตร โดยน้ำหนักของตุ้มไม่มีผลต่อการหมุน คานจึงสมดุล",
                    f"โมเมนต์ทางซ้าย {left_f} + {left_d} = {left_f + left_d} เท่ากับทางขวา "
                    f"{right_f} + {right_d} = {right_f + right_d} นิวตัน·เซนติเมตร คานจึงสมดุล"),
            hint="โมเมนต์ = แรง × ระยะจากจุดหมุน คานสมดุลเมื่อโมเมนต์ทวนเข็มเท่ากับโมเมนต์ตามเข็ม",
            topic=MOMENT_TOPIC,
        )


@question_type(
    "phys.moment_balance_fluency",
    display_name={"th": "คำนวณแรงหรือระยะเมื่อวัตถุสมดุลต่อการหมุนด้วย M = Fl"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=MOMENT_TOPIC,
)
class MomentBalanceFluency(QuestionType):
    """A balanced lever with one unknown; calculate it with M = Fl."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        f1 = rng.choice((10, 20, 30, 40, 60))
        d1 = rng.choice((1, 2, 3, 4))
        moment = f1 * d1
        d2 = rng.choice([d for d in (0.5, 1, 1.5, 2, 3, 4, 6) if (moment / d) == int(moment / d) and d != d1])
        f2 = int(moment / d2)
        ask_force = rng.random() < 0.5
        if ask_force:
            stem = (f"เด็กคนหนึ่งหนัก {f1 * 10} นิวตัน นั่งห่างจุดหมุนของไม้กระดก {d1} เมตร "
                    f"อีกฝั่งหนึ่งมีเด็กนั่งห่างจุดหมุน {d2:g} เมตร ไม้กระดกสมดุล เด็กคนที่สองหนักเท่าใด")
            answer = f2 * 10
            unit = "นิวตัน"
            slips = (f1 * 10, answer * 2, int(f1 * 10 * d2 / d1) if f1 * 10 * d2 % d1 == 0 else answer + 50)
        else:
            stem = (f"เด็กคนหนึ่งหนัก {f1 * 10} นิวตัน นั่งห่างจุดหมุนของไม้กระดก {d1} เมตร "
                    f"อีกฝั่งหนึ่งมีเด็กหนัก {f2 * 10} นิวตัน ไม้กระดกสมดุล เด็กคนที่สองนั่งห่างจุดหมุนกี่เมตร")
            answer = d2
            unit = "เมตร"
            slips = (d1, d2 * 2, d2 + 1)
        wrongs = [s for s in dict.fromkeys(slips) if s != answer][:3]
        while len(wrongs) < 3:
            wrongs.append(answer + len(wrongs) + 2)
        return _labelled(
            stem=stem,
            correct=f"{answer:g} {unit}",
            wrongs=tuple(f"{w:g} {unit}" for w in wrongs),
            hint="ใช้ M = F × l ให้โมเมนต์สองข้างเท่ากัน แล้วแก้หาค่าที่ไม่ทราบ",
            topic=MOMENT_TOPIC,
        )


@question_type(
    "phys.moment_balance_application",
    display_name={"th": "ใช้โมเมนต์ของแรงอธิบายเครื่องมือในชีวิตประจำวัน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=MOMENT_TOPIC,
)
class MomentBalanceApplication(QuestionType):
    """Authored cases, a spanner's moment, and the force a turn needs at a given distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            force = rng.randrange(10, 101, 5)
            arm = rng.choice((0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.5))
            tool = rng.choice(("ปลายประแจ", "มือจับประตู", "ปลายด้ามไขควงบล็อก", "ปลายคันโยก"))
            moment = Fraction(force) * Fraction(str(arm))
            return numeric(
                stem=f"ออกแรง {force} นิวตันตั้งฉากที่{tool} ซึ่งห่างจากจุดหมุน {arm:g} เมตร จะได้โมเมนต์เท่าใด",
                answer=moment, wrongs=(force + Fraction(str(arm)), moment * 10, moment / 10),
                unit="นิวตัน·เมตร", topic=MOMENT_TOPIC, hint="โมเมนต์ = แรง × ระยะตั้งฉากจากจุดหมุน (M = F × l)",
            )
        if roll < 0.7:
            moment = rng.randrange(10, 61, 5)
            arm = rng.choice((0.2, 0.25, 0.4, 0.5, 0.8, 1))
            force = Fraction(moment) / Fraction(str(arm))
            return numeric(
                stem=(f"น็อตตัวหนึ่งต้องใช้โมเมนต์ {moment} นิวตัน·เมตรจึงจะคลายออก ถ้าใช้ประแจที่ออกแรงห่างจากน็อต "
                      f"{arm:g} เมตร ต้องออกแรงอย่างน้อยเท่าใด"),
                answer=force, wrongs=(Fraction(moment) * Fraction(str(arm)), force * 2, force / 2),
                unit="นิวตัน", topic=MOMENT_TOPIC, hint="F = M ÷ l ยิ่งระยะยาว แรงที่ต้องใช้ยิ่งน้อย",
            )
        return _retopic(scenario_question(
            rng, MOMENT_SCENARIOS,
            hint="โมเมนต์เพิ่มได้ทั้งจากแรงที่มากขึ้นและระยะจากจุดหมุนที่ยาวขึ้น",
        ), MOMENT_TOPIC)
