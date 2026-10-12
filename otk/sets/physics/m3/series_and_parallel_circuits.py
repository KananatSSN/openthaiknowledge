"""วงจรอนุกรมและขนาน

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/4

Sets moved here from: electricity, science_wave_a.
"""

from __future__ import annotations

from abc import abstractmethod
from random import Random
from typing import NamedTuple

from otk.core.content import image, math, text
from otk.core.distractors import combine, fixed, label_pool, numeric_neighbors
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.numeric_scenario import fmt, slips
from otk.sets._support.electricity import LEVEL, SUBJECT, TOPIC
from otk.sets._support.science_wave_a import _question

PROVENANCE = Provenance("original")


def _parallel(values) -> float:
    """ความต้านทานรวมแบบขนาน: 1/R = Σ 1/Rᵢ."""
    return 1.0 / sum(1.0 / v for v in values)


class CircuitSpec(NamedTuple):
    """One drawn schematic: how it is connected, its resistors, its battery.

    ``mixed`` means ``resistors[0]`` in series with all of ``resistors[1:]`` in
    parallel — the way the generator draws it. Every spec is chosen so that both
    the total resistance and ``volts / total`` come out whole, so a student who
    does the algebra right lands exactly on a choice.
    """
    kind: str                          # "series" | "parallel" | "mixed"
    resistors: tuple[int, ...]         # โอห์ม, ตามลำดับที่วาดในภาพ
    volts: int                         # แรงเคลื่อนไฟฟ้าของแบตเตอรี่ที่เขียนบนภาพ

    @property
    def asset_id(self) -> str:
        return f"circuit_{self.kind}_{'_'.join(map(str, self.resistors))}_v{self.volts}"

    @property
    def total(self) -> float:
        """ความต้านทานรวม — the answer to ``elec.circuit_resistance``."""
        if self.kind == "series":
            return float(sum(self.resistors))
        if self.kind == "parallel":
            return _parallel(self.resistors)
        return self.resistors[0] + _parallel(self.resistors[1:])

    @property
    def current(self) -> float:
        """กระแสไฟฟ้ารวม — the answer to ``elec.circuit_current``."""
        return self.volts / self.total


# The schematics shipped as built-in assets. Kept here so the generator
# (otk/pictures/generate.py) draws exactly the set these types ask
# about — the two must agree, like WAVE_SPECS and the wave PNGs.
CIRCUIT_SPECS = [CircuitSpec(*t) for t in [
    ("series", (2, 3), 10),
    ("series", (4, 6), 20),
    ("series", (5, 7), 24),
    ("series", (2, 3, 5), 30),
    ("series", (1, 4, 5), 20),
    ("series", (3, 6, 9), 36),
    ("parallel", (6, 3), 12),
    ("parallel", (12, 4), 12),
    ("parallel", (10, 15), 12),
    ("parallel", (20, 5), 20),
    ("parallel", (6, 6, 6), 12),
    ("parallel", (2, 3, 6), 6),
    ("mixed", (2, 6, 3), 12),
    ("mixed", (4, 12, 4), 14),
    ("mixed", (5, 10, 15), 22),
    ("mixed", (3, 4, 4), 10),
    # Wave H: more of each shape, every total and current still whole.
    ("series", (1, 2), 9),
    ("series", (4, 4), 16),
    ("series", (6, 9), 30),
    ("series", (2, 4, 6), 24),
    ("series", (5, 5, 10), 40),
    ("parallel", (4, 4), 8),
    ("parallel", (3, 6), 6),
    ("parallel", (30, 6), 10),
    ("parallel", (12, 6), 16),
    ("parallel", (8, 8), 12),
    ("parallel", (3, 3, 3), 6),
    ("parallel", (12, 12, 6), 12),
    ("mixed", (1, 4, 4), 9),
    ("mixed", (3, 3, 6), 15),
    ("mixed", (6, 6, 3), 16),
    ("mixed", (5, 12, 6), 18),
    ("mixed", (4, 8, 8), 24),
]]


KIND_LABELS = {
    "series": "การต่อแบบอนุกรม",
    "parallel": "การต่อแบบขนาน",
    "mixed": "การต่อแบบผสม",
}


