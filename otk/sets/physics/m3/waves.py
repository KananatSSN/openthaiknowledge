"""คลื่นและสมบัติของคลื่น

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/10

Sets moved here from: physics, science_wave_a2.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import image, math, text
from otk.core.distractors import combine, fixed, numeric_neighbors
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.numeric_scenario import Calc, PhysCalc
from otk.sets._support.physics import SUBJECT, TOPIC, _n
from otk.sets._support.science_wave_a2 import PHYSICS, WAVES, _distinct, _question

PROVENANCE = Provenance("original")


class WaveSpec(NamedTuple):
    """A drawn wave: amplitude (cm), ความยาวคลื่น (m), and how many full ลูกคลื่น."""
    amp: int
    wavelength: int
    cycles: int

    @property
    def asset_id(self) -> str:
        return f"wave_a{self.amp}_w{self.wavelength}_c{self.cycles}"


# The wave diagrams shipped as built-in assets. Kept here so the generator
# (otk/pictures/generate.py) renders exactly the set this type draws
# from — the two must agree, like the anatomy markers and skeleton.png.
WAVE_SPECS = [WaveSpec(*t) for t in [
    (2, 4, 2), (3, 2, 3), (1, 3, 2), (2, 3, 3), (3, 4, 2), (1, 2, 4),
    (2, 2, 2), (3, 3, 2), (1, 4, 3), (2, 3, 2), (3, 2, 2), (1, 2, 3),
]]


@question_type("phys.wave_types",
               display_name={"th": "ประเภทของคลื่น"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class WaveTypes(ClassifyType):
    """คลื่นกล (ต้องอาศัยตัวกลาง) vs คลื่นแม่เหล็กไฟฟ้า (ไม่ต้องอาศัยตัวกลาง)."""

    CLASSIFY_STEM = "“{member}” จัดอยู่ในคลื่นประเภทใด"
    PICK_STEM = "ข้อใดต่อไปนี้จัดอยู่ในกลุ่ม{category}"

    CATEGORIES = [
        Category("คลื่นกล (Mechanical Waves)",
                 ("คลื่นเสียง", "คลื่นน้ำ", "คลื่นในเส้นเชือก",
                  "คลื่นแผ่นดินไหว", "คลื่นในสปริง",
                  "คลื่นที่ต้องอาศัยตัวกลางในการเคลื่อนที่")),
        Category("คลื่นแม่เหล็กไฟฟ้า (Electromagnetic Waves)",
                 ("คลื่นวิทยุ", "ไมโครเวฟ", "รังสีอินฟราเรด",
                  "แสงที่มองเห็นได้", "รังสีอัลตราไวโอเลต", "รังสีเอกซ์",
                  "รังสีแกมมา", "คลื่นที่ไม่ต้องอาศัยตัวกลางในการเคลื่อนที่")),
    ]


@question_type("phys.wave_diagram",
               display_name={"th": "อ่านกราฟคลื่น (จำนวนลูกคลื่น ความยาวคลื่น แอมพลิจูด)"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class WaveDiagram(QuestionType):
    """แสดงกราฟคลื่นรูปไซน์บนแกนระยะทาง–การกระจัด แล้วถามค่าที่อ่านได้จากกราฟ.

    ``ask`` pins one quantity (``1`` = จำนวนลูกคลื่น, ``2`` = ความยาวคลื่น,
    ``3`` = แอมพลิจูด); ``0`` draws one per item. Distractors are the classic
    misreadings — peak-to-peak for แอมพลิจูด, the whole span for ความยาวคลื่น —
    padded with neighbouring values.
    """

    ASKS = ("count", "wavelength", "amplitude")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        w = rng.choice(WAVE_SPECS)
        which = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        if which == "count":
            prompt = "จากกราฟ คลื่นที่ปรากฏมีทั้งหมดกี่ลูก"
            val = w.cycles
            cands = [w.cycles + 1, w.cycles - 1, w.wavelength, w.amp]
        elif which == "wavelength":
            prompt = "จากกราฟ ความยาวคลื่น (λ) มีค่ากี่เมตร"
            val = w.wavelength
            cands = [w.wavelength * w.cycles, w.wavelength * 2, w.amp, w.cycles]
        else:
            prompt = "จากกราฟ แอมพลิจูดของคลื่นมีค่ากี่เซนติเมตร"
            val = w.amp
            cands = [w.amp * 2, w.amp + 1, w.wavelength, w.cycles]

        seen, wrongs = {val}, []
        for c in cands:
            if c > 0 and c not in seen:
                seen.add(c)
                wrongs.append(c)
        return GeneratedQuestion(
            stem=[image(w.asset_id, alt="กราฟคลื่นรูปไซน์บนแกนระยะทาง–การกระจัด"),
                  text(prompt)],
            correct=[math(str(val))],
            distractors=combine(fixed(*[[math(str(c))] for c in wrongs[:3]]),
                                numeric_neighbors()),
            topic=self.topic,
        )


@question_type("phys.period_frequency",
               display_name={"th": "คาบและความถี่ของคลื่น"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class PeriodFrequency(PhysCalc):
    """คาบ T และความถี่ f จากจำนวนรอบในเวลาที่กำหนด และความสัมพันธ์ T = 1/f."""

    _F = [2, 4, 5, 10, 20, 25, 50]          # frequencies with a clean period

    def draw(self, rng: Random) -> Calc:
        r = rng.random()
        if r < 0.5:
            f = rng.choice([2, 4, 5, 10])
            t = rng.randint(2, 5)
            n = f * t                       # N complete cycles in t seconds
            if rng.random() < 0.5:
                return Calc(
                    f"คลื่นเคลื่อนที่ครบ {n} รอบ ในเวลา {t} วินาที "
                    f"จงหาความถี่ของคลื่น (เฮิรตซ์)",
                    str(f), wrongs=(str(n), _n(t / n), str(t)),
                    hint=r"f = \frac{N}{t}")
            return Calc(
                f"คลื่นเคลื่อนที่ครบ {n} รอบ ในเวลา {t} วินาที "
                f"จงหาคาบของคลื่น (วินาที)",
                _n(t / n), wrongs=(str(f), str(n), str(t)),
                hint=r"T = \frac{t}{N}")
        f = rng.choice(self._F)
        if rng.random() < 0.5:
            return Calc(
                f"คลื่นมีความถี่ {f} เฮิรตซ์ จงหาคาบของคลื่น (วินาที)",
                _n(1 / f), wrongs=(str(f), _n(2 / f), _n(1 / (2 * f))),
                hint=r"T = \frac{1}{f}")
        return Calc(
            f"คลื่นมีคาบ {_n(1 / f)} วินาที จงหาความถี่ของคลื่น (เฮิรตซ์)",
            str(f), wrongs=(_n(1 / f), str(2 * f), _n(f / 2)),
            hint=r"f = \frac{1}{T}")


@question_type("phys.wave_speed",
               display_name={"th": "อัตราเร็วของคลื่น (v = fλ)"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class WaveSpeed(PhysCalc):
    """อัตราเร็วคลื่น v = fλ — ถามทั้งสามทาง (หา v, หา f, หา λ).

    เมื่อโจทย์ให้ความถี่เป็นข้อมูล บางครั้งจะให้เป็น *คาบ* T แทน (f = 1/T จึง
    v = λ/T). ค่าถูกเลือกให้ทุกคำตอบเป็นจำนวนเต็มลงตัว และคาบเป็นทศนิยมลงตัว.
    ตัวลวงหลักคือความสับสนของการดำเนินการ — บวกแทนคูณเมื่อหา v, คูณแทนหารเมื่อหา λ.
    """

    _F = [2, 3, 4, 5, 6, 8, 10]              # ความถี่ (เฮิรตซ์)
    _F_CLEAN_T = [2, 4, 5, 8, 10]            # ความถี่ที่คาบ 1/f เป็นทศนิยมลงตัว
    _LAM = [2, 3, 4, 5, 6]                   # ความยาวคลื่น (เมตร)

    def draw(self, rng: Random) -> Calc:
        r = rng.random()
        if r < 0.34:                         # โจทย์ให้ (ความถี่ หรือ คาบ) กับ λ → หา v
            if rng.random() < 0.5:           # ให้เป็นคาบแทนความถี่: v = λ/T
                f = rng.choice(self._F_CLEAN_T)
                lam = rng.choice(self._LAM)
                v, t = f * lam, 1 / f
                return Calc(
                    f"คลื่นมีคาบ {_n(t)} วินาที และความยาวคลื่น {lam} เมตร "
                    f"จงหาอัตราเร็วของคลื่น (เมตร/วินาที)",
                    str(v), wrongs=(_n(lam * t), str(2 * v)),
                    hint=r"v = \frac{\lambda}{T}")
            f = rng.choice(self._F)
            lam = rng.choice(self._LAM)
            v = f * lam
            return Calc(
                f"คลื่นมีความถี่ {f} เฮิรตซ์ และความยาวคลื่น {lam} เมตร "
                f"จงหาอัตราเร็วของคลื่น (เมตร/วินาที)",
                str(v), wrongs=(str(f + lam), str(2 * v)),
                hint=r"v = f\lambda")
        if r < 0.67:                         # โจทย์ให้ v กับ λ → หา f
            f = rng.choice(self._F)
            lam = rng.choice(self._LAM)
            v = f * lam
            return Calc(
                f"คลื่นมีอัตราเร็ว {v} เมตร/วินาที และความยาวคลื่น {lam} เมตร "
                f"จงหาความถี่ของคลื่น (เฮิรตซ์)",
                str(f), wrongs=(str(v * lam), str(v - lam)),
                hint=r"f = \frac{v}{\lambda}")
        # โจทย์ให้ v กับ (ความถี่ หรือ คาบ) → หา λ
        if rng.random() < 0.5:               # ให้เป็นคาบแทนความถี่: λ = vT
            f = rng.choice(self._F_CLEAN_T)
            lam = rng.choice(self._LAM)
            v, t = f * lam, 1 / f
            return Calc(
                f"คลื่นมีอัตราเร็ว {v} เมตร/วินาที และคาบ {_n(t)} วินาที "
                f"จงหาความยาวคลื่น (เมตร)",
                str(lam), wrongs=(_n(v / t), str(2 * lam)),
                hint=r"\lambda = vT")
        f = rng.choice(self._F)
        lam = rng.choice(self._LAM)
        v = f * lam
        return Calc(
            f"คลื่นมีอัตราเร็ว {v} เมตร/วินาที และความถี่ {f} เฮิรตซ์ "
            f"จงหาความยาวคลื่น (เมตร)",
            str(lam), wrongs=(str(v * f), str(v - f)),
            hint=r"\lambda = \frac{v}{f}")


@question_type(
    "phys.wave_model_application",
    display_name={"th": "คลื่นและสมบัติของคลื่น: วิเคราะห์แบบจำลองและข้อมูล"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class WaveModelApplication(QuestionType):
    """Reason across two wave quantities, or judge a model of a wave."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            wavelength = rng.choice((2, 4, 5, 10))
            frequency = rng.choice((2, 3, 4, 5))
            factor = rng.choice((2, 4))
            for wavelength in (wavelength, *rng.sample([2, 4, 5, 10, 8, 20], 6)):
                speed = wavelength * frequency
                correct = (f"{wavelength // factor} m" if wavelength % factor == 0
                           else f"{wavelength / factor:g} m")
                wrongs = _distinct(correct, [
                    f"{wavelength * factor} m",
                    f"{wavelength} m",
                    f"{speed} m",
                    f"{wavelength + factor} m",
                ])
                if wrongs is None:
                    continue
                return _question(
                    stem=(f"คลื่นในตัวกลางหนึ่งมีความยาวคลื่น {wavelength} m และความถี่ {frequency} Hz "
                          f"ถ้าเพิ่มความถี่เป็น {frequency * factor} Hz โดยอัตราเร็วของคลื่น "
                          "ในตัวกลางนี้ไม่เปลี่ยน ความยาวคลื่นจะเป็นเท่าใด"),
                    correct=correct,
                    wrongs=wrongs,
                    hint="อัตราเร็วเท่ากับความถี่คูณความยาวคลื่น ถ้าอัตราเร็วคงที่ สองปริมาณนี้จึงแปรผกผันกัน",
                    topic=WAVES,
                )
            raise AssertionError("no wavelength produced four distinct choices")
        if which == 1:
            return _question(
                stem=("นักเรียนสร้างแบบจำลองคลื่นด้วยเชือกที่สะบัดขึ้นลง "
                      "และอ้างว่า “เชือกทั้งเส้นเคลื่อนที่ไปข้างหน้าพร้อมกับคลื่น” "
                      "ข้อใดประเมินข้ออ้างนี้ได้ถูกต้อง"),
                correct=("ไม่ถูกต้อง เพราะอนุภาคของเชือกสั่นขึ้นลงอยู่กับที่ "
                         "สิ่งที่เคลื่อนที่ไปข้างหน้าคือพลังงานของคลื่น"),
                wrongs=(
                    "ถูกต้อง เพราะคลื่นพาเนื้อเชือกเคลื่อนที่ไปด้วยเสมอ",
                    "ไม่ถูกต้อง เพราะเชือกไม่เคลื่อนที่เลยทั้งขึ้นลงและไปข้างหน้า",
                    "ถูกต้อง เพราะถ้าเนื้อเชือกไม่เคลื่อนที่ คลื่นก็เกิดขึ้นไม่ได้",
                ),
                hint="แยกให้ชัดระหว่างการสั่นของอนุภาคตัวกลางกับการเคลื่อนที่ของพลังงานคลื่น",
                topic=WAVES,
            )
        period = rng.choice((2, 4, 5))
        # period == count makes two of the classic slips identical.
        count = rng.choice([n for n in range(3, 8) if n != period])
        correct = f"คาบของคลื่นเท่ากับ {period} วินาที และความถี่เท่ากับ {1 / period:g} Hz"
        wrongs = _distinct(correct, [
            f"คาบของคลื่นเท่ากับ {period * count} วินาที และความถี่เท่ากับ {count} Hz",
            f"คาบของคลื่นเท่ากับ {count} วินาที และความถี่เท่ากับ {period} Hz",
            f"คาบของคลื่นเท่ากับ {period} วินาที และความถี่เท่ากับ {period} Hz",
            f"คาบของคลื่นเท่ากับ {count} วินาที และความถี่เท่ากับ {1 / count:g} Hz",
        ])
        assert wrongs is not None
        return _question(
            stem=(f"สังเกตคลื่นน้ำและพบว่ามียอดคลื่นผ่านจุดหนึ่งไป {count} ลูก "
                  f"ในเวลา {period * count} วินาที ข้อสรุปใดถูกต้อง"),
            correct=correct,
            wrongs=wrongs,
            hint="คาบคือเวลาต่อหนึ่งลูกคลื่น และความถี่คือส่วนกลับของคาบ",
            topic=WAVES,
        )
