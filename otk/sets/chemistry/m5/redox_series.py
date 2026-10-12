"""ความสามารถในการเป็นตัวรีดิวซ์และตัวออกซิไดส์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/26

Sets moved here from: science_wave_f38.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f38 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SERIES = "ความสามารถในการเป็นตัวรีดิวซ์และตัวออกซิไดส์"


# Strongest reducing agent first (the textbook's activity series).
METALS = ("Mg", "Al", "Zn", "Fe", "Pb", "Cu", "Ag")


ION = {"Mg": "Mg²⁺", "Al": "Al³⁺", "Zn": "Zn²⁺", "Fe": "Fe²⁺", "Pb": "Pb²⁺", "Cu": "Cu²⁺", "Ag": "Ag⁺"}


# Strongest oxidising agent first.
HALOGENS = ("Cl₂", "Br₂", "I₂")


HALIDE = {"Cl₂": "Cl⁻", "Br₂": "Br⁻", "I₂": "I⁻"}


def displaces(metal: str, other: str) -> bool:
    """A metal pushes a less active metal's ion out of solution."""
    return METALS.index(metal) < METALS.index(other)


@question_type(
    "chem.redox_series_foundation",
    display_name={"th": "ทำนายการเกิดปฏิกิริยาระหว่างโลหะกับไอออนโลหะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SERIES,
)
class RedoxSeriesFoundation(QuestionType):
    """A stronger reducing agent gives electrons to the ion of a weaker one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        order = " > ".join(METALS)
        if rng.random() < 0.6:
            metal, other = rng.sample(METALS, 2)
            right = (f"เกิด เพราะ {metal} เป็นตัวรีดิวซ์ที่ดีกว่า {other}" if displaces(metal, other)
                     else f"ไม่เกิด เพราะ {metal} เป็นตัวรีดิวซ์ที่ด้อยกว่า {other}")
            wrongs = (f"ไม่เกิด เพราะ {metal} เป็นตัวรีดิวซ์ที่ด้อยกว่า {other}" if displaces(metal, other)
                      else f"เกิด เพราะ {metal} เป็นตัวรีดิวซ์ที่ดีกว่า {other}",
                      f"เกิด เพราะแผ่น {metal} จุ่มอยู่ในสารละลายนานพอ",
                      f"ไม่เกิด เพราะ {metal} กับ {other} เป็นโลหะเหมือนกัน")
            return _labelled(stem=f"จุ่มแผ่น {metal} ลงในสารละลายที่มี {ION[other]} (ความสามารถเป็นตัวรีดิวซ์: {order}) "
                                  "จะเกิดปฏิกิริยาหรือไม่",
                             correct=right, wrongs=wrongs, topic=TOPIC_SERIES,
                             hint="โลหะที่เป็นตัวรีดิวซ์ดีกว่า (อยู่ทางซ้าย) ให้อิเล็กตรอนแก่ไอออนของโลหะที่อยู่ทางขวาได้")
        halogen, other = rng.sample(HALOGENS, 2)
        occurs = HALOGENS.index(halogen) < HALOGENS.index(other)
        right = (f"เกิด ได้ {other} และ {HALIDE[halogen]}" if occurs else "ไม่เกิดปฏิกิริยาเคมี")
        wrongs = [x for x in (f"เกิด ได้ {other} และ {HALIDE[halogen]}", "ไม่เกิดปฏิกิริยาเคมี",
                              f"เกิด ได้ {halogen} และ {HALIDE[other]}", f"เกิด ได้ {HALIDE[halogen]} และ {HALIDE[other]}")
                  if x != right]
        return _labelled(stem=f"เติม {halogen} ลงในสารละลายที่มี {HALIDE[other]} (ความสามารถเป็นตัวออกซิไดส์: Cl₂ > Br₂ > I₂) "
                              "จะเกิดอะไรขึ้น",
                         correct=right, wrongs=tuple(wrongs[:3]), topic=TOPIC_SERIES,
                         hint="แฮโลเจนที่เป็นตัวออกซิไดส์ดีกว่าดึงอิเล็กตรอนจากแฮไลด์ของแฮโลเจนที่ด้อยกว่าได้")


@question_type(
    "chem.redox_series_fluency",
    display_name={"th": "เรียงความสามารถเป็นตัวรีดิวซ์จากผลการทดลอง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SERIES,
)
class RedoxSeriesFluency(QuestionType):
    """Read displacement results; the metal that displaces the most is the strongest."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trio = sorted(rng.sample(METALS, 3), key=METALS.index)
        labels = rng.sample(("A", "B", "C", "X", "Y", "Z"), 3)
        name = dict(zip(trio, labels))
        results = []
        for metal in trio:
            for other in trio:
                if metal != other:
                    seen = "มีโลหะมาเกาะ" if displaces(metal, other) else "ไม่เปลี่ยนแปลง"
                    results.append(f"{name[metal]} ในสารละลายไอออนของ {name[other]}: {seen}")
        rng.shuffle(results)
        order = [name[m] for m in trio]
        right = " > ".join(order)
        wrong = [" > ".join(p) for p in ((order[2], order[1], order[0]), (order[1], order[0], order[2]),
                                          (order[0], order[2], order[1]), (order[2], order[0], order[1]))]
        return _labelled(stem=f"ผลการจุ่มโลหะในสารละลายไอออนของโลหะอื่น: {'; '.join(results)} "
                              "เรียงความสามารถในการเป็นตัวรีดิวซ์จากมากไปน้อยได้อย่างไร",
                         correct=right, wrongs=tuple(wrong), topic=TOPIC_SERIES,
                         hint="โลหะที่ทำให้โลหะอื่นมาเกาะได้มากที่สุดเป็นตัวรีดิวซ์ที่ดีที่สุด")


@question_type(
    "chem.redox_series_application",
    display_name={"th": "เขียนสมการรีดอกซ์ที่เกิดขึ้นได้จริง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SERIES,
)
class RedoxSeriesApplication(QuestionType):
    """Only the stronger reducing agent with the weaker one's ion reacts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        metal, other = sorted(rng.sample(("Mg", "Zn", "Fe", "Pb", "Cu", "Ag"), 2), key=METALS.index)
        charge = {"Mg": 2, "Zn": 2, "Fe": 2, "Pb": 2, "Cu": 2, "Ag": 1}

        def equation(reducer: str, ion_of: str) -> str:
            a, b = charge[reducer], charge[ion_of]
            # electrons balance: reducer gives a each, ion takes b each.
            n_red, n_ion = (b, a) if a != b else (1, 1)
            lead = lambda n: "" if n == 1 else str(n)
            return f"{lead(n_red)}{reducer} + {lead(n_ion)}{ION[ion_of]} → {lead(n_red)}{ION[reducer]} + {lead(n_ion)}{ion_of}"

        right = equation(metal, other)
        wrongs = (equation(other, metal), f"{metal} + {ION[metal]} → {ION[metal]} + {metal}",
                  f"{ION[metal]} + {other} → {metal} + {ION[other]}")
        if rng.random() < 0.5:
            return _labelled(stem=f"จากลำดับความสามารถเป็นตัวรีดิวซ์ {' > '.join(METALS)} สมการรีดอกซ์ใดเกิดขึ้นได้",
                             correct=right, wrongs=wrongs, topic=TOPIC_SERIES,
                             hint="ตัวรีดิวซ์ที่ดีกว่า (ทางซ้าย) ทำปฏิกิริยากับไอออนของโลหะที่ด้อยกว่า และดุลอิเล็กตรอนให้เท่ากัน")
        plated = rng.choice(("Pb", "Cu", "Ag"))
        # Any metal above the plated one works; the wrong choices cannot push it out of solution.
        good = rng.choice([m for m in METALS if displaces(m, plated)])
        bad = [m for m in METALS if not displaces(m, plated)]
        fillers = ["ใช้แผ่นโลหะใดก็ได้", "ต้องใช้แผ่นพลาสติก"]
        return _labelled(stem=f"ต้องการเคลือบโลหะ {plated} บนแผ่นโลหะโดยจุ่มในสารละลาย {ION[plated]} (ไม่ใช้ไฟฟ้า) ควรใช้แผ่นโลหะใด "
                              f"(ลำดับตัวรีดิวซ์ {' > '.join(METALS)})",
                         correct=good, wrongs=tuple((bad + fillers)[:3]), topic=TOPIC_SERIES,
                         hint="แผ่นโลหะต้องเป็นตัวรีดิวซ์ที่ดีกว่าโลหะที่จะมาเกาะ")