class CircuitType(QuestionType):
    """Base: show a schematic from ``CIRCUIT_SPECS``, ask one thing about it.

    The alt text names only what is drawn (a battery and resistors), never how
    they are connected — otherwise ``elec.circuit_type`` would answer itself for
    a screen reader, and in a printed worksheet, where an image renders as its
    alt text alone.
    """

    STEM = ""
    ALT = "แผนภาพวงจรไฟฟ้าแสดงแบตเตอรี่และตัวต้านทานพร้อมค่าความต้านทาน"

    @abstractmethod
    def answer(self, spec: CircuitSpec) -> str:
        """The correct value/label for this spec, as it will be shown."""

    @abstractmethod
    def choices(self, spec: CircuitSpec) -> GeneratedQuestion:
        """Assemble the question — subclasses differ in text vs math choices."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return self.choices(rng.choice(CIRCUIT_SPECS))

    def _stem(self, spec: CircuitSpec):
        return [image(spec.asset_id, alt=self.ALT), text(self.STEM)]


class CircuitCalc(CircuitType):
    """Base for the two numeric circuit questions: math choices from wrong totals.

    Both types share one distractor idea — work out what the *wrong* total
    resistance would be (adding a parallel pair, taking the parallel formula to a
    series pair) and offer the value that mistake leads to.
    """

    HINT = ""                          # the TeX formula shown as the hint

    def wrong_totals(self, spec: CircuitSpec) -> list[float]:
        rs = spec.resistors
        if spec.kind == "series":
            return [_parallel(rs), max(rs), sum(rs) - min(rs)]
        if spec.kind == "parallel":
            return [float(sum(rs)), float(max(rs)), float(min(rs))]
        return [float(sum(rs)), _parallel(rs), float(rs[0] + sum(rs[1:]))]

    @abstractmethod
    def value(self, total: float, spec: CircuitSpec) -> float:
        """Turn a (right or wrong) total resistance into this type's answer."""

    def answer(self, spec: CircuitSpec) -> str:
        return fmt(round(self.value(spec.total, spec), 2))

    def choices(self, spec: CircuitSpec) -> GeneratedQuestion:
        # Every spec is built so the right answer is whole; only the values a
        # wrong method lands on need rounding, and two places is as far as a
        # student would carry them.
        correct = self.answer(spec)
        wrong = slips(correct, *(round(self.value(t, spec), 2)
                                 for t in self.wrong_totals(spec)))
        return GeneratedQuestion(
            stem=self._stem(spec),
            correct=[math(correct)],
            distractors=combine(fixed(*[[math(w)] for w in wrong]),
                                numeric_neighbors()),
            topic=self.topic,
            hint=[math(self.HINT)],
        )


PHYSICS = "ฟิสิกส์"


ELECTRICITY = "ไฟฟ้า"


SERIES_FACTS = (
    ("กระแสไฟฟ้าที่ผ่านตัวต้านทานแต่ละตัวในวงจรอนุกรม",
     "เท่ากันทุกตัว",
     ("แบ่งกันตามค่าความต้านทาน", "มากที่สุดที่ตัวต้านทานค่าน้อยที่สุด",
      "เป็นศูนย์ที่ตัวต้านทานตัวสุดท้าย")),
    ("ความต่างศักย์คร่อมตัวต้านทานแต่ละตัวในวงจรอนุกรม",
     "รวมกันได้เท่ากับความต่างศักย์ของแหล่งกำเนิด",
     ("เท่ากับความต่างศักย์ของแหล่งกำเนิดทุกตัว",
      "เป็นศูนย์ทุกตัวเพราะกระแสเท่ากัน",
      "ขึ้นกับจำนวนตัวต้านทานเท่านั้น ไม่ขึ้นกับค่าความต้านทาน")),
    ("ความต่างศักย์คร่อมตัวต้านทานแต่ละตัวในวงจรขนาน",
     "เท่ากันทุกตัว และเท่ากับความต่างศักย์ของแหล่งกำเนิด",
     ("รวมกันได้เท่ากับความต่างศักย์ของแหล่งกำเนิด",
      "แบ่งกันตามค่าความต้านทาน",
      "มากที่สุดที่ตัวต้านทานค่ามากที่สุด")),
    ("กระแสไฟฟ้าที่ผ่านตัวต้านทานแต่ละตัวในวงจรขนาน",
     "รวมกันได้เท่ากับกระแสรวมที่ออกจากแหล่งกำเนิด",
     ("เท่ากันทุกตัวเสมอ",
      "รวมกันได้มากกว่ากระแสรวมที่ออกจากแหล่งกำเนิด",
      "เป็นศูนย์ที่ตัวต้านทานค่ามากที่สุด")),
)


CIRCUIT_BREAK_CASES = (
    ("อนุกรม", "หลอดที่เหลือดับทั้งหมด เพราะวงจรขาดจึงไม่มีกระแสไหล",
     ("หลอดที่เหลือยังสว่างเท่าเดิม เพราะแต่ละหลอดมีทางเดินของตัวเอง",
      "หลอดที่เหลือสว่างขึ้น เพราะได้รับกระแสมากขึ้น",
      "หลอดที่เหลือสว่างลดลงครึ่งหนึ่ง แต่ยังไม่ดับ")),
    ("ขนาน", "หลอดที่เหลือยังสว่างอยู่ เพราะแต่ละหลอดมีทางเดินของกระแสเป็นของตัวเอง",
     ("หลอดที่เหลือดับทั้งหมด เพราะวงจรขาด",
      "หลอดที่เหลือดับทีละดวงตามลำดับ",
      "หลอดที่เหลือสว่างลดลงจนมองไม่เห็น")),
)


CIRCUIT_USES = (
    ("ต้องการให้ไฟแต่ละดวงในบ้านเปิดปิดและทำงานอิสระจากกัน",
     "ต่อแบบขนาน เพราะแต่ละดวงได้รับความต่างศักย์เต็มและมีทางเดินกระแสของตัวเอง",
     ("ต่อแบบอนุกรม เพราะกระแสที่ผ่านทุกดวงเท่ากัน ทุกดวงจึงสว่างเท่ากันและเปิดปิดแยกกันได้",
      "ต่อแบบอนุกรม เพราะความต่างศักย์ของทุกดวงรวมกันได้เท่ากับความต่างศักย์ของแหล่งกำเนิด",
      "ต่อแบบใดก็ได้ เพราะการต่อวงจรไม่มีผลต่อความสว่างและการทำงานของหลอดแต่ละดวงเลย")),
    ("ต้องการให้ไฟชุดหนึ่งดับทั้งชุดทันทีเมื่อดวงใดดวงหนึ่งขาด เพื่อใช้เตือนว่ามีหลอดเสีย",
     "ต่อแบบอนุกรม เพราะวงจรที่ขาดจุดเดียวทำให้ไม่มีกระแสไหลทั้งชุด",
     ("ต่อแบบขนาน เพราะกระแสแยกไปแต่ละดวง เมื่อดวงหนึ่งขาดทุกดวงจึงดับ",
      "ต่อแบบขนาน เพราะความต่างศักย์เท่ากันทุกดวง ดวงที่เหลือจึงดับตาม",
      "ต่อแบบอนุกรม เพราะแต่ละดวงได้รับความต่างศักย์เต็มเท่ากับแหล่งกำเนิด")),
)


@question_type("elec.series_parallel_rules",
               display_name={"th": "สมบัติของการต่อแบบอนุกรมและแบบขนาน"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class SeriesParallelRules(ClassifyType):
    """สมบัติของวงจรที่ตามมาจากสูตรทั้งสอง — กระแส ความต่างศักย์ และผลเมื่อมีตัวหนึ่งขาด."""

    CLASSIFY_STEM = "“{member}” เป็นสมบัติของการต่อตัวต้านทานแบบใด"
    PICK_STEM = "ข้อใดเป็นสมบัติของ{category}"

    CATEGORIES = [
        Category("การต่อตัวต้านทานแบบอนุกรม",
                 ("กระแสไฟฟ้าที่ผ่านตัวต้านทานทุกตัวมีค่าเท่ากัน",
                  "ความต่างศักย์รวมเท่ากับผลบวกของความต่างศักย์คร่อมตัวต้านทานแต่ละตัว",
                  "ความต้านทานรวมหาได้จากผลบวกของความต้านทานทุกตัว",
                  "ความต้านทานรวมมีค่ามากกว่าความต้านทานของตัวที่มากที่สุด",
                  "ถ้าตัวต้านทานตัวใดตัวหนึ่งขาด กระแสไฟฟ้าจะหยุดไหลทั้งวงจร",
                  "กระแสไฟฟ้ามีทางเดินได้เพียงทางเดียว")),
        Category("การต่อตัวต้านทานแบบขนาน",
                 ("ความต่างศักย์คร่อมตัวต้านทานทุกตัวมีค่าเท่ากัน",
                  "กระแสไฟฟ้ารวมเท่ากับผลบวกของกระแสไฟฟ้าที่ผ่านตัวต้านทานแต่ละตัว",
                  "ส่วนกลับของความต้านทานรวมเท่ากับผลบวกของส่วนกลับของความต้านทานทุกตัว",
                  "ความต้านทานรวมมีค่าน้อยกว่าความต้านทานของตัวที่น้อยที่สุด",
                  "ถ้าตัวต้านทานตัวใดตัวหนึ่งขาด ตัวที่เหลือยังทำงานได้ตามปกติ",
                  "กระแสไฟฟ้ามีทางเดินได้มากกว่าหนึ่งทาง")),
    ]


@question_type("elec.circuit_type",
               display_name={"th": "อ่านแผนภาพวงจร: อนุกรม ขนาน หรือผสม"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class CircuitKind(CircuitType):
    """จากภาพวงจร ตัวต้านทานถูกต่อแบบใด — อ่านรูปแบบการต่อก่อนจะคำนวณอะไรได้."""

    STEM = "จากแผนภาพ ตัวต้านทานในวงจรนี้ถูกต่อกันแบบใด"

    def answer(self, spec: CircuitSpec) -> str:
        return KIND_LABELS[spec.kind]

    def choices(self, spec: CircuitSpec) -> GeneratedQuestion:
        return GeneratedQuestion(
            stem=self._stem(spec),
            correct=[text(self.answer(spec))],
            distractors=label_pool(list(KIND_LABELS.values())),
            topic=self.topic,
        )


@question_type(
    "elec.circuit_series_parallel_foundation",
    display_name={"th": "วงจรอนุกรมและขนาน: ระบุสมบัติของวงจร"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=ELECTRICITY,
)
class SeriesParallelFoundation(QuestionType):
    """State one rule of a series or parallel connection at a time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            count = rng.randint(2, 6)
            volts = count * rng.choice((1.5, 2, 3, 4, 6)) if rng.random() < 0.5 else rng.choice((6, 12, 24))
            series = rng.random() < 0.5
            share = volts / count
            if series and (share * 100) % 1:
                series = False
            kind = "อนุกรม" if series else "ขนาน"
            right = share if series else volts
            fmt_v = lambda v: f"{v:g} โวลต์"
            wrongs = [fmt_v(volts) if series else fmt_v(share) if (share * 100) % 1 == 0 else fmt_v(volts * 2),
                      fmt_v(volts * count), fmt_v(volts + count), fmt_v(volts / 2 if volts / 2 != right else volts * 3)]
            return _question(
                stem=(f"ต่อหลอดไฟที่เหมือนกันทุกประการ {count} ดวงแบบ{kind}กับแบตเตอรี่ {volts:g} โวลต์ "
                      "ความต่างศักย์คร่อมหลอดไฟแต่ละดวงเป็นเท่าใด"),
                correct=fmt_v(right),
                wrongs=tuple(w for w in dict.fromkeys(wrongs) if w != fmt_v(right))[:3],
                hint="วงจรอนุกรมแบ่งความต่างศักย์กันตามจำนวนหลอด ส่วนวงจรขนานทุกหลอดได้ความต่างศักย์เต็ม",
                topic=ELECTRICITY,
            )
        which = rng.randrange(2)
        if which == 0:
            quantity, correct, wrongs = rng.choice(SERIES_FACTS)
            return _question(
                stem=f"ข้อใดกล่าวถึง{quantity}ได้ถูกต้อง",
                correct=correct,
                wrongs=wrongs,
                hint="ในวงจรอนุกรมกระแสเท่ากันและความต่างศักย์แบ่งกัน ส่วนวงจรขนานความต่างศักย์เท่ากันและกระแสแบ่งกัน",
                topic=ELECTRICITY,
            )
        kind, correct, wrongs = rng.choice(CIRCUIT_BREAK_CASES)
        count = rng.randrange(3, 6)
        return _question(
            stem=(f"ต่อหลอดไฟ {count} ดวงแบบ{kind}เข้ากับแหล่งกำเนิดเดียวกัน "
                  "ถ้าหลอดดวงหนึ่งขาด จะเกิดอะไรขึ้นกับหลอดที่เหลือ"),
            correct=correct,
            wrongs=wrongs,
            hint="ถามว่ากระแสยังมีทางเดินครบวงจรไปถึงหลอดที่เหลือหรือไม่",
            topic=ELECTRICITY,
        )


@question_type("elec.circuit_resistance",
               display_name={"th": "ความต้านทานรวมจากแผนภาพวงจร"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class CircuitResistance(CircuitCalc):
    """หาความต้านทานรวมจากภาพ — อนุกรมบวกกันตรง ๆ ขนานใช้ผลบวกของส่วนกลับ."""

    STEM = "จากแผนภาพ ความต้านทานรวมของวงจรมีค่ากี่โอห์ม"
    HINT = r"\frac{1}{R} = \frac{1}{R_1} + \frac{1}{R_2}"

    def value(self, total: float, spec: CircuitSpec) -> float:
        return total


@question_type("elec.circuit_current",
               display_name={"th": "กระแสไฟฟ้ารวมจากแผนภาพวงจร"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class CircuitCurrent(CircuitCalc):
    """หาความต้านทานรวมก่อน แล้วจึงใช้กฎของโอห์มหากระแสรวม — สองขั้นตอนต่อกัน."""

    STEM = "จากแผนภาพ กระแสไฟฟ้ารวมที่ผ่านวงจรมีค่ากี่แอมแปร์"
    HINT = r"I = \frac{V}{R}"

    def value(self, total: float, spec: CircuitSpec) -> float:
        return spec.volts / total


@question_type(
    "elec.circuit_series_parallel_fluency",
    display_name={"th": "วงจรอนุกรมและขนาน: คำนวณจากผลการวัด"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=ELECTRICITY,
)
class SeriesParallelFluency(QuestionType):
    """Compute one quantity in a two-resistor series or parallel circuit."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    # Every pair's parallel combination ab/(a+b) is a whole number of ohms, so no
    # question ever depends on rounding. A test re-derives this from the table.
    _PAIRS = (
        (2, 2), (3, 6), (4, 4), (4, 12), (6, 3), (6, 6), (6, 12),
        (5, 20), (10, 10), (8, 8), (10, 15), (12, 24), (6, 30),
    )

    @staticmethod
    def _distinct(correct: str, candidates: list[str]) -> tuple[str, ...] | None:
        """Three distractors that differ from each other and from the answer."""
        out: list[str] = []
        for value in candidates:
            if value != correct and value not in out:
                out.append(value)
        return tuple(out[:3]) if len(out) >= 3 else None

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        # Retry rather than emit a colliding choice set: a few pairs make one of the
        # classic slips land on the right answer.
        for pair in (*rng.sample(self._PAIRS, len(self._PAIRS)),):
            first, second = pair
            series = first + second
            parallel = first * second // series
            if which == 0:
                correct = f"{series} โอห์ม"
                wrongs = self._distinct(correct, [
                    f"{parallel} โอห์ม",
                    f"{first * second} โอห์ม",
                    f"{abs(first - second)} โอห์ม",
                    f"{max(first, second)} โอห์ม",
                ])
                if wrongs is None:
                    continue
                return _question(
                    stem=(f"ต่อตัวต้านทาน {first} โอห์ม และ {second} โอห์ม แบบอนุกรม "
                          "ความต้านทานรวมของวงจรเป็นเท่าใด"),
                    correct=correct,
                    wrongs=wrongs,
                    hint="การต่ออนุกรมทำให้ทางเดินยาวขึ้น ความต้านทานรวมจึงเป็นผลบวกของทุกตัว",
                    topic=ELECTRICITY,
                )
            if which == 1:
                correct = f"{parallel} โอห์ม"
                wrongs = self._distinct(correct, [
                    f"{series} โอห์ม",
                    f"{first * second} โอห์ม",
                    f"{max(first, second)} โอห์ม",
                    f"{min(first, second)} โอห์ม",
                ])
                if wrongs is None:
                    continue
                return _question(
                    stem=(f"ต่อตัวต้านทาน {first} โอห์ม และ {second} โอห์ม แบบขนาน "
                          "ความต้านทานรวมของวงจรเป็นเท่าใด"),
                    correct=correct,
                    wrongs=wrongs,
                    hint="การต่อขนานเพิ่มทางเดินให้กระแส ความต้านทานรวมจึงน้อยกว่าตัวที่น้อยที่สุด",
                    topic=ELECTRICITY,
                )
            voltage = series * rng.randrange(1, 4)
            correct = f"{voltage // series} A"
            wrongs = self._distinct(correct, [
                f"{voltage // first} A",
                f"{voltage // second} A",
                f"{voltage} A",
                f"{voltage // parallel} A",
            ])
            if wrongs is None:
                continue
            return _question(
                stem=(f"ต่อตัวต้านทาน {first} โอห์ม และ {second} โอห์ม แบบอนุกรม "
                      f"เข้ากับแหล่งกำเนิด {voltage} V กระแสไฟฟ้าในวงจรเป็นเท่าใด"),
                correct=correct,
                wrongs=wrongs,
                hint="หาความต้านทานรวมของวงจรก่อน แล้วจึงใช้ I = V/R กับค่ารวมนั้น",
                topic=ELECTRICITY,
            )
        raise AssertionError("no resistor pair produced four distinct choices")


@question_type(
    "elec.circuit_series_parallel_application",
    display_name={"th": "วงจรอนุกรมและขนาน: เลือกและวิเคราะห์การต่อวงจร"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=ELECTRICITY,
)
class SeriesParallelApplication(QuestionType):
    """Choose a connection for a purpose, or read a two-branch measurement."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            need, correct, wrongs = rng.choice(CIRCUIT_USES)
            return _question(
                stem=f"{need} ควรต่อวงจรแบบใด และเพราะเหตุใด",
                correct=correct,
                wrongs=wrongs,
                hint="ตัดสินจากสิ่งที่ต้องการให้เกิดขึ้นเมื่อดวงหนึ่งขาด และจากความต่างศักย์ที่แต่ละดวงได้รับ",
                topic=ELECTRICITY,
            )
        if which == 1:
            voltage = rng.choice((12, 24, 36))
            first = rng.choice((2, 3, 4, 6))
            second = rng.choice([n for n in (2, 3, 4, 6, 12) if n != first])
            branch_a, branch_b = voltage // first, voltage // second
            return _question(
                stem=(f"ต่อตัวต้านทาน {first} โอห์ม และ {second} โอห์ม แบบขนาน "
                      f"กับแหล่งกำเนิด {voltage} V วัดกระแสในแต่ละสาขาได้ "
                      f"{branch_a} A และ {branch_b} A ข้อสรุปใดถูกต้อง"),
                correct=(f"ความต่างศักย์คร่อมทั้งสองตัวเท่ากันคือ {voltage} V "
                         f"และกระแสรวมเท่ากับ {branch_a + branch_b} A"),
                wrongs=(
                    (f"ความต่างศักย์แบ่งกันเป็น {voltage // 2} V ต่อตัว "
                     f"และกระแสรวมเท่ากับ {branch_a + branch_b} A"),
                    (f"ความต่างศักย์คร่อมทั้งสองตัวเท่ากันคือ {voltage} V "
                     f"และกระแสรวมเท่ากับ {max(branch_a, branch_b)} A"),
                    ("กระแสในสองสาขาต้องเท่ากันเสมอในวงจรขนาน ผลการวัดครั้งนี้จึงคลาดเคลื่อน"),
                ),
                hint="ในวงจรขนานความต่างศักย์เท่ากันทุกสาขา ส่วนกระแสของทุกสาขารวมกันเป็นกระแสรวม",
                topic=ELECTRICITY,
            )
        resistance = rng.choice((2, 3, 4, 6))
        voltage = rng.choice((12, 24))
        return _question(
            stem=(f"ใช้ตัวต้านทาน {resistance} โอห์ม สองตัวและแหล่งกำเนิด {voltage} V "
                  "ถ้าต้องการให้กระแสรวมที่ออกจากแหล่งกำเนิดมากที่สุด ควรต่ออย่างไร และเพราะเหตุใด"),
            correct=(f"ต่อแบบขนาน เพราะความต้านทานรวมเหลือ {resistance // 2 if resistance % 2 == 0 else resistance} "
                     "โอห์ม ซึ่งน้อยกว่าแบบอนุกรม จึงมีกระแสมากกว่า"),
            wrongs=(
                (f"ต่อแบบอนุกรม เพราะความต้านทานรวมเป็น {resistance * 2} โอห์ม "
                 "ซึ่งทำให้กระแสมากกว่า"),
                "ต่อแบบอนุกรม เพราะกระแสที่ผ่านตัวต้านทานทุกตัวเท่ากัน กระแสรวมจึงมากที่สุด",
                "ต่อแบบใดก็ได้ เพราะกระแสรวมขึ้นกับความต่างศักย์ของแหล่งกำเนิดอย่างเดียว",
            ),
            hint="เทียบความต้านทานรวมของสองแบบก่อน แล้วใช้ I = V/R กับความต่างศักย์เดิม",
            topic=ELECTRICITY,
        )
